from flask import request, jsonify, Response
from datetime import datetime, timedelta
from .models import SensorData
from .database import db
import json
import time

def setup_routes(server):
    @server.route('/receive_data', methods=['POST'])
    def receive_data():
        sensor_data = request.json
        name = sensor_data["name"]
        tide = sensor_data['hotspots'][0]['distance']
        unix_time_data = sensor_data['decoded']['payload']['timestamp']
        timestamp = datetime.utcfromtimestamp(unix_time_data).strftime('%Y-%m-%dT%H:%M:%S')

        new_data = SensorData(
            name = name,
            timestamp=timestamp,
            tide=tide,
        )
        db.session.add(new_data)
        db.session.commit()

        return jsonify({'message': 'Data received and broadcasted.'}), 200



