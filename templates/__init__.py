from web.template import CompiledTemplate, ForLoop, TemplateResult


# coding: utf-8
def about():
    __lineoffset__ = -5
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'\n'])
    extend_([u'<link rel="stylesheet" type="text/css" href="../static/blog.css">\n'])
    extend_([u"<div id='content'>\n"])
    extend_([u"        <div id='main'style='float:left'>\n"])
    extend_([u'                <h2>About Me</h2>\n'])
    extend_([u"                <p>I'm a software engineer currently living in New York City.</p>               \n"])
    extend_([u'                <h2>About the Website</h2>\n'])
    extend_([u"                <p>I like to mess around with emerging standards, therefore you might find that it doesn't render consistently accross browsers. \n"])
    extend_([u'                Technologies such as HTML5 and CSS3 were employed. The backend uses a python framework called web.py running on Google App Engine.</p>\n'])
    extend_([u'        </div>\n'])
    extend_([u'        <link rel="stylesheet" type="text/css" href="../static/floatybox.css">  \n'])
    extend_([u"        <div id='sidebar' style='float:right'>\n"])
    extend_([u'                <h2>Contact Me</h2>\n'])
    extend_([u'                <p>Email Me: jarman [at] jarmanrogers.com</p>\n'])
    extend_([u'        </div>\n'])
    extend_([u'</div>\n'])

    return self

about = CompiledTemplate(about, 'templates/about.html')
join_ = about._join; escape_ = about._escape

# coding: utf-8
def blog (posts, user, postOffset, morePosts):
    __lineoffset__ = -4
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
    extend_([u"                <p>This website is a repository for things I'm working on. Have a look around and let me know what you think.</p>\n"])
    extend_([u"                <p>I've been doing a lot of work on the audio player recently, so it's worth a look I think.</p>\n"])
    extend_([u'        </div>\n'])
    extend_([u'</div>\n'])
    extend_([u'<script type="text/javascript" src="static/fixSidebar.js"></script>\n'])

    return self

blog = CompiledTemplate(blog, 'templates/blog.html')
join_ = blog._join; escape_ = blog._escape

# coding: utf-8
def createPost (users):
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'\n'])
    extend_([u'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">\n'])
    extend_([u'<html>\n'])
    extend_([u'<head>\n'])
    extend_([u'        <link rel="stylesheet" type="text/css" href="../static/createPost.css"></link>\n'])
    extend_([u'        <link rel="shortcut icon" href="../static/favicon.ico" type="image/x-icon"></link>\n'])
    extend_([u'        <title>Create a post</title>\n'])
    extend_([u'</head>\n'])
    extend_([u'<body>\n'])
    extend_([u"        <div id='header'>\n"])
    extend_([u"                <h1><a href='createPost'>inFlux</a></h1>\n"])
    extend_([u'                \n'])
    if (users.get_current_user()):
        extend_(['                ', u"    <div id='login'><a href='", escape_((users.create_logout_url("/createPost")), True), u"' >logout ", escape_(users.get_current_user().nickname(), True), u'</a></div> \n'])
    else:
        extend_(['                ', u"    <div id='login'><a href='", escape_((users.create_login_url("/createPost")), True), u"'>login</a></div> \n"])
    extend_([u'        </div>\n'])
    extend_([u"        <div id='content'>\n"])
    extend_([u'                <form action="" method="post">\n'])
    extend_([u'                        <input type="text" name="kw1" class="field"/><br />\n'])
    extend_([u'                        <input type="text" name="kw2" class="field"/><br />\n'])
    extend_([u'                        <input type="text" name="kw3" class="field"/><br />\n'])
    extend_([u"                        I'm interested in this search for: <br />\n"])
    extend_([u'                        <input type="range" name="duration" id="rangeSlider" ><div id="searchTime">1 month</div><br />\n'])
    extend_([u'                        <input type="submit" id="submitButton" value="Search"><br />\n'])
    extend_([u'                </form>\n'])
    extend_([u'        </div>\n'])
    extend_([u'        <link rel="stylesheet" type="text/css" href="../static/glowbuttons.css">\n'])
    extend_([u'</body>\n'])
    extend_([u'</html>\n'])

    return self

createPost = CompiledTemplate(createPost, 'templates/createPost.html')
join_ = createPost._join; escape_ = createPost._escape

# coding: utf-8
def main (curTab, content, users):
    __lineoffset__ = -4
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
    extend_([u"        <div id='header'>\n"])
    extend_([u"                <h1><a href='index.html'>jarman rogers</a></h1>\n"])
    extend_([u'                <div id="sectionTabs">\n'])
    for tab in loop.setup(['blog', 'projects', 'music', 'about']):
        if (curTab == tab):
            extend_(['                    ', u'    <a id=\'curTab\' href="../', escape_((tab), True), u'">', escape_(tab, True), u'</a>\n'])
        else:
            extend_(['                    ', u'    <a class=\'tab\' href="../', escape_((tab), True), u'">', escape_(tab, True), u'</a>\n'])
    extend_([u'                </div>\n'])
    if (users.get_current_user()):
        extend_(['                ', u"    <div id='login'><a href='", escape_((users.create_logout_url("/" + curTab)), True), u"' >logout ", escape_(users.get_current_user().nickname(), True), u'</a></div> \n'])
    else:
        extend_(['                ', u"    <div id='login'><a href='", escape_((users.create_login_url("/" + curTab)), True), u"'>login</a></div> \n"])
    extend_([u'        </div>\n'])
    extend_([u"        <div id='contentDivider'></div>\n"])
    extend_([u'        ', escape_(content, False), u'\n'])
    extend_([u'        <link rel="stylesheet" type="text/css" href="../static/glowbuttons.css">\n'])
    extend_([u'</body>\n'])
    extend_([u'</html>\n'])

    return self

main = CompiledTemplate(main, 'templates/main.html')
join_ = main._join; escape_ = main._escape

# coding: utf-8
def music (libraries, users):
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'\n'])
    extend_([u'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">\n'])
    extend_([u'<html>\n'])
    extend_([u'<head>\n'])
    extend_([u'        <link rel="shortcut icon" href="../static/favicon.ico" type="image/x-icon" />\n'])
    extend_([u'        <link rel="stylesheet" type="text/css" href="static/mPlayer.css">\n'])
    extend_([u'        <title>jarman rogers</title>\n'])
    extend_([u'</head>\n'])
    extend_([u'<body>\n'])
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
    extend_([u'                                <li><a href=\'#\' id=\'typeSelected\' onclick="return changeType(event, \'playlist\');">Playlists</a></li><li><a href=\'#\' onclick="return changeType(event, \'artists\');">Artists</a></li><li><a href=\'#\' onclick="return changeType(event, \'albums\');">Albums</a></li>\n'])
    extend_([u'                        </ul>\n'])
    extend_([u'                </div>\n'])
    extend_([u"                <div id='searchBox'><input type='text' id='searchText' onKeyUp='search(event)'/><canvas id='searchClear' onClick='clearSearch(event)' height='12' width='12'></canvas></div>\n"])
    extend_([u"                <div id='sidebarContent'>\n"])
    extend_([u'                </div>\n'])
    extend_([u"                <div id='reloadButton' onclick='return(changeLibrary(event))'>Change Library</div>\n"])
    extend_([u'        </div>\n'])
    extend_([u"        <div id='main'>\n"])
    extend_([u'                <h2>Loading...</h2>\n'])
    extend_([u'        </div>\n'])
    extend_([u"        <div id='volumePopover'>Volume<div id='volumeOuter'><div id='volumeInner'></div></div></div>\n"])
    extend_([u'</div>\n'])
    extend_([u"<div id='mPlayerObj'> </div>\n"])
    extend_([u'        <!--[if IE]>\n'])
    extend_([u"        <div id='ieShadow'>\n"])
    extend_([u'        </div>\n'])
    extend_([u'        <script src="static/excanvas.js"></script>\n'])
    extend_([u'        <script defer type="text/javascript" src="static/ieShadow.js"></script>\n'])
    extend_([u'        <![endif]-->\n'])
    extend_([u"<div id='libraries'> \n"])
    extend_([u'        <canvas id="libClose" height=20 width=20 onclick="', u'$', u'id(\'libraries\').style.display = \'none\';"></canvas>\n'])
    extend_([u'        <h2>Please select a library:</h2>\n'])
    for library in loop.setup(libraries):
        if library.user and not (users.get_current_user() and library.user == users.get_current_user().email()):
            loginNeeded = 'true'
        else:
            loginNeeded = 'false'
        extend_(['        ', u'    <div class=\'libButton\' onclick=\'return selectLibrary("', escape_((library.name), True), u'", ', escape_(loginNeeded, True), u")'>\n"])
        extend_(['        ', u"            <div class='libName'>", escape_((library.name), True), u'</div>\n'])
        extend_(['        ', u"            <div class='libTime'>last checkin ", escape_(library.dateString, True), u'</div>\n'])
        extend_(['        ', u'    </div>\n'])
    extend_([u'</div> \n'])
    extend_([u'<script type="text/javascript" src="static/jquery.min.js"></script>\n'])
    extend_([u'<script type="text/javascript" src="static/jquery.jplayer.min.js"></script>\n'])
    extend_([u'<script type="text/javascript" src="static/mPlayerButtons.js"></script>\n'])
    extend_([u'<script type="text/javascript" src="static/mPlayerControls.js"></script>\n'])
    extend_([u'</body>\n'])
    extend_([u'</html>\n'])

    return self

music = CompiledTemplate(music, 'templates/music.html')
join_ = music._join; escape_ = music._escape

# coding: utf-8
def projects():
    __lineoffset__ = -5
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'\n'])
    extend_([u'<link rel="stylesheet" type="text/css" href="../static/blog.css">\n'])
    extend_([u"<div id='content'>\n"])
    extend_([u'        <h2>Projects</h2>\n'])
    extend_([u"        <div class='post'>\n"])
    extend_([u"                <a href='http://github.com/jarman/Jarman-s-Website'>iTunes Web App - sourcecode via github</a>\n"])
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
join_ = projects._join; escape_ = projects._escape

# coding: utf-8
def random_circles():
    __lineoffset__ = -5
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
join_ = random_circles._join; escape_ = random_circles._escape

# coding: utf-8
def reviewpost (post, user, postOffset, morePosts, users):
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'\n'])
    extend_([u'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">\n'])
    extend_([u'<html>\n'])
    extend_([u'<head>\n'])
    extend_([u'        <script defer type="text/javascript" src="static/ieShadow.js"></script><![endif]-->\n'])
    extend_([u'        <link rel="stylesheet" type="text/css" href="../static/main.css">\n'])
    extend_([u'        <link rel="shortcut icon" href="../static/favicon.ico" type="image/x-icon" />\n'])
    extend_([u'        <title>Reviews</title>\n'])
    extend_([u'</head>\n'])
    extend_([u'<body>\n'])
    extend_([u"        <div id='header'>\n"])
    extend_([u"                <h1><a href='/reviews'>Alex's Reviews</a></h1>\n"])
    if (users.get_current_user()):
        extend_(['                ', u"    <div id='login'><a href='", escape_((users.create_logout_url("/reviews")), True), u"' >logout ", escape_(users.get_current_user().nickname(), True), u'</a></div> \n'])
    else:
        extend_(['                ', u"    <div id='login'><a href='", escape_((users.create_login_url("/reviews")), True), u"'>login</a></div> \n"])
    extend_([u'        </div>\n'])
    extend_([u"        <div id='contentDivider'></div>\n"])
    extend_([u'\n'])
    extend_([u'        <link rel="stylesheet" type="text/css" href="../static/blog.css">\n'])
    extend_([u"        <div id='content'>\n"])
    extend_([u'                <div id="main" style=\'float:left\'>\n'])
    extend_([u'                        <h2>', escape_(post.title, True), u'</h2>\n'])
    extend_([u"                        <div class='post'>\n"])
    extend_([u'                                <p>', escape_(post.message, False), u'</p>\n'])
    if (post.who):
        extend_(['                                ', u"    <p class='postBottom'>- ", escape_(post.who, True), u' on ', escape_((post.when.month), True), u'.', escape_((post.when.day), True), u'.', escape_(post.when.year, True), u'</p>            \n'])
    else:
        extend_(['                                ', u"    <p class='postBottom'>- jarman on ", escape_((post.when.month), True), u'.', escape_((post.when.day), True), u'.', escape_(post.when.year, True), u'</p>                                                       \n'])
    extend_([u'                        </div>\n'])
    extend_([u'                        <div>\n'])
    extend_([u"                        <div id='postNavigation'>\n"])
    if morePosts:
        extend_(['                        ', u"    <div id='olderPosts'><a href='/reviews?offset=", escape_((postOffset+10), True), u"'>&lt&lt older posts</a></div>\n"])
    if (postOffset > 10):
        extend_(['                        ', u"    <div id='newerPosts'><a href='/reviews?offset=", escape_((postOffset-10), True), u"'>newer posts &gt&gt</a></div>\n"])
    elif (postOffset > 0):
        extend_(['                        ', u"    <div id='newerPosts'><a href='/reviews'>newer posts &gt&gt</a></div>\n"])
    extend_([u'                        </div>\n'])
    if user == 'jarman':
        extend_(['                        ', u"    <form action='' method='post' accept-charset='utf-8'>\n"])
        extend_(['                        ', u"            <p>Title: <input type='text' name='title' id='title' value='' size='40'></p>\n"])
        extend_(['                        ', u"            <p><textarea name='message' id='message' rows=10 cols=60></textarea></p>\n"])
        extend_(['                        ', u"            <p><input type='submit' value='Post'></p> \n"])
        extend_(['                        ', u'    </form>\n'])
    extend_([u'                        </div>\n'])
    extend_([u'                </div>\n'])
    extend_([u"                <div id='sidebar' style='float:right'>                  \n"])
    extend_([u'                        <h2>The Details</h2>\n'])
    extend_([u'                        <p>', escape_(post.details, False), u'</p>\n'])
    extend_([u'                </div>\n'])
    extend_([u'        </div>\n'])
    extend_([u'        <script type="text/javascript" src="static/fixSidebar.js"></script>\n'])
    extend_([u'\n'])
    extend_([u'\n'])
    extend_([u'        <link rel="stylesheet" type="text/css" href="../static/glowbuttons.css">\n'])
    extend_([u'</body>\n'])

    return self

reviewpost = CompiledTemplate(reviewpost, 'templates/reviewpost.html')
join_ = reviewpost._join; escape_ = reviewpost._escape

# coding: utf-8
def reviews (posts, user, postOffset, morePosts, users):
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'\n'])
    extend_([u'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">\n'])
    extend_([u'<html>\n'])
    extend_([u'<head>\n'])
    extend_([u'        <script defer type="text/javascript" src="static/ieShadow.js"></script><![endif]-->\n'])
    extend_([u'        <link rel="stylesheet" type="text/css" href="../static/main.css">\n'])
    extend_([u'        <link rel="shortcut icon" href="../static/favicon.ico" type="image/x-icon" />\n'])
    extend_([u'        <title>Reviews</title>\n'])
    extend_([u'</head>\n'])
    extend_([u'<body>\n'])
    extend_([u"        <div id='header'>\n"])
    extend_([u"                <h1><a href='/reviews'>Alex's Reviews</a></h1>\n"])
    if (users.get_current_user()):
        extend_(['                ', u"    <div id='login'><a href='", escape_((users.create_logout_url("/reviews")), True), u"' >logout ", escape_(users.get_current_user().nickname(), True), u'</a></div> \n'])
    else:
        extend_(['                ', u"    <div id='login'><a href='", escape_((users.create_login_url("/reviews")), True), u"'>login</a></div> \n"])
    extend_([u'        </div>\n'])
    extend_([u"        <div id='contentDivider'></div>\n"])
    extend_([u'\n'])
    extend_([u'        <link rel="stylesheet" type="text/css" href="../static/blog.css">\n'])
    extend_([u"        <div id='content'>\n"])
    extend_([u'                <div id="main" style=\'float:left\'>\n'])
    extend_([u'                        <h2>updates</h2>\n'])
    for post in loop.setup(posts):
        extend_(['                        ', u"    <div class='post'>\n"])
        extend_(['                        ', u"            <a href='/reviewposts/", escape_(post.key().id(), True), u"'>", escape_(post.title, True), u'</a>\n'])
        extend_(['                        ', u'            <p>', escape_(post.message, False), u'</p>\n'])
        if (post.who):
            extend_(['                                    ', u"    <p class='postBottom'>- ", escape_(post.who, True), u' on ', escape_((post.when.month), True), u'.', escape_((post.when.day), True), u'.', escape_(post.when.year, True), u'</p>            \n'])
        else:
            extend_(['                                    ', u"    <p class='postBottom'>- jarman on ", escape_((post.when.month), True), u'.', escape_((post.when.day), True), u'.', escape_(post.when.year, True), u'</p>                                                       \n'])
        extend_(['                        ', u'    </div>\n'])
    extend_([u'                        <div>\n'])
    extend_([u"                        <div id='postNavigation'>\n"])
    if morePosts:
        extend_(['                        ', u"    <div id='olderPosts'><a href='/reviews?offset=", escape_((postOffset+10), True), u"'>&lt&lt older posts</a></div>\n"])
    if (postOffset > 10):
        extend_(['                        ', u"    <div id='newerPosts'><a href='/reviews?offset=", escape_((postOffset-10), True), u"'>newer posts &gt&gt</a></div>\n"])
    elif (postOffset > 0):
        extend_(['                        ', u"    <div id='newerPosts'><a href='/reviews'>newer posts &gt&gt</a></div>\n"])
    extend_([u'                        </div>\n'])
    if user == 'jarman':
        extend_(['                        ', u"    <form action='' method='post' accept-charset='utf-8'>\n"])
        extend_(['                        ', u"            <p>Title: <input type='text' name='title' id='title' value='' size='40'></p>\n"])
        extend_(['                        ', u'            <p>Main review</p>\n'])
        extend_(['                        ', u"            <p><textarea name='message' id='message' rows=10 cols=60></textarea></p>\n"])
        extend_(['                        ', u'            <p>details section</p>\n'])
        extend_(['                        ', u"            <p><textarea name='details' id='details' rows=10 cols=60></textarea></p>\n"])
        extend_(['                        ', u"            <p><input type='submit' value='Post'></p> \n"])
        extend_(['                        ', u'    </form>\n'])
    extend_([u'                        </div>\n'])
    extend_([u'                </div>\n'])
    extend_([u"                <div id='sidebar' style='float:right'>                  \n"])
    extend_([u'                        <h2>Welcome</h2>\n'])
    extend_([u"                        <p>Here's a site with all of the info you need to have a fabulous night out in the NYScene.</p>\n"])
    extend_([u'                        <p>Check out our posts for more info.</p>\n'])
    extend_([u'                </div>\n'])
    extend_([u'        </div>\n'])
    extend_([u'        <script type="text/javascript" src="static/fixSidebar.js"></script>\n'])
    extend_([u'\n'])
    extend_([u'\n'])
    extend_([u'        <link rel="stylesheet" type="text/css" href="../static/glowbuttons.css">\n'])
    extend_([u'</body>\n'])

    return self

reviews = CompiledTemplate(reviews, 'templates/reviews.html')
join_ = reviews._join; escape_ = reviews._escape

# coding: utf-8
def searchPosts (posts, postOffset, morePosts, datetime, users):
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'\n'])
    extend_([u'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">\n'])
    extend_([u'<html>\n'])
    extend_([u'<head>\n'])
    extend_([u'        <link rel="stylesheet" type="text/css" href="../static/createPost.css"></link>\n'])
    extend_([u'        <link rel="stylesheet" type="text/css" href="../static/blog.css"></link>\n'])
    extend_([u'        <link rel="shortcut icon" href="../static/favicon.ico" type="image/x-icon"></link>\n'])
    extend_([u'        <title>Create a post</title>\n'])
    extend_([u'</head>\n'])
    extend_([u'<body>\n'])
    extend_([u"        <div id='header'>\n"])
    extend_([u"                <h1><a href='createPost'>inFlux</a></h1>\n"])
    extend_([u'                \n'])
    if (users.get_current_user()):
        extend_(['                ', u"    <div id='login'><a href='", escape_((users.create_logout_url("/searchPosts")), True), u"' >logout ", escape_(users.get_current_user().nickname(), True), u'</a></div> \n'])
    else:
        extend_(['                ', u"    <div id='login'><a href='", escape_((users.create_login_url("/searchPosts")), True), u"'>login</a></div> \n"])
    extend_([u'        </div>\n'])
    extend_([u"        <div id='content'>              \n"])
    extend_([u'                <h2>Results</h2>\n'])
    for post in loop.setup(posts):
        extend_(['                ', u"    <div class='post'>\n"])
        extend_(['                ', u'            <a>', escape_(post.keywords[0], True), u' ', escape_(post.keywords[1], True), u' ', escape_(post.keywords[2], True), u'</a>\n'])
        extend_(['                ', u"            <p class='postBottom'>", escape_(post.user, True), u' on ', escape_((post.submitDate.month), True), u'.', escape_((post.submitDate.day), True), u'.', escape_(post.submitDate.year, True), u'\n'])
        extend_(['                ', u'            and valid for ', escape_(( (post.endDate - datetime.datetime.now()).days), True), u' more days</p>           \n'])
        extend_(['                ', u'\n'])
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
    extend_([u'        </div>\n'])
    extend_([u'        <link rel="stylesheet" type="text/css" href="../static/glowbuttons.css">\n'])
    extend_([u'</body>\n'])
    extend_([u'</html>\n'])

    return self

searchPosts = CompiledTemplate(searchPosts, 'templates/searchPosts.html')
join_ = searchPosts._join; escape_ = searchPosts._escape

