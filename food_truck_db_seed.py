import csv
from flask_sqlalchemy import SQLAlchemy
# import os

truck_permit_records = open("mobile_food_permits.csv")
db = SQLAlchemy()

class Truck(db.Model):
    """
    Turns truck facility permit records into collected objects
    """

    __tablename__ = "trucks_info_test"
    
    #filter initial spreadsheet by Approved only; create process to remove 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(1000), nullable=False) #from city; Applicant
    permit_number = db.Column(db.String(50), nullable=False) #from city; permit
    location_description = db.Column(db.String(1000)) #from city; LocationDescription
    food_items = db.Column(db.String(1000)) #from city; FoodItems
    # description = db.Column(db.String(250)) #optionaltext; pull from any day
    expiration_date = db.Column(db.String(1000)) #from city; ExpirationDate
    url = db.Column(db.String(200))
    menu_link = db.Column(db.String(200))
    twitter_handle = db.Column(db.String(50))
    tweets = db.Column(db.String(200))
    price_range = db.Column(db.String(50))
    food_type = db.Column(db.String(200))
    yelp_url = db.Column(db.String(200))
    yelp_rating = db.Column(db.String(200)) #depends on how Yelp provides that data
    yelp_images = db.Column(db.String(200))
    payment_method = db.Column(db.String(200))

    @classmethod
    def make_truck_records():
        # file_open = open("mobile_food_permits.csv")
        # file_read = csv.reader(file_open)

        file_read = csv.reader(open('mobile_food_permits.csv', 'rU'), quotechar='"', delimiter = ',')

        for row in file_read:
            # temp_object = Truck(row)
            # object_list.append(temp_object)
            # print temp_object
            name = row[1] #from city; Applicant
            permit_number = row[9] #from city; may not use
            location_description = row[4]
            food_items = row[11]
            expiration_date = row[21]
            # description = row[3] #optionaltext; pull from any day
            url = None
            menu_link = None
            twitter_handle = None
            tweets = None
            price_range = None
            food_type = None
            yelp_url = None
            yelp_rating = None #depends on how Yelp provides that data
            yelp_images = None
            payment_method = None

            temp_object = Truck(name=name, permit_number=permit_number, location_description=location_description, food_items=food_items, expiration_date=expiration_date, url=url, menu_link=menu_link, twitter_handle=twitter_handle, tweets=tweets, price_range=price_range, food_type=food_type, yelp_url=yelp_url, yelp_rating=yelp_rating, yelp_images=yelp_images, payment_method=payment_method)

            db.session.add(temp_object)

        db.session.commit()

        # return object_list
        print "Whoa, you made objects! And they apparently committed! Holy crap!"

class Truck_schedule(db.Model):

    __tablename__ = "trucks_schedule_information"

    schedule_line_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    truck_id = db.Column(db.Integer, db.ForeignKey('trucks_info_test.id'))
    truck_name = db.Column(db.String(100), nullable=False)
    day_of_week = db.Column(db.String(50), nullable=False)
    permit_number = db.Column(db.String(50), nullable=False)
    location_description = db.Column(db.String(1000))
    extra_text = db.Column(db.String(1000))
    location_id = db.Column(db.String(50), nullable=False)
    schedule_id = db.Column(db.String(50), nullable=False)
    start_time = db.Column(db.String(10))
    end_time = db.Column(db.String(10))
    x_coordinate = db.Column(db.String(50))
    y_coordinate = db.Column(db.String(50))

    # self.truck_id = truck_id
    # self.truck_name = truck_name
    # self.day_of_week = day_of_week
    # self.permit_number = permit_number
    # self.location_description = location_description
    # self.extra_text = extra_text
    # self.location_id = location_id
    # self.schedule_id = schedule_id
    # self.start_time = start_time
    # self.end_time = end_time
    # self.coordinates = coordinates

    @classmethod
    def make_truck_schedule(cls):
        file_read = csv.reader(open('Mobile_Food_Schedule.csv', 'rU'), quotechar='"', delimiter = ',')

        i = 1
        for row in file_read:
            if i % 100 == 0:
                print "Hello! ", i
            i += 1
            truck_name = row[9]
            truck_id_tuple = db.session.query(Truck.id).filter_by(name=truck_name).first()
            if not truck_id_tuple:
                continue
            else:
                truck_id = truck_id_tuple[0]
                
            # day_of_week, permit_number, location_description, extra_text, location_id,
            if row[0]:
                day_of_week = row[0]
            else: 
                day_of_week = ""

            if row[1]:
                permit_number = row[1]
            else:
                permit_number = ""

            if row[2]:
                # location_description = row[2].encode('latin1', errors='ignore')
                location_description = row[2].decode('utf8', errors='ignore')
            else: 
                location_description = ""

            if row[3]:
                extra_text = row[3].decode('utf8', errors='ignore')
            else: 
                extra_text = ""
  
            if row[4]:
                location_id = row[4]
            else: 
                location_id = ""

            if row[5]:
                schedule_id = row[5]
            else: 
                schedule_id = ""

            if row[6]:
                start_time = row[6]
            else:
                start_time = ""

            if row[7]:
                end_time = row[7]
            else: 
                end_time = ""

            if len(row) > 10:
                x_coordinate = row[10]
                y_coordinate = row[11]
            else:
                x_coordinate = ""
                y_coordinate = ""

            temp_object = cls(truck_id=truck_id, truck_name=truck_name, day_of_week=day_of_week, permit_number=permit_number, location_description=location_description, extra_text=extra_text, location_id=location_id, schedule_id=schedule_id, start_time=start_time, end_time=end_time, x_coordinate=x_coordinate, y_coordinate=y_coordinate)

            db.session.add(temp_object)

        db.session.commit()

        # return object_list
        print "Whoa, you made more objects! And they apparently committed again! Woohoo!"

    @classmethod
    def dump(self):

        return {"truckscheduleinfo": {'truck_id': self.truck_id,
                                    'truck_name': self.truck_name,
                                    'day_of_week': self.day_of_week,
                                    'permit_number': self.permit_number,
                                    'location_description': self.location_description,
                                    'extra_text': self.extra_text,
                                    'location_id': self.location_id,
                                    'schedule_id': self.schedule_id,
                                    'start_time': self.start_time,
                                    'end_time': self.end_time,
                                    'coordinates': self.coordinates}}

# class Truck_permit(db.Model):
#     """Creates between table linking truck info with all associated location permits.
#     """

#     __tablename__ = "trucks_and_permits"

#     combination_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     truck_id = db.Column(db.Integer, db.ForeignKey('trucks_info_test.id'), nullable=False)
#     location_permit = db.Column(db.String(50), nullable=False) # from city; permit, row[1] on CSV
#     name = db.Column(db.String(100), nullable=False) # from city; Applicant, row [9] on CSV

#     @classmethod
#     def make_truck_permit_records(cls):

#         file_read = csv.reader(open('mobile_food_permits.csv', 'rU'), quotechar='"', delimiter = ',')

#         for row in file_read:
#             # temp_object = Truck(row)
#             # object_list.append(temp_object)
#             # print temp_object
#             name = row[1] #from city; Applicant
#             print "Name:", name
#             location_permit = row[9] #from city; may not use            
#             print "Location permit:", location_permit
#             truck_id = db.session.query(Truck.id).filter_by(name=row[1]).first()[0]
#             print "Queried truck ID:", truck_id

#             temp_object = cls(name=name, location_permit=location_permit, truck_id=truck_id)

#             db.session.add(temp_object)

#         db.session.commit()

#         # return object_list
#         print "Whoa, you made more objects! And they apparently committed again! Woohoo!"

def update_db():
    """
    Connects to https://data.sfgov.org/Economy-and-Community/Mobile-Food-Schedule/jjew-r69b to query the Addr_Date_Modified column to find any changes committed since the last date the thing ran. (Let's say it should go once a week.)
    """

    # pseudocode:
    # connect to my db
    # connect to city db
    # API query by Addr_Date_Modified to see what fields have changed since the last update (will need to account for blank cells)
    # collect permit numbers of rows with changes
    # create list of those permit numbers 

    # if there is an update:
    #     use that list of permit numbers to loop a removal/query like so:
    #     remove existing records for that permit number
    #     reseed those rows from schedule table using existing seed function, taking only the appropriate fields
    #     run the function to add neighborhoods to those rows
    #     commit

    # set system update date to date of that query
    # set it to run again in a week or whatever

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use Postgres database
    # SQLALCHEMY_DATABASE_URI = os.environ['postgresql://localhost:5432/truck_info']
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost:5432/truck_info'
    db.app = app
    db.init_app(app)



if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    # So that we can use Flask-SQLAlchemy, we'll make a Flask app
    from server import app
    # from flask import Flask
    # app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."
