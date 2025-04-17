from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv
from flask_cors import CORS
from google import genai




app = Flask(__name__)
CORS(app, origins=["http://localhost:*"])

load_dotenv(override=True)
API_KEY = os.getenv("WEATHER_API_KEY")
GEM_API_KEY = os.getenv("GEMINI_API_KEY")


@app.route("/")
def home():
    return "🌦️ NovaWeather API is live! "

@app.route("/test")


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

    weather_data = response.json()

    # Call your AI function AFTER getting weather data
    ai_response = ai(city)  # Pass weather data if needed

    # Merge AI into the response
    combined_response = {
        "weather": weather_data,
        "summary": ai_response
    }

    return jsonify(combined_response)


def ai(city):
    client = genai.Client(api_key=GEM_API_KEY)

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"Create a description with exactly 20-30 words (try to not use the word 'vibrant' so much) and be sure to include the name of the location (but not the region or country and use ',' instead of ':') for: {city}",
    )

    return response.text



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)