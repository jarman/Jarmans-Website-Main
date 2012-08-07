import web
import datetime
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import urlfetch


render = web.template.render('templates/')

# GQL entry for a search
class postSearchRecord(db.Model):
	user = db.UserProperty()
	submitDate = db.DateTimeProperty()
	endDate = db.DateTimeProperty()
	keywords = db.StringListProperty()
	searchType = db.IntegerProperty()

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


