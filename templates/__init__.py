from web.template import CompiledTemplate, ForLoop, TemplateResult

_dummy = CompiledTemplate(lambda: None, 'dummy')
join_ = _dummy._join
escape_ = _dummy._escape

def about():
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u"<div id='content'>\n"])
    extend_([u"        <div id='main'style='float:left'>\n"])
    extend_([u'                <h2>About Me</h2>\n'])
    extend_([u"                <p>I'm a software engineer currently living in Seattle, WA.</p>         \n"])
    extend_([u'                <h2>About the Website</h2>\n'])
    extend_([u"                <p>I like to mess around with emerging standards, therefore you might find that it doesn't render consistently accross browsers. \n"])
    extend_([u'                Technologies such as HTML5 and CSS3 were employed. The backend uses a python framework called web.py running on Google App Engine.</p>\n'])
    extend_([u'        </div>\n'])
    extend_([u'        <link rel="stylesheet" type="text/css" href="../static/floatybox.css">  \n'])
    extend_([u"        <div id='floatybox' style='float:right'>\n"])
    extend_([u'                <h2>Contact Me</h2>\n'])
    extend_([u'                <p>Email Me: jarman [at] jarmanrogers.com</p>\n'])
    extend_([u'        </div>\n'])
    extend_([u'</div>\n'])

    return self

about = CompiledTemplate(about, 'templates/about.html')

def albums (name, albums):
    __lineoffset__ = -3
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'\n'])
    extend_([u'<html>\n'])
    extend_([u'<h2>', escape_(name, True), u'</h2>\n'])
    extend_([u"<ul id='sidebarContent'>\n"])
    items = albums.items();
    items.sort()
    for folder, folderContents in loop.setup(items):
        extend_([u'    <li><a onclick="return openFolder(event, \'', escape_(folder, True), u'\')" href=\'blah.html\'>', escape_(folder, True), u'</a></li>\n'])
        extend_([u"    <div class='folder' id='", escape_(folder, True), u"'>\n"])
        extend_([u'            <ul>\n'])
        for pl in loop.setup(folderContents):
            extend_(['            ', u'    <li><a onClick=\'return getContent(event, "', escape_(name, True), u'", "', escape_(pl, True), u'")\' href="music.html?', escape_(name, True), u'=', escape_(pl, True), u'">', escape_(pl, True), u'</a></li>\n'])
        extend_([u'            </ul>\n'])
        extend_([u'    </div>\n'])
    extend_([u'</ul>\n'])
    extend_([u'</html>\n'])

    return self

albums = CompiledTemplate(albums, 'templates/albums.html')

def blog (posts, user, postOffset, morePosts):
    __lineoffset__ = -3
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'\n'])
    extend_([u'<link rel="stylesheet" type="text/css" href="../static/blog.css">\n'])
    extend_([u"<div id='content'>\n"])
    extend_([u'        <div id="main" style=\'float:left\'>\n'])
    extend_([u'                <h2>updates</h2>\n'])
    for post in loop.setup(posts):
        extend_(['                ', u"    <div class='post'>\n"])
        extend_(['                ', u'            <a>', escape_(post.title, True), u'</a>\n'])
        extend_(['                ', u'            <p>', escape_(post.message, False), u'</p>\n'])
        if (post.who):
            extend_(['                            ', u"    <p class='postBottom'>- ", escape_(post.who, True), u' on ', escape_((post.when.month), True), u'.', escape_((post.when.day), True), u'.', escape_(post.when.year, True), u'</p>            \n'])
        else:
            extend_(['                            ', u"    <p class='postBottom'>- jarman on ", escape_((post.when.month), True), u'.', escape_((post.when.day), True), u'.', escape_(post.when.year, True), u'</p>                                                       \n'])
        extend_(['                ', u'    </div>\n'])
    extend_([u'                <div>\n'])
    extend_([u"                <div id='postNavigation'>\n"])
    if morePosts:
        extend_(['                ', u"    <div id='olderPosts'><a href='/blog?offset=", escape_((postOffset+10), True), u"'>&lt&lt older posts</a></div>\n"])
    if (postOffset > 10):
        extend_(['                ', u"    <div id='newerPosts'><a href='/blog?offset=", escape_((postOffset-10), True), u"'>newer posts &gt&gt</a></div>\n"])
    elif (postOffset > 0):
        extend_(['                ', u"    <div id='newerPosts'><a href='/blog'>newer posts &gt&gt</a></div>\n"])
    extend_([u'                </div>\n'])
    if user == 'jarman':
        extend_(['                ', u"    <form action='' method='post' accept-charset='utf-8'>\n"])
        extend_(['                ', u"            <p>Title: <input type='text' name='title' id='title' value='' size='40'></p>\n"])
        extend_(['                ', u"            <p><textarea name='message' id='message' rows=10 cols=60></textarea></p>\n"])
        extend_(['                ', u"            <p><input type='submit' value='Post'></p> \n"])
        extend_(['                ', u'    </form>\n'])
    extend_([u'                </div>\n'])
    extend_([u'        </div>\n'])
    extend_([u"        <div id='sidebar' style='float:right'>                  \n"])
    extend_([u'                <h2>Welcome</h2>\n'])
    extend_([u"                <p>This website is a repository for things i'm working on. Have a look around and let me know what you think.</p>\n"])
    extend_([u"                <p>I've been doing a lot of work on the audio player recently, so it's worth a look I think.</p>\n"])
    extend_([u'        </div>\n'])
    extend_([u'</div>\n'])
    extend_([u'<script type="text/javascript" src="static/fixSidebar.js"></script>\n'])

    return self

blog = CompiledTemplate(blog, 'templates/blog.html')

def main (curTab, content):
    __lineoffset__ = -3
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'\n'])
    extend_([u'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">\n'])
    extend_([u'<html>\n'])
    extend_([u'<head>\n'])
    extend_([u'        <!--[if IE]><script src="static/excanvas.js"></script>\n'])
    extend_([u'        <script defer type="text/javascript" src="static/ieShadow.js"></script><![endif]-->\n'])
    extend_([u'        <link rel="stylesheet" type="text/css" href="../static/main.css">\n'])
    extend_([u'        <link rel="shortcut icon" href="../static/favicon.ico" type="image/x-icon" />\n'])
    extend_([u'        <title>jarman rogers</title>\n'])
    extend_([u'</head>\n'])
    extend_([u'<body>\n'])
    extend_([u"        <div id='center'>\n"])
    extend_([u"                <h1><a href='index.html'>jarman rogers</a></h1>\n"])
    extend_([u'                <div id="topMenu">\n'])
    for tab in loop.setup(['blog', 'projects', 'music', 'about']):
        if (curTab == tab):
            extend_(['                    ', u'    <a id=\'curTab\' href="../', escape_((tab), True), u'">', escape_(tab, True), u'</a>\n'])
        else:
            extend_(['                    ', u'    <a class=\'tab\' href="../', escape_((tab), True), u'">', escape_(tab, True), u'</a>\n'])
    extend_([u'                </div>\n'])
    extend_([u'                ', escape_(content, True), u'\n'])
    extend_([u"                <div id='footer'>\n"])
    extend_([u'                        design by jarman rogers \n'])
    extend_([u'                </div>\n'])
    extend_([u'        </div>\n'])
    extend_([u'        <!--[if IE]>\n'])
    extend_([u"        <div id='ieShadow'>\n"])
    extend_([u'        </div>\n'])
    extend_([u'        <script src="static/excanvas.js"></script>\n'])
    extend_([u'        <script defer type="text/javascript" src="static/ieShadow.js"></script>\n'])
    extend_([u'        <![endif]-->\n'])
    extend_([u'        <link rel="stylesheet" type="text/css" href="../static/glowbuttons.css">\n'])
    extend_([u'</body>\n'])
    extend_([u'</html>\n'])

    return self

main = CompiledTemplate(main, 'templates/main.html')

def music (playlists, songs, title='.Recently Added'):
    __lineoffset__ = -3
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'\n'])
    extend_([u'<link rel="stylesheet" type="text/css" href="static/mPlayer.css">\n'])
    extend_([u"<div id='mPlayer'>\n"])
    extend_([u"        <a href='#' onclick='return playSong(null, event)' class='mpButton' id='play'><canvas id='playCanvas' height='12' width='10'>play</canvas></a>\n"])
    extend_([u"        <a href='#' onclick='return prevSong(event)' class='mpButton' id='prev'><canvas id='prevCanvas' height='10' width='15'>prev</canvas></a>\n"])
    extend_([u"        <a href='#' onclick='return seekBackward(event)' class='mpButton' id='backward'><canvas id='backCanvas' height='10' width='15'></canvas></a>\n"])
    extend_([u"        <a href='#' onclick='return seekForward(event)' class='mpButton' id='forward'><canvas id='forwCanvas' height='10' width='15'></canvas></a>\n"])
    extend_([u"        <a href='#' onclick='return nextSong(event)' class='mpButton' id='next'><canvas id='nextCanvas' height='10' width='15'>next</canvas></a>\n"])
    extend_([u"        <a href='#' onclick='return toggleRepeat(event)' class='mpButton' id='repeat'><canvas id='repeatCanvas' height='12' width='17'>repeat</canvas></a>\n"])
    extend_([u"        <a href='#' onclick='return toggleShuffle(event)' class='mpButton' id='shuffle'><canvas id='shuffleCanvas' height='12' width='20'>shuffle</canvas></a>\n"])
    extend_([u"        <a href='#' onmouseover='return openVolume(event)' onmouseout='closeVolume(event)' onclick='return mute(event)' class='mpButton' id='volume'><canvas id='volumeCanvas' height='12' width='16'>volume</canvas></a>\n"])
    extend_([u"        <div onmouseout='closeVolume(event)' onmousedown='return startDrag(event)' return false' id='volBar'><div id='volSlider'></div></div>\n"])
    extend_([u"        |<div id='songTime'></div>|<div id='songInfo'></div>\n"])
    extend_([u'</div>\n'])
    extend_([u"<a  id='progressBar' onMouseDown='return setMouseDown(event)' onClick='return false' href='#'><div id='loadBar'><div id='time'></div></div></a>\n"])
    extend_([u"<div id='content'>\n"])
    extend_([u"        <div id ='mediaSidebar'>\n"])
    extend_([u"                <div id='typeSelect'>\n"])
    extend_([u'                        <ul>\n'])
    extend_([u'                                <li><a href=\'#\' id=\'typeSelected\' onclick="return changeType(event, \'Playlist\');">Playlists</a></li><li><a href=\'#\' onclick="return changeType(event, \'artists\');">Artists</a></li><li><a href=\'#\' onclick="return changeType(event, \'albums\');">Albums</a></li>\n'])
    extend_([u'                        </ul>\n'])
    extend_([u'                </div>\n'])
    extend_([u"                <div id='searchBox'><input type='text' id='searchText' onKeyUp='search(event)'/><canvas id='searchClear' onClick='clearSearch(event)' height='12' width='12'></canvas></div>\n"])
    extend_([u"                <div id='sidebarContent'>\n"])
    extend_([u'                        <h2>Playlists</h2>\n'])
    extend_([u"                        <ul id='sidebarContent'>\n"])
    for folder in loop.setup(playlists):
        extend_(['                        ', u'    <li><a onclick="return openFolder(event, \'', escape_(folder[1], True), u'\')" href=\'blah.html\'>', escape_(folder[0], True), u'</a></li>\n'])
        extend_(['                        ', u"    <div class='folder' id='", escape_(folder[1], True), u"'>\n"])
        extend_(['                        ', u'            <ul>\n'])
        for pl in loop.setup(folder[2]):
            if (title == pl[0]):
                extend_(['                                        ', u'    <li id=\'curPl\'><a onClick=\'return getContent(event, "Playlist", "', escape_(pl[1], True), u'")\' href="music.html?Playlist=', escape_(pl[1], True), u'">', escape_(pl[0], True), u'</a></li> \n'])
            else:
                extend_(['                                        ', u'    <li><a onClick=\'return getContent(event, "Playlist", "', escape_(pl[1], True), u'")\' href="music.html?Playlist=', escape_(pl[1], True), u'">', escape_(pl[0], True), u'</a></li>\n'])
        extend_(['                        ', u'            </ul>\n'])
        extend_(['                        ', u'    </div>\n'])
    extend_([u'                        </ul>\n'])
    extend_([u'                </div>\n'])
    extend_([u"                <button type='button' id='reloadButton' style='display:none' onclick='return(reloadLibrary())'>Reload Library</button>\n"])
    extend_([u'        </div>\n'])
    extend_([u"        <div id='main'>\n"])
    extend_([u'                <h2>', escape_(title, True), u'</h2>\n'])
    extend_([u'                        <ul>\n'])
    for name in loop.setup(songs):
        extend_(['                        ', u"    <li><a onclick='return playSong(", escape_(loop.index0, True), u', event)\' href="', escape_(name[0], True), u'">', escape_(loop.index, True), u'. ', escape_(name[1], True), u' - ', escape_(name[2], True), u'</a></li>\n'])
    extend_([u'                        </ul>\n'])
    extend_([u'        </div>\n'])
    extend_([u"        <div id='volumePopover'>Volume<div id='volumeOuter'><div id='volumeInner'></div></div></div>\n"])
    extend_([u'</div>\n'])
    extend_([u"<div id='mPlayerObj'> </div>\n"])
    extend_([u'<script type="text/javascript" src="static/jquery.min.js"></script>\n'])
    extend_([u'<script type="text/javascript" src="static/jquery.jplayer.min.js"></script>\n'])
    extend_([u'<script type="text/javascript" src="static/mPlayerButtons.js"></script>\n'])
    extend_([u'<script type="text/javascript" src="static/mPlayerControls.js"></script>\n'])

    return self

music = CompiledTemplate(music, 'templates/music.html')

def playlistsxml (playlists):
    __lineoffset__ = -3
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'\n'])
    extend_([u'<playlists>\n'])
    for folder in loop.setup(playlists):
        extend_([u'    <folder id="', escape_(folder[1], True), u'" name="', escape_(folder[0], True), u'">\n'])
        for pl in loop.setup(folder[2]):
            extend_(['    ', u'    <playlist id="', escape_(pl[1], True), u'" name="', escape_(pl[0], True), u'" />\n'])
        extend_([u'    </folder>\n'])
    extend_([u'</playlists>\n'])

    return self

playlistsxml = CompiledTemplate(playlistsxml, 'templates/playlistsxml.xml')

def projects():
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u"<div id='content'>\n"])
    extend_([u'        <h2>Projects</h2>\n'])
    extend_([u"        <div class='post'>\n"])
    extend_([u"                <a href='music'>iTunes Web App</a>\n"])
    extend_([u"                <p>I wanted a way to access my music at work and didn't like the existing solutions I found, so i built one. \n"])
    extend_([u"                It tends to work best in newer versions of Chrome/Safari/Firefox. Opera and IE kind of work but don't look quite the same.</p>\n"])
    extend_([u'                <p>Some Features:</p>\n'])
    extend_([u'                <ul>\n'])
    extend_([u'                        <li>Now attempts to use HTML5 audio and then falls back to flash for other browsers. I replaced my own HTML5 audio implementation with an a plugin called jPlayer</li>\n'])
    extend_([u'                        <li>Added the ablility to shuffle tracks</li>\n'])
    extend_([u'                        <li>Redesigned the sidebar CSS to be a bit more minimalistic. Made some elements look glossy (in some browsers).</li>\n'])
    extend_([u'                        <li>Added the ability to view by artists and albums</li>\n'])
    extend_([u'                        <li>Added the ability to change the volume</li>\n'])
    extend_([u'                        <li>The progress of the buffering is now displayed</li>\n'])
    extend_([u'                        <li>Fixed search so that only most recent AJAX results are loaded</li>\n'])
    extend_([u'                        <li>HTML now served by Google App Engine and not the computer in my living room</li>\n'])
    extend_([u'                        <li>Key Commands are supported:\n'])
    extend_([u'                        <ul>\n'])
    extend_([u'                                <li><b>Spacebar</b>: play/pause</li>\n'])
    extend_([u'                                <li><b>Left/Right Arrows</b>: Previous/Next Track</li>\n'])
    extend_([u'                                <li><b>Up/Down Arrows</b>: Volume Up/Down (check out the UI)</li>\n'])
    extend_([u'                                <li><b>s</b>: Toggle Shuffle</li>\n'])
    extend_([u'                                <li><b>r</b>: Toggle Repeat</li>\n'])
    extend_([u'                        </ul>\n'])
    extend_([u'                        </li>\n'])
    extend_([u'                        <li>Bugs\n'])
    extend_([u'                        <ul>\n'])
    extend_([u"                                <li>If the file isn't an MP3 things aren't pretty. I have some AAC and Apple Lossless files which don't behave well. I've removed lossless from the playlists but normal AAC files remain, since they play in some browsers. Note that this may cause problems.</li>\n"])
    extend_([u'                        </ul>\n'])
    extend_([u'                        </li>\n'])
    extend_([u'                </ul>\n'])
    extend_([u'        </div>\n'])
    extend_([u"        <div class='post'>\n"])
    extend_([u"                <a href='projects/random_circles.html'>Random Circles</a>\n"])
    extend_([u'                <p>Generates randomly placed circles on a canvas</p>    \n'])
    extend_([u'        </div>\n'])
    extend_([u"        <div class='post'>\n"])
    extend_([u"                <a href='http:\\\\jarman.homedns.org:82\\sudiflash\\index.html'>Sudikoff Interactive Directory</a>\n"])
    extend_([u"                <p>An interactive directory of the dartmouth computer science department. Note that it was designed for a touchscreen and also that the database that the flash uses is incomplete. It wasn't optimized for the internet at all because it would have normally run locally.</p>                 \n"])
    extend_([u'        </div>\n'])
    extend_([u'</div>\n'])

    return self

projects = CompiledTemplate(projects, 'templates/projects.html')

def random_circles():
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u"<div id='content'>\n"])
    extend_([u'        <h2>Random circles</h2>\n'])
    extend_([u'        A demo I made of the HTML5 canvas capabilities. It simply creates a bunch of circles with a random number generator.    \n'])
    extend_([u'        <canvas id="canvas" height="400" width="800">This text is displayed if your browser does not support HTML5 Canvas.</canvas>\n'])
    extend_([u'        <script type="text/javascript" src="../static/gEngine.js"></script>\n'])
    extend_([u'</div>\n'])

    return self

random_circles = CompiledTemplate(random_circles, 'templates/random_circles.html')

def search (search, songs, titles):
    __lineoffset__ = -3
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'\n'])
    extend_([u'<html>\n'])
    extend_([u"        <h1 style='display:none'>", escape_(search, True), u'</h1>\n'])
    extend_([u"        <h2>Search for '", escape_(search, True), u"'</h2>\n"])
    i = 0
    for title in loop.setup(titles):
        extend_([u'    <h2>', escape_(title, True), u'</h2>\n'])
        extend_([u'            <ul>\n'])
        for name in loop.setup(songs[loop.index0]):
            extend_(['            ', u"    <li><a class='songLink' onclick='return playSong(", escape_(i, True), u', event)\' href="', escape_(name[0], True), u'">', escape_(loop.index, True), u'. ', escape_(name[1], True), u' - ', escape_(name[2], True), u'</a></li>\n'])
            i += 1;
        extend_([u'            </ul>\n'])
    extend_([u'</html>                         \n'])

    return self

search = CompiledTemplate(search, 'templates/search.html')

def songs (songs, title):
    __lineoffset__ = -3
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'\n'])
    extend_([u'<html>\n'])
    extend_([u'<h2>', escape_(title, True), u'</h2>\n'])
    extend_([u'        <ul>\n'])
    for name in loop.setup(songs):
        extend_(['        ', u"    <li><a class='songLink' onclick='return playSong(", escape_(loop.index0, True), u', event)\' href="', escape_(name[0], True), u'">', escape_(loop.index, True), u'. ', escape_(name[1], True), u' - ', escape_(name[2], True), u'</a></li>\n'])
    extend_([u'        </ul>\n'])
    extend_([u'</html>                         \n'])

    return self

songs = CompiledTemplate(songs, 'templates/songs.html')

def songsxml (songs, title):
    __lineoffset__ = -3
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'\n'])
    extend_([u'<songs>\n'])
    extend_([u'<title>', escape_(title, True), u'</title>\n'])
    for name in loop.setup(songs):
        extend_([u'    <song>\n'])
        extend_([u'            <url>', escape_(name[0], True), u'</url>\n'])
        extend_([u'            <name>', escape_(loop.index, True), u'. ', escape_(name[1], True), u' - ', escape_(name[2], True), u'</name>\n'])
        extend_([u'    </song>\n'])
    extend_([u'</songs>                                \n'])

    return self

songsxml = CompiledTemplate(songsxml, 'templates/songsxml.xml')

