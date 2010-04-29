
setTimeout(fixSidebar, 50)

function fixSidebar() {
	documentMain = document.getElementById('main')
	documentSidebar = document.getElementById('sidebar')
	if (documentMain.offsetHeight > documentSidebar.offsetHeight) {
		documentSidebar.style.paddingBottom = ((documentMain.offsetHeight - documentSidebar.offsetHeight) + 50) + 'px';
	}
}