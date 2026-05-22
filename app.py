from flask import Flask, render_template, request
import requests
import logging
import os

app = Flask(__name__)

# =========================
# Logging Configuration
# =========================
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Test log
logger.error("Test error log from Flask application")

# =========================
# OpenWeatherMap API
# =========================
API_KEY = os.getenv("OPENWEATHER_API_KEY", "803f77a96502ec00149f4b07055e5dd5")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


# =========================
# Home Route
# =========================
@app.route('/')
def index():
    logger.info("Home page opened")
    return render_template('index.html')


# =========================
# Weather Route
# =========================
@app.route('/weather', methods=['POST'])
def weather():

    city = request.form.get('city', '').strip()

    # Empty city validation
    if not city:

        logger.warning("City name not entered")

        return render_template(
            'result.html',
            error="Please enter a city name",
            weather=None
        )

    try:

        logger.info(f"Fetching weather for city: {city}")

        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'
        }

        # API request with timeout
        response = requests.get(
            BASE_URL,
            params=params,
            timeout=5
        )

        logger.info(f"API Status Code: {response.status_code}")

        data = response.json()

        # API error handling
        if data.get('cod') != 200:

            message = data.get('message', 'City not found')

            logger.error(f"API Error: {message}")

            return render_template(
                'result.html',
                error=message.capitalize(),
                weather=None
            )

        # Weather data
        weather_data = {
            'city': data['name'],
            'country': data['sys']['country'],
            'temperature': round(data['main']['temp'], 1),
            'description': data['weather'][0]['description'].title(),
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed']
        }

        logger.info(f"Weather fetched successfully for {city}")

        return render_template(
            'result.html',
            weather=weather_data,
            error=None
        )

    except requests.exceptions.Timeout:

        logger.exception("API Timeout Error")

        return render_template(
            'result.html',
            error="API request timed out",
            weather=None
        )

    except requests.exceptions.ConnectionError:

        logger.exception("Network Connection Error")

        return render_template(
            'result.html',
            error="Network connection error",
            weather=None
        )

    except Exception as e:

        logger.exception(f"Application Error: {str(e)}")

        return render_template(
            'result.html',
            error=f"Error: {str(e)}",
            weather=None
        )


# =========================
# Main
# =========================
if __name__ == '__main__':

    logger.info("Flask application started")

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
