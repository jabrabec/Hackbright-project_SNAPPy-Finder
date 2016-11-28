// alternate the display of search-by-coords or search-by-address forms on homepage
$('#toggle-coords-search').click(function() {
    $('#search-by-coords').css('display', 'none');
    $('#search-by-address').css('display', 'block');
});

$('#toggle-addr-search').click(function() {
    $('#search-by-coords').css('display', 'block');
    $('#search-by-address').css('display', 'none');
});

// when getting to /search route via 'search by address' button on index page,
// simulates a button click to toggle search-by-address form on homepage upon
// completed page load - /search route thus shows appropriate form type depending
// on how user got there
$(document).ready(function() {
    if(window.location.hash == "#addr") {
        $('#toggle-coords-search').trigger('click');
    }
});
