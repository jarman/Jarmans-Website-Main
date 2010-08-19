#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
import datetime
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import urlfetch

urls = (
    '/songs(.*)', 'proxy',
    '/artists(.*)', 'proxy',
    '/albums(.*)', 'proxy',
    '/playlists(.*)', 'proxy',
    '/register', 'registerClient',
    '/login(.*)', 'login',
    '/projects(.*)', 'projects',
    '/about', 'about',
    '/music', 'music',
    '/selectLibrary', 'selectLibrary',
    '/(.*)', 'blog'
)

render = web.template.render('templates/')

# holds the information related to a blog post entry
class blogPost(db.Model):
    title = db.StringProperty(required=True)
    message = db.TextProperty(required=True)
    when = db.DateTimeProperty(auto_now_add=True)
    who = db.StringProperty()

# holds the information about an itunes library
class libraries(db.Model):
    name = db.StringProperty(required=True)
    url = db.StringProperty(required=True)
    lastAvailable = db.DateTimeProperty(required=True)
    user = db.StringProperty()
    dateString = db.StringProperty()

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

class login:
    def GET(self, ref):
        # use app engine's build in login method
        raise web.seeother(users.create_login_url(ref))

class registerClient:
    def GET(self):

        # first attempt to find the user library in the database
        q = db.GqlQuery("SELECT * FROM libraries WHERE name = :1",
                            web.input().name)
        existingEntry = q.fetch(1);
        if (len(existingEntry) > 0):
            # the library was found in the DB, update their entry
            # use the ip address if the url is not provided
            existingEntry[0].url = web.input(url=web.ctx.ip).url
            existingEntry[0].lastAvailable = datetime.datetime.now()
            db.put(existingEntry);
            return '<html>Updated Entry</html>'
        else:
            # the library was not found in the DB, create a new entry
            entry = libraries(
                name = web.input().name,
                # use the ip address if the url is not provided
                url = web.input(url=web.ctx.ip).url,
                # use an empty string if no user was provided
                user = web.input(user='').user,
                lastAvailable = datetime.datetime.now())
            entry.put();
            return '<html>Added new entry</html>'
        
class projects:
    def GET(self, subpage):
        if (subpage == '/random_circles.html'):
            contents = render.random_circles()
        else:
            contents = render.projects()
        return render.main('projects', contents, users)

class about:
    def GET(self):
        return render.main('about', render.about(), users)

class music:    
    def GET(self):
        # get the libraries from the db
        libraries = db.GqlQuery(
            'SELECT * FROM libraries '
            'ORDER BY lastAvailable DESC')
        for library in libraries:
            # construct a string to indicate how long since the library phoned home
            daysAgo = datetime.datetime.now() - library.lastAvailable            
            if (daysAgo.days > 1):
                value = daysAgo.days
                dateString = str(value) + " day"
            elif (daysAgo.seconds > 3600):
                value = daysAgo.seconds/3600
                dateString = str(value) + " hour"
            else:
                value = daysAgo.seconds/60
                dateString = str(value) + " minute"

            # Add an 's' to the end of the time unit if necessary
            if (value == 1):
                library.dateString = dateString + " ago"
            else:
                library.dateString = dateString + "s ago"
            
            library.put()
        return render.main('music', render.music(libraries, users), users);

class blog:
    def GET(self, name):
        postOffset = int(web.input(offset='0').offset)
        morePosts = 'true'
        query = db.GqlQuery(
            'SELECT * FROM blogPost '
            'ORDER BY when DESC')
        posts = query.fetch(limit=10, offset=postOffset)
        morePosts = (query.count(limit=(11+postOffset)) > (postOffset+10))
        if (users.get_current_user()):
            user = users.get_current_user().nickname()
        else:
            user = 'Anonymous'
        return render.main('blog', render.blog(posts, user, postOffset, morePosts), users);
    
    def POST(self, name):
        post = blogPost(
            message = web.input(message='').message,
            title = web.input(title='Untitled').title,
            who = users.get_current_user().nickname())
        post.put();
        raise web.seeother('/')

app = web.application(urls, globals())

def main():
    app.cgirun()


if __name__ == "__main__":
    main()
