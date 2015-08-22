from jinja2 import StrictUndefined
from flask import Flask, render_template, request, redirect, flash, session, jsonify
from food_truck_db_seed import Truck, Truck_schedule, connect_to_db, db
from flask_debugtoolbar import DebugToolbarExtension
import json
import datetime

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

    # Assigns based on number passed via URL
    print truck_id
    truck = Truck.query.get(truck_id)
    print truck
    # Gets truck information from truck info db
    truck_schedule = Truck_schedule.query.filter_by(truck_id=truck_id).all() 
    #list of schedule objectsby truck ID foreign key - will be empty for some truck IDs
    print truck_schedule 

# Overall approach to this data: could do a join to only get IDs in both lists. 

    if truck_schedule:
        truck_schedule_1 = truck_schedule[0]
        print "Truck_schedule_1=", truck_schedule_1
    else:
        truck_schedule_1 = {"name": "fake data",
                            "schedule_line_id": "666",
                            "location_description": "fake data",
                            "food_items": "fake data",
                            "expiration_date": "fake data",
                            "day_of_week": "Any day",
                            "start_time": "99 AM",
                            "end_time": "99 PM",
                            "extra_text": "Here is where extra text might go.",
                            "x_coordinate": "72.222222",
                            "y_coordinate": "27"
                            }
        print "You got the dummy."
        # Added a fake dictionary for now so that it doesn't freak out if there's no information. But now it only uses that fake dictionary, rrrrrrr.
        #Add something here that passes the value if it exists and ignore it if it doesn't so the randomly selected pages don't error if there are no schedule lines! But Jinja ignores variables without value, so there are ways to put this together... Could make a second simpler file to call in case of no schedule lines. 

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

@app.route("/truck_schedule_times")
def truck_schedule_times():
    truck_id = request.args.get("truck_id")
    truck_schedule = Truck_schedule.query.filter_by(truck_id=truck_id).all() 


    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    schedule_range = {"Sunday": [],
                      "Monday": [],
                      "Tuesday": [],
                      "Wednesday": [],
                      "Thursday": [],
                      "Friday": [],
                      "Saturday": []
                      }
    # # What if they're two different places in a day? Might need to add permit numbers to that function.

    for truck_object in truck_schedule:
        print "Opened an object!"
        print "Start time: ", truck_object.start_time
        print "End time: ", truck_object.end_time

        if truck_object.start_time not in schedule_range[truck_object.day_of_week]:
            if len(truck_object.start_time) < 5:
                revised_time = "0" + truck_object.start_time
                print "The revised start_time got added!", revised_time
                schedule_range[truck_object.day_of_week].append(revised_time)
            else:
                schedule_range[truck_object.day_of_week].append(truck_object.start_time)
                print "It added the start_time as it was!", truck_object.start_time

        if truck_object.end_time not in schedule_range[truck_object.day_of_week]:
            if len(truck_object.end_time) < 5:
                revised_time = "0" + truck_object.start_time
                print "This is the revised end_time got added: ", revised_time
                schedule_range[truck_object.day_of_week].append(revised_time)
            else:
                schedule_range[truck_object.day_of_week].append(truck_object.end_time)
                print "It added the end_time as it was!", truck_object.start_time


    print "After-function schedule_range: ", schedule_range

    # print "This should be the opening time Sunday: ", min(schedule_range["Sunday"])
    # print "This should be the closing time Sunday: ", max(schedule_range["Sunday"])

    # sunday_start_time = min(schedule_range["Sunday"])
    # sunday_close_time = max(schedule_range["Sunday"])

    schedule_open_close = {"Sunday": [],
                          "Monday": [],
                          "Tuesday": [],
                          "Wednesday": [],
                          "Thursday": [],
                          "Friday": [],
                          "Saturday": []
                          }

    for key in schedule_range: 
        if schedule_range[key] == []:
            pass
        else: 
            print "HERE IS THE KEY, NEW LOOP!", key
            formatted_open = datetime.datetime.strptime(min(schedule_range[key]), "%H:%M")
            print "Formatted open: ", formatted_open

            if formatted_open.hour < 12:
                augment = " AM"
            else: 
                augment = " PM"

            open_time = str(formatted_open.hour % 12) + ":" + str(formatted_open.minute) + "0" + augment 
            print "Open time: ", open_time
            schedule_open_close[key].append(open_time)

            formatted_close = datetime.datetime.strptime(max(schedule_range[key]), "%H:%M")
            print "Formatted close: ", formatted_close

            if formatted_close.hour < 12:
                augment = " AM"
            else: 
                augment = " PM"

            close_time = str(formatted_close.hour % 12) + ":" + str(formatted_close.minute) + "0" + augment
            print "Close time: ", close_time
            schedule_open_close[key].append(close_time)

        print schedule_open_close

        # if statement that turns numbers over 12 to regular hours and adds AM or PM
        # line that turns numbers into datetime objects and puts correct information on
        # part that adds this formatted bit to the two-item list this will ultimately pass to the page, appended to each day-key
        # do it for both min and max

    # schedule_range_json = json.dumps(schedule_open_close)
    # print "This is the jsonified version: ", schedule_range_json

    return render_template("truck_schedule.html",
                            days=days,
                            schedule_open_close=schedule_open_close)

@app.route("/truck_info.json")
def truck_information():
    """JSON information about truck schedules."""

    truck_id = request.args.get("truck_id")
    # Add more args/variables for future filters, then pass down. If [x variable], then (this filtered query).

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
    for truck in Truck_schedule.query.filter_by(truck_id=truck_id).all()}

    return jsonify(truck_schedule_info)


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