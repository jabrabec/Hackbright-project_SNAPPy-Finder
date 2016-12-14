**ABOUT**

SNAPPy Finder is a web application designed to help users find retailers near
them that accept EBT/SNAP (public assistance) forms of payment. Users can
perform the following:
 1. Query the database for retailers near them using automatic geolocation.
 2. Query the database for retailers near a specified address.
 3. View Yelp information for retailers in the search results.
 4. IN PROGRESS: Send search results to their mobile phone and/or email.

Basic architecture:
PostgreSQL DB ('snap') <-->
server.py (Python [Flask/SQL Alchemy], Google Maps APIs, Yelp Fusion API) <-->
client browser (Javascript [JQuery/AJAX, Google Maps APIs])


**REQUIREMENTS**

System must have the following components available in order to run this package:
 1. Python
  1. Python modules as specified in requirements.txt
 2. PostgreSQL
 3. Google Maps API key
 4. Yelp Fusion API key
 5. Standard web-browser

PostgreSQL database should be populated using the provided 'data/snap_db.sql'
file:

	`$ createdb snap` 
	`$ psql snap < data/snap_db.sql`


**USAGE INSTRUCTIONS**

Server-side:
 1.	Set up and activate a virtual environment:

	`$ virtualenv env`

	`$ source env/bin/activate`

 2. pip install from requirements.txt:

	`(env) $ pip freeze -r requirements.txt`

 3. Source a secrets.sh file (not provided in this repository) containing:
  1. GMAPS_API_KEY
  2. YELP_APP_ID
  3. YELP_APP_SECRET
  4. FLASK_KEY (only required if using sessions and the Flask debug toolbar)
  5. MAIL_PASSWORD
	`(env) $ source secrets.sh`

4. Run the server.py file with your desired host & port values (default is set
to http://0.0.0.0:5000/ for running on virtual machines):

	`(env) $ python server.py`


Client-side:
 1. Load the main webpage (e.g. http://localhost:5000/):
 2. For automatic geolocation:
  1. Select a search range (default: 0.1 miles)
  2. Click "Search!"
  3. Results will be displayed in a table with corresponding map markers and
	links to Yelp listings.
 3. For searching a specific address:
  1. Enter values into the street, city, and state fields (required)
  2. Select a search range (default: 0.1 miles)
  3. Click "Search!"
  4. Results will be displayed in a table with corresponding map markers and
	links to Yelp listings.
  5. Users can send particular results to themselves via email or SMS.


**DEMO USAGE**

in progress


**QUESTIONS**

https://github.com/jabrabec/Hackbright-project_SNAPPy-Finder
jenniferbrabec@gmail.com
November 2016

