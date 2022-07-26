import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

### 9.5.1
 
## Set up the Database Engine
engine = create_engine("sqlite:///hawaii.sqlite")

## reflect the database into our classes.
Base = automap_base()

## reflect the database
Base.prepare(engine, reflect=True)

## create a variable for each of the classes so that we can reference them later
Measurement = Base.classes.measurement
Station = Base.classes.station

## create a session link from Python to our database 
session = Session(engine)

## Set up Flask - create a Flask application called "app."
app = Flask(__name__)

# Notice the "__name__" variable in this code. 
# This is a special type of variable in Python. 
# Its value depends on where and how the code is run.
# For example, if we wanted to import our app.py file into another Python file named example.py, 
# the variable __name__ would be set to example. 
# Here's an example of what that might look like:
# import app
# print("example __name__ = %s", __name__)
# if __name__ == "__main__":
#     print("example is being run directly.")
# else:
#     print("example is being imported")
# However, when we run the script with python app.py, 
# the __name__ variable will be set to __main__. 
# This indicates that we are not using any other file to run this code.

### 9.5.2
## Create the Welcome Route
## Our first task when creating a Flask route is to define what our route will be. 
# We want our welcome route to be the root, 
# which in our case is essentially the homepage.

## define the welcome route using the code below:
@app.route("/")

## The next step is to add the routing information for each of the other routes.
## add the precipitation, stations, tobs, and temp routes that 
# we'll need for this module into our return statement. 
# We'll use f-strings to display them for our investors:
## When creating routes, we follow the naming convention /api/v1.0/ followed by the name of the route
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')


## Start by using the command line to navigate to your project folder.
#  #Open Terminal on "Surfs Up" Folder
#Type - "export FLASK_APP=app2.py" and press enter
#Type - "flask run" and press enter
# Then run your code: flask run

### 9.5.3 Precipitation Route

## The next route we'll build is for the precipitation analysis.
@app.route("/api/v1.0/precipitation")

## create the precipitation() function.
def precipitation():
    #add the line of code that calculates the date one year ago from the most recent date
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # query to get the date and precipitation for the previous year.
    # Notice the .\ in the first line of our query? 
    # This is used to signify that we want our query to continue on the next line. 
    # You can use the combination of .\ to shorten the length of your query
    precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
    # Create a dictionary with the date as the key and the precipitation as the value.
    precip = {date: prcp for date, prcp in precipitation}
    # use jsonify() to format our results into a JSON structured file
    return jsonify(precip)

# At this point, you might be wondering where to view the output of your code. 
# Just like we did previously, copy the web address (http://127.0.0.1:5000/) into our web browser. 
# You will need to navigate to the precipitation route in order to see the output of your code. 
#IMPORTANT: You can do this by adding api/v1.0/precipitation to the end of the web address.

### 9.5.4 Stations Route

## Define route and route name
@app.route("/api/v1.0/stations")

## With our route defined, we'll create a new function
def stations():
    # create a query that will allow us to get all of the stations in our database
    results = session.query(Station.station).all()
    # unraveling our results into a one-dimensional array using np.ravel
    # convert our unraveled results into a list using list()
    stations = list(np.ravel(results))
    # jsonify the list and return it as JSON
    # You may notice here that to return our list as JSON, 
    # we need to add stations=stations.
    # This formats our list into JSON
    return jsonify(stations=stations)

## Start by using the command line to navigate to your project folder.
#  #Open Terminal on "Surfs Up" Folder
#Type - "export FLASK_APP=app2.py" and press enter
#Type - "flask run" and press enter
# Then run your code: flask run
#You will need to navigate to the stations route in order to see the output of your code. 
#IMPORTANT: You can do this by adding api/v1.0/stations to the end of the web address.

### 9.5.5 Monthly Temperature Route

## defining the route 
@app.route("/api/v1.0/tobs")

# Create Function
def temp_monthly():
    # calculate the date one year ago from the last date in the database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # query the primary station for all the temperature observations from the previous year
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    # As before in Stations
    # --> unravel the results into a one-dimensional array and 
    # convert that array into a list
    temps = list(np.ravel(results))    
    # jsonify and return
    return jsonify(temps=temps)

## Start by using the command line to navigate to your project folder.
#  #Open Terminal on "Surfs Up" Folder
#Type - "export FLASK_APP=app2.py" and press enter
#Type - "flask run" and press enter
# Then run your code: flask run
#You will need to navigate to the tobs route in order to see the output of your code. 
#IMPORTANT: You can do this by adding api/v1.0/tobs to the end of the web address.


### 9.5.6: Statistics Route
## investors will need to see the minimum, maximum, and average temperatures. 
# For this we'll create a route for our summary statistics report.

# Define route
# different from the previous ones in that 
# we will have to provide both a starting and ending date
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

# Create Function
# add parameters to our stats()function: a start parameter and an end parameter
def stats(start=None, end=None):
    # query to select the minimum, average, and maximum temperatures
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]    
    # determine the starting and ending date, 
    # add an if-not statement to our code. 
    # This will help us accomplish a few things. 
    # We'll need to query our database using the list that we just made. 
    # Then, we'll unravel the results into a one-dimensional array and convert them to a list. 
    # Finally, we will jsonify our results and return them.
    if not end:
        # take note of the asterisk in the query next to the sel list. 
        # Here the asterisk is used to indicate there will be multiple results for our query: 
        # minimum, average, and maximum temperatures.
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
    # calculate the temperature minimum, average, and maximum with the start and end dates
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

# we have not specified a start and end date for our range. 
# Fix this by entering any date in the dataset as a start and end date. 
# The code will output the minimum, maximum, and average temperatures.
## Important - > You would add the following path to the address in your web browser: /api/v1.0/temp/2017-06-01/2017-06-30

## Start by using the command line to navigate to your project folder.
# Open Terminal on "Surfs Up" Folder
# Type - "export FLASK_APP=app2.py" and press enter
# Type - "flask run" and press enter
# Then run your code: flask run
# You will need to navigate to the temp route in order to see the output of your code.
# You must specify start and end dates to @app.route("/api/v1.0/temp/<start>/<end>")
# Example -> for June 2017
#IMPORTANT: You can do this by adding /api/v1.0/temp/2017-06-01/2017-06-30 to the end of the web address.