from datetime import datetime

import openmeteo_requests
import requests_cache
from geopy.geocoders import Nominatim
from retry_requests import retry

from app.config import Config

geolocator = Nominatim(user_agent="WeatherFlask")

WMO_WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Drizzle: Light",
    53: "Drizzle: Moderate",
    55: "Drizzle: Dense intensity",
    61: "Rain: Slight",
    63: "Rain: Moderate",
    65: "Rain: Heavy",
    66: "Freezing Rain: Light",
    67: "Freezing Rain: Heavy",
    71: "Snow fall: Slight",
    73: "Snow fall: Moderate",
    75: "Snow fall: Heavy",
    77: "Snow grains",
    80: "Rain showers: Slight",
    81: "Rain showers: Moderate",
    82: "Rain showers: Violent",
    85: "Snow showers: Slight",
    86: "Snow showers: Heavy",
    95: "Thunderstorm: Slight or moderate",
    96: "Thunderstorm with hail: Slight",
    99: "Thunderstorm with hail: Heavy",
}


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
    current_apparent_temperature = f"{round(current.Variables(0).Value(), 1)}°C"
    current_temperature_2m = f"{round(current.Variables(1).Value(), 1)}°C"
    current_weather_code = current.Variables(2).Value()
    weather_description = WMO_WEATHER_CODES.get(
        current_weather_code, "Unknown weather condition"
    )
    current_wind_speed_10m = f"{round(current.Variables(3).Value(), 1)} km/h"
    current_time_iso = current.Time()
    current_time_formatted = datetime.fromtimestamp(current_time_iso).strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    return {
        "City": city_name,
        "Coordinates": f"Lat: {round(response.Latitude(), 4)}°N Lon: {round(response.Longitude(), 4)}°E",
        "Current apparent temperature": current_apparent_temperature,
        "Current temperature": current_temperature_2m,
        "Current weather code": current_weather_code,
        "Current wind speed": current_wind_speed_10m,
        "Last update": current_time_formatted,
        "Weather description": weather_description,
    }
