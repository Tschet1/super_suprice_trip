from django.core.management.base import BaseCommand
from location.models import Location
from time_map.time_travel_map import get_travel_time, Coordinates
from datetime import datetime

class Command(BaseCommand):
    def handle(self, *args, **options):
        polygon = get_travel_time(datetime.now(), 90, Coordinates(lat=47.0568, long=8.2771))
        print(Location.objects.filter(coordinates__within=polygon))

        
