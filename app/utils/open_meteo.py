from datetime import datetime

import openmeteo_requests
import requests_cache
from geopy.geocoders import Nominatim
from retry_requests import retry

from app.config import Config

geolocator = Nominatim(user_agent="WeatherFlask")


def get_city_name(lat, lon):
    """
    Fetch city name from coordinates using geopy.

    :param lat: Latitude
    :param lon: Longitude
    :return: City name as string or 'Location not found' if not found
    """
    location = geolocator.reverse((lat, lon), language="en")

    if location:
        address = location.raw["address"]
        return address.get("city") or address.get("town") or address.get("village")

    return "Location not found"


def get_coordinates(city_name):
    """
    Fetch latitude and longitude for a given city name using geopy.

    :param city_name: Name of the city
    :return: Tuple (latitude, longitude) or None if not found
    """

    location = geolocator.geocode(city_name)
    if location:
        return location.latitude, location.longitude
    return None


def get_weather(lat, lon):
    """
    Fetches weather data from Open-Meteo API for given latitude and longitude.

    :param lat: Latitude of the location
    :param lon: Longitude of the location
    :return: Dictionary with weather data
    """
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    params = {
        "latitude": lat,
        "longitude": lon,
        "current": [
            "apparent_temperature",
            "temperature_2m",
            "weather_code",
            "wind_speed_10m",
        ],
    }
    responses = openmeteo.weather_api(Config.OPEN_METEO_API_URL, params=params)

    response = responses[0]
    current = response.Current()

    city_name = get_city_name(lat, lon)
    current_apparent_temperature = current.Variables(0).Value()
    current_temperature_2m = current.Variables(1).Value()
    current_weather_code = current.Variables(2).Value()
    current_wind_speed_10m = current.Variables(3).Value()
    current_time_iso = current.Time()
    current_time_formatted = datetime.fromtimestamp(current_time_iso).strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    return {
        "Coordinates": f"Lat: {response.Latitude()}°N Lon: {response.Longitude()}°E",
        "City": city_name,
        "Current temperature": current_temperature_2m,
        "Current apparent temperature": current_apparent_temperature,
        "Current wind speed": current_wind_speed_10m,
        "Current weather code": current_weather_code,
        "Last update": current_time_formatted,
    }
