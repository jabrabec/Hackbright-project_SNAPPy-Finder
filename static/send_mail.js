function getEmail(evt) {
    evt.preventDefault();

    var yelpID = $(this).data()['yelpid'];
    $('#td-' + yelpID).append('<div id="email-form-' + yelpID + '"><form action="#" \
                                method="POST"><input type="text" id="email' + yelpID + '" \
                                placeholder="email@domain.com" required><input \
                                type="submit" value="Send" \
                                id="submit-email' + yelpID + '"></form></div>');
    $('#email' + yelpID).focus();
    $('#submit-email' + yelpID).click( function(evt){
        evt.preventDefault();
        sendEmail(yelpID);
    });
}

function sendEmail(yelpID) {
    var recipient = $('#email' + yelpID).val();
    var params = {'yelpID': yelpID, 'recipient': recipient};
    $.post('/send-mail', params, processMailResponse);
    $('#email-form-' + yelpID).html("Sending message...");
}

function processMailResponse(result) {
    $('#email-form-' + result.yelpID).html(result.success_result).fadeOut(3000);
}
