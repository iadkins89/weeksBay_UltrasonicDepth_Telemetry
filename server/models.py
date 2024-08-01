from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import distinct
from datetime import datetime
from server import db
import pandas as pd

class SensorData(db.Model):
    __tablename__ = 'depth_table'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=True)
    timestamp = db.Column(db.DateTime, index=True, nullable=False)
    depth = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<SensorData {self.name} {self.timestamp} {self.temperature} {self.humidity}>"

def query_data(start_date, end_date, name):
    start_date = start_date.split('T')[0]  # Get only the date part
    end_date = end_date.split('T')[0]  # Get only the date part

    start_dt = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_dt = datetime.strptime(end_date, '%Y-%m-%d').date()

    result = db.session.query(SensorData).filter(SensorData.name == name, SensorData.timestamp >= start_dt, SensorData.timestamp <= end_dt).all()
    return result

def save_data_to_csv(data, filename='output.csv'):
    sensor_name = data[0].name

    data_dict = {
        'id': [d.id for d in data],
        'timestamp': [d.timestamp for d in data],
        'depth': [d.depth for d in data],
    }
    df = pd.DataFrame(data_dict)
    csv_data = df.to_csv(index=False)

    # Add the sensor name at the beginning
    sensor_name_line = f"Sensor Name: {sensor_name}\n"
    csv_data = sensor_name_line + csv_data

    return csv_data

def get_unique_sensor_names():
    unique_names = db.session.query(distinct(SensorData.name)).all()
    return [name[0] for name in unique_names] #result is a tuple with only the first entry filled. Hence name[0] is used to extract each unique name.
