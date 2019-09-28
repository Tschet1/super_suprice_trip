import requests
import json
from datetime import datetime
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import os
import dotenv
from collections import namedtuple
dotenv.load_dotenv()

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

    return [Polygon(
        shell=[Coordinates(long=point['lng'], lat=point['lat']) for point in shape['shell']],
        holes=[(point['lat'], point['lng']) for point in shape['holes']],
    ) for shape in res['results'][0]['shapes']]

def is_point_in_shape(shape, coordinates):
    return shape.contains(Point(coordinates.long, coordinates.lat))

if __name__ == '__main__':
    coordinates_zug = Coordinates(lat=47.166168, long=8.515495)
    coordinates_zurich = Coordinates(lat=47.36667, long=8.55)

    time_distance = get_travel_time(datetime.now(), 90, coordinates_zug)[0]

    print(is_point_in_shape(time_distance, coordinates_zug))
    print(is_point_in_shape(time_distance, coordinates_zurich))





