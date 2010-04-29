#!/usr/bin/env python

import web
import logging
import datetime
from pyItunes import *
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.runtime import DeadlineExceededError

urls = (
    '/songs.(.*)', 'songs',
    '/artists.(.*)', 'artists',
    '/albums.(.*)', 'albums',
    '/clear', 'clearLibrary',
    '/load(.*)', 'loadDb',
    '/login', 'login',
    '/projects(.*)', 'projects',
    '/about', 'about',
    '/music', 'music',
    '/playlists', 'playlists',
    '/(.*)', 'blog'
)

render = web.template.render('templates/')

maxDbEntry = 0;
newEntries = ''
maxDate = None

class blogPost(db.Model):
    title = db.StringProperty(required=True)
    message = db.TextProperty(required=True)
    when = db.DateTimeProperty(auto_now_add=True)
    who = db.StringProperty()

class songEntry(db.Model):
    name = db.StringProperty()
    artist = db.StringProperty()
    album = db.StringProperty()
    filetype = db.StringProperty()
    location = db.TextProperty()
    trackNumber = db.IntegerProperty()
    modified = db.DateTimeProperty()

class playlistEntry(db.Model):
    songs = db.StringListProperty()
    parentID = db.StringProperty()
    name = db.StringProperty()
    folder = db.BooleanProperty()
    
def numeric_compare(x, y):
    if x[0] > y[0]:
       return 1
    elif x[0] == y[0]:
       return 0
    else:  #x < y
       return -1

def putSongsInDatabase(lib, post):
    global maxDbEntry, newEntries, maxDate
    i = 0

    if (not maxDate):
        dateQuery = songEntry.gql("ORDER BY modified DESC")
        if (dateQuery.count(1) == 1):
            maxDate = dateQuery.get().modified
        else:
            maxDate = datetime.datetime.min
            
    maxDate = datetime.datetime.min
    
    for song,attributes in lib.songs.iteritems():
        if (i == maxDbEntry):
            dateModified = datetime.datetime.strptime(attributes.get('Date Modified'), '%Y-%m-%dT%H:%M:%SZ')
            if (maxDate < dateModified):

                entry = songEntry.get_by_key_name(song)


                if (not entry or (not entry.modified) or (entry.modified < dateModified)):

                    if (not entry):
                        entry = songEntry(key_name = song)
                        if (attributes.get('Artist')):
                            postLine = attributes.get('Artist') + ' - ' + attributes.get('Name') + '<br>'
                        else:
                             postLine = attributes.get('Name') + '<br>'
                        newEntries += postLine

                    # add a new entry
                    if (attributes.get('Name')):
                        entry.name = unicode(attributes.get('Name'), 'latin-1')
                    if (attributes.get('Artist')):
                        entry.artist = unicode(attributes.get('Artist'), 'latin-1')
                    if (attributes.get('Album')):
                        entry.album = unicode(attributes.get('Album'), 'latin-1')
                    if (attributes.get('Kind')):
                        entry.filetype = attributes.get('Kind')
                        
                    localLoc = attributes.get('Location')
                    localFolder = localLoc[localLoc.find('iTunes%20Music/')+15:]
                    entry.location = unicode("http://jarman.homedns.org:82/" + localFolder, 'latin-1')
                    entry.modified = dateModified

                    if (attributes.get('Track Number')):
                        entry.trackNumber = int(attributes.get('Track Number'))
                    entry.put()

                    if (i % 500 == 0):
                        logging.info("records processed: %d of %d", i, len(lib.songs))
            maxDbEntry += 1
        i += 1

    if newEntries != '' and post == 'True':
        post = blogPost(
            title = 'Newly Added Songs',
            message = newEntries,
            who = 'the music app')
        post.put();
        newEntries = ''

def putPlaylistsInDatabase(lib):
    logging.info("Putting Playlists into Library")
    
    for playlist,attributes in lib.playlists.iteritems():
        entry = playlistEntry.get_or_insert(attributes.get('Playlist Persistent ID'))

        entry.name = attributes.get('Name')
        entry.songs = attributes.get('songs')

        if (attributes.get('Parent Persistent ID')):
            entry.parentID = attributes.get('Parent Persistent ID')
        
        if attributes.get('Folder') == '':
            entry.folder = True
        else:
            entry.folder = False

        entry.put();
    
    logging.info("Finished putting Playlists into Library")

def clearDatabase(dbToClear):
    while (dbToClear.all().count(1) == 1):
        db.delete(dbToClear.all().fetch(500))

def getPlaylistContents(plid):    
    songs = [];
    logging.info("starting to build result")
    pl = playlistEntry.get_by_key_name(plid)
    entries = songEntry.get_by_key_name(pl.songs)
    for song in entries:
        songs.append([song.location, song.artist, song.name])
    
    logging.info("finished building result")
        
    return songs, pl.name

def getArtistSongs(artist):    
    songs = [];
    query = songEntry.gql('WHERE artist = :1 '
                          'ORDER BY album, trackNumber ASC',
                          artist)
    for song in query:
        songs.append([song.location, song.artist, song.name])
    
    return songs

def getAlbumSongs(album):    
    songs = [];
    query = songEntry.gql('WHERE album = :1 '
                          'ORDER BY trackNumber ASC',
                          album)
    for song in query:
        songs.append([song.location, song.artist, song.name])
    
    return songs

def getPlaylists():
    playlists = []
    folders = []

    folderEntries = playlistEntry.gql('WHERE folder = True '
                                      'ORDER BY name')
    playlistEntries = playlistEntry.gql('WHERE folder = False '
                                      'ORDER BY name')

    for folderEntry in folderEntries:
        folders.append([folderEntry.name, folderEntry.key().name(), []]);
    for entry in playlistEntries:
        for folder in folders:
            if (folder[1] == entry.parentID):
                folder[2].append([entry.name, entry.key().name()])
    return folders

def getArtists():
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'] 
    artistNames = { 'A':[], 'B':[], 'C':[], 'D':[], 'E':[], 'F':[], 'G':[], 'H':[], 'I':[], 'J':[], 'K':[], 'L':[], 'M':[], 'N':[], 'O':[], 'P':[], 'Q':[], 'R':[], 'S':[], 'T':[], 'U':[], 'V':[], 'W':[], 'X':[], 'Y':[], 'Z':[], '#':[]}  
    for i in range(0,len(letters)-1):
        query = songEntry.gql("WHERE artist > :1 AND artist < :2 "
                              "ORDER BY artist ASC",
                              letters[i], letters[i+1])
        for entry in query:
            if (0 == artistNames[letters[i]].count(entry.artist)):
                artistNames[letters[i]].append(entry.artist);
    for i in range(0,len(letters)-1):
        query = songEntry.gql("WHERE artist < 'A'"
                              "ORDER BY artist ASC")
        for entry in query:
            if ((entry.artist != '') and (0 == artistNames['#'].count(entry.artist))):
                artistNames['#'].append(entry.artist);
    for i in range(0,len(letters)-1):
        query = songEntry.gql("WHERE artist > 'Z' "
                              "ORDER BY artist ASC")
        for entry in query:
            if (0 == artistNames['Z'].count(entry.artist)):
                artistNames['Z'].append(entry.artist);
    return artistNames

    

def getAlbums():
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'] 
    artistNames = { 'A':[], 'B':[], 'C':[], 'D':[], 'E':[], 'F':[], 'G':[], 'H':[], 'I':[], 'J':[], 'K':[], 'L':[], 'M':[], 'N':[], 'O':[], 'P':[], 'Q':[], 'R':[], 'S':[], 'T':[], 'U':[], 'V':[], 'W':[], 'X':[], 'Y':[], 'Z':[], '#':[]}  
    for i in range(0,len(letters)-1):
        query = songEntry.gql("WHERE album > :1 AND album < :2 "
                              "ORDER BY album ASC",
                              letters[i], letters[i+1])
        for entry in query:
            if (0 == artistNames[letters[i]].count(entry.album)):
                artistNames[letters[i]].append(entry.album);
    for i in range(0,len(letters)-1):
        query = songEntry.gql("WHERE album < 'A'"
                              "ORDER BY album ASC")
        for entry in query:
            if ((entry.album != '') and (0 == artistNames['#'].count(entry.album))):
                artistNames['#'].append(entry.album);
    for i in range(0,len(letters)-1):
        query = songEntry.gql("WHERE album > 'Z' "
                              "ORDER BY album ASC")
        for entry in query:
            if (0 == artistNames['Z'].count(entry.album)):
                artistNames['Z'].append(entry.album);
    return artistNames
    

def findSongs(s):
    
    cats = ['name', 'artist', 'album']
    titles = ['Name', 'Artist', 'Album']
    songs = [[], [], []]
    #s = s.encode('latin-1').lower();

    for i in range(len(cats)):
        entries = songEntry.all()
        entries.filter(cats[i], s)
        #entries = songEntry.gql('WHERE album = :1 ',
        #                        s)

        for entry in entries:
            songs[i].append([entry.location, entry.artist, entry.name])

    return songs, titles

class songs:    
    def GET(self, name):
        web.header('Content-Type', 'text/xml')
        if web.input(Playlist='null').Playlist != 'null':
            songs, plName = getPlaylistContents(web.input().Playlist)
            if name == 'xml':
                return render.songsxml(songs, plName)
            else:
                return render.songs(songs, plName);
        if web.input(Artists='null').Artists != 'null':
            artist = web.input().Artists
            songs = getArtistSongs(artist)
            return render.songs(songs, artist);
        if web.input(Albums='null').Albums != 'null':
            album = web.input().Albums
            songs = getAlbumSongs(album)
            return render.songs(songs, album);
        if len(web.input(search='null').search) > 1:
            songs, titles = findSongs(web.input().search)
            return render.search(web.input().search, songs, titles);
        else:
            return('invalid');

class artists:    
    def GET(self, name):
        return render.albums('Artists', getArtists());

class albums:    
    def GET(self, name):
        return render.albums('Albums', getAlbums());

class clearLibrary:
    def GET(self):
        clearDatabase(songEntry)
        return('cleared');

class loadDb:
    def GET(self, loadType):
        global lib, maxDbEntry
        if (loadType == 'Library'):
            if (lib == None):
                logging.info('loading library into memory')
                lib = XMLLibraryParser("iTunes Music Library.xml")
                logging.info('Finished loading library into memory')
            return('Finished loading library into memory.');
        elif (loadType == 'Songs'):
            if (web.input(pos='null').pos != 'null'):
                maxDbEntry = int(web.input().pos)
            try:
                if (lib == None):
                    logging.info('loading library into memory')
                    lib = XMLLibraryParser("iTunes Music Library.xml")
                    logging.info('Finished loading library into memory')
                putSongsInDatabase(lib, web.input(post='True').post)

                return('Finished loading songs into DB');
            except DeadlineExceededError:
                return maxDbEntry
        elif (loadType == 'Playlists'):
            try:
                if (lib == None):
                    logging.info('loading library into memory')
                    lib = XMLLibraryParser("iTunes Music Library.xml")
                    logging.info('Finished loading library into memory')
                putPlaylistsInDatabase(lib)

                return('Finished Loading playlists into DB');
            except DeadlineExceededError:
                return('couldnt finish playlist load')
        else:
            #Load both the songs and the playlists into the DB
            if (web.input(pos='null').pos != 'null'):
                maxDbEntry = int(web.input().pos)
            try:
                if (lib == None):
                    logging.info('loading library into memory')
                    lib = XMLLibraryParser("iTunes Music Library.xml")
                    logging.info('Finished loading library into memory')
                putSongsInDatabase(lib, web.input(post='True').post)
                putPlaylistsInDatabase(lib)

                return('Finished loading everything into DB');
            except DeadlineExceededError:
                return maxDbEntry


class login:
    def GET(self):
        raise web.seeother(users.create_login_url(''))

class projects:
    def GET(self, subpage):
        if (subpage == '/random_circles.html'):
            contents = render.random_circles()
        else:
            contents = render.projects()
        return render.main('projects', contents)

class about:
    def GET(self):
        return render.main('about', render.about())

class playlists:
    def GET(self):
        web.header('Content-Type', 'text/xml')
        return render.playlistsxml(getPlaylists())

class music:    
    def GET(self):
        return render.main('music', render.music(getPlaylists(), [], "Loading..."));

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
        return render.main('blog', render.blog(posts, user, postOffset, morePosts));
    
    def POST(self, name):
        post = blogPost(
            message = web.input(message='').message,
            title = web.input(title='Untitled').title,
            who = users.get_current_user().nickname())
        post.put();
        raise web.seeother('/')

app = web.application(urls, globals())

lib = None;

def main():
    logging.info("Received Request")
    app.cgirun()


if __name__ == "__main__":
    main()
