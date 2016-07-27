/*	Picturehandler

	The aim of the following Javascript is to simplify the picture handling using JS
 	to manage the action mostly in the frontend and only secondly in the backend

*/


/* 1. Helper functions */
var createUrl = function() {

	var index = window.location.pathname.split('/')[2];
	var url = 'http://localhost:8000/artworks/' + index + '/pictures/JSON'
	
	return url
}

var html_insert = function(pictures) {
	if (pictures.length() > 0) {
		pictures.forEach(function(picture) {
	
		var html_insert = '<tr class="container">>'
	
		html_insert += '<td class="col-md-6">%data%</td>'
		html_insert += '<td class="col-md-3">Stored</td>'
		html_insert += '<td class="col-md-3">Delete</td>'
		html_insert += '</tr>'
	
		html_insert = html_insert.replace('%data%', picture.filename)
	
		$('#pictures_list').append(html_insert) 
		})
	} else {
		$('#pictures_header').text('No Related Pictures') 

	}

}



/* 2. Ajax request */

var getpictures = function() {

	// correct later
	var url = createUrl()

	$.ajax({
		url: url,
		datatype: 'json'
	})
	.done(function(responses)
	{
		console.log('AJAX request worked !');
		console.log(responses);

		var pictures = responses.pictures

		html_insert(pictures)
	
	})
	.fail(function(responses){
		console.log('Ajax failed!')
	})
}()

