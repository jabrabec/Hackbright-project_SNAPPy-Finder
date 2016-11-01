"""EBT/SNAP Webapp"""

from jinja2 import StrictUndefined
# Tailor the imported methods later
from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension
from model import Retailer, User, Favorite, connect_to_db, db

import os


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
# Secret key to be changed later
app.secret_key = "ABC"

#Jinja will raise an error instead of failing with any undefined variables
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """Show homepage."""

    return render_template('homepage.html', key=os.environ['GMAPS_API_KEY'])

if __name__ == "__main__":
    # debut=True allows for use of DebugToolbarExtension downstream
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0", port=5000)
