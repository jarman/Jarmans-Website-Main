import web
import datetime
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import urlfetch


render = web.template.render('templates/')

# GQL entry for a post
# holds the information related to a blog post entry
class reviewPost(db.Model):
    title = db.StringProperty(required=True)
    message = db.TextProperty(required=True)
    details = db.TextProperty(required=True)
    when = db.DateTimeProperty(auto_now_add=True)
    who = db.UserProperty()

class reviews:
    def GET(self, name):
        postOffset = int(web.input(offset='0').offset)
        morePosts = 'true'
        query = db.GqlQuery(
            'SELECT * FROM reviewPost '
            'ORDER BY when DESC')
        posts = query.fetch(limit=10, offset=postOffset)
        morePosts = (query.count(limit=(11+postOffset)) > (postOffset+10))
        if (users.get_current_user()):
            user = users.get_current_user().nickname()
        else:
            user = 'Anonymous'
        return render.reviews(posts, user, postOffset, morePosts, users);
    
    def POST(self, name):
        post = reviewPost(
            message = web.input(message='').message.replace('\n','<br>'),
	        details = web.input(details='').details.replace('\n','<br>'),
            title = web.input(title='Untitled').title,
            who = users.get_current_user())
        post.put();
        raise web.seeother('/reviews')

class reviewposts:
    def GET(self, name):
        posts = reviewPost.get_by_id(int(name))
        if (users.get_current_user()):
            user = users.get_current_user().nickname()
        else:
            user = 'Anonymous'
        return render.reviewpost(posts, user, 0, 0, users);