import requests, certifi
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY", "0723d71a05e58ae3f7fc91e39a901e6b")
CITY = os.getenv("CITY", "Manila")
URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

def get_weather_data():
    response = requests.get(URL, verify=certifi.where())  # use certifi bundle
    data = response.json()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    wind_speed = data["wind"]["speed"]
    wind_dir = data["wind"]["deg"]
    cloudiness = data["clouds"]["all"]
    solar_irradiance = round((100 - cloudiness) * 10)

    return (timestamp, wind_speed, wind_dir, solar_irradiance)
