from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:*"])

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

@app.route("/")
def home():
    return "🌦️ NovaWeather API is live! "

# Use post method for security
@app.route("/weather", methods=["POST"])
def get_weather():
    data = request.get_json()
    city = data.get("city")

    if not city:
        return jsonify({"error": "Missing 'city' in JSON body"}), 400

    # Call OpenWeatherMap API
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return jsonify({"error": "City not found or API request failed"}), response.status_code

    return jsonify(response.json())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)