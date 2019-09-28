import requests
import json
from datetime import datetime

def get_travel_time(departure_time, max_travel_time_min, lat, long):
    url = "http://api.traveltimeapp.com/v4/time-map"
    payload = json.dumps({
        "departure_searches": [{
            'id': 'start',
            'coords': {
                'lat': lat,
                'lng': long
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
        'X-Application-Id': "###",
        'X-Api-Key': "###",
        'Accept': "application/json",
        'Cache-Control': "no-cache",
        'Host': "api.traveltimeapp.com",
        'Accept-Encoding': "gzip, deflate",
        'Content-Length': "259",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)

if __name__ == '__main__':
    get_travel_time(datetime.now(), 90, 47.166168, 8.515495)
