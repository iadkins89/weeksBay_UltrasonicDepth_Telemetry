from flask import request, jsonify
from datetime import datetime
import pytz
from .models import SensorData
from .database import db

def setup_routes(server):
    @server.route('/receive_data', methods=['POST'])
    def receive_data():
        sensor_data = request.json
        name = sensor_data['deviceInfo']["deviceName"]
        tide = sensor_data['object']['distance']
        unix_timestamp = sensor_data['object']['timestamp']
        battery = sensor_data['object']['battery']


        # Set timezone to Central Time
        #central_tz = pytz.timezone('America/Chicago')
        #timestamp = datetime.fromtimestamp(unix_timestamp, central_tz).strftime('%Y-%m-%dT%H:%M:%S')

        # Convert Unix timestamp directly to local datetime without further timezone conversion
        local_dt = datetime.fromtimestamp(unix_timestamp)

        # Format the timestamp in the desired format
        timestamp = local_dt.strftime('%Y-%m-%dT%H:%M:%S')

        #NAVDD88 adjustment
        tide = round(1.291 - tide, 3)

        new_data = SensorData(
            name = name,
            timestamp=timestamp,
            tide=tide,
            battery=battery,
        )
        db.session.add(new_data)
        db.session.commit()

        return jsonify({'message': 'Data received and broadcasted.'}), 200



