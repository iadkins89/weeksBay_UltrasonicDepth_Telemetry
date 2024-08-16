from flask import request, jsonify
from datetime import datetime
import pytz
from .models import SensorData
from .database import db

def setup_routes(server):
    @server.route('/receive_data', methods=['POST'])
    def receive_data():
        sensor_data = request.json
        name = sensor_data["name"]
        tide = sensor_data['decoded']['payload']['distance']

        # Set timezone to Central Time
        central_tz = pytz.timezone('America/Chicago')
        timestamp = datetime.now(central_tz).strftime('%Y-%m-%dT%H:%M:%S')

        new_data = SensorData(
            name = name,
            timestamp=timestamp,
            tide=tide,
        )
        db.session.add(new_data)
        db.session.commit()

        return jsonify({'message': 'Data received and broadcasted.'}), 200



