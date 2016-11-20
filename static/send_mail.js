// function sendEmail(evt) {
//     evt.preventDefault();

//     var yelpID = $(this).data()['yelpid'];
//     var recipient = window.prompt("Please enter your email: ");
//     if (recipient) {
//         recipient = recipient.trim();
//     }
//     var params = {'yelpID': yelpID, 'recipient': recipient};
//     $.post('/send-mail', params);    
// }
function getEmail(evt) {
    evt.preventDefault();

    var yelpID = $(this).data()['yelpid'];
    console.log(yelpID);
    $('#td-' + yelpID).append('<div id="email-form"><form action="#" \
                                method="POST"><input type="text" id="email" \
                                placeholder="email@domain.com" required><input \
                                type="submit" value="Send" id="submit-email"> \
                                </form></div>');
    // var recipient = $('#email').val();
    // console.log('getEmail func: recipient:' + recipient);
    // var params = {'yelpID': yelpID, 'recipient': recipient};
    // console.log('getEmail params: ' params);
    $('#submit-email').click( function(evt){
        evt.preventDefault();
        console.log('prevented submit-email redirect');
        sendEmail(yelpID);
        console.log('called sendEmail function');
    });
}

function sendEmail(yelpID) {
    var recipient = $('#email').val();
    console.log('getEmail func: recipient:' + recipient);
    var params = {'yelpID': yelpID, 'recipient': recipient};
    console.log('getEmail func: params:' + params);
    $.post('/send-mail', params);
}
