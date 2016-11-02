"""File to seed EBT database with retailer data in data/"""
from model import Retailer, connect_to_db, db
from server import app

import csv


def load_retailers():
    """Load reailers from source CSV into database."""

    print "Importing retailers..."

    # Read CSV file
    with open("data/94610_only.csv") as source_file:
        example_data = list(csv.reader(source_file))

    # skip header row for populating db
    for list_item in example_data[1:]:
        retailer = Retailer(name=list_item[0], lat=list_item[2],
                            lng=list_item[1], address_1=list_item[3],
                            address_2=list_item[4], city=list_item[5],
                            state=list_item[6], zipcode=list_item[7],
                            county=list_item[9])

        # Add the current retailer to the session
        db.session.add(retailer)

    # Commit the db.session changes to the database
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import data
    load_retailers()
