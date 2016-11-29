function getEmail(evt) {
    evt.preventDefault();

    var yelpID = $(this).data()['yelpid'];
    $('#td-' + yelpID).append('<div id="email-form-' + yelpID + '"><form action="#" \
                                method="POST"><input type="text" \
                                id="email' + yelpID + '" \
                                placeholder="e.g. email@domain.com" required><input \
                                type="submit" value="Send" \
                                id="submit-email' + yelpID + '"></form><span \
                                class="incorrect-input">Please input correct \
                                email format.</span></div>');
    $('#email' + yelpID).focus();
    $('#submit-email' + yelpID).click( function(evt){
        evt.preventDefault();
        var recipient = $('#email' + yelpID).val();
        if (/^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$/.test(recipient)) {
            sendEmail(yelpID, recipient);
            $('#email-form-' + yelpID + ' .incorrect-input').removeClass("revealed");
        } else {
            $('#email-form-' + yelpID + ' .incorrect-input').addClass("revealed");
        }
    });
}

function sendEmail(yelpID, recipient) {
    var params = {'yelpID': yelpID, 'recipient': recipient};
    $.post('/send-mail', params, processMailResponse);
    $('#email-form-' + yelpID).html("Sending message...");
}

function processMailResponse(result) {
    $('#email-form-' + result.yelpID).html(result.success_result).fadeOut(3000);
    var container = document.getElementById('email-form-' + result.yelpID);
    setTimeout(function(){
        removeFormDiv(container)
    }, 4000);
}

function removeFormDiv(container){
    container.parentNode.removeChild(container);
}
