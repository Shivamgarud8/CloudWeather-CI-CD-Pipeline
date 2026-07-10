from flask import Flask, render_template, request
import requests
import os
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

# Internal Docker network address of the API service
API_URL = os.getenv("API_URL", "http://cloudweather-api:5000")

@app.route('/')
def index():
    logger.info("Home page opened")
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form.get('city', '').strip()
    if not city:
        return render_template('result.html', error="Please enter a city name", weather=None)

    try:
        logger.info(f"Requesting weather for {city} from API")
        resp = requests.get(f"{API_URL}/api/weather", params={"city": city}, timeout=5)
        data = resp.json()

        if resp.status_code != 200:
            return render_template('result.html', error=data.get('error', 'Unable to fetch weather'), weather=None)

        return render_template('result.html', weather=data, error=None)

    except requests.exceptions.Timeout:
        return render_template('result.html', error="API request timed out", weather=None)
    except requests.exceptions.ConnectionError:
        return render_template('result.html', error="Cannot reach weather API", weather=None)
    except Exception as e:
        logger.exception("UI error")
        return render_template('result.html', error=str(e), weather=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
