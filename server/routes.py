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
        depth = sensor_data['hotspots'][0]['distance']
        unix_time_data = sensor_data['decoded']['payload']['timestamp']
        timestamp = datetime.utcfromtimestamp(unix_time_data).strftime('%Y-%m-%dT%H:%M:%S')

        new_data = SensorData(
            name = name,
            timestamp=timestamp,
            depth=depth,
        )
        db.session.add(new_data)
        db.session.commit()

        return jsonify({'message': 'Data received and broadcasted.'}), 200

    @server.route('/eventsource')
    def eventsource():
        def generate():
            with server.app_context():
                while True:
                    data = db.session.query(SensorData).filter(
                                SensorData.timestamp >= datetime.utcnow() - timedelta(days=2)
                            ).all()
                    data_json = [
                        {
                            "name":d.name,
                            "timestamp": d.timestamp.strftime('%Y-%m-%dT%H:%M:%S'),
                            "depth": d.depth
                        } for d in data
                    ]
                    time.sleep(5)
                    yield f"data: {json.dumps(data_json)}\n\n"
        return Response(generate(), mimetype='text/event-stream')



