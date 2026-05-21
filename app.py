from flask import Flask, render_template, request
import requests
import logging

app = Flask(__name__)

# =========================
# Logging Configuration
# =========================
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

logging.error("Test error")

# =========================
# OpenWeatherMap API
# =========================
API_KEY = "803f77a96502ec00149f4b07055e5dd5"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


@app.route('/')
def index():
    logging.info("Home page opened")
    return render_template('index.html')


@app.route('/weather', methods=['POST'])
def weather():

    city = request.form.get('city', '').strip()

    if not city:
        logging.warning("City name not entered")
        return render_template(
            'result.html',
            error="Please enter a city name",
            weather=None
        )

    try:
        logging.info(f"Fetching weather for city: {city}")

        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'
        }

        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if data.get('cod') != 200:
            message = data.get('message', 'City not found')
            logging.error(f"API Error: {message}")

            return render_template(
                'result.html',
                error=message.capitalize(),
                weather=None
            )

        weather_data = {
            'city': data['name'],
            'country': data['sys']['country'],
            'temperature': round(data['main']['temp'], 1),
            'description': data['weather'][0]['description'].title(),
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed']
        }

        logging.info(f"Weather data fetched successfully for {city}")

        return render_template(
            'result.html',
            weather=weather_data,
            error=None
        )

    except Exception as e:
        logging.exception("Application Error")

        return render_template(
            'result.html',
            error=f"Error: {str(e)}",
            weather=None
        )


if __name__ == '__main__':
    logging.info("Flask app started")
    app.run(host='0.0.0.0', port=5000, debug=True)
