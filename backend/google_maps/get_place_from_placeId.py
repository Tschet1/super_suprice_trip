import requests
import os
import json
from time_map.time_travel_map import Coordinates

def get_place_from_placeId(placeId):
    url = "https://maps.googleapis.com/maps/api/place/details/json"

    querystring = {
        "placeid": placeId,
        "key": os.environ['GOOGLE_MAPS_API_KEY'],
    }

    headers = {
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    response = json.loads(response.text)
    return response['result']['formatted_address'], \
           Coordinates(
               lat=response['result']['geometry']['location']['lat'],
               long=response['result']['geometry']['location']['lng']
           )


if __name__ == '__main__':
    import dotenv
    dotenv.load_dotenv()
    print(get_place_from_placeId('ChIJrTLr-GyuEmsRBfy61i59si0'))