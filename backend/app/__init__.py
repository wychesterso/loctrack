import sqlite3
from flask import Flask, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)

DB_PATH = os.environ.get("DB_PATH", "data/db.sqlite3")

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lat REAL NOT NULL,
            lng REAL NOT NULL,
            timestamp TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()

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

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO locations (lat, lng, timestamp) VALUES (?, ?, ?)", (lat, lng, timestamp))
    conn.commit()
    entry_id = cur.lastrowid
    conn.close()

    return jsonify({"status": "ok", "entry": {
        "id": entry_id,
        "lat": lat,
        "lng": lng,
        "timestamp": timestamp
    }}), 201

@app.route("/locations", methods=["GET"])
def get_locations():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, lat, lng, timestamp FROM locations")
    rows = cur.fetchall()
    conn.close()

    location_data = [
            {"id": row[0], "lat": row[1], "lng": row[2], "timestamp": row[3]}
            for row in rows
    ]

    return jsonify(location_data)


init_db()

if __name__ == "__main__":
    app.run()
