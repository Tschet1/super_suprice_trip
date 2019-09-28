import requests
import os
import time
import json
from backend.time_map.time_travel_map import Coordinates


def get_route_from_to(origin, destination, arrival_time: int = 0, departure_time: int = 0):
    if arrival_time == 0 and departure_time == 0:
        raise Exception('Define start arrival time or departure time')

    if arrival_time != 0 and departure_time != 0:
        raise Exception('Do not define start and end time')

    if type(origin) is Coordinates:
        origin = "{},{}".format(origin.long, origin.lat)

    url = "https://maps.googleapis.com/maps/api/directions/json"

    querystring = {
        "origin": origin,
        "destination": destination,
        "key": os.environ['GOOGLE_MAPS_API_KEY'],
        "mode": 'transit'
    }
    if arrival_time != 0:
        querystring['arrival_time'] = arrival_time
    else:
        querystring['departure_time'] = departure_time

    headers = {
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Host': "maps.googleapis.com",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    return json.loads(response.text)


if __name__ == '__main__':
    import dotenv

    dotenv.load_dotenv()
    print(get_route_from_to('zug', 'zürich', departure_time=round(time.time())))
