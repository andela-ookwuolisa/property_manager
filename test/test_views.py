import os
import json
from unittest import TestCase
from app import my_app, create_db, drop_db
from app.views import *


class TestLogin(TestCase):
    def setUp(self):
        create_db()
        self.app = my_app.test_client()

    def tearDown(self):
        drop_db()

    def test_landing_page(self):
        response = self.app.get("/")
        data = response.data.decode()
        data = json.loads(data)
        self.assertEqual("Welcome to property manager API", data["data"])

    def test_properties_route_without_login(self):
        response = self.app.get("/properties")
        data = response.data.decode()
        self.assertIn("This route requires login", data)
        self.assertEqual(response.status_code, 401)

    def test_properties_route_with_login(self):
        self.app.post(
            "/register",
            data={
                "first_name": "Fred",
                "last_name": "Shizkov",
                "username": "stable",
                "password": "simplekey",
            },
        )
        self.app.post("/login", data={"username": "stable", "password": "simplekey"})
        response = self.app.get("/properties")
        data = response.data.decode()
        self.assertIn("success", data)
        self.assertEqual(response.status_code, 200)


class TestProperty(TestCase):
    def setUp(self):
        create_db()
        os.environ["FLASK_ENV"] = "testing"
        self.app = my_app.test_client()

        self.app.post(
            "/register",
            data={
                "first_name": "Fred",
                "last_name": "Shizkov",
                "username": "stable",
                "password": "simplekey",
            },
        )
        self.app.post("/login", data={"username": "stable", "password": "simplekey"})

    def tearDown(self):
        drop_db()

    def test_property_is_empty(self):
        response = self.app.get("/properties")
        data = response.data.decode()
        data = json.loads(data)
        self.assertEqual([], data["properties"])

    def test_property_post_request(self):
        self.app.post("/owner", data={"user_id": 1})
        response = self.app.post(
            "/properties",
            data={
                "owner_id": 1,
                "property_type": "Apartment",
                "property_name": "Freds",
                "location": "Lagos",
            },
        )
        data = response.data.decode()
        data = json.loads(data)
        self.assertEqual("Apartment", data["properties"]["property_type"])
        self.assertEqual(response.status_code, 201)

    def test_property_post_request_with_wrong_data(self):
        self.app.post("/owner", data={"user_id": 1})
        response = self.app.post(
            "/properties",
            data={
                "owner_id": 100,
                "property_type": "Apartment",
                "property_name": "Freds",
                "location": "Lagos",
            },
        )
        data = response.data.decode()
        data = json.loads(data)
        self.assertEqual("error", data["message"])
        self.assertEqual(response.status_code, 400)
