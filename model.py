"""Models and database functions for EBT/SNAP project."""

from flask_sqlalchemy import SQLAlchemy
import datetime


#connect to the db
db = SQLAlchemy()

##############################################################################
# Model definitions


class Retailer(db.Model):
    """Retailer listing in database."""

    __tablename__ = "retailers"

    retailer_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    lat = db.Column(db.Numeric(10, 6), nullable=False)
    lng = db.Column(db.Numeric(10, 6), nullable=False)
    address_1 = db.Column(db.String(80), nullable=False)
    address_2 = db.Column(db.String(80), nullable=True)
    city = db.Column(db.String(30), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zipcode = db.Column(db.Integer, nullable=False)
    county = db.Column(db.String(30), nullable=False)
    yelp_id = db.Column(db.String(125), nullable=True)
    yelp_url = db.Column(db.String(125), nullable=True)
    yelp_img = db.Column(db.String(125), nullable=True)

    def __repr__(self):
        """How the object should be represented when printed."""

        return "<Retailer retailer_id=%s name=%s city=%s>" % (
            self.retailer_id, self.name, self.city)


class User(db.Model):
    """User listing in database."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        """How the object should be represented when printed."""

        return "<User user_id=%s first=%s email=%s>" % (
            self.user_id, self.first_name, self.email)


class Favorite(db.Model):
    """Saved favorite retailer by user database."""

    __tablename__ = "favorites"

    fav_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    retailer_id = db.Column(db.Integer, db.ForeignKey(
        'retailers.retailer_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)
    date_favorited = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    retailer = db.relationship('Retailer', backref='favorites')
    user = db.relationship('User', backref='favorites')

    def __repr__(self):
        """How the object should be represented when printed."""

        return "<Favorite fav_id=%s retailer=%s user=%s>" % (
            self.fav_id, self.retailer_id, self.user_id)


def example_data():
    """Create some sample data."""

    # In case this is run more than once, empty out existing data
    Retailer.query.delete()
    User.query.delete()
    Favorite.query.delete()

    # Add sample employees and departments
    qs = Retailer(name='Quik Stop Market 8003', lat=37.818584, lng=-122.253760,
                  address_1='66 Macarthur Blvd', city='Oakland', state='CA', zipcode=94610,
                  county='ALAMEDA', yelp_id='quik-stop-oakland-2',
                  yelp_url='https://www.yelp.com/biz/quik-stop-oakland-2',
                  yelp_img='https://s3-media2.fl.yelpcdn.com/bphoto/osfaPtXy_GIl7gpK5thnZw/o.jpg')
    mm = Retailer(name='Market Mayflower & Deli', lat=37.789536, lng=-122.413430,
                  address_1='985 Bush St', city='San Francisco', state='CA',
                  zipcode=94109, county='SAN FRANCISCO',
                  yelp_id='market-mayflower-and-deli-san-francisco',
                  yelp_url='https://www.yelp.com/biz/market-mayflower-and-deli-san-francisco',
                  yelp_img='https://s3-media1.fl.yelpcdn.com/bphoto/mekkXctsflvuxgJBIM-1Ow/o.jpg')
    test_user = User(first_name='Hack', last_name='Bright',
                     email='hack@bright.com', password='password')
    test_fave = Favorite(retailer_id=1, user_id=1)

    db.session.add_all([qs, mm, test_user, test_fave])
    db.session.commit()


##############################################################################
# Helper functions

def connect_to_db(app, db_uri=None):
    """Connect the database to our Flask app."""

    # live/snap db connection is set with default db_uri parameter:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri or 'postgres:///snap'
    # disable verbose sqlalchemy version information output:
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to DB."
