from flask import Blueprint, jsonify, request

from app.config import Config
from app.utils.open_meteo import get_weather

weather_bp = Blueprint("weather", __name__)


@weather_bp.route("/weather", methods=["GET"])
def weather():
    lat = request.args.get("lat", default=Config.DEFAULT_LAT, type=float)
    lon = request.args.get("lon", default=Config.DEFAULT_LON, type=float)

    weather_data = get_weather(lat, lon)

    if "error" in weather_data:
        return jsonify({"error": "Failed to fetch weather data"}), 500

    return jsonify(weather_data)
