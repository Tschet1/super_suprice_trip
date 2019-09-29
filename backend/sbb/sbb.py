import requests
#import dotenv
import os
import time
import json
import datetime
import logging
from typing import NamedTuple
from funcy import cache, log_durations, retry, ignore, log_errors
from datetime import timedelta

@cache(timeout=timedelta(minutes=15))
def _login():
    url = "https://sso-int.sbb.ch/auth/realms/SBB_Public/protocol/openid-connect/token"

    payload = {
        'grant_type': 'client_credentials',
        'client_id': os.environ['SBB_CLIENT_ID'],
        'client_secret': os.environ['SBB_CLIENT_SECRET']
    }
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Host': "sso-int.sbb.ch",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    if response.status_code == 200:
        return json.loads(response.text)['access_token']

@cache(timeout=timedelta(minutes=15), key_func=lambda src_id, dst_id, header, arrival=None, departure=None: (src_id, dst_id, arrival, departure,))
def _get_trips_by_departure_or_arrival(src_id, dst_id, header, arrival=None, departure=None):
    url = 'https://b2p-int.api.sbb.ch/api/trips'

    if (arrival is None and departure is None) or (arrival is not None and departure is not None):
        raise Exception('set earliest departure OR latest arrival')

    if arrival is not None:
        sc = 'LA'
        date = arrival
    else:
        sc = 'ED'
        date = departure

    # TODO: maybe add vias
    params = {
        'originId': src_id,
        'destinationId': dst_id,
        'date': date.strftime("%Y-%m-%d"),
        'time': date.strftime("%H:%M"),
        'passengers': ' paxa;42;half-fare',
        'arrivalDeparture': sc,
    }

    response = requests.request("GET", url, headers=header, params=params)
    if response.status_code == 200:
        response = json.loads(response.text)
        return [trip['tripId'] for trip in response]



class Trip(NamedTuple):
    id: str
    price: int
    is_supersaver: bool

@cache(timeout=timedelta(minutes=15), key_func=lambda tripId, headers: tripId)
def _get_trip_cost(tripId, headers):
    url = 'https://b2p-int.api.sbb.ch/api/v2/prices'

    params = {
        'passengers': 'paxa;42;half-fare', #TODO: make this dynamic
        'tripIds': tripId,
    }

    response = requests.request("GET", url, headers=headers, params=params)
    if response.status_code == 200:
        response = json.loads(response.text)
        
        trips = [
            Trip(
                trip['tripId'], 
                trip['price']/100., 
                trip['productId'] == 4004
            )  for trip in response if "status" not in response
        ]
        if trips:
            return min(trips, key=lambda trip: trip.price)

uid_cache = {}

@cache(timeout=timedelta(minutes=15), key_func=lambda location, headers: location)
def _get_uid(location, headers):
    if location in uid_cache:
        return uid_cache[location]
    url = 'https://b2p-int.api.sbb.ch/api/locations?name={}'.format(location)
    response = requests.request("GET", url, headers=headers)

    if response.status_code == 200:
        uid = json.loads(response.text)[0]['id']
        uid_cache[location] = uid
        return uid


def _get_trips_start(src_id, dst_id, date, headers):
    headers_new = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Accept-Encoding': "gzip, deflate",
        'cache-control': "no-cache",
        'X-Contract-Id': headers['X-Contract-Id'],
        'Authorization': headers['Authorization'],
        'X-Conversation-Id': headers['X-Conversation-Id'],
        'Accept-Language': 'en',
    }

    params = {
        'originId': src_id,
        'destinationId': dst_id,
        'date': date.strftime("%Y-%m-%d"),
        'time': date.strftime("%H:%M"),
        'passengers': ' paxa;42;half-fare' #TODO: check if user has halbtax
    }

    url = 'https://b2p-int.api.sbb.ch/api/route-offers'
    response = requests.request("GET", url, headers=headers_new, params=params)
    if response.status_code == 200:
        return [(trip['offers'][0]['offerId'], trip['totalPrice'], trip['offers'][0]['productId'] == 4004) for trip in json.loads(response.text) if len(trip['offers']) > 0 and not trip['offers'][0]['direction'] == 'round']


def _get_trips_arrival(src_id, dst_id, date, headers):
    headers_new = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Accept-Encoding': "gzip, deflate",
        'cache-control': "no-cache",
        'X-Contract-Id': headers['X-Contract-Id'],
        'Authorization': headers['Authorization'],
        'X-Conversation-Id': headers['X-Conversation-Id'],
        'Accept-Language': 'en',
    }


    params = {
        'originId': src_id,
        'destinationId': dst_id,
        'date': date.strftime("%Y-%m-%d"),
        'time': date.strftime("%H:%M"),
        'passengers': ' paxa;42;half-fare'
    }

    url = 'https://b2p-int.api.sbb.ch/api/route-offers'
    response = requests.request("GET", url, headers=headers_new, params=params)
    
    if response.status_code == 200:
        return [(trip['offers'][0]['offerId'], trip['totalPrice'], trip['offers'][0]['productId'] == 125) for trip in json.loads(response.text) if len(trip['offers']) > 0 and not trip['offers'][0]['direction'] == 'round']


def get_prize_info_with_depart_time(start_loc, end_loc, start_time):
    return get_prize_info(start_loc, end_loc, departure=start_time)

def get_prize_info_with_arrival_time(start_loc, end_loc, arrival_time):
    return get_prize_info(start_loc, end_loc, arrival=arrival_time)

def get_prize_info(start_loc, end_loc, **kwargs):
    token = _login()

    headers = {
        'X-Contract-Id': os.environ['SBB_CONTRACT_ID'],
        'Accept': 'application/json',
        'Cache-Control': 'no-cache',
        'Authorization': 'Bearer {}'.format(token),
        'X-Conversation-Id': 'e5eeb775-1e0e-4f89-923d-afa780ef844b',  # TODO: find a way to set this
    }

    # get UIDs
    start_id = _get_uid(start_loc, headers)
    dst_id = _get_uid(end_loc, headers)

    # get trips
    trip_ids = _get_trips_by_departure_or_arrival(start_id, dst_id, headers, **kwargs)

    if trip_ids:
        # get costs
        costs = [_get_trip_cost(trip_id, headers) for trip_id in trip_ids]
        costs = [cost for cost in costs if cost is not None]
        if costs:
            return min(costs)



if __name__ == "__main__":
    #print(get_prize_info_with_depart_time('47.166168,8.515495', 'Zürich HB', datetime.datetime.now() + datetime.timedelta(hours=2)))
    print(get_prize_info_with_arrival_time('Zug', 'Zürich HB', datetime.datetime.now() + datetime.timedelta(hours=5)))

