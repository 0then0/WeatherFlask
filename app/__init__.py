from flask import Flask

from app.config import Config
from app.routes import weather_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(weather_bp)

    return app
