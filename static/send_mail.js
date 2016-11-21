function getEmail(evt) {
    evt.preventDefault();

    var yelpID = $(this).data()['yelpid'];
    $('#td-' + yelpID).append('<div id="email-form"><form action="#" \
                                method="POST"><input type="text" id="email" \
                                placeholder="email@domain.com" required><input \
                                type="submit" value="Send" \
                                id="submit-email"></form></div>');
    $('#email').focus();
    $('#submit-email').click( function(evt){
        evt.preventDefault();
        sendEmail(yelpID);
    });
}

function sendEmail(yelpID) {
    var recipient = $('#email').val();
    var params = {'yelpID': yelpID, 'recipient': recipient};
    $.post('/send-mail', params, processResponse);
}

function processResponse(success_result) {
    $('#email-form').html(success_result).fadeOut(3000);
}