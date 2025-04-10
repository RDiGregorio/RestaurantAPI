from django.test import TestCase
from datetime import datetime
from restaurants.models import Restaurant
from restaurants.utils import time_range_to_dates
from restaurants.utils import expand_date_range
from restaurants.utils import time_range
from restaurants.utils import date_ranges
from restaurants.utils import start_date
from restaurants.utils import end_date

class OpenRestaurantsTestCase(TestCase):
    def setUp(self):
        Restaurant.objects.create(name="Restaurant A", hours="Mon-Fri, Sat 11 am - 12 pm  / Sun 11 am - 10 pm")
        Restaurant.objects.create(name="Restaurant B", hours="Mon-Fri, Sat 12 pm - 9 pm  / Sun 11 am - 10 pm")

    def test_open_restaurants(self):
        # Wednesday
        response = self.client.get('/api/open-restaurants/', {'datetime': '2025-04-09 11:00:00'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['open_restaurants'], ["Restaurant A"])

    def test_open_restaurants_failure(self):
        response = self.client.get('/api/open-restaurants/', {'datetime': 'bad date'})
        self.assertEqual(response.status_code, 400)

class RestaurantModelTestCase(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(name="Test Restaurant", hours="Mon-Fri 11 am - 12:30 pm / Sat 1 pm - 2 pm")

    def test_schedule(self):
        expected_schedule = {
            "Mon": "11 am - 12:30 pm",
            "Tue": "11 am - 12:30 pm",
            "Wed": "11 am - 12:30 pm",
            "Thu": "11 am - 12:30 pm",
            "Fri": "11 am - 12:30 pm",
            "Sat": "1 pm - 2 pm"
        }
        self.assertEqual(self.restaurant.schedule(), expected_schedule)

    def test_contains_date(self):
        # Monday
        self.assertTrue(self.restaurant.contains_date(datetime(1900, 1, 1, 11, 0)))
        self.assertFalse(self.restaurant.contains_date(datetime(1900, 1, 1, 13, 0)))
        # Saturday
        self.assertTrue(self.restaurant.contains_date(datetime(1900, 1, 6, 13, 0)))
        # Sunday
        self.assertFalse(self.restaurant.contains_date(datetime(1900, 1, 7, 11, 0)))
        self.assertFalse(self.restaurant.contains_date(datetime(1900, 1, 7, 13, 0)))

class UtilTestCase(TestCase):
    def test_time_range_to_dates(self):
        self.assertEqual(time_range_to_dates("11 am - 1:30 pm")[0].time(), datetime(1900, 1, 1, 11, 0).time())
        self.assertEqual(time_range_to_dates("11 am - 1:30 pm")[1].time(), datetime(1900, 1, 1, 13, 30).time())

    def test_expand_date_range(self):
        self.assertEqual(expand_date_range("Mon-Tue"), ["Mon", "Tue"])
        self.assertEqual(expand_date_range("Mon-Wed"), ["Mon", "Tue", "Wed"])
        self.assertEqual(expand_date_range("Wed-Sun"), ["Wed", "Thu", "Fri", "Sat", "Sun"])
        self.assertEqual(expand_date_range("Mon"), ["Mon"])

    def test_time_range(self):
        self.assertEqual(time_range("Mon-Fri, Sat 11 am - 12:30 pm"), "11 am - 12:30 pm")
        self.assertEqual(time_range("Sun 11 am - 10 pm"), "11 am - 10 pm")

    def test_date_ranges(self):
        self.assertEqual(date_ranges("Mon-Fri, Sat 11 am - 12:30 pm"), ["Mon-Fri", "Sat"])
        self.assertEqual(date_ranges("Sun 11 am - 10 pm"), ["Sun"])
        self.assertEqual(date_ranges("Mon"), ["Mon"])

    def test_start_date(self):
        self.assertEqual(start_date("11 am - 10 pm").time(), datetime(1900, 1, 1, 11, 0).time())
    
    def test_end_date(self):
        self.assertEqual(end_date("11 am - 10:30 pm").time(), datetime(1900, 1, 1, 22, 30).time())