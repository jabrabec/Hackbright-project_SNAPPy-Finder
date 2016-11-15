function displayYelpReviews(resultString) {
    var rowContents = [];
    yelpInformation = '<img src="static/img/yelp-2c-outline.png"' +
                    ' id="yelp-logo"><ul>Overall rating: ' +
                    resultString[1].rating +
                    ' out of 5 stars, with ' + resultString[1].review_count +
                    ' reviews.';
    rowContents.push(yelpInformation);
    for (var i in resultString[0].reviews) {
        var reviewString = '<li>' + resultString[0].reviews[i].rating +
                        ' out of 5, on ' +
                        resultString[0].reviews[i].time_created + '<br>"' +
                        resultString[0].reviews[i].text + '"</li>';
        rowContents.push(reviewString);
        }
    rowContents = rowContents.join('');
    $("#" + resultString[1].id).html(rowContents);
}