from django.db import models
from restaurants.utils import time_range_to_dates, expand_date_range, time_range, date_ranges, start_date, end_date

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    hours = models.TextField()

    def __str__(self):
        return self.name

    def schedule(self):
        result = {}
        fragments = self.hours.split('/')
        
        for fragment in fragments:
            for date_range in date_ranges(fragment):
                for day in expand_date_range(date_range):
                    result[day] = time_range(fragment)
        
        return result

    def contains_date(self, date):
        schedule = self.schedule()

        if date.strftime('%a') not in schedule:
            return False

        start_time = start_date(schedule[date.strftime('%a')]).time()
        end_time = end_date(schedule[date.strftime('%a')]).time()
        return start_time <= date.time() <= end_time