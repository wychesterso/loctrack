import pytest
import json
import os
from app import app, init_db

@pytest.fixture(autouse=True)
def test_client():
    os.environ["DB_PATH"] = ":memory:"
    init_db()
    with app.test_client() as client:
        yield client

def test_home(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert b"LocTrack" in response.data

def test_post_location_valid(test_client):
    payload = {"lat": 51.5, "lng": -0.1}
    response = test_client.post("/location",
            data=json.dumps(payload),
            content_type="application/json"
    )
    assert response.status_code == 201
    assert response.get_json()["status"] == "ok"

def test_post_location_missing_data(test_client):
    response = test_client.post("/location",
            data=json.dumps({}),
            content_type="application/json"
    )
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_get_locations(test_client):
    test_client.post("/location",
            data=json.dumps({"lat": 1.1, "lng": 2.2}),
            content_type="application/json"
    )
    response = test_client.get("/locations")
    data = response.get_json()
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) >= 1
