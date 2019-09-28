from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point
from location.models import Location
import json

class Command(BaseCommand):
    def handle(self, *args, **options):
        with open("data/opentripmap/welness.geojson", "r") as file:
            data = json.load(file)

        for feature in data["features"]:
            feature_id = feature["properties"]["xid"]
            feature_coordinate = feature["geometry"]["coordinates"]
            Location.objects.get_or_create(id=feature_id, coordinates=Point(*feature_coordinate))
