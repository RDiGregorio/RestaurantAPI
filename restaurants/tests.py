from django.test import TestCase
from restaurants.models import Restaurant

class OpenRestaurantsTestCase(TestCase):
    def setUp(self):
        Restaurant.objects.create(name="Restaurant A", hours="Monday 09:00-17:00;Tuesday 10:00-16:00")
        Restaurant.objects.create(name="Restaurant B", hours="Wednesday 11:00-14:00")
        Restaurant.objects.create(name="Restaurant C", hours="Monday-Friday 08:00-18:00")

    def test_open_restaurants(self):
        response = self.client.get('/api/open-restaurants/', {'datetime': '2025-04-09 10:00:00'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['open_restaurants'], ["Restaurant C"])