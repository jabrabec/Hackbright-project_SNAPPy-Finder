function displayYelpReviews(resultString) {
    var rowContents = [];

    // convert half-star numeric ratings to string-type ratings with dashes
    // instead of periods; e.g. 3.5 --> 3.5
    // for use in applying class to overall business rating for styling purposes.
    var ratingClass = resultString[1].rating.toString().replace(/\./, '-');

    yelpInformation = '<ul><span class="rating r' + ratingClass +
                    ' stars">' + resultString[1].rating + ' of 5</span>' +
                    'based on ' + resultString[1].review_count +
                    ' reviews on <a href="https://www.yelp.com/biz/' +
                    resultString[1].id + '"><img src="static/img/yelp-2c-outline.png"' +
                    ' class="yelp-logo"></a>';
    rowContents.push(yelpInformation);
    for (var i in resultString[0].reviews) {
        var reviewString = '<li>' + resultString[0].reviews[i].rating +
                        ' out of 5, on ' +
                        resultString[0].reviews[i].time_created + '<br>"' +
                        resultString[0].reviews[i].text + '"</li>';
        rowContents.push(reviewString);
        }
    rowContents.push('</ul>');
    rowContents = rowContents.join('');
    // $("#row-" + resultString[1].id).removeClass("hidden-row");
    $("#" + resultString[1].id).html(rowContents);
}
