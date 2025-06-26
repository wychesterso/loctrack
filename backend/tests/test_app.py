import unittest
import json
from app import app

class LocTrackTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_home(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"LocTrack", response.data)

    def test_post_location_valid(self):
        payload = {"lat": 51.5, "lng": -0.1}
        response = self.client.post("/location",
                data = json.dumps(payload),
                content_type = "application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("status", response.get_json())

    def test_post_location_missing_data(self):
        response = self.client.post("/location",
                data = json.dumps({}),
                content_type = "application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_get_locations(self):
        self.client.post("/location",
                data = json.dumps({"lat": 1.1, "lng": 2.2}),
                content_type = "application/json"
        )

        response = self.client.get("/locations")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

if __name__ == "__main__":
    unittest.main()
