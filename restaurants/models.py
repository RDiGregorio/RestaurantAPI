from django.db import models
from restaurants.utils import time_range_to_dates, expand_date_range, time_range, date_ranges

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    hours = models.TextField()

    def __str__(self):
        return self.name

    def schedule(self):
        result = {}
        fragments = self.hours.split('/')
        
        for fragment in fragments:
            for day in date_ranges(fragment):
                for expanded_day in expand_date_range(day):
                    result[expanded_day] = time_range(fragment)
        
        return result

    def contains_date(datetime):
        return false