import os
import requests
from dotenv import load_dotenv

load_dotenv()

OWM_API_KEY = os.getenv("OWM_API_KEY")
OWM_BASE_URL = os.getenv("OWM_BASE_URL", "https://api.openweathermap.org/data/2.5/weather")

def fetch_openweather(city="Melbourne,AU", units="metric"):
    if not OWM_API_KEY:
        raise RuntimeError("Missing OWM_API_KEY in environment (.env)")
    params = {"q": city, "appid": OWM_API_KEY, "units": units}
    r = requests.get(OWM_BASE_URL, params=params, timeout=15)
    r.raise_for_status()
    j = r.json()
    # minimal normalized record
    rec = {
        "city": city,
        "datetime": pd.Timestamp.utcnow().tz_localize(None),
        "temp_c": j["main"]["temp"],
        "feels_like_c": j["main"]["feels_like"],
        "humidity": j["main"]["humidity"],
        "lat": j["coord"]["lat"],
        "lon": j["coord"]["lon"],
    }
    return rec
