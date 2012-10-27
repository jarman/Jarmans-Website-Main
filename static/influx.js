function submitPressed(event) {
	// post the data to the api
	event.preventDefault();
	
	var submitInfo = {
		"offer_type": 1,
		"exp_date": "2012-08-27T00:53:25.712Z",
		"have": [$('#kw1').val(), $('#kw2').val(), $('#kw3').val()],
		"want": [$('#kw1').val(), $('#kw2').val(), $('#kw3').val()],
		"note": "brand new bike, never used",
		"min_price": 100.00,
		"max_price": 100.00,
		"location": {"lat": -34.63, "lon": 74.02},
		"location_range": 2.5
  	}
	
	$.post('../api/offers/search', submitInfo, function(data) {
		var items = [];
		
		$.each(data, function(key, val) {
			items.push('<li id="' + key + '">' + val + '</li>');
		});
		
		$('<ul/>', {
			'class': 'my-new-list',
			html: items.join('')
		}).appendTo('#results');
	}, 'json' );
	
	return false;
}
 
 
$(document).ready(function() {
	$('#mainForm').submit(submitPressed);
});