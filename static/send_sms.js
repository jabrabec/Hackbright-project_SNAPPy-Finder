function getPhone(evt) {
    evt.preventDefault();

    var yelpID = $(this).data()['yelpid'];
    $('#td-' + yelpID).append('<div id="sms-form-' + yelpID + '"><form action="#" \
                                method="POST"><input type="number" \
                                id="sms-' + yelpID + '" \
                                placeholder="e.g. 14158872215" maxlength="11" \
                                required><input type="submit" value="Send" \
                                id="submit-sms-' + yelpID + '"></form><span \
                                class="incorrect-input">Please input exactly 11 \
                                digits.</span></div>');
    $('#sms-' + yelpID).focus();
    $('#submit-sms-' + yelpID).click( function(evt){
        evt.preventDefault();
        var recipient = $('#sms-' + yelpID).val();
        if (recipient.length === 11) {
            sendSMS(yelpID, recipient);
            $('#sms-form-' + yelpID + ' .incorrect-input').removeClass("revealed");
        } else {
            $('#sms-form-' + yelpID + ' .incorrect-input').addClass("revealed");
        }
    });
}

function sendSMS(yelpID, recipient) {
    var params = {'yelpID': yelpID, 'recipient': recipient};
    $.post('/send-sms', params, processSMSResponse);
    $('#sms-form-' + yelpID).html("Sending message...");
}

function processSMSResponse(result) {
    $('#sms-form-' + result.yelpID).html(result.success_result).fadeOut(3000);
    var container = document.getElementById('sms-form-' + result.yelpID);
    setTimeout(function(){
        removeFormDiv(container)
    }, 4000);
}

// removeFormDiv() is stored in send_mail.js file
