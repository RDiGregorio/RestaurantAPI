import csv
from django.core.management.base import BaseCommand
from restaurants.models import Restaurant

class Command(BaseCommand):
    help = 'Load restaurant data from a CSV file'

    def handle(self, *args, **kwargs):
        with open('restaurants.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Restaurant.objects.create(name=row['Restaurant Name'], hours=row['Hours'])
        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
