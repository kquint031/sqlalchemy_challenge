# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    """List all available routes"""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    prev_year = dt.datetime(2017, 8, 23)-dt.timedelta(days=365)
    # Query precipitation
    results = session.query(Measurement.station, Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).\
    order_by(Measurement.date).all()

    session.close()

    # Create prcp dictionary from raw data and append to list
    all_prcp = []
    for station, date, prcp in results:
        prcp_dict = {}
        prcp_dict["station"] = station
        prcp_dict["date"] = date
        prcp_dict["precipitation"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""

    # Query precipitation
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    station_list = list(np.ravel(results))

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query precipitation
    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').all()

    session.close()

    all_tobs = []
    for station, date, tobs in results:
        tobs_dict = {}
        tobs_dict["station"] = station
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def start_date(start):

    session = Session(engine)

    # Query start date
    results_start = session.query(
        func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.avg(Measurement.tobs)).filter(Measurement.date >= start).first()

    session.close()

    # Convert to list 
    start_list = list(np.ravel(results_start))

    return jsonify(start_list)

@app.route("/api/v1.0/<start>/<end>")
def end_date(start, end):
 
    session = Session(engine)

    # Query start-end date
    results_start_end = session.query(
        func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.avg(Measurement.tobs)).filter(Measurement.date >= start, Measurement.date <= end).all()

    session.close()

    # Convert list of tuples into normal list
    start_end_list = list(np.ravel(results_start_end))

    return jsonify(start_end_list)

if __name__ == '__main__':
   app.run(debug = True)

