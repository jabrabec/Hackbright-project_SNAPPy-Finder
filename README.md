##ABOUT
SNAPPy Finder is a web application designed to help users find retailers near
them that accept EBT/SNAP (public assistance) forms of payment. Users can
perform the following:
 1. Query the database for retailers near them using automatic geolocation.
 2. Query the database for retailers near a specified address.
 3. View Yelp information for retailers in the search results.
 4. Send search results to their mobile phone and/or email.

Basic architecture:  
PostgreSQL DB ('snap') <-->  
    server.py (Python [Flask/SQL Alchemy], Google Maps APIs, Yelp Fusion API) <-->  
      client browser (Javascript [JQuery/AJAX, Google Maps APIs])  

![landing page screenshot](https://raw.githubusercontent.com/jabrabec/Hackbright-project_SNAPPy-Finder/master/static/img/landing_page.PNG)


##REQUIREMENTS
System must have the following components available in order to run this package:
 1. Python
  1. Python modules as specified in requirements.txt
 2. PostgreSQL
 3. Google Maps API key
 4. Yelp Fusion API key
 5. Twilio API key
 6. Personal login, password, and smtp settings for sending email.
 7. Standard web-browser

PostgreSQL database should be populated using the provided 'data/snap_db.sql'
file:  
 `$ createdb snap`  
 `$ psql snap < data/snap_db.sql`  
 

##USAGE INSTRUCTIONS
**Server-side**:
 1. Set up and activate a virtual environment:  
 `$ virtualenv env`  
 `$ source env/bin/activate`  

 2. pip install from requirements.txt:  
 `(env) $ pip freeze -r requirements.txt`  

 3. Source a secrets.sh file (not provided in this repository):  
 `(env) $ source secrets.sh`  
 secrets.sh must contain the following:
  1. GMAPS_API_KEY
  2. YELP_APP_ID
  3. YELP_APP_SECRET
  4. FLASK_KEY (only required if using sessions and the Flask debug toolbar)
  5. MAIL_PASSWORD
  6. TWILIO_ACCOUNT_SID
  7. TWILIO_AUTH_TOKEN
  8. PRIVATE_NUMBER (phone number; only required if running tests.py)  

 4. Run the server.py file with your desired host & port values (default is set
to http://0.0.0.0:5000/ for running on virtual machines):  
 `(env) $ python server.py`  


**Client-side**:
 1. Load the main webpage (e.g. http://localhost:5000/):
 2. For automatic geolocation:
  1. Select a search range (default: 0.1 miles)
  2. Click "Go!"
 3. For searching a specific address:
  1. Enter values into the street and city fields (required)
    1. Search is currently only available in northern California so this field is locked.
  2. Select a search range (default: 0.1 miles)
  3. Click "Go!"
 4. Results will be displayed in a table with corresponding map markers and
	links to Yelp listings.
 5. Users can click on any table row to get additional Yelp review information for that result.
 6. Users can send particular results to themselves via email or SMS.  

Example email:  
![email result screenshot](https://raw.githubusercontent.com/jabrabec/Hackbright-project_SNAPPy-Finder/master/static/img/email_example.PNG)  
Example SMS:  
![SMS result screenshot](https://raw.githubusercontent.com/jabrabec/Hackbright-project_SNAPPy-Finder/master/static/img/SMS_example.PNG)  


##DEMOS  
Demo video with annotation:  
https://vimeo.com/202998033  

Live deployment:  
https://snappyfinder.herokuapp.com/  


##QUESTIONS
https://github.com/jabrabec/Hackbright-project_SNAPPy-Finder  
jenniferbrabec@gmail.com
