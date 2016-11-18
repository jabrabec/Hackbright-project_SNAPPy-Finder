function sendEmail(evt) {
    evt.preventDefault();

    var yelpID = $(this).data('yelpID');
    // var yelpID = $(this).dataset.yelpID;
    // var yelpID = $(this).find('.yelp-id').html();
    console.log(yelpID);
    var recipient = window.prompt("Please enter your email: ");
    console.log(recipient);
    if (recipient) {
        recipient = recipient.trim();
    }
    var params = {'yelpID': yelpID, 'recipient': recipient};
    $.post('/send-mail', params);    
}
