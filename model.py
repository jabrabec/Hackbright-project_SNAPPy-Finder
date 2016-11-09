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


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our test PostgreSQL database
    # testdb connection:
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///testdb'
    # live/snap db connection:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///snap'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to DB."
