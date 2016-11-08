"""Query Yelp API for business ID, URL, and preview IMG, and add to DB"""

from yelp.client import Client
import json
import requests
import os
import re

from model import connect_to_db, Retailer, db

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

# temporary holding list for testing purposes
temp_list = []

for db_id in range(15):
    db_id += 1

    curr_retailer = Retailer.query.get(db_id)

    location = curr_retailer.address_1 + ", " + curr_retailer.city + ", " + curr_retailer.state

    search_names = curr_retailer.name.split()

    # set-up regex to find any strings that start with
    pattern = re.compile("^\d.*")
    # if the last item in list of search terms for retailer name starts
    # with a digit, delete it as it is probably a store number
    if bool(pattern.match(search_names[-1])):
        del search_names[-1]

    # Yelp search returns more accurate results with fewer terms provided
    search_terms = " ".join(search_names[:3])

    params = {'location': location,
              'term': search_terms,
              # 'categories': "food,health,restaurants",
              'limit': 1,
              'sort_by': "distance"}

    yelp_search = requests.get(url=url, params=params, headers=headers)

    temp_list.append(yelp_search)


if __name__ == "__main__":

    # from server import app
    # connect_to_db(app)
    print "Connected to DB."
