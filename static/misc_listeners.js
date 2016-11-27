$('#toggle-coords-search').click(function() {
    $('#search-by-coords').css('display', 'none');
    $('#search-by-address').css('display', 'block');
});

$('#toggle-addr-search').click(function() {
    $('#search-by-coords').css('display', 'block');
    $('#search-by-address').css('display', 'none');
});

$(document).ready(function() {
    if(window.location.hash == "#addr") {
        $('#toggle-coords-search').trigger('click');
    }
});