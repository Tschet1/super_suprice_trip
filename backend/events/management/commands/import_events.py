from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from events.models import Event, EventCategory
import json

class Command(BaseCommand):
    def handle(self, *args, **options):
        with open("data/guidle/category.json", "r") as file:
            categories = json.load(file)

        for category in categories:
            category_id = category["category_id"]
            category_name = category["title_en"]
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
            event_name = event["title_en"][0:100]
            event_venue = event["address_venue_name"][0:100]
            coordinates = Point(event["address_longitude"], event["address_latitude"])

            event, _ = Event.objects.get_or_create(id=event_id)
            event.event_name = event_name
            event.venue_name = event_venue
            event.date = event_date
            event.start_time = start_time
            event.end_time = end_time
            event.coordinates=coordinates
            event.save()

        with open("data/guidle/event_category.json", "r") as file:
            mappings = json.load(file)

        for mapping in mappings:
            event, _ = Event.objects.get_or_create(id=mapping["event_id"])
            category, _ = EventCategory.objects.get_or_create(id=mapping["category_id"])

            event.categories.add(category)