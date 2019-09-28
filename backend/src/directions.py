import requests
import dotenv
import os
import time

dotenv.load_dotenv()


def get_route_from_to(origin, destination, arrival_time=None, departure_time=None):
    if arrival_time is None and departure_time is None:
        raise Exception('Define start arrival time or departure time')

    if arrival_time is not None and type(arrival_time) is not int or \
            departure_time is not None and type(departure_time) is not int:
        raise ValueError('Please give a timestamp as departure or arrival time')

    url = "https://maps.googleapis.com/maps/api/directions/json"

    querystring = {
        "origin": origin,
        "destination": destination,
        "key": os.environ['GOOGLE_MAPS_API_KEY']}

    headers = {
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Host': "maps.googleapis.com",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)

if __name__ == '__main__':
    get_route_from_to('zug', 'zürich', departure_time=round(time.time()))