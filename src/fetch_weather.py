import os
import requests
import pandas as pd

def get_5day_forecast(lat=-37.8136, lon=144.9631, api_key=None, units="metric"):
    """
    OpenWeatherMap 5-day/3-hour forecast.
    Returns a DataFrame indexed by datetime with columns:
    temp (°C), humidity (%), rain_mm_3h (mm in the 3h bucket)
    """
    # supports .env locally and Streamlit Cloud secrets
    api_key = api_key or os.getenv("OWM_API_KEY")
    if not api_key:
        # Streamlit secrets support
        try:
            import streamlit as st
            api_key = st.secrets.get("OWM_API_KEY", None)
        except Exception:
            pass
    if not api_key:
        raise RuntimeError("Missing OWM_API_KEY (set in .env or Streamlit secrets).")

    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {"lat": lat, "lon": lon, "appid": api_key, "units": units}
    resp = requests.get(url, params=params, timeout=20)
    resp.raise_for_status()
    data = resp.json()

    rows = []
    for item in data["list"]:
        dt = pd.to_datetime(item["dt"], unit="s")
        rows.append({
            "dt": dt,
            "temp": item["main"]["temp"],
            "humidity": item["main"]["humidity"],
            "rain_mm_3h": item.get("rain", {}).get("3h", 0.0)
        })
    df = pd.DataFrame(rows).set_index("dt").sort_index()
    return df
