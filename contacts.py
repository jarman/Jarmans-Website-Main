"""
This file contains all of the logic for dealing with google's contacts api

Helper functions which could be abstracted away from dealing with the google api
were placed in a separate file for testability.
"""

import web
import datetime
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import urlfetch
import atom.data
import atom.url
import gdata.data
import gdata.contacts.client
import gdata.contacts.data
import gdata.contacts.service
import gdata.service
import gdata.alt.appengine
import os
import types
from UserString import MutableString
import logging
import sys
from contacts_helper import *

#max results displayed in a page
MAX_RESULTS = 100
# max results downloaded from server
MAX_DOWNLOADED = 10000

render = web.template.render('templates/')
# The url to get the contacts feed
feed_url = 'https://www.google.com/m8/feeds/contacts/default/full?max-results=' + str(MAX_DOWNLOADED)
# Storage dictionary for user contacts, keyed from their login
feedcaches = {}


class contacts:
	def GET(self):
	
		# generate a URL to pass into the google API
		port = os.environ['SERVER_PORT']
		if port and port != '80':
			  hostname = '%s:%s' % (os.environ['SERVER_NAME'], port)
		else:
			  hostname = os.environ['SERVER_NAME']	
	
		next_url = atom.url.Url('http', hostname, path='/contacts')
		
		# Initialize a client to talk to Google Data API services.
		client = gdata.contacts.service.ContactsService(additional_headers = {gdata.contacts.service.GDATA_VER_HEADER: 3})
		gdata.alt.appengine.run_on_appengine(client)
		
		# If the user isn't logged in, make them log in
		if users.get_current_user():
			if users.get_current_user().nickname() in feedcaches:
				# user is logged in and their feed is already stored
				# here we just return the page to print their contacts (and search them)
				return render.contactsEntriesView(users);	
		else:
			#make the user login so that their contacts can be stored against that login
			return render.contactsLogin(users.create_login_url(str(next_url)));

		
		# reahching this point means the user is logged in, but doesn't have a stored feed
		# they need to authorize again to download their contacts
		
		# first, try to extract the the session token from the URL, in case the user
		# has just authroized the app to download contacts

		session_token = None
		# Find the AuthSub token and upgrade it to a session token.
		auth_token = gdata.auth.extract_auth_sub_token_from_url(web.ctx.fullpath)
		#auth_token = web.input(token=None).token
		
		old_session_token = client.GetClientLoginToken()
		
		if auth_token:
			# Upgrade the single-use AuthSub token to a multi-use session token.
			try:
				session_token = client.upgrade_to_session_token(auth_token)
				#print "Session token created"
			except:
				pass
				#print "Token was probably revoked"
				#session_token = auth_token
		
		if session_token:
			# If there is a current user, store the token in the datastore and
			# associate it with the current user. Since we told the client to
			# run_on_appengine, the add_token call will automatically store the
			# session token if there is a current_user.
			client.token_store.add_token(session_token)
			
		if (session_token):
			try:
				# get the contacts feed
				# Note: future optimizations would possibly do this asyncronously since
				# the client is fetching them with ajax requests. At this point we could return
				# the framing page
				response = client.Get(feed_url, converter=gdata.contacts.ContactsFeedFromString)
				# look through the contacts for groups and add their names
				response = addGroupNames(client,response)
				# split up names into first and last; format contacts 
				response = formatNamesAndStrings(response)
				# store the data in an in-memory dictionary.
				# Note: this is the place where we'd normally want to stick things in a database
				feedcaches[users.get_current_user().nickname()] = response
				# Return the page that display the contacts
				# Note that this page get's the contacts via an ajax request
				return render.contactsEntriesView(users);	
			except gdata.service.RequestError, request_error:
				#something mostly unexpected has gone wrong
				print '<h1>There was an error</h1>'
				#the above is sent to the user
				# If fetching fails, then tell the user that they need to login to
				# authorize this app by logging in at the following URL.
				if request_error[0]['status'] == 401:
					# If there is a current user, we can request a session token, otherwise
					# we should ask for a single use token.
					auth_sub_url = client.GenerateAuthSubURL(next_url, ('https://www.google.com/m8/feeds/',),secure=False, session=True)
					print '<a href="%s">' % (auth_sub_url)
					print 'Click here to authorize this application to view the feed</a>'
				else:
					print 'Something went wrong, here is the error object: %s ' % (str(request_error[0]))
		else:
			# the session token has expired or never existed in the first place
			# display the login page 
			return render.contactsAccess(client.GenerateAuthSubURL(next_url, ('https://www.google.com/m8/feeds/',), secure=False, session=True));
			
	def POST(self):
		""" 
		The webapp posts to this page to get a list of contacts which match certain parameters
		
		These users are given in the order that they are received from google's service (more or less random).
		posting empty or no parameters results in the full list being displayed (though capped at the number defined above as "MAX_RESULTS")
		"""
		if users.get_current_user():
			if users.get_current_user().nickname() in feedcaches:
			
				# putting the terms into a dict so I can pass them into functions easily (better testability)
				searchTerms = {}
				searchTerms["search"] = web.input(search="").search
				searchTerms["firstname"] = web.input(firstname="").firstname
				searchTerms["lastname"] = web.input(lastname="").lastname
				searchTerms["job"] = web.input(job="").job
				searchTerms["company"] = web.input(company="").company
				searchTerms["birthday"] = web.input(birthday="").birthday
				searchTerms["email"] = web.input(email="").email
				searchTerms["labels"] = web.input(labels="").labels
				searchTerms["exclude"] = web.input(exclude="").exclude
				searchTerms["rangename"] = web.input(rangename="").rangename
				searchTerms["beginswith"] = web.input(beginswith="").beginswith
				searchTerms["endswith"] = web.input(endswith="").endswith
				searchTerms["phone"] = web.input(phone="").phone
				
				# Process search terms for easier use later
				searchTerms = formatSearchTerms(searchTerms)
				
				if not searchTerms:
					# this is returned, for example, when the date format is not recognized
					return '<h4>search term error</h4>'
				else:
					# get users that match the search query
					foundEntries = PrintContactsThatMatch(feedcaches[users.get_current_user().nickname()], searchTerms);
					logging.info("there were %s matches", len(foundEntries))
					if (len(foundEntries) == 0):
						return "<h4>There were no matches</h4>"
					return render.contactsEntryElement(foundEntries, MAX_RESULTS)
			else:
				return "can't find anything cached"
		else:
			return "you don't appear to be logged in"
			
def addGroupNames(client,feed):
	"""
	Adds group names to user entries by querying the server for group names
	
	Group Names aren't included so we have to fetch those from the service
	I just add them back to the contact element as a text value of group since this label is otherwise unused
	"""

	groupInfo = {}
	for i, entry in enumerate(feed.entry):
		for group in entry.group_membership_info:
			urlparts = group.href.split('/')
			groupId = urlparts[len(urlparts)-1]			
			if groupId not in groupInfo:
				groupInfo[groupId] = client.Get('https://www.google.com/m8/feeds/groups/default/full/'+groupId)
			group.text = groupInfo[groupId].title.text	
	return feed