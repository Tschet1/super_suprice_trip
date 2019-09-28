from time_map.time_travel_map import Coordinates
from google_maps.directions import get_route_from_to
import datetime

def find_nearest_station_name(coordinates: Coordinates):
    res = get_route_from_to(coordinates, "Olten", departure_time=round(datetime.datetime.now().timestamp()))
    for step in res['routes'][0]['legs'][0]['steps']:
        if step['travel_mode'] == 'TRANSIT':
            return step['transit_details']['departure_stop']['name']

if __name__ == '__main__':
    import dotenv
    dotenv.load_dotenv()
    print(find_nearest_station_name(Coordinates(long=47.166507, lat=8.522576)))