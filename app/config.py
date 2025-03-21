import os


class Config:
    DEBUG = False
    TESTING = False
    OPEN_METEO_API_URL = "https://api.open-meteo.com/v1/forecast"
    DEFAULT_LAT = 37.7749  # Default latitude (San Francisco)
    DEFAULT_LON = -122.4194  # Default longitude
