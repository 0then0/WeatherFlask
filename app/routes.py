from flask import Blueprint, jsonify, request

from app.config import Config
from app.utils.open_meteo import get_coordinates, get_weather

weather_bp = Blueprint("weather", __name__)


@weather_bp.route("/weather", methods=["GET"])
def weather():
    """Fetch weather data by city name or coordinates."""
    city = request.args.get("city")
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)

    if city:
        coordinates = get_coordinates(city)
        if not coordinates:
            return jsonify({"error": "City not found"}), 404
        lat, lon = coordinates

    if lat is None or lon is None:
        return jsonify({"error": "Missing latitude and longitude"}), 400

    weather_data = get_weather(lat, lon)
    return jsonify(weather_data)
