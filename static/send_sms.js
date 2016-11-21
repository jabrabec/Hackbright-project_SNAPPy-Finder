function getPhone(evt) {
    evt.preventDefault();

    var yelpID = $(this).data()['yelpid'];
    $('#td-' + yelpID).append('<div id="sms-form"><form action="#" \
                                method="POST"><input type="number" id="sms" \
                                placeholder="1##########" maxlength="11" \
                                required><input type="submit" value="Send" \
                                id="submit-sms"></form><span \
                                class="incorrect-input">Please input exactly 11 \
                                digits.</span></div>');
    $('#sms').focus();
    $('#submit-sms').click( function(evt){
        evt.preventDefault();
        var recipient = $('#sms').val();
        console.log(recipient.length);
        if (recipient.length === 11) {
            sendSMS(yelpID, recipient);
            $('#sms-form .incorrect-input').removeClass("revealed");
        } else {
            // $('#sms-form').append("Please input exactly 11 digits.");
            $('#sms-form .incorrect-input').addClass("revealed");
        }
    });
}

function sendSMS(yelpID, recipient) {
    // var recipient = $('#sms').val();
    var params = {'yelpID': yelpID, 'recipient': recipient};
    $.post('/send-sms', params, processSMSResponse);
    $('#sms-form').html("Sending message...");
}

function processSMSResponse(success_result) {
    $('#sms-form').html(success_result).fadeOut(3000);
}
