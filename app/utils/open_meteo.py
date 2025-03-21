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
        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": True,
        }
        response = requests.get(Config.OPEN_METEO_API_URL, params=params, timeout=5)
        response.raise_for_status()

        data = response.json()
        current_weather = data.get("current_weather", {})

        return {
            "location": f"Lat: {lat}, Lon: {lon}",
            "temperature": current_weather.get("temperature"),
            "wind_speed": current_weather.get("windspeed"),
            "weather_code": current_weather.get("weathercode"),
            "time": current_weather.get("time"),
        }

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
