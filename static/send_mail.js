function sendEmail(evt) {
    evt.preventDefault();

    var yelpID = $(this).data()['yelpid'];
    var recipient = window.prompt("Please enter your email: ");
    if (recipient) {
        recipient = recipient.trim();
    }
    var params = {'yelpID': yelpID, 'recipient': recipient};
    $.post('/send-mail', params);    
}
