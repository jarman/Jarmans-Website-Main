var curSongNumber = 0;
var repeat = false;
var shuffle = false;
var mPlayer = null;
var playing = false;
var posX = 0;
var posY = 0;
var mouseDown = false;
var mouseDownTime = 0;
var lastUpdate = 0;
var songs = []
var errors = 0;
var shuffleOrder;
var playedSomething = false;
var songsReloaded = false;
var sidebarPl = null;
var sidebarArtists = null;
var sidebarAlbums = null;
var volume = 100;
var prevVolume = 0;
var timeoutID = null;


function playSong(songNum, e) {
	
	if (playing && songNum == null )
	{
		mPlayer.jPlayer("pause");
		playing = false;
	}
	else 
	{
		playing = true;
		playedSomething = true;
		
		if (songNum != null && songsReloaded)
		{
			updateSongList()
		}
		
		if (songNum == null && !mPlayer.jPlayer("getData", "diag.isPlaying")) 
		{
			mPlayer.jPlayer("play");
		}
		else
		{
			curSongNumber = songNum;
			makeShuffleOrder();
			loadSong(true);
		}
		
	}
	
	drawPlayButton();
	
	e = e || window.event;
	e.returnValue = false;
	return false;
}

function loadSong(autoPlay)
{
	if (shuffle) 
	{
		mPlayer.jPlayer("setFile", songs[shuffleOrder[curSongNumber]][1]);
		document.getElementById("songInfo").innerHTML = songs[shuffleOrder[curSongNumber]][0];
		document.title = songs[shuffleOrder[curSongNumber]][0];
	}
	else if (songs && songs[curSongNumber])
	{
		mPlayer.jPlayer("setFile", songs[curSongNumber][1]);
		document.getElementById("songInfo").innerHTML = songs[curSongNumber][0];
		document.title = songs[curSongNumber][0];
	}
	
	if (autoPlay)
	{
		mPlayer.jPlayer("play");
	}
	
	links = $id('main').getElementsByTagName("li"); 
	
	for (i = 0; i < links.length; i++) {
		if (links[i].id == 'curSong') {
			links[i].id = '';
		}
		temp = links[i].textContent || links[i].innerText
		if (((shuffle) && (temp == songs[shuffleOrder[curSongNumber]][0])) || ((!shuffle) && (temp == songs[curSongNumber][0]))) {
			links[i].id = 'curSong';
		}
	}
}

function nextSong()
{
	curSongNumber = (curSongNumber + 1) % songs.length
	
	if (playing) {
		loadSong(true);
	}
	else {
		loadSong(false);
	}
	
	if (window.event) {
		window.event.returnValue = false;
	}
	return false;
}

function prevSong()
{
	curSongNumber = (curSongNumber - 1 + songs.length) % songs.length
	
	if (playing) {
		loadSong(true);
	}
	else {
		loadSong(false);
	}
	
	window.event.returnValue = false;
	return false;
}

function toggleRepeat()
{
	repeat = !repeat;
	
	drawRepeatButton();
	
	if (window.event)
		window.event.returnValue= false;
	return false;
}

function toggleShuffle()
{
	shuffle = !shuffle;
	
	drawShuffleButton();
	
	if (shuffle)
	{
		makeShuffleOrder();
	}
	else
	{
		curSongNumber = shuffleOrder[curSongNumber]
	}
	
	if (window.event)
		window.event.returnValue= false;
	return false;
}

function openVolume(e)
{
	e = e || window.event;
	var target = e.target || e.srcElement;
	
	if (!mouseDown) {
		if ($id('ieShadow'))
		{
			$id('volBar').style.display = 'inline'
		}
		$id('volSlider').style.display = 'block'
		$id('volBar').style.opacity = '1'
		$id('volBar').style.height = '120px'
		$id('volume').style.border = '1px solid #797770'
		$id('volume').style.borderBottom = '0px solid transparent'
		$id('volume').style.backgroundColor = '#A9A7A0';
		if (!$id('ieShadow')) {
			$id('volume').style.background = '-webkit-gradient(linear, left bottom, right bottom, from(#B9B7B0), color-stop(0.45, #A9A7A0), color-stop(0.50, #999790))';
			$id('volume').style.background = '-moz-linear-gradient(right, #999790 50%, #A9A7A0 55%, #B9B7B0)';
		}
	}
	
	e.returnValue= false;
	return false;
}

function closeVolume(e)
{
	e = e || window.event;
	var target = e.toElement || e.relatedTarget;
	
	if (!target)
	{
		target = e.target || e.srcElement;
	}

	if (!target || (target && target.id != 'volBar' && target.id != 'volumeCanvas' && target.id != 'volume' && target.id != 'volSlider' && !mouseDown)) 
	{
		$id('volSlider').style.display = 'none'
		$id('volBar').style.opacity = '0'
		$id('volBar').style.height = '0px'
		if ($id('ieShadow'))
		{
			$id('volBar').style.display = 'none'
		}
		$id('volume').style.border = '1px solid transparent';
		$id('volume').style.backgroundColor = 'transparent';
		$id('volume').style.background = '';
	}
}

function startDrag(e)
{
	e = e || window.event;
	var target = e.target || e.srcElement;
	
	posY = e.clientY ? e.clientY : e.pageY 
	prevVolume = volume;
	mouseDown = true;
	
	moveSlider(e)
	
	if (target.id == 'volSlider')
	{
		document.body.onmousemove = moveSlider;
	}
	document.body.onmouseup = volumeMouseUp;
	
	e.returnValue= false;
	return false;
}

function moveSlider(e){
	e = e || window.event;
	var target = e.target || e.srcElement;
	curY = e.clientY ? e.clientY : e.pageY
	
	volume = prevVolume + (posY - curY)
	
	if (volume < 0) {
		volume = 0;
	}
	else if (volume > 100) {
		volume = 100;
	}
	
	if (mouseDown) {
		$id('volSlider').style.marginTop = 103 - volume +  'px'
		mPlayer.jPlayer( "volume", volume);
		drawVolumeButton();
	}
	
	e.returnValue= true;
	return true;
}

function volumeMouseUp(e)
{
	e = e || window.event;
	mouseDown = false;
	var target = e.target || e.srcElement;
	
	if (document.body.onmousemove != moveSlider && target.id == 'volBar'){
		//alert(e.offsetY)
		if (e.offsetY) {
			volume = 108 - e.offsetY
		}
		else {
			//alert(e.layerY + 'volBar').offsetY)
			//alert($id('volBar').offsetTop)
			volume = 108 - e.layerY
		}
		
		if (volume < 0) {
			volume = 0;
		}
		else if (volume > 100) {
			volume = 100;
		}
		
		$id('volSlider').style.marginTop = 103 - volume +  'px'
		mPlayer.jPlayer( "volume", volume);
		drawVolumeButton();
	}
	
	document.body.onmousemove = null;
	document.body.onmouseup = null;
	closeVolume(e);
	
	e.returnValue= true;
	return true;
}

function mute(e)
{
	e = e || window.event;
	var target = e.target || e.srcElement;
	
	if (volume > 0) {
		prevVolume = volume;
		volume = 0;
	}
	else
	{
		volume = prevVolume;
	}
	
	$id('volSlider').style.marginTop = 103 - volume + 'px'
	mPlayer.jPlayer( "volume", volume);
	drawVolumeButton();
	
	e.returnValue= true;
	return true;
}

function songEnded()
{
	if (repeat)
	{
		this.play();
	}
	else
	{
		curSongNumber = (curSongNumber + 1) % songs.length
		loadSong(true);
	}
}

function seekBackward(e)
{
	curTime = mPlayer.jPlayer("getData", "diag.playedTime")
	if (curTime < 30000) 
	{
		mPlayer.jPlayer( "playHeadTime", 0);
	}
	else 
	{
		mPlayer.jPlayer( "playHeadTime", curTime - 30000);
	}
	e = e || window.event;
	e.returnValue= false;
	return false;
}

function seekForward(e)
{
	currentTime = mPlayer.jPlayer("getData", "diag.playedTime")
	
	if (currentTime < (mPlayer.jPlayer("getData", "diag.totalTime") -30000))
	{
		mPlayer.jPlayer("playHeadTime", currentTime + 30000);
	}
	e = e || window.event;
	e.returnValue= false;
	return false;
}

// ----------------------------------------------------------------- Mouse Events ---------------------------------------------------------------------------

function setMouseDown(e){
	e = e || window.event;
	curX = e.clientX ? e.clientX : e.pageX 
	mouseDown = true;
	mouseDownTime = mPlayer.jPlayer("getData", "diag.playedTime") / 1000;
	
	$id('progressBar').onDrag = new Function();
	$id('progressBar').onDragStart = new Function();
	$id('progressBar').onDragEnd = new Function();
	
	document.body.onmousemove = changeTime;
	document.body.onmouseup = setMouseUp;
	
	$id('time').style.webkitTransitionDuration = '0s';
	
	e.returnValue= false;
	return false;
}

function changeTime(e) {
	e = e || window.event;
	xPos = e.clientX ? e.clientX : e.pageX 
	
	playedPercent = mPlayer.jPlayer("getData", "diag.playedPercentAbsolute")
	
	if (mouseDown) {
		tempPos = (playedPercent * 830/100) + (xPos - curX)
		
		if (tempPos < 0) {
			tempPos = 0;
		}
		else if (tempPos > 830) {
			tempPos = 830;
		}
		
		tempTime = tempPos * duration / 830;
		
		$id("time").style.marginLeft = tempPos + 'px';
	}
	
	e.returnValue= false;
	return false;
}

function setMouseUp(e) {
	e = e || window.event;
	var xPos = e.clientX ? e.clientX : e.pageX;
	var target = e.target ? e.target : e.srcElement;
	var tempPos;
	
	playedPercent = mPlayer.jPlayer("getData", "diag.playedPercentAbsolute")
	
	if (mouseDown) {
		if (target.id != 'time' && Math.abs(xPos - curX) < 3) {
			//alert("layerX = " + e.layerX + "target = " + $(e.target).position().left + "parent =" + $(e.target).parent().position().left);
			
			offsetX = e.offsetX ? (e.offsetX - 10) : (e.layerX - $('#mPlayer').position().left + 10);
			tempPos = offsetX;
		}
		else {
			tempPos = (playedPercent * 830/100) + (xPos - curX)
		}
		
		if (tempPos < 0)
		{
			tempPos = 0;
		}
		else if (tempPos > 830)
		{
			tempPos = 830;
		}
		
		$id("time").style.marginLeft = tempPos + 'px';
		
		var newPercent = (tempPos / 830 * 10000) / mPlayer.jPlayer("getData", "diag.loadPercent")
		mPlayer.jPlayer( "playHead", newPercent);
		
		mouseDown = false;
		
	}
	
	
	document.body.onmousemove = null;
	document.body.onmouseup = null;
	$id('time').style.webkitTransitionDuration = '0.2s';
	
	e.returnValue= false;
	return false;
}

// ----------------------------------------------------------------- Formatting Screen ---------------------------------------------------------------------------

function progress(loadPercent,ppr,ppa,playedTime,totalTime)
{
	if (playedTime == null) 
	{
		playedTime = 0;
	}
		
	curTime = formatTime(playedTime);

	if (loadPercent >= 0)
	{
		$id('loadBar').style.width = Math.ceil(loadPercent * 850/100) + 'px';
		$id('loadBar').style.borderRightWidth = (850 - Math.ceil(loadPercent * 850/100)) + 'px';
	}
	
	if (totalTime > 0) 
	{
		duration = formatTime(totalTime)
		
		if (!mouseDown){
			$id("time").style.marginLeft = (ppa * 830/100) + 'px'
		}
	}
	else
	{
		$id("time").style.marginLeft = '0px'
		duration = "?";
	}
	
	
	document.getElementById("songTime").innerHTML = curTime + " / " + duration;	
}

function formatTime(i)
{
	i = i / 1000
	mins = Math.floor(i / 60)
	secs = Math.floor(i) % 60;
	
	if (secs < 10)
	{
		t = mins + ":0" + secs;
	}
	else
	{
		t = mins + ":" + secs;
	}
	
	return t
}

function readCookie(name) {
	var nameEQ = name + "=";
	var ca = document.cookie.split(';');
	for(var i=0;i < ca.length;i++) {
		var c = ca[i];
		while (c.charAt(0)==' ') c = c.substring(1,c.length);
		if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
	}
	return null;
}

function reopenFolders() {
	var nameEQ = "=open";
	var ca = document.cookie.split(';');
	for(var i=0;i < ca.length;i++) {
		var c = ca[i];
		while (c.charAt(0)==' ') c = c.substring(1,c.length);
		if (c.indexOf(nameEQ) > 0) {
			folder = c.substring(0, c.indexOf(nameEQ));
			if ($id(folder)) {
				$id(folder).style.opacity = '1';
				$id(folder).style.height = $id(folder).scrollHeight + 'px';
				
				// fix parent folder heights
				curFolder = $id(folder).parentNode.parentNode;
				while (curFolder && curFolder.className == "folderContents" && readCookie(curFolder.id) == "open") {
					curFolder.style.height = "auto"
					curFolder.style.height = curFolder.scrollHeight + 'px';
					curFolder.style.opacity = '1';
					curFolder = curFolder.parentNode.parentNode;
				}
			}
		}
	}
	fixSidebarHeight()
}

function openFolder(e, name){
	if (readCookie(name) == 'open') {
	
		$id(name).style.height = '0px';
		$id(name).style.opacity = '0';
		document.cookie = name + "=closed; path=/";
	}
	else {
		$id(name).style.opacity = '1';
		$id(name).style.height = $id(name).scrollHeight + 'px';
		document.cookie = name + "=open; path=/";
	}
	
	// fix parent folder heights
	curFolder = $id(name).parentNode.parentNode;
	while (curFolder && curFolder.className == "folderContents") {
		curFolder.style.height = "auto"
		curFolder.style.height = curFolder.scrollHeight + 'px';
		curFolder = curFolder.parentNode.parentNode;
	}
	
	if ($id('ieShadow')) {
		setTimeout(fixShadowHeight, 100);
	}
	
	fixSidebarHeight();
	
	e=window.event || e
	if (e)
	{
		e.returnValue= false;
	}
	return false;
}

function keyPress(e)
{
	e=window.event || e
	target = e.target || e.srcElement
	key = e.charCode || e.keyCode
	
	if (target.id != 'searchText')
	{
		switch (key) {
			case 32:
				playSong(null, e);
				break;
			case 39:
				nextSong()
				break;
			case 37:
				prevSong();
				break;
			case 38:
				volume = (volume < 90) ? (volume + 10) : 100;
				mPlayer.jPlayer( "volume", volume);
				showVolumePopover();
				drawVolumeButton();
				break;
			case 40:
				volume = (volume > 10) ? (volume - 10) : 0;
				mPlayer.jPlayer( "volume", volume);
				showVolumePopover();
				drawVolumeButton();
				break;
			case 82:
				toggleRepeat();
				break;
			case 83:
				toggleShuffle();
				break;
		}
		
		
		if(e.preventDefault){
			e.preventDefault()
		}
		else
		{
			e.returnValue= false;
			return false;
		}
	}
	
	//e.returnValue= true;
	//return true;
}

function showVolumePopover() {
	$id('volumePopover').style.display = 'block';
	if (!$id('ieShadow'))
	{
		$id('volumePopover').style.webkitTransitionDuration = '0.1s'
		$id('volumePopover').style.opacity = 1;
	}
	
	$id('volumeInner').style.width = volume + 'px'
	
	if (timeoutID)
	{
		clearTimeout(timeoutID)
	}
	timeoutID = setTimeout(hideVolumePopover, 1000);
}

function hideVolumePopover() {
	if ($id('ieShadow'))
	{
		$id('volumePopover').style.display = 'none';
	}
	else
	{
		$id('volumePopover').style.webkitTransitionDuration = '0.5s'
		$id('volumePopover').style.opacity = 0;
	}
	timeoutID = null;
}

function search(e)
{
	e=window.event || e
	
	//alert($id('searchText').value)
	sendRequest('/songs.html?search=' + $id('searchText').value, updateContent);
	document.cookie = "lastPage=search; path=/";
	document.cookie = "search=" + $id('searchText').value + "; path=/";
	drawSearchClearButton()
	
	e.returnValue = false;
	return false;
}

function clearSearch()
{
	$id('searchText').value = ''
	document.cookie = "search=" + "; path=/";
	reloadLastPage();
	drawSearchClearButton()
}

function getContent(e, type, id) {
	e=window.event || e
	
	$id('main').style.opacity = 0;
	sendRequest('/songs.html?' + type + '=' + id, updateContent);
	document.cookie = "lastPage=" + type + "; path=/";
	document.cookie = type + "=" + id + "; path=/";
	
	e.returnValue = false;
	return false;
}

function updateContent(req){
	if (req.responseText == 'invalid') {
		reloadLastPage()
		return;
	}
	
	temp = $id('main').innerHTML
	$id('main').innerHTML = req.responseText;
	
	if ($id('main').getElementsByTagName('h1').length) {
		name = $id('main').getElementsByTagName('h1')[0].innerHTML
		if (name != readCookie('search')) {
			// this an old search that has loaded too late;
			$id('main').innerHTML = temp;
			return;
		}
	}
	
	
	$id('main').style.opacity = 1;
	
	if (playedSomething) {
		songsReloaded = true;
	}
	else {
		updateSongList()
		curSongNumber = 0;
		loadSong(false);
	}
	
	if ($id('ieShadow')) {
		setTimeout(fixShadowHeight, 100);
	}
	
	fixSidebarHeight();
	highlightPlaylist();
	
}
	
function highlightPlaylist(){
	
	playlists = $id('sidebarContent').getElementsByTagName("li")
	titleElement = $id('main').getElementsByTagName("h2")
	
	if (titleElement.length > 0) {
		title = titleElement[0].innerHTML;
		
		for (i = 0; i < playlists.length; i++) {
			temp = playlists[i].textContent || playlists[i].innerText
			if (playlists[i].id = 'curPl') {
				playlists[i].id = "";
			}
			if (temp == title) {
				playlists[i].id = 'curPl'
			}
		}
	}
}

function fixSidebarHeight()
{
	if ($id('main').offsetHeight > ($id('mediaSidebar').offsetHeight -35) || 
		(($id('main').offsetHeight < ($id('mediaSidebar').offsetHeight - 35)) && $id('mediaSidebar').style.paddingBottom != '0px'))
	{
		$id('mediaSidebar').style.paddingBottom = '0px';
		if ($id('main').offsetHeight > ($id('mediaSidebar').offsetHeight - 35))
		{
			$id('mediaSidebar').style.paddingBottom = ($id('main').offsetHeight - $id('mediaSidebar').offsetHeight + 35) + 'px';
		}
	}
}

function fixShadowHeight()
{
	$id('ieShadow').style.height = $id('center').offsetHeight + 'px';
}

function changeType(e, type) {
	e = e || window.event;
	target = e.target || e.srcElement
	
	if ($id('typeSelected').innerHTML == 'Playlists')
	{
		sidebarPl = $id('sidebarContent').innerHTML;
	}
	else if ($id('typeSelected').innerHTML == 'Albums')
	{
		sidebarAlbums = $id('sidebarContent').innerHTML;
	}
	else if ($id('typeSelected').innerHTML == 'Artists')
	{
		sidebarArtists = $id('sidebarContent').innerHTML;
	}
	
	$id('typeSelected').id = null
	target.id = 'typeSelected';
	
	// first try to reload the saved content into the sidebar
	if (target.innerHTML == 'Playlists' && sidebarPl) {
		$id('sidebarContent').innerHTML = sidebarPl;
		fixSidebarHeight();
		highlightPlaylist();
	}
	else if (target.innerHTML == 'Artists' && sidebarArtists) {
		$id('sidebarContent').innerHTML = sidebarArtists;
		fixSidebarHeight();
		highlightPlaylist();
	}
	else if (target.innerHTML == 'Albums' && sidebarAlbums) {
		$id('sidebarContent').innerHTML = sidebarAlbums;
		fixSidebarHeight();
		highlightPlaylist();
	}
	else {
		// if there is no saved content, reload from the server
		$id('sidebarContent').style.opacity = 0;
		sendRequest('/' + type + '.html', updateSidebar);
	}
	
	document.cookie = "lastPage=" + type + "; path=/";
	
	e.returnValue = false;
	return false;
}

function updateSidebar(req){
	$id('sidebarContent').innerHTML = req.responseText;
	$id('sidebarContent').style.opacity = 1;
	
	reopenFolders();
	highlightPlaylist();
}
	
function updateSongList() {
	
	links = $id('main').getElementsByTagName("a"); 
	
	songs = []
	for (i = 0; i < links.length; i++) {
		songs.push([links[i].innerHTML, links[i].href])
	}
	
	if (shuffle)
	{
		makeShuffleOrder();
	}
}

function makeShuffleOrder()
{
	shuffleOrder = []
	
	for (var i = 0; i < songs.length; i++)
	{
		shuffleOrder.push(i);
	}
	
	for (i = 0; i < songs.length; i++)
	{
		pos = Math.floor(Math.random() * songs.length)
		
		if (pos != curSongNumber && i != curSongNumber) 
		{
			temp = shuffleOrder[pos]
			shuffleOrder[pos] = shuffleOrder[i]
			shuffleOrder[i] = temp
		}
	}
}

function mediaError(e)
{	
	if (errors < 10)
	{
		nextSong()
		errors += 1;
	}
	else
	{
		alert("10 playback errors");
	}
}

function loadPage()
{
	// Load the sidebar
	sendRequest('/playlists.html', updateSidebar);
	
	reloadLastPage();
	reopenFolders();
	loadSong(false)
}

function reloadLastPage()
{	
	if (readCookie('lastPage') == 'search' && readCookie('search') && readCookie('search').length > 1)
	{
		id = readCookie('search');
		sendRequest('/songs.html?search=' + readCookie('search'), updateContent);
		if (!$id('searchText').value)
		{
			$id('searchText').value = readCookie('search');
			drawSearchClearButton()
		}
	}
	else if (readCookie('Playlist'))
	{
		id = readCookie('Playlist');
		sendRequest('/songs.html?Playlist=' + id, updateContent);
	}
	else
	{
		document.cookie = "lastPage=Playlist; path=/";
        document.cookie = "Playlist=6FC1A60398C0CEB9; path=/";
        document.cookie = "9F4D3B18D81B3CC1=open; path=/";
		sendRequest('/songs.html?Playlist=6FC1A60398C0CEB9', updateContent);
	}
}

function finishedReload()
{
	$id('reloadButton').style.background = "webkit-gradient(linear, left top, left bottom, from(#444), to(#222))";
	alert('reload is finished');
}

function selectLibrary(lib, loginNeeded){
	document.cookie = "library=" + lib + "; path=/";
	if (loginNeeded) {
		// redirect to the login page if necessary
		window.location.href = '/login/music'
	}
	
	// otherwise load the selected library
	loadPage();
	$id('libraries').style.display = "none";
}

function changeLibrary()
{
	$id('libraries').style.display = "block";
	if ($id('mediaSidebar').scrollHeight > $id('libraries').scrollHeight){
		$id('libraries').style.height = $id('mediaSidebar').scrollHeight + "px"
	} else {
		$id('mediaSidebar').style.paddingBottom = '0px';
		$id('mediaSidebar').style.paddingBottom = ($id('libraries').scrollHeight - $id('mediaSidebar').scrollHeight) + 'px';
	}
	
	if (readCookie("library")) {
		depressSelectedLibrary(readCookie("library"));
		$id("libClose").style.display = "block";
	} else {
		$id("libClose").style.display = "none";
	}
}

function depressSelectedLibrary(lib)
{
	names = $id('libraries').getElementsByTagName("div");
	for (var i = 0; i < names.length; i++) {
		if (names[i].id == "libSelected") {
			names[i].id = ""
		}
		if (names[i].innerText == lib && names[i].className == "libName") {
			names[i].parentNode.id = "libSelected"
		}
	}
}

// ----------------------------------------------------------------- Helpers ---------------------------------------------------------------------------

function $id(a) 
{ 
	return document.getElementById(a); 
}

function sendRequest(url,callback,postData) {
	var req = createXMLHTTPObject();
	if (!req) return;
	var method = (postData) ? "POST" : "GET";
	req.open(method,url,true);
	// req.setRequestHeader('User-Agent','XMLHTTP/1.0');
	if (postData)
		req.setRequestHeader('Content-type','application/x-www-form-urlencoded');
	req.onreadystatechange = function () {
		if (req.readyState != 4) return;
		if (req.status != 200 && req.status != 304) {
		//	alert('HTTP error ' + req.status);
			return;
		}
		callback(req);
	}
	if (req.readyState == 4) return;
	req.send(postData);
}

function XMLHttpFactories() {
	return [
		function () {return new XMLHttpRequest()},
		function () {return new ActiveXObject("Msxml2.XMLHTTP")},
		function () {return new ActiveXObject("Msxml3.XMLHTTP")},
		function () {return new ActiveXObject("Microsoft.XMLHTTP")}
	];
}

function createXMLHTTPObject() {
	var xmlhttp = false;
	var factories = XMLHttpFactories();
	for (var i=0;i<factories.length;i++) {
		try {
			xmlhttp = factories[i]();
		}
		catch (e) {
			continue;
		}
		break;
	}
	return xmlhttp;
}

function drawButtons()
{
	drawPlayButton();
	drawPrevButton();
	drawRepeatButton();
	drawShuffleButton();
	drawVolumeButton();
	drawSearchClearButton();
	drawLibCloseButton();
}

$(document).ready(function()
{

	//forceLogin();
	//updateSongList();
	
	mPlayer = $("#mPlayerObj");
	
	if ($id('ieShadow')) {
		setTimeout(drawButtons, 100);
	}
	else {
		drawButtons();
		$id('volBar').style.display = 'inline'
	}
	
	document.onkeyup = keyPress;
	document.onkeypress = document.onkeydown = function(e){
		e = window.event || e
		target = e.target || e.srcElement
		key = e.charCode || e.keyCode
		
		if (target.id != 'searchText' && target.id != 'pword' && !e.altKey) {
		
			if (e.preventDefault) {
				e.preventDefault()
			}
			else {
				e.returnValue = false;
				return false;
			}
		}
	}
	
	
	//jplayer stuff
	$("#mPlayerObj").jPlayer( {
	 ready: function () {
        mPlayer.jPlayer( "onSoundComplete", songEnded )
        mPlayer.jPlayer( "onProgressChange", progress )
        progress();
		if (readCookie('library')) {
			loadPage();
		}
		else {
			changeLibrary()
		}
	},
	swfPath: "static",
	errorAlerts: true,
	warningAlerts: true,
	nativeSupport: true,
	volume: 100
	});
})