from django.db import models
from restaurants.utils import time_range_to_dates, expand_date_range, time_range, date_ranges, start_date, end_date

# Represents a restaurant with a name and operating hours.
class Restaurant(models.Model):

    # The name of the restaurant.
    name = models.CharField(max_length=255)

    # A textual representation of the restaurant's operating hours.
    hours = models.TextField()

    def __str__(self):
        return self.name

    # Parses the operating hours and returns a dictionary mapping days of the week
    # to their respective time ranges.
    def schedule(self):
        result = {}
        fragments = self.hours.split('/')
        
        for fragment in fragments:
            for date_range in date_ranges(fragment):
                for day in expand_date_range(date_range):
                    result[day] = time_range(fragment)
        
        return result

    # Checks if the restaurant is open at a specific datetime.
    def contains_date(self, date):
        schedule = self.schedule()

        if date.strftime('%a') not in schedule:
            return False

        start_time = start_date(schedule[date.strftime('%a')]).time()
        end_time = end_date(schedule[date.strftime('%a')]).time()
        return start_time <= date.time() <= end_time