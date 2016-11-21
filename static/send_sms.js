function getPhone(evt) {
    evt.preventDefault();

    var yelpID = $(this).data()['yelpid'];
    $('#td-' + yelpID).append('<div id="sms-form"><form action="#" \
                                method="POST"><input type="number" id="sms" \
                                placeholder="1##########" maxlength="10" \
                                size="10" minlength="10" required><input \
                                type="submit" value="Send" \
                                id="submit-sms"></form></div>');
    $('#sms').focus();
    $('#submit-sms').click( function(evt){
        evt.preventDefault();
        sendSMS(yelpID);
    });
}

function sendSMS(yelpID) {
    var recipient = $('#sms').val();
    var params = {'yelpID': yelpID, 'recipient': recipient};
    $.post('/send-sms', params, processSMSResponse);
    $('#sms-form').html("Sending message...");
}

function processSMSResponse(success_result) {
    $('#sms-form').html(success_result).fadeOut(5000);
}