**ABOUT**

SNAPPy Finder is a web application designed to help users find retailers near them that accept EBT/SNAP (public assistance) forms of payment. Users can perform the following:
	1. Query the database for retailers near them using automatic geolocation.
	2. Query the database for retailers near a specified address.
	3. View Yelp information for retailers in the search results.
	4. IN PROGRESS: Send search results to their mobile phone and/or email.

Basic architecture:
PostgreSQL DB ('snap') <--> server.py (Python: Flask/SQL Alchemy, Google Maps API) <--> client browser (Javascript [JQuery/AJAX, Google Maps API])


**REQUIREMENTS**

System must have the following components available in order to run this package:
	1. Python
		a. Python modules as specified in requirements.txt
	2. PostgreSQL
	3. Google Maps API key
	4. Yelp Fusion API key
	5. Standard web-browser

PostgreSQL database should be populated using the provided 'data/snap_db.sql' file:
	$ createdb snap
	$ psql snap < data/snap_db.sql


**USAGE INSTRUCTIONS**

Server-side:
1. Set up and activate a virtual environment:
	$ virtualenv env
	$ source env/bin/activate
2. pip install from requirements.txt:
	(env) $ pip freeze -r requirements.txt
3. Source a secrets.sh file (not provided in this repository) containing:
	a. GMAPS_API_KEY
	b. YELP_APP_ID
	c. YELP_APP_SECRET
	d. FLASK_KEY (only required if sessions and the Flask debug toolbar)

	(env) $ source secrets.sh

4. Run the server.py file with your desired host & port values (default is set to http://0.0.0.0:5000/ for running on virtual machines):
	(env) $ python server.py


Client-side:
1. Load the main webpage (e.g. http://localhost:5000/):
2. For automatic geolocation:
	a. Select a search range (default: 0.1 miles)
	b. Click "Search!"
	c. Results will be displayed in a table with corresponding map markers and links to Yelp listings.
3. For searching a specific address:
	a. Enter values into the street, city, and state fields (required)
	b. Select a search range (default: 0.1 miles)
	c. Click "Search!"
	d. Results will be displays in a table with corresponding map markers and links to Yelp listings.
4. IN PROGRESS: users can send particular results to themselves via text or email


**DEMO USAGE**

in progress


**QUESTIONS**

https://www.github.com/jabrabec/HB-project
jenniferbrabec@gmail.com
November 2016