from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///locations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/locations', methods=['POST'])
def add_location():
    data = request.get_json()
    if not data or not 'latitude' in data or not 'longitude' in data:
        return jsonify({"error": "Invalid data"}), 400
    
    new_location = Location(
        latitude=data['latitude'],
        longitude=data['longitude']
    )
    
    db.session.add(new_location)
    db.session.commit()
    
    return jsonify({"message": "Location added successfully"}), 201

@app.route('/locations', methods=['GET'])
def get_locations():
    locations = Location.query.all()
    result = []
    for location in locations:
        result.append({
            'id': location.id,
            'latitude': location.latitude,
            'longitude': location.longitude,
            'timestamp': location.timestamp
        })
    return jsonify(result), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
