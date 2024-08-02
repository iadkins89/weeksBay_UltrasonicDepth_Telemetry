from flask_sqlalchemy import SQLAlchemy
import math
from sqlalchemy import distinct
from datetime import datetime, timedelta
from server import db
import pandas as pd

harmonic_constituents = [
    (0.09, 183.6, 28.984104),   # Amplitude(ft), Phase (degrees), Speed (deg/hour)
    (0.04, 203.2, 30.0),
    (0.01, 215.8, 28.43973),
    (0.51, 55.1, 15.041069),
    (0.01, 113.3, 57.96821),
    (0.49, 45.1, 13.943035),
    (0.0, 286.5, 86.95232),
    (0.02, 174.5, 44.025173),
    (0.0, 267.6, 60.0),
    (0.01, 65.5, 57.423832),
    (0.0, 285.9, 28.512583),
    (0.0, 0.0, 90.0),
    (0.0, 112.9, 27.968208),
    (0.0, 0.0, 27.895355),
    (0.04, 34.9, 16.139101),
    (0.0, 189.9, 29.455626),
    (0.04, 176.4, 15.0),
    (0.02, 71.1, 14.496694),
    (0.03, 83.0, 15.5854435),
    (0.0, 0.0, 0.5443747),
    (0.17,53.1,0.0821373),
    (0.3,143.1,0.0410686),
    (0.05, 14.2, 1.0158958),
    (0.0, 0.0, 1.0980331),
    (0.03, 45.0, 13.471515),
    (0.11, 32.2, 13.398661),
    (0.01, 178.8, 29.958933),
    (0.0, 0.0, 30.041067),
    (0.0, 20.8, 12.854286),
    (0.16, 56.0, 14.958931),
    (0.0, 0.0, 31.015896),
    (0.0, 294.6, 43.47616),
    (0.0, 141.4, 29.528479),
    (0.01, 158.8, 42.92714),
    (0.05, 204.5, 30.082138),
    (0.0, 0.0, 115.93642),
    (0.01, 122.6, 58.984104)
]
class SensorData(db.Model):
    __tablename__ = 'tide_table'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=True)
    timestamp = db.Column(db.DateTime, index=True, nullable=False)
    tide = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<SensorData {self.name} {self.timestamp} {self.tide}>"

def save_data_to_csv(data, datum_name, filename='output.csv'):
    sensor_name = data[0].name

    data_dict = {
        'id': [d.id for d in data],
        'timestamp': [d.timestamp for d in data],
        'tide': [d.tide for d in data],
    }
    df = pd.DataFrame(data_dict)
    csv_data = df.to_csv(index=False)

    # Add the sensor name at the beginning
    sensor_name_line = f"Sensor Name: {sensor_name}\n"
    datum_name_line = f"Sensor Name: {datum_name}\n"
    csv_data = sensor_name_line + datum_name_line + csv_data

    return csv_data

def date_query(start_date, end_date):
    start_date = start_date.split('T')[0]  # Get only the date part
    end_date = end_date.split('T')[0]  # Get only the date part

    start_dt = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_dt = datetime.strptime(end_date, '%Y-%m-%d').date()

    result = db.session.query(SensorData).filter(SensorData.timestamp >= start_dt, SensorData.timestamp <= end_dt).all()
    return result

def predictions(start_time_str,end_time_str,interval_minutes=6):
    """
    Predict tides using harmonic constituents.

    :param start_time: The start time for prediction (datetime object).
    :param duration_minutes: The total duration for which prediction is to be made in minutes.
    :param interval_minutes: The interval at which to make predictions in minutes.
    :return: List of tuples containing (time, predicted tide level).
    """
    # Convert string to datetime
    start_dt = datetime.fromisoformat(start_time_str)
    end_dt = datetime.fromisoformat(end_time_str)

    predictions = []
    duration_minutes = (end_dt - start_dt).days*24*60
    total_intervals = duration_minutes // interval_minutes

    for i in range(total_intervals + 1):
        current_time = start_dt + timedelta(minutes=i * interval_minutes)
        tide_level = 0

        for amplitude, phase, speed in harmonic_constituents:
            # Calculate the contribution of each constituent
            tide_level += amplitude * math.cos(
                speed * (i * interval_minutes / 60) * (math.pi / 180) + math.radians(phase)) #/ 60))

        tide_level += 0.80 + tide_level
        predictions.append((current_time, tide_level))

    return predictions




