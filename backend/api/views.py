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
from random import shuffle
from api.preferences_filter import preferences_filter_for_events, WeightedEvent
import time
from multiprocessing import dummy


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

    # the more information we get from the user, the better we are able to score the results
    activity_score = int(request.GET.get('activity_score', 50)) / 100
    social_score = int(request.GET.get('social_score', 50)) / 100
    budget = int(request.GET.get('budget', 100))

    # get the total time that we have available in minutes
    total_time_budget_minutes = (datetime_end - datetime_start).seconds // 60

    # we define a maximum of 25% of the time available for travelling per way
    max_travel_time_min = max(15, total_time_budget_minutes // 4)

    logger.error('Coordinates {}, time start {}, travel time {}'.format(coordinates, datetime_start, max_travel_time_min*60))

    # get reachable area
    get_travel_time_start = time.time()
    travel_time_area = get_travel_time(
        departure_time=datetime_start,
        max_travel_time_sec=max_travel_time_min * 60,
        coordinates=coordinates
    )
    get_travel_time_duration = time.time() - get_travel_time_start

    # find locations in reachable area
    #locations = Location.objects.filter(coordinates__within=travel_time_area)
    load_events_start = time.time()
    events_in_the_area = Event.objects.prefetch_related("categories").filter(coordinates__within=travel_time_area)
    load_events_duration = time.time() - load_events_start


    logger.error('Found {} locations and {} events'.format(0, len(events_in_the_area)))

    filter_prefered_start = time.time()
    prefered_events = preferences_filter_for_events(events_in_the_area, { "activity_score": activity_score, "social_score": social_score}, 20)
    filter_prefered_duration = time.time() - filter_prefered_start
    
    filter_budget_start = time.time()
    best_priced_events = budget_filter_for_events(prefered_events, budget, address, datetime_start, datetime_end, 10)
    filter_budget_duration = time.time() - filter_budget_start

    logger.error(f"get_travel_time_duration: {get_travel_time_duration}")
    logger.error(f"load_events_duration: {load_events_duration}")
    logger.error(f"filter_prefered_duration: {filter_prefered_duration}")
    logger.error(f"filter_budget_duration: {filter_budget_duration}")

    # TODO: add place label
    return JsonResponse({
            "success":True, 
            "results": [
                {
                    "type": "event",
                    "name": weighted_event.event.event_name,
                    "price": weighted_event.cost
                } for weighted_event in best_priced_events
            ],
        }, 
        safe=False, 
        json_dumps_params={"ensure_ascii": False}
    )

def budget_filter_for_events(events, budget, address, datetime_start, datetime_end, max_results):
    pool = dummy.Pool(20)
    def wheight_event(event):
        trip_to_event = get_prize_info_with_depart_time(address, event.event.venue_name, datetime_start)
        trip_from_event = get_prize_info_with_depart_time(event.event.venue_name, address, datetime_end)
        if trip_to_event and trip_from_event:
            cost = trip_to_event.price + trip_from_event.price
            return WeightedEvent(event.event, event.preference_score, cost)

    weighted_events=filter(lambda weighted_event: weighted_event is not None, pool.map(wheight_event, events))

    filtered_weighted_events = filter(lambda weighted_event: weighted_event.cost <= budget, weighted_events)
    sorted_weighted_events = sorted(filtered_weighted_events, key=lambda weighted_event: weighted_event.cost * (1-weighted_event.preference_score))

    return sorted_weighted_events[0:max_results]

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