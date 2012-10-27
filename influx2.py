import web
import datetime
import logging
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import urlfetch
from google.appengine.ext import webapp


render = web.template.render('templates/')


class influx:
	def GET(self, path):
		return render.influx()
	
class influxProxy:
	def GET(self, name):
		web.header('Content-Type', 'application/json')
		
		#requestPayload  = self.request.body()
		#recreate the query using the same things passed in
		wholeURL = "https://107.22.122.208:4000" + name + web.ctx.query
		logging.debug(wholeURL);
		result = urlfetch.fetch(url=wholeURL, method='GET', deadline=10, validate_certificate=False)
		return result.content
	def POST(self, name):
		web.header('Content-Type', 'application/json')
		
		#requestPayload  = self.request.body()
		#recreate the query using the same things passed in
		wholeURL = "https://107.22.122.208:4000" + web.ctx.fullpath
		logging.debug(wholeURL);
		result = urlfetch.fetch(url=wholeURL, method='POST', payload=self.request.body, deadline=10, validate_certificate=False)
		return result.content