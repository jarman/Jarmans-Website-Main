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
    '/load', 'loadLibrary',
    '/login', 'login',
    '/projects(.*)', 'projects',
    '/about', 'about',
    '/music', 'music',
    '/(.*)', 'home'
)

render = web.template.render('templates/')

maxDbEntry = 0;

class blogPost(db.Model):
    title = db.StringProperty(required=True)
    message = db.StringProperty(required=True, multiline=True)
    when = db.DateTimeProperty(auto_now_add=True)

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

def putLibraryInDatabase(lib):
    global maxDbEntry
    i = 0
    newEntries = ''
    for song,attributes in lib.songs.iteritems():
        if (i == maxDbEntry):
            entry = songEntry.get_by_key_name(song)
            dateModified = datetime.datetime.strptime(attributes.get('Date Modified'), '%Y-%m-%dT%H:%M:%SZ')

            if (not entry or (not entry.modified) or (entry.modified < dateModified)):

                if (not entry):
                    entry = songEntry(key_name = song)
                    newEntries += attributes.get('Artist') + ' - ' + attributes.get('Name') + '\n'

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

    if newEntries != '':
        post = blogPost(
            title = 'Newly Added Songs',
            message = newEntries)
        post.put();


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
        db.delete(dbToClear.all())

def getPlaylistContents(plid):    
    songs = [];
    logging.info("starting to build result")
    """
    for id in lib.playlists[plid]['songs']:
        if (lib.songs[id]['Kind'] != 'Apple Lossless audio file'):
            localLoc = lib.songs[id]['Location']
            localFolder = localLoc[localLoc.find('iTunes%20Music/')+15:]
            networkLoc = "http://jarman.homedns.org:82/" + localFolder
            songs.append([networkLoc,lib.songs[id]['Artist'],lib.songs[id]['Name']])
    return songs, lib.playlists[plid]['Name']
    """
    pl = playlistEntry.get_by_key_name(plid)
    entries = songEntry.get_by_key_name(pl.songs)
    for song in entries:
        songs.append([song.location, song.artist, song.name])
    
    logging.info("finished building result")
        
    return songs, pl.name

def getArtistSongs(artist):    
    songs = [];
    """
    for id in lib.artists[artist]['songs']:
        localLoc = lib.songs[id]['Location']
        localFolder = localLoc[localLoc.find('iTunes%20Music/')+15:]
        networkLoc = "http://jarman.homedns.org:82/" + localFolder
        songs.append([networkLoc,lib.songs[id]['Artist'],lib.songs[id]['Name']])
    """
    query = songEntry.gql('WHERE artist = :1 '
                          'ORDER BY album, trackNumber ASC',
                          artist)
    for song in query:
        songs.append([song.location, song.artist, song.name])
    
    return songs

def getAlbumSongs(album):    
    songs = [];
    """
    for id in lib.albums[album]:
        localLoc = lib.songs[id]['Location']
        localFolder = localLoc[localLoc.find('iTunes%20Music/')+15:]
        networkLoc = "http://jarman.homedns.org:82/" + localFolder
        songs.append([networkLoc,lib.songs[id]['Artist'],lib.songs[id]['Name']])
    """
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

    """
    for song,attributes in lib.playlists.iteritems():
        if attributes.get('Folder') == '':
            folders.append([attributes.get('Name'),attributes.get('Playlist Persistent ID'), []]);
    for song,attributes in lib.playlists.iteritems():
        if attributes.get('Folder') != '':
            for folder in folders:
                if (folder[1] == attributes.get('Parent Persistent ID')):
                    folder[2].append([attributes.get('Name'),attributes.get('Playlist Persistent ID')])
    for folder in folders:
        folder[2] = sorted(folder[2], numeric_compare);
    
    return sorted(folders, numeric_compare);
    """
    return folders

def getArtists():
    """
    query = db.GqlQuery("SELECT artist FROM songEntry")
    
    artistNames = { 'A':[], 'B':[], 'C':[], 'D':[], 'E':[], 'F':[], 'G':[], 'H':[], 'I':[], 'J':[], 'K':[], 'L':[], 'M':[], 'N':[], 'O':[], 'P':[], 'Q':[], 'R':[], 'S':[], 'T':[], 'U':[], 'V':[], 'W':[], 'X':[], 'Y':[], 'Z':[], '#':[]} 
    for entry in query:
        artist = entry.artist
        if ((artist >= 'A' and artist <= 'Z') or (artist >= 'a' and artist <= 'z')):
            s = artist[0].encode('latin-1').upper();
            artistNames[s].append(artist);
        elif artist:
            artistNames['#'].append(artist);
    for letter, names in artistNames.iteritems():
        artistNames[letter] = sorted(names)
    return artistNames
    """
    return {'Temporarily Disabled':[]}

    

def getAlbums():
    """
    query = db.GqlQuery("SELECT album FROM songEntry")
    
    albumNames = { 'A':[], 'B':[], 'C':[], 'D':[], 'E':[], 'F':[], 'G':[], 'H':[], 'I':[], 'J':[], 'K':[], 'L':[], 'M':[], 'N':[], 'O':[], 'P':[], 'Q':[], 'R':[], 'S':[], 'T':[], 'U':[], 'V':[], 'W':[], 'X':[], 'Y':[], 'Z':[], '#':[]} 
    for entry in query:
        album = entry.album
        if (album and ((album[0] >= 'A' and album[0] <= 'Z') or (album[0] >= 'a' and album[0] <= 'z'))):
            s = album[0].encode('latin-1').upper();
            albumNames[s].append(album);
        elif album:
            albumNames['#'].append(album);
    for albumLetter, names in albumNames.iteritems():
        albumNames[albumLetter] = sorted(names)
    return albumNames
    """
    return {'Temporarily Disabled':[]}
    

def findSongs(s):
    """
    cats = ['Name', 'Artist', 'Album']
    songs = [[], [], []]
    s = s.encode('latin-1').lower();


    for song,attributes in lib.songs.iteritems():
        for i in range(len(cats)):
            if attributes.get(cats[i]) and attributes.get(cats[i]).lower().find(s) > -1:
                localLoc = attributes.get('Location')
                localFolder = localLoc[localLoc.find('iTunes%20Music/')+15:]
                networkLoc = "http://jarman.homedns.org:82/" + localFolder
                songs[i].append([networkLoc,attributes.get('Artist'),attributes.get('Name')])
    
    return songs, cats
    """
    return [], []

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

class loadLibrary:
    def GET(self):
        global maxDbEntry
        if (web.input(pos='null').pos != 'null'):
            maxDbEntry = int(web.input().pos)
        try:
            global lib
            if (lib == None):
                logging.info('loading library into memory')
                lib = XMLLibraryParser("iTunes Music Library.xml")
                logging.info('Finished loading library into memory')
            putLibraryInDatabase(lib)

            return('finished!');
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

class music:    
    def GET(self):
        #songs, plName = getPlaylistContents(web.input(Playlist='0B1C1C648E64D1E0').Playlist)
        return render.main('music', render.music(getPlaylists(), [], "Loading..."));

class home:
    def GET(self, name):
        posts = db.GqlQuery(
            'SELECT * FROM blogPost '
            'ORDER BY when DESC')
        if (users.get_current_user()):
            user = users.get_current_user().nickname()
        else:
            user = 'Anonymous'
        return render.main('home', render.home(posts, user));
    
    def POST(self, name):
        post = blogPost(
            message = web.input(message='').message,
            title = web.input(title='Untitled').title)
        post.put();
        raise web.seeother('/')
    
class index:    
    def GET(self, name):
        if name == 'music.html':
            songs, plName = getPlaylistContents(web.input(Playlist='0B1C1C648E64D1E0').Playlist)
            return render.index(name, getPlaylists(), songs, plName);
        else:
            posts = db.GqlQuery(
                'SELECT * FROM blogPost '
                'ORDER BY when DESC')
            if (users.get_current_user()):
                user = users.get_current_user().nickname()
            else:
                user = 'Anonymous'
            return render.index(name, posts, user, users.create_login_url(''));
                
    def POST(self, name):
        post = blogPost(
            message = web.input(message='').message,
            title = web.input(title='Untitled').title)
        post.put();
        raise web.seeother('/')

app = web.application(urls, globals())

lib = None;

def main():
    logging.info("Received Request")
    """
    global lib
    if (songEntry.all().count(1) == 0):
        if (lib == None):
            logging.info('loading library into memory')
            lib = XMLLibraryParser("iTunes Music Library.xml")
            logging.info('Finished loading library into memory')
        putLibraryInDatabase(lib)
    """
    app.cgirun()


if __name__ == "__main__":
    main()
