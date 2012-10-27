"""
Helper functions to produce results

In general, they do no need knowledge of the google contacts api or datastructure
"""


import re
import logging
import datetime

def findDateFormat(value):
	""" 
	Parses dates into datetime object and returns that and booleans 
	indicating if year, month, day fields were found
	"""
	formats = [ {'format':'%b %d %y', 'year':True, 'month':True, 'day':True},
				{'format':'%b %d %Y', 'year':True, 'month':True, 'day':True},
				{'format':'%B %d %y', 'year':True, 'month':True, 'day':True},
				{'format':'%B %d %Y', 'year':True, 'month':True, 'day':True},
				{'format':'%Y-%m-%d', 'year':True, 'month':True, 'day':True},
				{'format':'--%m-%d', 'year':False, 'month':True, 'day':True},
				{'format':'%m-%d-%y', 'year':True, 'month':True, 'day':True},
				{'format':'%m-%d-%Y', 'year':True, 'month':True, 'day':True},
				{'format':'%m/%d/%y', 'year':True, 'month':True, 'day':True},
				{'format':'%m/%d/%Y', 'year':True, 'month':True, 'day':True},
				{'format':'%Y/%m/%d', 'year':True, 'month':True, 'day':True},
				{'format':'%m/%d', 'year':False, 'month':True, 'day':True},
				{'format':'%m-%d', 'year':False, 'month':True, 'day':True},
				{'format':'%b %d', 'year':False, 'month':True, 'day':True},
				{'format':'%B %d', 'year':False, 'month':True, 'day':True},
				{'format':'%b', 'year':False, 'month':True, 'day':False},
				{'format':'%B', 'year':False, 'month':True, 'day':False}]
	for format in formats:
		try:
			entryDate = datetime.datetime.strptime(value, format['format'])
			return entryDate, format['year'], format['month'], format['day']
		except:
			pass
	return None, None, None, None
			
def formatSearchTerms(searchTerms):
	""" 
	Formats strings so that they're all lowercase, and parses some others into a more usable format 
	
	Birthdays are converted into datetimes
	Label lists are converted into arrays with the spaces between labels removed
	Phone number have all but the numbers stripped out
	All text fields are converted to lowercase
	"""
	searchTerms["search"] = searchTerms["search"].lower()
	searchTerms["firstname"] = searchTerms["firstname"].lower();
	searchTerms["lastname"] = searchTerms["lastname"].lower();
	searchTerms["job"] = searchTerms["job"].lower()
	searchTerms["company"] = searchTerms["company"].lower()
	
	userDate, year, month, day = findDateFormat(searchTerms['birthday'])
	
	if searchTerms['birthday'] and not userDate:
		return None
	
	searchTerms["b_date"] = userDate
	searchTerms["b_year"] = year
	searchTerms["b_month"] = month
	searchTerms["b_day"] = day
	
	searchTerms["email"] = searchTerms["email"].lower()
	searchTerms["labels"] = re.sub(",[\s]+", ",",searchTerms["labels"].lower()).split(',')
	searchTerms["exclude"] = re.sub(",[\s]+", ",",searchTerms["exclude"].lower()).split(',')
	searchTerms["phone"] = re.sub("[^0-9]", "", searchTerms["phone"])
	
	return searchTerms


def formatNamesAndStrings(feed):
	""" 
	Sets encoding on a few strings and parses names into first and last for easier searching
	
	Family and given names (equivalent to first and last names) are not returned by the service
	which only appears to return a title. Therefore, it's easier to add these elements to the contact feed
	so they can be easily accessed. If the contact has only one word in their title, it will be put into
	both fields, so both last and first names will match for contacts with one word titles
	
	Note that I don't mess with a lot of fields here because I use the same things for display
	and running functions like 'lower' now would alter the appearance on display
	"""
	for i, entry in enumerate(feed.entry):
		#print "title: %s - " % (entry.title)
		if (entry.title and entry.title.text):
			#try:
			entry.title.text = entry.title.text.decode('utf8', 'xmlcharrefreplace');
			if entry.organization:
				if entry.organization.org_name:
					entry.organization.org_name.text = entry.organization.org_name.text.decode('utf8', 'xmlcharrefreplace')
				if entry.organization.org_title:
					entry.organization.org_title.text = entry.organization.org_title.text.decode('utf8', 'xmlcharrefreplace')
			
			fullname = entry.title.text
			splitnames = fullname.split()
			entry.givenname = splitnames[0]
			entry.familyname = splitnames[-1] #the last element
		else:
			#it's helpful to populate these values to save some error handling later
			entry.givenname=""
			entry.familyname=""		
	return feed

def convertGoogleDate(date):
	"""
	Tries to parse a datetime, returns none on failure
	
	There only seemed to be options for giving (y-m-d and --m-d) combos without google
	flagging the formatting as an error so I'm only handling those two
	"""
	yearPresent = True
	try:
		if (date[0] == '-'):
			# this means the year is missing
			yearPresent = False
			entryDate = datetime.datetime.strptime(date, "--%m-%d")
		else:
			# hopefully the year is there
			entryDate = datetime.datetime.strptime(date, "%Y-%m-%d")
		
		logging.info("Returning %s", entryDate)
		return entryDate, yearPresent
	except Exception, e:
		# the date wasn't in either format
		logging.error("Returning None")
		return None, None;
		

def PrintContactsThatMatch(feed, terms):
	"""
	Tries to match each entry with the given search terms and returns a list of matches
	
	Search terms which are not present are ignored
	"""
	foundEntries = []
	for i, entry in enumerate(feed.entry):
		#logging.info("title: %s - " % (entry.title))
		if (matchTextOrNotApplicable(terms['search'],entry.title) and
			matchOrNotApplicable(terms['firstname'], entry.givenname) and 
			matchOrNotApplicable(terms['lastname'], entry.familyname) and 
			matchOrgTitleOrNotApplicable(terms['job'], entry.organization) and 
			matchOrgNameOrNotApplicable(terms['company'], entry.organization) and 
			matchEmailOrNotApplicable(terms['email'],entry.email) and
			matchPhoneOrNotApplicable(terms['phone'],entry.phone_number) and
			matchLabelsOrNotApplicable(terms['labels'],entry.group_membership_info) and
			excludeLabelsOrNotApplicable(terms['exclude'],entry.group_membership_info) and
			matchBirthdayOrNotApplicable(terms['b_date'], terms['b_year'], terms['b_month'], terms['b_day'], entry.birthday) and
			matchNameRangeOrNotApplicable(terms['rangename'],terms['beginswith'],terms['endswith'],entry.givenname,entry.familyname)):
			
			# Everything either matched, or wasn't being searched
			foundEntries.append(entry)
			
	return foundEntries
	
def matchTextOrNotApplicable(terms, value):
	""" 
	Checks if the term matches any part of the value given 

	Returns true on substring matches at the beginning of a word
	or if there is no term passed in
	"""
	
	if terms:
		if (value and value.text):
			foundMatches = 0
			for term in terms.split():
				if (matchSingleTerm(term, value)):
					foundMatches += 1
					continue;
			if foundMatches != len(terms.split()):
				return False
		else:
			return False
	#else the term wasn't there, so return true
	return True;

def matchSingleTerm(term, values):
	""" 
	helper for matchTextOrNotApplicable
	
	returns true if the term matches the beginning of any word in values
	allows me to jump out of a nested loop
	"""
	for word in values.text.split():
		if (word.lower().find(term) == 0):
			return True
	return False
	
def matchOrNotApplicable(term, value):
	"""
	Used for matching a single word without a text value
	
	familyname and givenname use this function
	Only matches beginning at the start of the word
	"""
	if term:
		if (value):
			if (value.lower().find(term) != 0):
				return False
		else:
			return False
	#else
	return True;
	
def matchOrgTitleOrNotApplicable(term,value):
	"""
	Matches a substring of the given orgtitle at any position
	
	Using complex substring matching did not seem necessary
	"""
	if (term):
		if (value and value.org_title):
			if (value.org_title.text.lower().find(term) == -1):
				return False
		else:
			return False
	return True
	
def matchOrgNameOrNotApplicable(term,value):
	"""
	Matches a substring at any position of the orgname
	"""
	if (term):
		if (value and value.org_name):
			if (value.org_name.text.lower().find(term) == -1):
				return False
		else:
			return False
	return True

def matchEmailOrNotApplicable(term,value):
	"""
	Matches substring of email at any position
	"""
	if (term):
		foundAMatch = False
		for email in value:
			if (email.primary and email.address.lower().find(term) > -1):
				foundAMatch = True;
		if not foundAMatch:
			return False
	return True

def matchPhoneOrNotApplicable(term,value):
	"""
	Matches the phone number beginning at any position
	
	Originally coded to only match only the right end of the phone number
	but this didn't work well for type ahead
	"""
	if (term):
		foundAMatch = False
		for number in value:
			if number.primary:
				strippedNumber = re.sub("[^0-9]", "", number.text)
				#make sure this matches the left side of the string
				#the second part of the check is to make sure that the two lengths aren't working out to be -1 (not a match)
				if ((strippedNumber.find(term) > -1 )):
					foundAMatch = True;
		if not foundAMatch:
			return False
	return True

def matchLabelsOrNotApplicable(terms,value):
	"""
	Matches an array of labels. All labels must be found
	
	Matches the label name at any position. If any label is not matched
	the NoMatches bool gets set and causes the function to return false
	"""
	NoMatches = False
	for label in terms:
		if label == '':
			continue;
		foundAMatch = False
		for group in value:
			if (group.text.lower().find(label) > -1):
				foundAMatch = True;
		if not foundAMatch:
			NoMatches = True
			continue
	if (NoMatches):
		return False
	return True

def excludeLabelsOrNotApplicable(terms,value):
	"""
	Takes an array of labels and returns true if any of them are found
	
	Uses substring matching at any position
	"""
	matches = False
	for label in terms:
		if label == '':
			continue
		foundAMatch = False
		for group in value:
			if (group.text.lower().find(label) > -1):
				foundAMatch = True;
		if foundAMatch:
			matches = True
			continue
	if (matches):
		return False
	return True

def matchBirthdayOrNotApplicable(b_date, b_year, b_month, b_day, value):
	"""
	Matches birthday based on all the fields matching
	
	If a value is is missing from either the entry or the given term
	it is skipped. 
	"""
	if (b_date):
		if value and value.when:
			entryDate, yearPresent = convertGoogleDate(value.when)
			if not entryDate:
				# the date must be in some format which isn't recognized
				return False;
			if not ((not b_year or not yearPresent or entryDate.year==b_date.year) and 
					(not b_month or entryDate.month==b_date.month) and 
					(not b_day or entryDate.day==b_date.day)):
					return False
		else:
			return False
	return True

def matchNameRangeOrNotApplicable(rangename,beginswith,endswith,givenname,familyname):
	"""
	Matches first or last name in a given range. Returns true if the provided name
	is within the range, or no range was given. 
	
	Rangename is either 'first' or 'last' which is enforced by a clientside dropdown
	If no term is selected, beginswith is empty
	beginswith and endswith are capitalized (clientside enforcement)
	
	"""
	if (rangename == ('first') and beginswith):
		if not (givenname and len(givenname) > 0):
			return False
		if(givenname[0].upper() < beginswith):
			return False
		if(givenname[0].upper() > endswith):
			return False
	elif (rangename == ('last') and beginswith):
		if not (familyname and len(familyname) > 0):
			return False
		if(familyname[0].upper() < beginswith):
			return False
		if(familyname[0].upper() > endswith):
			return False
	return True