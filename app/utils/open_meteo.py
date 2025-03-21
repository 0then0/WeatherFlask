import openmeteo_requests

import requests_cache
from retry_requests import retry

import requests

from app.config import Config

def get_weather(lat, lon):
    """
    Fetches weather data from Open-Meteo API for given latitude and longitude.

    :param lat: Latitude of the location
    :param lon: Longitude of the location
    :return: Dictionary with weather data or error message
    """
    try:
        # Setup the Open-Meteo API client with cache and retry on error
        cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
        retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
        openmeteo = openmeteo_requests.Client(session = retry_session)
        
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": ["apparent_temperature", "temperature_2m", "weather_code", "wind_speed_10m"],
        }
        responses = openmeteo.weather_api(Config.OPEN_METEO_API_URL, params=params)
        
        response = responses[0]
        current = response.Current()
        
        current_apparent_temperature = current.Variables(0).Value()
        current_temperature_2m = current.Variables(1).Value()
        current_weather_code = current.Variables(2).Value()
        current_wind_speed_10m = current.Variables(3).Value()

        return {
            "Coordinates": f"Lat: {response.Latitude()}°N, Lon: {response.Longitude()}°E",
            "Current temperature": current_temperature_2m,
            "Current apparent temperature": current_apparent_temperature,
            "Current wind speed": current_wind_speed_10m,
            "Current weather code": current_weather_code,
        }
    
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
