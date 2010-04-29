

function drawPlayButton(){
	canvas = $id("playCanvas").getContext('2d');
	canvas.clearRect(0, 0, 10, 12)
	
	if (playing) {
		canvas.fillStyle = '#E9E7E0';
		canvas.shadowColor = '#50463d';
		canvas.shadowOffsetY = -1;
	}
	else {
		canvas.fillStyle = '#50463d';
		canvas.shadowColor = '#E9E7E0';
		canvas.shadowOffsetY = 1;
	}
	canvas.beginPath();
	canvas.moveTo(0, 1);
	canvas.lineTo(0, 11);
	canvas.lineTo(10, 6);
	canvas.lineTo(0, 1);
	canvas.closePath();
	canvas.shadowBlur = 1;
	canvas.fill();
}

function drawPrevButton()
{
	pass = 1;
	while (pass < 3) {
		if (pass == 1) {
			canvas = $id("prevCanvas").getContext('2d');
		}
		else {
			canvas = $id("backCanvas").getContext('2d');
		}
		
		canvas.fillStyle = '#50463d';
		canvas.shadowColor = '#E9E7E0';
		canvas.shadowOffsetY = 1;
		canvas.shadowBlur = 1;
		canvas.beginPath();
		canvas.moveTo(15, 1);
		canvas.lineTo(15, 9);
		canvas.lineTo(8, 5);
		canvas.moveTo(15, 1);
		canvas.closePath();
		canvas.fill();
		canvas.beginPath();
		canvas.moveTo(8, 1);
		canvas.lineTo(8, 9);
		canvas.lineTo(1, 5);
		canvas.moveTo(8, 1);
		canvas.closePath();
		canvas.fill();
		
		if (pass == 1) {
			canvas.fillRect(0, 1, 1, 8)
			canvas = $id("nextCanvas").getContext('2d');
		}
		else {
			canvas = $id("forwCanvas").getContext('2d');
		}
		
		canvas.fillStyle = '#50463d';
		canvas.shadowColor = '#E9E7E0';
		canvas.shadowOffsetY = 1;
		canvas.shadowBlur = 1;
		canvas.beginPath();
		canvas.moveTo(0, 1);
		canvas.lineTo(0, 9);
		canvas.lineTo(7, 5);
		canvas.moveTo(0, 1);
		canvas.closePath();
		canvas.fill();
		canvas.beginPath();
		canvas.moveTo(7, 1);
		canvas.lineTo(7, 9);
		canvas.lineTo(14, 5);
		canvas.moveTo(7, 1);
		canvas.closePath();
		canvas.fill();
		
		if (pass == 1) {
			canvas.fillRect(14, 1, 1, 8)
		}
		
		pass += 1;
	}
}

function drawRepeatButton()
{
	canvas = $id("repeatCanvas").getContext('2d');
	
	canvas.clearRect(0,0,17,12)
	
	if (repeat) {
		canvas.fillStyle = '#E9E7E0';
		canvas.shadowColor = '#50463d';
		canvas.shadowOffsetY = -1;
	}
	else 
	{
		canvas.fillStyle = '#50463d';
		canvas.shadowColor = '#E9E7E0';
		canvas.shadowOffsetY = 1;
	}
	canvas.shadowBlur = 1;
	
	// upper arrow
	canvas.beginPath();
	canvas.moveTo(2,2);
	canvas.lineTo(10,2);
	canvas.lineTo(10,1);
	canvas.lineTo(15,3);
	canvas.lineTo(10,5);
	canvas.lineTo(10,4);
	canvas.lineTo(3,4);
	canvas.lineTo(2,5);
	canvas.lineTo(2,7);
	canvas.lineTo(0,8);
	canvas.lineTo(0,4);
	canvas.lineTo(2,2);
	canvas.closePath();
	canvas.fill();
	
	// lower arrow
	canvas.beginPath();
	canvas.moveTo(15,10);
	canvas.lineTo(7,10);
	canvas.lineTo(7,11);
	canvas.lineTo(2,9);
	canvas.lineTo(7,7);
	canvas.lineTo(7,8);
	canvas.lineTo(14,8);
	canvas.lineTo(15,7);
	canvas.lineTo(15,5);
	canvas.lineTo(17,4);
	canvas.lineTo(17,8);
	canvas.lineTo(15,10);
	canvas.closePath();
	canvas.fill();
}

function drawShuffleButton()
{
	canvas = $id("shuffleCanvas").getContext('2d');
	
	canvas.clearRect(0,0,20,12)
	
	if (shuffle) {
		canvas.fillStyle = '#E9E7E0';
		canvas.shadowColor = '#50463d';
		canvas.shadowOffsetY = -1;
	}
	else 
	{
		canvas.fillStyle = '#50463d';
		canvas.shadowColor = '#E9E7E0';
		canvas.shadowOffsetY = 1;
	}
	canvas.shadowBlur = 1;
	
	// upper arrow
	canvas.beginPath();
	canvas.moveTo(0,2);
	canvas.lineTo(3,2);
	canvas.lineTo(5,3);
	canvas.lineTo(13,8);
	canvas.lineTo(15,8);
	canvas.lineTo(15,7);
	canvas.lineTo(20,9);
	canvas.lineTo(15,11);
	canvas.lineTo(15,10);
	canvas.lineTo(13,10);
	canvas.lineTo(11,9);
	canvas.lineTo(3,4);
	canvas.lineTo(0,4);
	canvas.lineTo(0,2);
	canvas.closePath();
	canvas.fill();
	
	// lower arrow
	canvas.beginPath();
	canvas.moveTo(0,10);
	canvas.lineTo(3,10);
	canvas.lineTo(5,9);
	canvas.lineTo(13,4);
	canvas.lineTo(15,4);
	canvas.lineTo(15,5);
	canvas.lineTo(20,3);
	canvas.lineTo(15,1);
	canvas.lineTo(15,2);
	canvas.lineTo(13,2);
	canvas.lineTo(11,3);
	canvas.lineTo(3,8);
	canvas.lineTo(0,8);
	canvas.lineTo(0,10);
	canvas.closePath();
	canvas.fill();
}

function drawVolumeButton()
{
	canvas = $id("volumeCanvas").getContext('2d');
	canvas.clearRect(0,0,16,12)

	canvas.fillStyle = '#50463d';
	canvas.strokeStyle = '#50463d';
	canvas.shadowColor = '#E9E7E0';
	canvas.shadowOffsetY = 1;
	canvas.shadowBlur = 1;
	
	canvas.beginPath();
	canvas.moveTo(0,3);
	canvas.lineTo(3,3);
	canvas.lineTo(6,0);
	canvas.lineTo(6,12);
	canvas.lineTo(3,9);
	canvas.lineTo(0,9);
	canvas.lineTo(0,3);
	canvas.closePath();
	canvas.fill();
	
	if (volume > 5)
	{
		canvas.beginPath();
		canvas.arc(6,6,3,-Math.PI/4,Math.PI/4,false);
		canvas.stroke();
	}
	if (volume > 50)
	{
		canvas.beginPath();
		canvas.arc(6,6,6,-Math.PI/4,Math.PI/4,false);
		canvas.stroke();
	}
	if (volume > 90)
	{
		canvas.beginPath()
		canvas.arc(6,6,9,-Math.PI/4,Math.PI/4,false);
		canvas.stroke();
	}
	
}

function drawSearchClearButton()
{
	canvas = $id("searchClear").getContext('2d');
	canvas.clearRect(0,0,12,12)
	
	if ($id('searchText').value == '') {
		canvas.strokeStyle = '#999790';
		
		//canvas.arc(4, 4, 4, 0, 2 * Math.PI, false);
		canvas.beginPath();
		canvas.arc(5, 5, 4, 0, 2 * Math.PI, false);
		canvas.stroke();
		
		canvas.beginPath();
		canvas.moveTo(7, 7);
		canvas.lineTo(12, 12);
		canvas.stroke();
	}
	else
	{
		canvas.fillStyle = '#B9B7B0';
		canvas.strokeStyle = '#fff';
		canvas.beginPath();
		canvas.arc(6, 6, 6, 0, 2 * Math.PI, false);
		canvas.fill();
		
		canvas.beginPath();
		canvas.moveTo(3, 3);
		canvas.lineTo(9, 9);
		canvas.stroke();
		
		canvas.beginPath();
		canvas.moveTo(9, 3);
		canvas.lineTo(3, 9);
		canvas.stroke();
	}
}