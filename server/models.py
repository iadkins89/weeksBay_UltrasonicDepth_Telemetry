import math
from sqlalchemy import desc
from datetime import datetime, timedelta
from server import db
import pandas as pd
from dateutil.parser import parse as parse_date

class SensorData(db.Model):
    __tablename__ = 'lidar_tide_table'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=True)
    timestamp = db.Column(db.DateTime, index=True, nullable=False)
    tide = db.Column(db.Float, nullable=False)
    battery = db.Column(db.Float, nullable=False)

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

    # Parse the strings into datetime objects and set the times
    start_dt = parse_date(start_date).replace(hour=0, minute=0, second=0)
    end_dt = parse_date(end_date).replace(hour=23, minute=59, second=59)

    result = db.session.query(SensorData).filter(SensorData.timestamp >= start_dt, SensorData.timestamp <= end_dt).all()
    return result

def most_recent_query():
    return db.session.query(SensorData).order_by(desc(SensorData.timestamp)).first()






