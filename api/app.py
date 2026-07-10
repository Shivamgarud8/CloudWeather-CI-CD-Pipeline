from flask import Flask, jsonify, request
import requests
import logging
import os

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

@app.route('/health')
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/api/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city', '').strip()
    if not city:
        return jsonify({"error": "City name is required"}), 400
    try:
        logger.info(f"Fetching weather for city: {city}")
        params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
        response = requests.get(BASE_URL, params=params, timeout=5)
        data = response.json()

        if data.get('cod') != 200:
            message = data.get('message', 'City not found')
            logger.warning(f"API Error: {message}")
            return jsonify({"error": message.capitalize()}), 404

        weather_data = {
            'city': data['name'],
            'country': data['sys']['country'],
            'temperature': round(data['main']['temp'], 1),
            'description': data['weather'][0]['description'].title(),
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed']
        }
        return jsonify(weather_data), 200

    except requests.exceptions.Timeout:
        logger.exception("Upstream API timeout")
        return jsonify({"error": "Weather API request timed out"}), 504
    except requests.exceptions.ConnectionError:
        logger.exception("Upstream connection error")
        return jsonify({"error": "Network connection error"}), 502
    except Exception as e:
        logger.exception("Unhandled error")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
