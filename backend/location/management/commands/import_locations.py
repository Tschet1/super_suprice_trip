from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from location.models import Location, LocationKind
import json

def load_geojson(path):
    with open(path, "r") as file:
        data = json.load(file)

    for feature in data["features"]:
        feature_id = feature["properties"]["xid"]
        feature_name = feature["properties"]["name"]
        feature_coordinate = feature["geometry"]["coordinates"]
        kinds = feature["properties"]["kinds"].split(",")
        kinds = [LocationKind.objects.get_or_create(name=kind)[0] for kind in kinds]
        location, _ = Location.objects.get_or_create(id=feature_id)
        location.name=feature_name[0:100]
        location.coordinates=Point(feature_coordinate[0], feature_coordinate[1])
        location.save()
        location.kinds.set(kinds)

class Command(BaseCommand):
    def handle(self, *args, **options):
        load_geojson("data/opentripmap/amusement.geojson")
        load_geojson("data/opentripmap/architecture.geojson")
        load_geojson("data/opentripmap/cultural.geojson")
        load_geojson("data/opentripmap/historical.geojson")
        load_geojson("data/opentripmap/natural.geojson")
        load_geojson("data/opentripmap/welness.geojson")