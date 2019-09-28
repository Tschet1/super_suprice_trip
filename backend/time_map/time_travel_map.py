import requests
import json
from datetime import datetime
import os
from collections import namedtuple
from django.contrib.gis.geos import Polygon, LinearRing

Coordinates = namedtuple('Coordinates', ['long', 'lat'])

def get_travel_time(departure_time, max_travel_time_min, coordinates):
    url = "http://api.traveltimeapp.com/v4/time-map"
    payload = json.dumps({
        "departure_searches": [{
            'id': 'start',
            'coords': {
                'lat': coordinates.lat,
                'lng': coordinates.long
            },
            'transportation': {
                'type': 'public_transport'
            },
            'departure_time': departure_time.isoformat(),
            'travel_time': max_travel_time_min,
        }],
        'arrival_searches': []
    })

    headers = {
        'Content-Type': "application/json",
        'X-Application-Id': os.environ['TRAVEL_TIME_APP_ID'],
        'X-Api-Key': os.environ['TRAVEL_TIME_API_KEY'],
        'Accept': "application/json",
        'Cache-Control': "no-cache",
        'Host': "api.traveltimeapp.com",
        'Accept-Encoding': "gzip, deflate",
        'Content-Length': "259",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    res = json.loads(response.text)
    shape = res['results'][0]['shapes'][0]
    ext_coords = LinearRing([(point['lng'], point['lat']) for point in shape['shell']])
    int_coords = LinearRing([(point['lng'], point['lat']) for point in shape['holes']])
    return Polygon(ext_coords) 





