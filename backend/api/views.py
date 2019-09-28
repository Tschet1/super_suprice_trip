from django.http import JsonResponse
from time_map.time_travel_map import get_travel_time, Coordinates
from datetime import datetime
from urllib.parse import unquote
from location.models import Location, LocationKind
from events.models import Event, EventCategory
from scoring.get_cost import get_cost
from location.models import Location
from events.models import Event
from sbb.sbb import get_prize_info_with_depart_time, get_prize_info_with_arrival_time
from google_maps.get_place_from_placeId import get_place_from_placeId
from time_map.time_travel_map import Coordinates
import get_categories_guidle
import logging

def surprise_me(request):
    logger = logging.getLogger('logger')

    # collect information from the request
    place_id = request.GET.get('location', None)
    if place_id is None:
        return JsonResponse({"success": False, "error": "location needs to be set"})

    address, coordinates = get_place_from_placeId(place_id)
    logger.error('address {}, coordinates {}'.format(address, coordinates))

    datetime_start = request.GET.get('startDT', None)
    datetime_end = request.GET.get('endDT', None)

    if datetime_end is None or datetime_start is None:
        return JsonResponse({"success": False, "error": "time needs to be set"})

    try:
        datetime_start = datetime.fromisoformat(unquote(datetime_start))
    except AttributeError as error:
        return JsonResponse({"success": False, "error": "invalide departure query parameter"})

    try:
        datetime_end = datetime.fromisoformat(unquote(datetime_end))
    except AttributeError as error:
        return JsonResponse({"success": False, "error": "invalide departure query parameter"})

    if datetime_end < datetime_start:
        return JsonResponse({"success": False, "error": "make sure the end is before the start"})

    # get the total time that we have available in minutes
    total_time_budget_minutes = (datetime_end - datetime_start).seconds // 60

    # we define a maximum of 25% of the time available for travelling per way
    max_travel_time_min = total_time_budget_minutes // 4

    logger.error('Coordinates {}, time start {}, travel time {}'.format(coordinates, datetime_start, max_travel_time_min*60))

    # get reachable area
    travel_time_area = get_travel_time(
        departure_time=datetime_start,
        max_travel_time_sec=max_travel_time_min * 60,
        coordinates=coordinates
    )

    # find locations in reachable area
    locations = Location.objects.filter(coordinates__within=travel_time_area)
    events = Event.objects.filter(coordinates__within=travel_time_area)


    logger.error('Found {} locations and {} events'.format(locations, events))

    # the more information we get from the user, the better we are able to score the results
    activity_score = request.GET.get('activity_score', 0.5)
    social_score = request.GET.get('social_score', 0.5)
    budget = request.GET.get('budget', None)

    # TODO: add traveltime to cost

    for event in events:
        connections_there = get_prize_info_with_depart_time(address, event.venue_name, datetime_start)
        connections_back = get_prize_info_with_depart_time(address, event.venue_name, datetime_start)
        # TODO: select connection
        selected_connection_there = connections_there[0]
        selected_connection_back = connections_back[0]

        price = selected_connection_there[1] + selected_connection_back[1]
        is_supersaver = selected_connection_there[2] or selected_connection_back[2]

        category = get_categories_guidle.get_categories(events.id)

        score = get_cost(
            weights=[
                activity_score,
                social_score
            ],
            event_category=category,
            price=price,
            price_limit=budget,
            superprice_flag=is_supersaver
        )

        print(score)

    # TODO: add place label
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

# ?location=ChIJGaK-SZcLkEcRA9wf5_GNbuY&startDT=2019-09-30t12:00&endDT=2019-09-30t16:00&