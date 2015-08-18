from jinja2 import StrictUndefined
from flask import Flask, render_template, request, redirect, flash, session, jsonify
from food_truck_db_seed import Truck, Truck_schedule, connect_to_db, db
from flask_debugtoolbar import DebugToolbarExtension
import json

# from model import tbd


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "super_secret_key_thing_WHOA"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
#Map goes here, initial data (whatever that is)
    return render_template("homepage.html")

@app.route('/truck/<int:truck_id>')
def truck_details(truck_id):
    """Shows fuller details for individual food truck"""

    #Call full truck record
    #Call all applicable rows from schedule spreadsheet
    #Divide into variables to pass into the site itself

    truck_id = truck_id 
    truck = Truck.query.get(truck_id)
    truck_schedule = Truck_schedule.query.filter_by(truck_id=truck_id).all() #list of objects

    schedule_range = {"Sunday": [],
                      "Monday": [],
                      "Tuesday": [],
                      "Wednesday": [],
                      "Thursday": [],
                      "Friday": [],
                      "Saturday": []
                      }

    for truck_object in truck_schedule:
        if truck_object.start_time not in schedule_range[truck_object.day_of_week]:
            schedule_range[truck_object.day_of_week].append(truck_object.start_time)
        else:
            pass

        if truck_object.end_time not in schedule_range:
            schedule_range["Sunday"].append(truck_object.end_time)
        else: 
            pass


# Thoughts and questions: is there a more efficient way to do this? Do I need to creat the DOW dictionary keys first? Does this need to be a JSON route like the basic query information? And once I get the function down, I need to figure out how best to do the sort and then taking the first and last time in that range. 

    truck_schedule_1 = truck_schedule[0]
    # truck_schedule_json_object = json.dumps(truck_schedule_1)
    # print truck_schedule_json_object
    # print type(truck_schedule_json_object)

    # coordinates = [truck_schedule_1.x_coordinate, truck_schedule_1.y_coordinate]

    #going to need some if-else Jinja stuff to account for blank cells. Missing coordinates: "This truck didn't tell SF its coordinates, but here's its address: {{ blah blah }}." Will also need to convert 24-hour time to American-friendly time.


#JS: JSON.stringify(jsObject);        // --> a string of valid JSON (to send)
# JSON.parse(jsonString);          // --> a javascript object
# Python:
# json.dumps(python_dict)          # --> a string of valid JSON (to send)
# json.loads(json_string)          # --> a Python dict
# return jsonify(days=2, cost=5)

#Figure out what ID I will use for trucks
#Uses ID from truck detail table to create, then uses same ID on schedule table to add schedule information


    return render_template("truck_details.html", truck_id=truck_id, truck=truck, truck_schedule=truck_schedule, truck_schedule_1=truck_schedule_1)
        # truck_schedule_object_list=truck_schedule_object_list)

@app.route("/truck_info.json")
def truck_information():
    """JSON information about trucks."""

    truck_schedule_info = {
        truck.schedule_line_id: {
        "truckName": truck.truck_name,
        "truckId": truck.truck_id,
        "dayOfWeek": truck.day_of_week,
        "permitNumber": truck.permit_number,
        "locationDescription": truck.location_description,
        "extraText": truck.extra_text,
        "locationId": truck.location_id,
        "scheduleId": truck.schedule_id,
        "startTime": truck.start_time,
        "endTime": truck.end_time,
        "xCoordinate": truck.x_coordinate,
        "yCoordinate": truck.y_coordinate
    }

    for truck in Truck_schedule.query.limit(150)}

    return jsonify(truck_schedule_info)

@app.route("/truck-schedule-info")
def get_schedule_info():

    delivery_info = {
        'days': days,
        'cost': cost
    }

    return json.dumps(delivery_info) 

@app.route('/neighborhood/<string:neighborhood_name>')
def neighborhood_page(neighborhood_name):
    """Gives neighborhood information and shows local trucks for it, by day/time"""
    
    return render_template("neighborhood_details.html")
    
@app.route('/add-a-truck')
def user_submits_truck():
    """Submission/correction page for users """
    #Flash message thanking for submission
    #Function committing submission to submission db

    return render_template("submissions.html")

@app.route('/add-my-truck')
def truck_submits_truck():
    """Truck owners can submit truck information for inclusion"""
    #Flash message thanking for submission

    return render_template("truck-submission.html")

@app.route('/about-this-project')
def about_page():
    """ 
    About page for this project, detailing technology and directing to GitHub page
    """
    

    return render_template("about.html")




@app.route('/truck-me')
def get_random_truck():
    """ 
    Presents a random truck when the user pushes a button (ideally one that's open, if possible). Could it use geographic data to find the closest one?). Needs a function to choose a random row number from the API db.
    """
    

    return render_template("random-truck.html")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()