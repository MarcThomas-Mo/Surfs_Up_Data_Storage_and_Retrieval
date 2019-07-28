import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine('sqlite:///hawaii.sqlite')
Base = automap_base()

Base.prepare(engine, reflect=True)
Base.classes.keys()
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

from flask import Flask, jsonify

app = Flask(__name__)

@app.route ("/")
def home():
    return(
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/<start><br/>")
#    f"/api/v1.0/<start>/<end><br/>"


@app.route("/api/v1.0/precipitation")
def precip():
     rain = (session.query (Measurement.date, Measurement.prcp).order_by(Measurement.date)[-365:])
     rain_dict = dict(rain)
     return jsonify(rain_dict)

@app.route("/api/v1.0/stations")
def stations():
     station = (session.query(Measurement.station, 
          func.count(Measurement.prcp)).group_by(Measurement.station).order_by(func.count(Measurement.prcp).desc()).all())
     station_dict = dict(station)
     return jsonify(station_dict)

@app.route("/api/v1.0/tobs")
def tobs():
     tob = (session.query(Measurement.station, 
          func.count(Measurement.prcp)).group_by(Measurement.station).order_by(func.count(Measurement.prcp).desc()).first())
     tob_dict = dict(tob)
     return jsonify(tob_dict)



if __name__ == "__main__":
    app.run(debug=True)
