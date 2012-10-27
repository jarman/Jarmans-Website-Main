import web
import datetime
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import urlfetch


render = web.template.render('templates/')


class influx:
	def GET(self, path):
		return render.influx()
	
class influxProxy:
	def GET(self, name):
		web.header('Content-Type', 'text/xml')
		#recreate the query using the same things passed in
		wholeURL = "https://107.22.122.208:4000" + name
		result = urlfetch.fetch(url=wholeURL, deadline=10)
		return result.content

'''

class createPost:
	def GET(self,name):
		return render.createPost(users)

	def POST(self, name):
		
		joinedKeywords = [ web.input(kw1='').kw1, web.input(kw2='').kw2, web.input(kw3='').kw3 ]
		
		entry = postSearchRecord(
			user = users.get_current_user(),
			submitDate = datetime.datetime.now(),
			endDate = (datetime.datetime.now() + datetime.timedelta(int(web.input().duration))),
			keywords = joinedKeywords,
			searchType = 3)

		entry.put();	
		
		raise web.seeother('/searchPosts' + "?kw1=" + web.input(kw1='').kw1 + "&kw2=" + web.input(kw2='').kw2 + "&kw3=" + web.input(kw3='').kw3 )

class searchPosts:
	def GET(self,name):
		postOffset = int(web.input(offset='0').offset)
		morePosts = 'true'
		joinedKeywords = []
		if (len(web.input(kw1='').kw1) > 0):
			joinedKeywords.append(web.input(kw1='').kw1)
		if (len(web.input(kw1='').kw2) > 0):
			joinedKeywords.append(web.input(kw1='').kw2)
		if (len(web.input(kw1='').kw3) > 0):
			joinedKeywords.append(web.input(kw3='').kw3)
			
		query = db.GqlQuery(
			"SELECT * FROM postSearchRecord " +
			"WHERE endDate > :1 " +
			"AND keywords IN :2 " +
			"ORDER BY endDate DESC",
			datetime.datetime.now(), joinedKeywords)
		posts = query.fetch(limit=20, offset=postOffset)
		morePosts = (query.count(limit=(11+postOffset)) > (postOffset+10))
		return render.searchPosts(posts, postOffset, morePosts, datetime, users);
		
		class proxy:    
		    def GET(self, name):
		        web.header('Content-Type', 'text/xml')

		        # note that naming a library "null" will cause errors
		        c = web.cookies(library="null")
		        if (c.library != "null"):
		            # Get the URL of the library in use
		            q = db.GqlQuery("SELECT * FROM libraries WHERE name = :1",
		                            c.library)
		            existingEntries = q.fetch(1)
		            if (len(existingEntries) < 1):
		                return '<html>library not found</html>'

		            lib = existingEntries[0]

		            # if the library doesn't require a username or the user is correct
		            if (lib.user == "" or lib.user == None or
		                (users.get_current_user() and lib.user == users.get_current_user().email())):

		                #recreate the query using the same things passed in
		                wholeURL = "http://" + lib.url + web.ctx.fullpath
		                result = urlfetch.fetch(url=wholeURL, deadline=10)
		                return result.content
		            elif not users.get_current_user():
		                return '<html>please login to use this library</html>'
		            else:
		                return '<html>' + users.get_current_user().email() + ' is not authorized for this library</html>'
		        else:
		            # return empty html if the library is not found
		            return '<html></html>'


'''