from jinja2 import StrictUndefined
from flask import Flask, render_template, request, redirect, flash, session, jsonify
# from flask_debugtoolbar import DebugToolbarExtension

# from model import tbd


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"
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
#Figure out what ID I will use for trucks


    return render_template("truck_details.html")

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




@app.route('/truck-oracle')
def get_random_truck():
    """ 
    Presents a random truck when the user pushes a button (ideally one that's open, if possible). Could it use geographic data to find the closest one?). Needs a function to choose a random row number from the API db.
    """
    

    return render_template("random-truck.html")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    # app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run()