from jinja2 import StrictUndefined
from flask import Flask, render_template, request, redirect, flash, session, jsonify
from food_truck_db_seed import Truck, Truck_schedule, connect_to_db, db
from flask_debugtoolbar import DebugToolbarExtension
import json
import datetime
import random
from sqlalchemy import or_, distinct

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
    truck = Truck.query.get(truck_id)
    # Gets truck information from truck info db
    truck_schedule = Truck_schedule.query.filter_by(truck_id=truck_id).all() 
    truck_details = Truck.query.filter_by(id=truck_id).one()

    return render_template("truck_details.html", truck_id=truck_id, truck=truck, truck_schedule=truck_schedule)

@app.route("/truck_schedule_times")
def truck_schedule_times():
    """Returns formatted times for each day, filtering by truck ID"""
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

        if truck_object.start_time not in schedule_range[truck_object.day_of_week]:
            if len(truck_object.start_time) < 5:
                revised_time = "0" + truck_object.start_time
                schedule_range[truck_object.day_of_week].append(revised_time)
            else:
                schedule_range[truck_object.day_of_week].append(truck_object.start_time)

        if truck_object.end_time not in schedule_range[truck_object.day_of_week]:
            if len(truck_object.end_time) < 5:
                revised_time = "0" + truck_object.start_time
                schedule_range[truck_object.day_of_week].append(revised_time)
            else:
                schedule_range[truck_object.day_of_week].append(truck_object.end_time)

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
            formatted_open = datetime.datetime.strptime(min(schedule_range[key]), "%H:%M")

            if formatted_open.hour < 12:
                augment = " AM"
            else: 
                augment = " PM"

            open_time = str(formatted_open.hour % 12) + ":" + str(formatted_open.minute) + "0" + augment 
            schedule_open_close[key].append(open_time)

            formatted_close = datetime.datetime.strptime(max(schedule_range[key]), "%H:%M")

            if formatted_close.hour < 12:
                augment = " AM"
            else: 
                augment = " PM"

            close_time = str(formatted_close.hour % 12) + ":" + str(formatted_close.minute) + "0" + augment
            schedule_open_close[key].append(close_time)

    return render_template("truck_schedule.html",
                            days=days,
                            schedule_open_close=schedule_open_close)

@app.route("/truck_info.json")
def truck_information():
    """JSON information about truck schedules, pulled by truck ID only. Made for truck_details.html-truck/int page."""

    truck_id = request.args.get("truck_id")
    print truck_id
    trucks = Truck_schedule.query.filter_by(truck_id=truck_id).all()

    truck_schedule_info = {}

    for truck in trucks: 
    # truck_schedule_info = {
        temp_dict = {
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

        truck_schedule_info[truck.schedule_line_id] = temp_dict
    # for truck in Truck_schedule.query.filter_by(truck_id=truck_id).all()}

    return jsonify(truck_schedule_info)

@app.route("/all_truck_info.json")
def all_truck_information():
    """JSON feed of all truck schedule lines, returning those open today, as determined by datetime.now."""

    day = datetime.datetime.now()
    print "Day: ", day
    today_ordinal = day.weekday()
    print "Today_ordinal: ", today_ordinal

    weekdays = {
            0: "Monday",
            1: "Tuesday",
            2: "Wednesday",
            3: "Thursday",
            4: "Friday",
            5: "Saturday",
            6: "Sunday"
    }

    weekday_string = weekdays[today_ordinal]
    print "Weekday_string: ", weekday_string

    all_truck_schedule_info = {
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
        for truck in Truck_schedule.query.filter_by(day_of_week=weekday_string).all()
    }

    return jsonify(all_truck_schedule_info)

@app.route('/day/<string:dayOfWeek>')
def test(dayOfWeek):
    """ Why don't things work, sigh """
    print dayOfWeek

    truck_schedule = Truck_schedule.query.filter_by(day_of_week=dayOfWeek).all() 

    return render_template("daypage.html", dayOfWeek = dayOfWeek)

@app.route("/truck_info_by_day.json")
def truck_information_by_day():
    """JSON feed of all truck schedule lines with adaptable query."""

    day = request.args.get("dayOfWeek")
    day_trucks = Truck_schedule.query.filter_by(day_of_week=day).all()

    truck_schedule_info = {}

    for truck in day_trucks: 
        temp_dict = {
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
 
        truck_schedule_info[truck.schedule_line_id] = temp_dict

    return jsonify(truck_schedule_info)

@app.route('/search')
def search_db():
    """Does a text search of the truck name and description fields, returns list of trucks with link to truck pages"""
    search_term = request.args.get("search-text")
    search_term_formatted = '%' + search_term + '%'
 
    search_results = Truck_schedule.query.filter(or_(Truck_schedule.truck_name.ilike(search_term_formatted), Truck_schedule.extra_text.ilike(search_term_formatted))).distinct(Truck_schedule.truck_id).all()

    if search_results:
        pass
    else:
        search_results = None

    return render_template("search_results.html", search_term=search_term, search_results=search_results)

# @app.route('/neighborhood/<string:neighborhood_name>')
# def neighborhood_page(neighborhood_name):
#     """Gives neighborhood information and shows local trucks for it, by day/time"""
    
#     return render_template("neighborhood_details.html")
    
@app.route('/add-a-truck')
def user_submits_truck():
    """Submission/correction page for users """
    #Flash message thanking for submission
    #Function committing submission to submission db

    return render_template("submissions.html")

@app.route('/truck-submitted')
def record_truck_submission():
    """Records submitted truck information to system txt file; tells users thank you."""
    truck_name = request.args.get("truck-name")
    if request.args.get("truck-url"):
        truck_url = request.args.get("truck-url")
    else:
        truck_url = ""
    if request.args.get("truck-deets"):
        truck_info = request.args.get("truck-deets")
    else: 
        truck_info = ""
    
    if truck_url and truck_info:
        truck_line = "|".join([truck_name, truck_url, truck_info])
    elif truck_url:
        truck_line = "|".join([truck_name, truck_url, " "])
    elif truck_info:
        truck_line = "|".join([truck_name, " ", truck_info])
    else:
        truck_line = truck_name + " | | "

    print truck_line
    this_file = open("truck-submissions.txt", "a")
    this_file.write(truck_line)
    this_file.close()

    return render_template("submitted.html", truck_info=truck_info)


@app.route('/search-permits')
def access_sfopendata_api():
    """Constructs via form and returns via AJAX queries of food truck permits by business or location permit record"""

    return render_template("api-search.html")


@app.route('/permit-search-results' )
def give_sfopendata_results():
    day_of_week = request.args.get("dayofweek")

    if request.args.get("truckname"):
        truck_name = request.args.get("truckname")
    else:
        truck_name = ""

    return render_template("api-search-results.html",
                            day_of_week=day_of_week,
                            truck_name=truck_name)

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

    #Add validator here to make sure a schedule query with the returned ID actually has results; if not, choose a new number
    #Still not working. Revisit. 
    valid_id_returned = False
    
    while valid_id_returned == False:
        rand = random.randrange(0, Truck_schedule.query.count()) 
        truck_object = Truck.query.filter_by(id=rand).one()
        # Need try/except here? What's the way to use this error to spur it back through the loop?

        if truck_object:
            valid_id_returned = True
            url = "/truck/" + str(rand)
    
    return redirect(url)        


@app.route('/test')
def test_stuff():
    """Playing with Google Maps marker clustering"""

    return render_template("test.html")

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True
    DebugToolbarExtension(app)

    connect_to_db(app)

    # Use the DebugToolbar


    app.run()