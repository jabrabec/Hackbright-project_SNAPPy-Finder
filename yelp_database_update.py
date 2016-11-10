"""Query Yelp API for business ID, URL, and preview IMG, and add to DB"""

from yelp.client import Client
import json
import requests
import os
import re

from model import connect_to_db, Retailer, db

from sqlalchemy import update

from server import app
connect_to_db(app)

# set up Yelp Search API query
yelp_token = requests.post(
    'https://api.yelp.com/oauth2/token',
    data={'grant_type': 'client_credentials',
          'client_id': os.environ['YELP_APP_ID'],
          'client_secret': os.environ['YELP_APP_SECRET']})
url = 'https://api.yelp.com/v3/businesses/search'
yelp_access_token = yelp_token.json()['access_token']
headers = {'Authorization': 'Bearer %s' % yelp_access_token}

# for populating testdb:
# first, updated retailer_ids 1-15
# for db_id in range(15):
#   db_id += 1

# next, update retailer_ids 16-48
# for db_id in range(33):
#     db_id += 16

# for populating live snap db, approx. half of all entries:
# for db_id in range(12500):
#     db_id += 1

# for populating live snap db, remaining approx. half of all entries:
# for db_id in range(12552):
#     db_id += 12501

# for populating live snap db, picking up where API returned JSON error:
# for db_id in range(11685):
#     db_id += 13368

# for populating live snap db, picking up where API returned JSON error:
for db_id in range(9597):
    db_id += 15456

    curr_retailer = Retailer.query.get(db_id)

    location = curr_retailer.address_1 + ", " + curr_retailer.city + ", " + curr_retailer.state

    search_names = curr_retailer.name.split()

    # set-up regex to find any strings that start with digits
    pattern = re.compile("^\d.*")
    # if the last item in list of search terms for retailer name starts
    # with a digit, delete it as it is probably a store ID number (e.g. for
    # chains retailers).
    # also, including this field in search terms returns empty list from Yelp.
    if bool(pattern.match(search_names[-1])):
        del search_names[-1]

    # Yelp search seems to return more accurate results with fewer terms provided.
    # Only the first up to 3 search terms from the name field are submitted.
    search_terms = " ".join(search_names[:3])

    # parameters to search in Yelp
    params = {'location': location,
              'term': search_terms,
              'categories': "food,health,restaurants,shopping",
              'limit': 1,
              'sort_by': "distance"}

    # execute the Yelp search API call
    yelp_search = requests.get(url=url, params=params, headers=headers)

    # Convert API call results into JSON format
    yelp_result = yelp_search.json()

    # check that yelp_search did not return empty list; assign values and add to
    # db as long as this is true.
    if yelp_result.get('businesses'):
        yelp_id = yelp_result.get('businesses')[0].get('id')
        yelp_url = yelp_result.get('businesses')[0].get('url')
        # truncate Yelp URL to remove tracking arguments
        yelp_url = yelp_url.split("?")[0]
        yelp_img = yelp_result.get('businesses')[0].get('image_url')
        print search_terms + ": \t" + yelp_id + "\t" + yelp_url

        db.session.query(Retailer).filter_by(
            retailer_id=curr_retailer.retailer_id).update(
            {'yelp_id': yelp_id, 'yelp_url': yelp_url, 'yelp_img': yelp_img})

        # commit these .update() changes to the db
        db.session.commit()


if __name__ == "__main__":

    print "Connected to DB."
