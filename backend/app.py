from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# temp storage
location_data = []

@app.route("/")
def hello():
    return "Welcome to LocTrack!"

@app.route("/location", methods=["POST"])
def save_location():
    data = request.get_json()
    lat = data.get("lat")
    lng = data.get("lng")

    if lat is None or lng is None:
        return jsonify({"error": "Missing lat/lng"}), 400

    timestamp = datetime.utcnow().isoformat()
    entry = {"lat": lat, "lng": lng, "timestamp": timestamp}
    location_data.append(entry)

    return jsonify({"status": "ok", "entry": entry}), 201

@app.route("/locations", methods=["GET"])
def get_locations():
    return jsonify(location_data)
