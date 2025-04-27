import json
import os
from datetime import datetime

import requests

from instance.config import Config


def time_remaining(departure_time):
    departure_datetime = datetime.strptime(departure_time, "%I:%M %p - %d/%m/%y")
    current_datetime = datetime.now()
    time_diff = departure_datetime - current_datetime
    eta_minutes = int(time_diff.total_seconds() / 60)
    return abs(eta_minutes)


def calculate_eta(distance_km, average_speed, buffer_factor=1.5):
    eta_hours = (distance_km / 1000) / average_speed
    eta = eta_hours * buffer_factor
    return int(eta * 60)


def convert_time_format(minutes):
    minutes = int(float(minutes))
    hours = minutes // 60
    remaining_minutes = minutes % 60
    return f"{hours} hour{'s' if hours != 1 else ''} and {remaining_minutes} minute{'s' if remaining_minutes != 1 else ''}"


def get_provinces():
    file_path = os.path.join("app", "static", "provinces.json")
    with open(file_path, "r") as file:
        provinces_data = json.load(file)
    province_names = [province["name"] for province in provinces_data]
    return sorted(province_names)


def get_province_key(province_name):
    if province_name is None:
        return None

    province_path = os.path.join("app", "static", "provinces.json")
    with open(province_path, "r") as file:
        provinces_data = json.load(file)
    for province in provinces_data:
        if province["name"].lower() == province_name.lower():
            return province["key"]
    return None


def get_municipalities(province):
    province_key = get_province_key(province)

    if not province_key:
        return []

    cities_path = os.path.join("app", "static", "cities.json")
    with open(cities_path, "r") as file:
        cities_data = json.load(file)

    cities_list = []

    for city in cities_data:
        if city["province"].lower() == province_key.lower() and city["name"]:
            cities_list.append(city["name"])

    return sorted(cities_list)


# API Things


def geocode_place(place_name):
    api_key = Config.ORS_API_KEY
    url = "https://api.openrouteservice.org/geocode/search"
    headers = {"Authorization": api_key}
    params = {"text": place_name, "size": 1, "boundary.country": "PH"}

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if "features" in data and len(data["features"]) > 0:
        coordinates = data["features"][0]["geometry"]["coordinates"]
        return coordinates
    else:
        raise ValueError(f"Could not geocode place: {place_name}")


def get_distance(origin, destination):
    api_key = Config.ORS_API_KEY
    url = "https://api.openrouteservice.org/v2/matrix/driving-car"
    headers = {
        "Accept": "application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8",
        "Authorization": api_key,
        "Content-Type": "application/json; charset=utf-8",
    }
    payload = {"locations": [origin, destination], "metrics": ["distance"]}

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()

    distance = data["distances"][0][1]

    return distance
