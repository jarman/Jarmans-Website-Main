import re
class XMLLibraryParser:
	def __init__(self,xmlLibrary):
		f = open(xmlLibrary)
		s = f.read()
		f.close();
		lines = s.split("\n")
		self.songs, self.playlists = self.parser(lines)
		#self.albums, self.artists, self.albumNames, self.artistNames = self.getAlbumsAndArtists()
		
	def getValue(self,restOfLine):
		value = re.sub("<.*?>","",restOfLine)
		#u = unicode(value,"utf-8")
		#cleanValue = u.encode("ascii","xmlcharrefreplace")
		value = value.replace('&#38;', '&');
		return value

	def keyAndRestOfLine(self,line):
		rawkey = re.search('<key>(.*?)</key>',line).group(0)
		key = re.sub("</*key>","",rawkey)
		restOfLine = re.sub("<key>.*?</key>","",line).strip()
		return key,restOfLine

	def parser(self,lines):
		dicts = 0
		songs = {}
		playlists = {}
		inSong = False
		inPlaylists = False
		for line in lines:
			if re.search('<dict>',line):
				dicts += 1
			if not inPlaylists:
                                if re.search('</dict>',line):
                                        dicts -= 1
                                        inSong = False
                                        songs[songkey] = temp
                                if dicts == 2 and re.search('<key>(.*?)</key>',line):
                                        rawkey = re.search('<key>(.*?)</key>',line).group(0)
                                        songkey = re.sub("</*key>","",rawkey)
                                        inSong = True
                                        temp = {}
                                if dicts == 3  and re.search('<key>(.*?)</key>',line):
                                        key,restOfLine = self.keyAndRestOfLine(line)
                                        temp[key] = self.getValue(restOfLine)
                                if len(songs) > 0 and dicts < 2:
                                        inPlaylists = True
                                        temp = {}
                                        temp2 = []
                        else:
                                if re.search('</dict>',line):
                                        dicts -= 1
                                        if dicts == 1:
                                                temp['songs'] = temp2
                                                playlists[temp['Playlist Persistent ID']] = temp
                                                temp = {}
                                                temp2 = []
                                if dicts == 2 and re.search('<key>(.*?)</key>',line):
                                        key,restOfLine = self.keyAndRestOfLine(line)
                                        temp[key] = self.getValue(restOfLine)
                                if dicts == 3 and re.search('<key>(.*?)</key>',line):
                                        key,restOfLine = self.keyAndRestOfLine(line)
                                        temp2.append(self.getValue(restOfLine))
		return songs, playlists
	
	def getAlbumsAndArtists(self):
		tempAlbums = {}
		artists = {}
		for song,attributes in self.songs.iteritems():
			album = attributes.get('Album')
			artist = attributes.get('Artist')
			if (not tempAlbums.get(album)):
				tempAlbums[album] = []
			if (not artists.get(artist)):
				artists[artist] = {}
				artists[artist]['songs'] = []
				artists[artist]['albums'] = []
			if (album):
				tempAlbums[album].append(song)
			if (artist):
				artists[artist]['songs'].append(song)
				if (0 == artists[artist]['albums'].count(album)):
					artists[artist]['albums'].append(album);
		albums = {}
		albumNames = { 'A':[], 'B':[], 'C':[], 'D':[], 'E':[], 'F':[], 'G':[], 'H':[], 'I':[], 'J':[], 'K':[], 'L':[], 'M':[], 'N':[], 'O':[], 'P':[], 'Q':[], 'R':[], 'S':[], 'T':[], 'U':[], 'V':[], 'W':[], 'X':[], 'Y':[], 'Z':[], '#':[]} 
		for album, songs in tempAlbums.iteritems():
			albums[album] = sorted(songs, self.trackNumCompare)
			if (album and ((album[0] >= 'A' and album[0] <= 'Z') or (album[0] >= 'a' and album[0] <= 'z'))):
				s = album[0].encode('latin-1').upper();
				albumNames[s].append(album);
			else:
				albumNames['#'].append(album);
		for albumLetter, names in albumNames.iteritems():
			albumNames[albumLetter] = sorted(names)

		artistNames = { 'A':[], 'B':[], 'C':[], 'D':[], 'E':[], 'F':[], 'G':[], 'H':[], 'I':[], 'J':[], 'K':[], 'L':[], 'M':[], 'N':[], 'O':[], 'P':[], 'Q':[], 'R':[], 'S':[], 'T':[], 'U':[], 'V':[], 'W':[], 'X':[], 'Y':[], 'Z':[], '#':[]} 
		for artist, songs in artists.iteritems():
			if ((artist >= 'A' and artist <= 'Z') or (artist >= 'a' and artist <= 'z')):
				s = artist[0].encode('latin-1').upper();
				artistNames[s].append(artist);
			else:
				artistNames['#'].append(artist);
		for letter, names in artistNames.iteritems():
			artistNames[letter] = sorted(names)

		
		return albums, artists, albumNames, artistNames
		
	def trackNumCompare(self, x,y):
		xN = self.songs[x].get('Track Number')
		yN = self.songs[y].get('Track Number')
		if (not xN):
			return 1
		if (not yN):
			return -1
		if (xN > yN):
			return 1
		elif xN == yN:
			return 0
		else:  #x < y
			return -1




