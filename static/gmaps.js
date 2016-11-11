// GMaps: get location

  // Note: This example requires that you consent to location sharing when
  // prompted by your browser. If you see the error "The Geolocation service
  // failed.", it means you probably did not give permission for the browser to
  // locate you.

  // define map, pos, & userInfoWindow outside of function so that map markers can
  // be referenced in search_results.js file
  var map;
  var userInfoWindow;
  var pos;

  function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
      center: {lat: 37.7886679, lng: -122.411499},
      zoom: 17
    });
    userInfoWindow = new google.maps.InfoWindow({map: map});

    // Try HTML5 geolocation.
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(position) {
        pos = {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        };

        userInfoWindow.setPosition(pos);
        userInfoWindow.setContent('You are here.');
        map.setCenter(pos);
      }, function() {
        handleLocationError(true, userInfoWindow, map.getCenter());
      });
    } else {
      // Browser doesn't support Geolocation
      handleLocationError(false, userInfoWindow, map.getCenter());
    }
  }

  function handleLocationError(browserHasGeolocation, userInfoWindow, pos) {
    userInfoWindow.setPosition(pos);
    userInfoWindow.setContent(browserHasGeolocation ?
                          'Error: The Geolocation service failed.' :
                          'Error: Your browser doesn\'t support geolocation.');
  }
