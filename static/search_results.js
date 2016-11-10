"use strict";


function displayResultsList(result){
  // This clears out the div in case there were previous search results.
  $('#search-results').empty();
  
  // Fill out #search-results div either with results table or 'no results' text
  // create empty divContents array for holding results
  var divContents = ['<h3>Results:</h3>'];
  // perform the following only if 'results' has content:
  if (result[0]) {
    // create header row
    var headerRow = '<table>' +
                    '<tr>' +
                    '<th>Name</th>' +
                    '<th>Address</th>' +
                    '<th>City</th>' +
                    '<th>State</th>' +
                    '<th>Zipcode</th>' +
                    '<th>Distance (mi)</th>' +
                    '<th>Preview img</th>' +
                    '</tr>';
    // add header row to divContents holding array
    divContents.push(headerRow);
    // iterate over items in JSON-formatted results
    for (var i in result) {
      // create a temporary holding string to concatenate html for a single row
      var tempString = '<tr><td><a href="' + result[i][8] + 
                      '">'+ result[i][0] +
                      '</a></td><td>' + result[i][3] +
                      ' ' + result[i][4] +
                      '</td><td>' + result[i][5] + 
                      '</td><td>' + result[i][6] + 
                      '</td><td>' + result[i][7] + 
                      '</td><td>' + result[i][10] + 
                      '</td><td><img class="preview-img" src="' + result[i][9] + 
                      '"></tr>';
      // add this row to the divContents holding array
      divContents.push(tempString);
      var markerLat = parseFloat(result[i][1]);
      var markerLong = parseFloat(result[i][2]);
      var latLng = {lat: markerLat, lng: markerLong};
      var marker = new google.maps.Marker({
          position: latLng,
          map: map,
          title: result[i][0]
        });
    }
    // finalize table tag
    divContents.push('</table>');
    // concatenate all results in divContents into a single string
    divContents = divContents.join('');
  // if not result[0], simply state "no results found"
  } else {
    divContents.push('No results found.');
  }
  // update the contents on main page of div id="search-results"
  $('#search-results').html(divContents);
}    


function submitCoords(position) {
  // get the lat/long/search range values via HTML5 geolocation
  var latitude = position.coords.latitude;
  var longitude = position.coords.longitude;
  var searchRange = $('#coords-search-range').val();
  // set data parameters for sending with the AJAX request
  var params = {'latitude': latitude, 'longitude': longitude, 'searchRange': searchRange };
  // send AJAX get request, passing in data, referring to success handler.
  $.get('/search-coords.json', params, displayResultsList);
}

// named to avoid confusion with gmaps function
function alsoGetLocation(evt) {
  evt.preventDefault();

  // get HTML5 geolocation and pass to submitCoords function
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(submitCoords);
  }
}

// Event listener for search by coordinates button.
$('#coords-search').on('click', alsoGetLocation);


// Submit address to server and recenter map on that location.
function submitAddress(evt) {
  evt.preventDefault();
  // get the address & search range values entered into text fields by user
  var street = $('#street').val();
  var city = $('#city').val();
  var state = $('#state').val();
  var searchRange = $('#addr-search-range').val();

  var address = (street + ", " + city + ", " + state)
  var geocoder = new google.maps.Geocoder();
  geocoder.geocode( { 'address': address}, function(results, status) {
      if (status == 'OK') {
        map.setCenter(results[0].geometry.location);
        infoWindow.setPosition(results[0].geometry.location);
        infoWindow.setContent('Searching near this address.');
      } else {
        alert('Geocode was not successful for the following reason: ' + status);
      }
    });

  // set data parameters for sending with the AJAX request
  var params = {'street': street,
                'city': city,
                'state': state,
                'searchRange': searchRange };
  // send AJAX get request, passing in data, referring to success handler.
  $.get('/search-address.json', params, displayResultsList);
  }

// Event listener for search by address button.
$('#addr-search').on('click', submitAddress);
