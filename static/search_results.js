"use strict";


function displayResultsList(result){
  console.log(result);
  // This clears out the div in case there were previous search results.
  $('#search-results').empty();
  
  // Fill out #search-results div either with results table or 'no results' text
  var divContents = [];
  if (result[0]) {
    var headerRow = '<table>' +
                    '<tr>' +
                    '<th>Name</th>' +
                    '<th>Address</th>' +
                    '<th>City</th>' +
                    '<th>State</th>' +
                    '<th>Zipcode</th>' +
                    '<th>Distance (mi)</th>' +
                    '</tr>';
    divContents.push(headerRow);
    for (var i in result) {
      // create a temporary holding string to concatenate html
      var tempString = '<tr><td>' + result[i][0] + 
                      '</td><td>' + result[i][3] +
                      ' ' + result[i][4] +
                      '</td><td>' + result[i][5] + 
                      '</td><td>' + result[i][6] + 
                      '</td><td>' + result[i][7] + 
                      '</td><td>' + result[i][8] + 
                      '</tr>';
      divContents.push(tempString);
    }
    divContents.push('</table>');
    divContents = divContents.join('');
  } else {
    divContents.push('No results found.');
  }
  $('#search-results').html(divContents);
}    


function submitCoords(position) {
  // Grab the lat/long/search range values
  var latitude = position.coords.latitude;
  console.log(latitude);
  var longitude = position.coords.longitude;
  console.log(longitude);
  var searchRange = $('#coords-search-range').val();
  console.log(searchRange);
  // Creating the data to be sent with the AJAX request
  var params = {'latitude': latitude, 'longitude': longitude, 'searchRange': searchRange };
  // The AJAX get request, passing in data, referring to success handler.
  $.get('/search-coords.json', params, displayResultsList);
}


function alsoGetLocation(evt) {
  evt.preventDefault();

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(submitCoords);
  }
}

// Event listener for search by coordinates button.
$('#coords-search').on('click', alsoGetLocation);


function submitAddress(evt) {
  evt.preventDefault();
  
  var street = $('#street').val();
  console.log(street);
  var city = $('#city').val();
  console.log(city);
  var state = $('#state').val();
  console.log(state);
  var searchRange = $('#addr-search-range').val();
  console.log(searchRange);
  // Creating the data to be sent with the AJAX request
  var params = {'street': street,
                'city': city,
                'state': state,
                'searchRange': searchRange };
  // The AJAX get request, passing in data, referring to success handler.
  $.get('/search-address.json', params, displayResultsList);
  }

// Event listener for search by address button.
$('#addr-search').on('click', submitAddress);
