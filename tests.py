import json
import unittest
from model import connect_to_db, db, Retailer, User, Favorite, example_data
from server import app
import os


class FlaskTestsBasic(unittest.TestCase):
    """Test basic route responses without database connection."""

    def setUp(self):
        """Stuff to do before every test."""
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_index(self):
        '''Test that homepage displays correctly.'''

        result = self.client.get('/')
        self.assertIn('<h2>Find a retailer near you:</h2>', result.data)

    def test_yelp(self):
        '''Test that search_yelp_reviews_by_id returns JSON correctly.'''

        result = self.client.get('/search-yelp-reviews.json',
                                 query_string={'yelpID': 'market-mayflower-and-deli-san-francisco'})

        self.assertIn('"id": "market-mayflower-and-deli-san-francisco"', result.data)

    def test_mail(self):
        '''Test that send_mail route works correctly'''

        recipient = 'snappyfinder@gmail.com'
        subject = 'testing flask mail route'
        body = 'testing flask mail route'

        result = self.client.post('/send-mail', data={'recipient': recipient,
                                                      'subject': subject,
                                                      'body': body})

        self.assertIn('Successfully sent mail to %s\n' % (recipient), result.data)
        self.assertNotIn('Failed to send mail to %s\n' % (recipient), result.data)

    def test_sms(self):
        '''Test that send_sms route works correctly'''

        recipient = "+" + os.environ['PRIVATE_NUMBER']
        body = 'testing flask sms route'

        result = self.client.post('/send-sms', data={'recipient': recipient,
                                                     'body': body})

        self.assertIn('SMS to %s, status:' % (recipient), result.data)


class FlaskTestsDatabase(unittest.TestCase):
    """Test route responses with database."""

    def setUp(self):
        """Stuff to do before every test."""
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_search_coords_json(self):
        '''Test that search_retailers_by_coords_json route returns correctly.'''

        result = self.client.get('/search-coords.json',
                                 query_string={"latitude": '37.7886679',
                                               "longitude": '-122.411499',
                                               "searchRange": '0.2'})

        self.assertIn('''"Market Mayflower & Deli"''', result.data)

    def test_search_addr_json(self):
        '''Test that search_retailers_by_addr_json route returns correctly.'''

        result = self.client.get('/search-address.json',
                                 query_string={'street': '150 santa clara ave',
                                               'city': 'oakland', 'state': 'CA',
                                               'searchRange': '0.3'})

        self.assertIn('''"Quik Stop Market 8003"''', result.data)

    def test_dunder_repr(self):
        '''Tests model.py for setting up and populating DB, and __repr__ statements.'''

        retailer_result = Retailer.query.all()
        self.assertIn('name=Quik Stop Market 8003', str(retailer_result))

        user_result = User.query.all()
        self.assertIn('email=hack@bright.com>', str(user_result))

        favorite_result = Favorite.query.all()
        self.assertIn('Favorite fav_id=', str(favorite_result))


if __name__ == "__main__":
    import unittest

    unittest.main()
