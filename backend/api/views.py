from django.http import JsonResponse
from time_map.time_travel_map import get_travel_time, Coordinates
from datetime import datetime
from urllib.parse import unquote

from location.models import Location, LocationKind
from events.models import Event, EventCategory

def surprise_me(request):
    if "lat" not in request.GET or "long" not in request.GET:
        return JsonResponse({"success": False, "error": "lat and long query parameter needs to be set"})

    if "departure" not in request.GET:
        return JsonResponse({"success": False, "error": "departure query parameter needs to be set"})

    try:
        departure_time = datetime.fromisoformat(unquote(request.GET["departure"]))
    except AttributeError as error:
        return JsonResponse({"success": False, "error": "invalide departure query parameter"})

    coordinates = Coordinates(lat=float(request.GET["lat"]), long=float(request.GET["long"]))

    travel_time_area = get_travel_time(
        departure_time=departure_time, 
        max_travel_time_sec=3600, 
        coordinates=coordinates
    )

    locations = Location.objects.filter(coordinates__within=travel_time_area)
    events = Event.objects.filter(coordinates__within=travel_time_area)
    
    return JsonResponse({
            "success":True, 
            "results": [
                {
                    "type": "location",
                    "name": location.name
                } for location in locations
            ]+[
                {
                    "type": "event",
                    "name": event.event_name
                } for event in events
            ],
        }, 
        safe=False, 
        json_dumps_params={"ensure_ascii": False}
    )

def le_preferences(request):
    kinds = LocationKind.objects.all()
    categories = EventCategory.objects.filter(parent=None)
    return JsonResponse({
        "success":True,
        "preferences": [
            {
                "id": kind.name,
                "name": kind.name.replace("_", " ").title()
            } for kind in kinds
            
        ] + [
            {
                "id": str(category.id),
                "name": category.name
            } for category in categories
        ]
        },
        safe=False, 
        json_dumps_params={"ensure_ascii": False}
    )