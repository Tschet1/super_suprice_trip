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
    max_travel_time_min = max(15, total_time_budget_minutes // 4)

    logger.error('Coordinates {}, time start {}, travel time {}'.format(coordinates, datetime_start, max_travel_time_min*60))

    # get reachable area
    travel_time_area = get_travel_time(
        departure_time=datetime_start,
        max_travel_time_sec=max_travel_time_min * 60,
        coordinates=coordinates
    )

    # find locations in reachable area
    #locations = Location.objects.filter(coordinates__within=travel_time_area)
    events_in_the_area = Event.objects.prefetch_related("categories").filter(coordinates__within=travel_time_area)


    logger.error('Found {} locations and {} events'.format(0, len(events_in_the_area)))

    # the more information we get from the user, the better we are able to score the results
    activity_score = int(request.GET.get('activity_score', 50)) / 100
    social_score = int(request.GET.get('social_score', 50)) / 100
    budget = int(request.GET.get('budget', 100))

#    # TODO: add traveltime to cost
#    logger.error('start filter')
#    shuffle(list(events))
#    events = filter(events, address, datetime_start, datetime_end, activity_score, social_score, budget, max_results=300, with_train_info=False, threshold=100)
#
#    logger.error('done 1')
#    events = filter(events, address, datetime_start, datetime_end, activity_score, social_score, budget, max_results=10, with_train_info=True, threshold=100)
#    logger.error('done 2')
    prefered_events = preferences_filter_for_events(events_in_the_area, { "activity_score": activity_score, "social_score": social_score}, 20)
    best_priced_events = budget_filter_for_events(prefered_events, budget, address, datetime_start, datetime_end, 10)

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

#def filter(events, address, datetime_start, datetime_end, activity_score, social_score, budget, max_results=10, with_train_info=False, threshold=1):
#    logger = logging.getLogger('logger')
#    events_chosen = []
#    for event in events:
#        logger.error(len(events_chosen))
#        is_supersaver = False
#        price = 0
#        travel_duration=0
#        if with_train_info:
#            try:
#                logger.error('load')
#                connections_there = get_prize_info_with_depart_time(address, event.venue_name, datetime_start)
#                logger.error('load 1')
#                connections_back = get_prize_info_with_arrival_time(address, event.venue_name, datetime_end)
#                logger.error('load 2')
#            except Exception as e:
#                logger.error(e)
#                logger.error('skip')
#                continue
#            # TODO: select connection
#            selected_connection_there = connections_there[0]
#            selected_connection_back = connections_back[0]
#
#            price = selected_connection_there[1] + selected_connection_back[1]
#            is_supersaver = selected_connection_there[2] or selected_connection_back[2]
#            travel_duration = selected_connection_there[3] + selected_connection_back[3]
#
#        category = get_categories_guidle.get_categories(event.id)
#
#        score = get_cost(
#            weights=[
#                activity_score,
#                social_score
#            ],
#            event_category=category,
#            price=price,
#            price_limit=budget,
#            superprice_flag=is_supersaver,
#            travel_duration=travel_duration
#        )
#
#        logger.error(score)
#        if score < threshold:
#            events_chosen.append((score, event))
#        if len(events_chosen) >= max_results:
#            break
#    return [e[1] for e in sorted(events_chosen, key=lambda x:x[0])]

def budget_filter_for_events(events, budget, address, datetime_start, datetime_end, max_results):
    weighted_events = []
    for event in events:
        trip_to_event = get_prize_info_with_depart_time(address, event.event.venue_name, datetime_start)
        trip_from_event = get_prize_info_with_depart_time(event.event.venue_name, address, datetime_end)
        if trip_to_event and trip_from_event:
            cost = trip_to_event.price + trip_from_event.price
            weighted_events.append(WeightedEvent(event.event, event.preference_score, cost))

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
