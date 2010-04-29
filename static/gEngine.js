var shapes = [];
var canvas;
var shapesRemaining;

window.onload = main;

function main()
{
	canvas = $("canvas").getContext('2d');
	shapesRemaining = 200;
	
	setTimeout('drawRandomCircle()', 100);
}
	
function drawRandomCircle() {
	
	var x = Math.floor(Math.random()*801);
	var y = Math.floor(Math.random()*451);
	var size = Math.floor(Math.random()*100)+10
	var r = Math.floor(Math.random()*256)
	var g = Math.floor(Math.random()*256)
	var b = Math.floor(Math.random()*256)
	
	canvas.fillStyle = 'rgba(' + r + ',' + g + ',' + b + ', 0.5)';
	canvas.beginPath();
	canvas.arc(x,y,size,0,Math.PI*2,true);
	canvas.closePath();
	canvas.fill();
	
	if (shapesRemaining > 0) {
		shapesRemaining = shapesRemaining -1;
		setTimeout('drawRandomCircle()', 100);
	}
}



function $(a) 
{ 
	return document.getElementById(a); 
}