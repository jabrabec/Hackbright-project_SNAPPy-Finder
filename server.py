"""EBT/SNAP Webapp"""

from jinja2 import StrictUndefined
# Tailor the imported methods later
from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension
from model import Retailer, User, Favorite, connect_to_db, db

from helper_functions import sql_query_by_coords

import os
import googlemaps


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
# Secret key to be changed later
app.secret_key = "ABC"

#Jinja will raise an error instead of failing with any undefined variables
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """Show homepage."""

    # how to mask API key in raw HTML that gets rendered?
    return render_template('homepage.html', key=os.environ['GMAPS_API_KEY'])


@app.route('/search-coords', methods=['GET'])
def search_retailers_by_coords():
    """Search DB for a list of results given lat & long by user."""

    latitude = float(request.args.get("latitude"))
    print "\nlatitude: ", latitude
    longitude = float(request.args.get("longitude"))
    print "\nlongitude: ", longitude
    search_range = float(request.args.get("search-range"))
    print "\nsearch range: ", search_range

    retailers_list = sql_query_by_coords(latitude, longitude, search_range)

    geocode_string = ''

    return render_template('search_results.html', retailers_list=retailers_list,
                           geocode_string=geocode_string, latitude=latitude, longitude=longitude,
                           search_range=search_range)


@app.route('/search-address', methods=['GET'])
def search_retailers_by_addr():
    """Search DB for a list of results given an address by user."""

    search_range = float(request.args.get("search-range"))
    print "\nsearch range: ", search_range

    geocode_string = "%s, %s, %s" % (
        request.args.get("street"),
        request.args.get("city"),
        request.args.get("state"))

    print geocode_string

    gmaps = googlemaps.Client(key=os.environ['GMAPS_API_KEY'])
    geocode_result = gmaps.geocode(geocode_string)
    print geocode_result

    latitude = geocode_result[0].get('geometry').get('location').get('lat')
    print "\nlatitude: ", latitude
    longitude = geocode_result[0].get('geometry').get('location').get('lng')
    print "\nlongitude: ", longitude

    retailers_list = sql_query_by_coords(latitude, longitude, search_range)

    return render_template('search_results.html', retailers_list=retailers_list,
                           geocode_string=geocode_string, latitude=latitude, longitude=longitude,
                           search_range=search_range)


if __name__ == "__main__":
    # debug=True allows for use of DebugToolbarExtension downstream
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0", port=5000)
