import requests
import json
from datetime import datetime
import os
from collections import namedtuple
from django.contrib.gis.geos import Polygon, LinearRing, MultiPolygon

Coordinates = namedtuple('Coordinates', ['long', 'lat'])

def get_travel_time(departure_time, max_travel_time_sec, coordinates):
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
            'travel_time': max_travel_time_sec,
        }],
        'arrival_searches': []
    })

    headers = {
        'Content-Type': "application/json",
        'X-Application-Id': os.environ['TRAVEL_TIME_APP_ID'],
        'X-Api-Key': os.environ['TRAVEL_TIME_API_KEY'],
        'Accept': "application/json",
        'Cache-Control': "no-cache",
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    res = json.loads(response.text)

    polygons = []
    for shape in res['results'][0]['shapes']:
        ext_coords = []
        for point in shape['shell']:
            ext_coords.append((point['lng'], point['lat']))
        int_coords = []
        for hole in shape['holes']:
            hol_coords = []
            for point in hole:
                hol_coords.append((point['lng'], point['lat']))
            int_coords.append(LinearRing(hol_coords))
        polygons.append(Polygon(ext_coords, *int_coords))

    multi_polygon = MultiPolygon(polygons)

    with open("data.geojson", "w") as f:
        f.write(multi_polygon.geojson)

    return multi_polygon




