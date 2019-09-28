from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from events.models import Event, EventCategory
from google_maps.find_nearest_station import find_nearest_station_name
from time_map.time_travel_map import Coordinates
import json


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open("data/guidle/category.json", "r") as file:
            categories = json.load(file)

        for category in categories:
            category_id = category["category_id"]
            category_name = category["title_de"]
            category_parent_id = category["parent_category_id"]

            category, _ = EventCategory.objects.get_or_create(id=category_id, name=category_name)
            category.parent_id = category_parent_id

            category.save()

        with open("data/guidle/event.json", "r") as file:
            events = json.load(file)

        for event in events:
            event_id = event["event_id"]
            event_date = event["date"]
            start_time = event["start_time"]
            end_time = event["end_time"]
            event_name = event["title_de"][0:100]
            event_venue = event["address_venue_name"][0:100]
            coordinates = Point(event["address_latitude"], event["address_longitude"])

            nevent, _ = Event.objects.get_or_create(id=event_id)
            nevent.event_name = event_name
            nevent.venue_name = event_venue
            nevent.date = event_date
            nevent.start_time = start_time
            nevent.end_time = end_time
            nevent.coordinates = coordinates
            nevent.nearest_public_transport = find_nearest_station_name(
                Coordinates(long=event["address_longitude"], lat=event["address_latitude"]))
            nevent.save()

        with open("data/guidle/event_category.json", "r") as file:
            mappings = json.load(file)

        for mapping in mappings:
            event, _ = Event.objects.get_or_create(id=mapping["event_id"])
            category, _ = EventCategory.objects.get_or_create(id=mapping["category_id"])

            event.categories.add(category)
