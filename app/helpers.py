import requests

from instance.config import Config


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
    payload = {"locations": [origin, destination], "metrics": ["distance", "duration"]}

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()

    distance = data["distances"][0][1]
    duration = data["durations"][0][1]

    return distance, duration
