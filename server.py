"""EBT/SNAP Webapp"""

from jinja2 import StrictUndefined
from flask import (Flask,
                   render_template,
                   # redirect,
                   request,
                   # flash,
                   # session,
                   jsonify)
from flask_debugtoolbar import DebugToolbarExtension
from model import (connect_to_db,
                   # Retailer, User, Favorite, db
                   )

from helper_functions import (sql_query_by_coords,
                              query_yelp_reviews_by_id,
                              send_email,
                              send_sms)


import os
import googlemaps

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = os.environ['FLASK_KEY']

#Jinja will raise an error instead of failing with any undefined variables
app.jinja_env.undefined = StrictUndefined

# to fix non-serializable JSON error with decimal types, per:
# https://stackoverflow.com/questions/24706951/how-to-convert-all-decimals-in-a-python-data-structure-to-string
import decimal
import flask.json


class MyJSONEncoder(flask.json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return str(obj)
        return super(MyJSONEncoder, self).default(obj)

app.json_encoder = MyJSONEncoder


@app.route('/search')
def search_page():
    """Show main search page."""

    return render_template('homepage.html', key=os.environ['GMAPS_API_KEY'])


@app.route('/')
def index():
    """Show landing page."""

    return render_template('index.html')


@app.route('/search-coords.json', methods=['GET'])
def search_retailers_by_coords_json():
    """Search DB for a list of results given lat, long, and range by user."""

    latitude = float(request.args.get("latitude"))
    longitude = float(request.args.get("longitude"))
    search_range = float(request.args.get("searchRange"))

    retailers_list = sql_query_by_coords(latitude, longitude, search_range)

    return jsonify(retailers_list)


@app.route('/search-address.json', methods=['GET'])
def search_retailers_by_addr_json():
    """Search DB for a list of results given an address by user."""

    search_range = float(request.args.get("searchRange"))

    geocode_string = "%s, %s, %s" % (
        request.args.get("street"),
        request.args.get("city"),
        request.args.get("state"))

    gmaps = googlemaps.Client(key=os.environ['GMAPS_API_KEY'])
    geocode_result = gmaps.geocode(geocode_string)

    latitude = geocode_result[0].get('geometry').get('location').get('lat')
    longitude = geocode_result[0].get('geometry').get('location').get('lng')

    retailers_list = sql_query_by_coords(latitude, longitude, search_range)

    return jsonify(retailers_list)


@app.route('/send-mail', methods=['POST'])
def send_email_to_user():
    """Send an email to user with a link to the selected Yelp listing."""

    recipient = request.form.get("recipient")
    subject = 'Search Result from SNAPPy Finder'
    yelp_bus_id = request.form.get("yelpID")
    body = '''Find information on your selected retailer at:\n
    https://www.yelp.com/biz/%s''' % (yelp_bus_id)

    success_result = send_email(recipient, subject, body)
    results_dict = {'yelpID': yelp_bus_id, 'success_result': success_result}

    return jsonify(results_dict)


@app.route('/send-sms', methods=['POST'])
def send_sms_to_user():
    """Send an SMS to user with a link to the selected Yelp listing."""

    recipient = request.form.get("recipient")
    yelp_bus_id = request.form.get("yelpID")
    body = '''Find information on your selected retailer at:
    https://m.yelp.com/biz/%s''' % (yelp_bus_id)

    success_result = send_sms(recipient, body)
    results_dict = {'yelpID': yelp_bus_id, 'success_result': success_result}

    return jsonify(results_dict)


@app.route('/search-yelp-reviews.json', methods=['GET'])
def search_yelp_reviews_by_id():
    """Search Yelp Reviews API by business ID."""

    yelp_bus_id = request.args.get("yelpID")

    reviews = query_yelp_reviews_by_id(yelp_bus_id)

    return jsonify(reviews)


@app.route('/about')
def about():
    """Show about page."""

    return render_template('about.html')


if __name__ == "__main__":
    # debug=True allows for use of DebugToolbarExtension downstream
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0", port=5000)
