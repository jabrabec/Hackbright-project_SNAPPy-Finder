from model import db


def sql_query_by_coords(latitude, longitude, search_range, limit_to=20, offset_by=0):
    """Helper function used by both search routes to query database"""

    # Haversine equation for finding the geodesic distance between two points
    sql_query = """SELECT name, lat, lng, address_1, address_2, city, state,
        zipcode, yelp_url, yelp_img, (3959*acos(cos(radians(:latitude))*cos(
        radians(lat))*cos(radians(lng)-radians(:longitude))+sin(radians(
        :latitude))*sin(radians(lat)))) AS distance, yelp_id
    FROM retailers
    WHERE (3959*acos(cos(radians(:latitude))*cos(radians(lat))*cos(
        radians(lng)-radians(:longitude))+sin(radians(:latitude))*sin(
        radians(lat)))) < :search_range
    ORDER BY distance
    LIMIT :limit_to
    OFFSET :offset_by"""

    # perform db query and get all results
    cursor = db.session.execute(sql_query, {
        'latitude': latitude,
        'longitude': longitude,
        'search_range': search_range,
        'limit_to': limit_to,
        'offset_by': offset_by})
    results = cursor.fetchall()

    # turn results into a list of lists instead of a list of tuples
    results_list = [list(item) for item in results]

    # round the returned distance calculation to 3 decimal places only
    for item in results_list:
        item[10] = round(item[10], 3)

    return results_list


from yelp.client import Client
import json
import requests
import os


def query_yelp_reviews_by_id(yelp_bus_id):

    # set up Yelp Reviews API query
    yelp_token = requests.post(
        'https://api.yelp.com/oauth2/token',
        data={'grant_type': 'client_credentials',
              'client_id': os.environ['YELP_APP_ID'],
              'client_secret': os.environ['YELP_APP_SECRET']})

    yelp_reviews_url = 'https://api.yelp.com/v3/businesses/' + yelp_bus_id + '/reviews'

    yelp_access_token = yelp_token.json()['access_token']

    headers = {'Authorization': 'Bearer %s' % yelp_access_token}

    # perform Reviews API call
    yelp_reviews = requests.get(url=yelp_reviews_url, headers=headers)
    # Convert Reviews API call results into JSON format
    yelp_reviews = yelp_reviews.json()
    print yelp_reviews

    # Perform Business Search API call to get overall rating
    overall_rating_url = 'https://api.yelp.com/v3/businesses/' + yelp_bus_id
    yelp_ratings_search = requests.get(url=overall_rating_url, headers=headers)
    yelp_ratings_result = yelp_ratings_search.json()

    return yelp_reviews, yelp_ratings_result
