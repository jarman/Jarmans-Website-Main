$(document).ready(function()

{

    //$("#headerpadding").height($("#header").height());
    
	$.post('contacts', function(data) {
			$('#entries').html(data);
		});
		
	$('#searchfield').keyup(submitSearch);
		
	$('#searchfield').submit(function(event) {
	 	event.preventDefault();
	 	var $form = $( this )
		
		submitSearch()
		return false;
	});
	
    $("#showadvancedsearch").click(function(event) {
    	event.preventDefault(); 
    	$("#advancedsearch").toggle()
    	$("#headerpadding").height($("#header").height());
      
    });
    
    
    var alphaRange = {start: 65,end: 90}
    
    var s = $('#beginswith')[0];
    i = 1
    for (var cc = alphaRange.start; cc <= alphaRange.end; cc++) {
		//Create "Option i" with value of i
		//Add it at index i
		s[i++] = new Option(String.fromCharCode(cc), String.fromCharCode(cc));
	}
	
	$('#beginswith').change(function(event) {
		var s = $('#endswith').empty()[0];
	    i = 0
	    for (var cc = ($('#beginswith').val()).charCodeAt(0); cc <= alphaRange.end; cc++) {
			//Create "Option i" with value of i
			//Add it at index i
			s[i++] = new Option(String.fromCharCode(cc), String.fromCharCode(cc));
		}
	})
})

function submitSearch() {
	 	var $form = $('#searchfield')
		
		url = 'contacts?search=' + $form.find( 'input[name="search"]' ).val(); 
		url += '&firstname=' + $form.find( 'input[name="firstname"]' ).val();
		url += '&lastname=' + $form.find( 'input[name="lastname"]' ).val();
		url += '&company=' + $form.find( 'input[name="company"]' ).val();
		url += '&job=' + $form.find( 'input[name="job"]' ).val();
		url += '&birthday=' + $form.find( 'input[name="birthday"]' ).val();
		url += '&phone=' + $form.find( 'input[name="phone"]' ).val();
		url += '&email=' + $form.find( 'input[name="email"]' ).val();
		url += '&labels=' + $form.find( 'input[name="labels"]' ).val();
		url += '&exclude=' + $form.find( 'input[name="exclude"]' ).val();
		url += '&rangename=' + $('#rangename').val();
		url += '&beginswith=' + $('#beginswith').val();
		url += '&endswith=' + $('#endswith').val();
		
		$.post(url, function(data) {
				$('#entries').html(data);
		});
}