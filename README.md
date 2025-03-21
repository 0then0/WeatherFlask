# Weather API using Flask

This is a simple REST API built with Flask that fetches weather data from the Open-Meteo API and returns it to the user.

## Features

- Fetches current weather data for a given location
- Uses Open-Meteo API for weather data
- Simple and modular project structure
- Easy to extend and modify

## Installation

### Prerequisites

- Python 3.8+
- `pip` package manager

### Steps

1. Clone the repository:
   ```sh
   git clone https://github.com/0then0/WeatherFlask
   cd weather-app
   ```
2. Create a virtual environment and activate it:
   ```sh
   python -m venv .venv
   source venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the application:
   ```sh
   python run.py
   ```
5. The API will be available at `http://127.0.0.1:5000/`

## Usage

Send a GET request to fetch weather data:

```
GET /weather?lat=37.7749&lon=-122.4194
```

Example response:

```json
{
	"City": "San Francisco",
	"Coordinates": "Lat: 37.7632°N Lon: -122.4128°E",
	"Current apparent temperature": 6.91,
	"Current temperature": 8.5,
	"Current weather code": 0,
	"Current wind speed": 3.75,
	"Last update": "2025-03-21 18:30:00"
}
```
