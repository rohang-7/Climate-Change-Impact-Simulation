import os
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

from src.clean import engineer_features
from src.cluster import run_kmeans, run_dbscan
from src.forecasting import try_prophet_forecast

st.set_page_config(page_title="Climate Impact – Melbourne", layout="wide")

st.title("🌡️ Climate Change Impact Simulation — Melbourne")
st.caption("API-driven sample → Prophet forecast → K-Means & DBSCAN clustering → +1.5 °C / +2 °C scenarios.")

@st.cache_data
def load_sample():
    df = pd.read_csv("data/sample_weather.csv", parse_dates=["datetime"])
    return df

df = load_sample()
df = engineer_features(df)

st.sidebar.header("Controls")
k = st.sidebar.slider("K-Means: number of clusters (k)", min_value=2, max_value=6, value=3, step=1)
db_eps = st.sidebar.slider("DBSCAN: eps (standardized units)", min_value=0.05, max_value=0.5, value=0.12, step=0.01)
db_min = st.sidebar.slider("DBSCAN: min_samples", min_value=3, max_value=20, value=5, step=1)
do_forecast = st.sidebar.checkbox("Run Prophet forecast (if installed)", value=True)

# Clustering
k_labels = run_kmeans(df, k=k, use_cols=["lat","lon","temp_c"])
d_labels = run_dbscan(df, eps=float(db_eps), min_samples=int(db_min), use_cols=["lat","lon"])

c1, c2 = st.columns(2, gap="large")
with c1:
    st.subheader("K-Means (lat, lon, temp)")
    fig1, ax1 = plt.subplots()
    sc = ax1.scatter(df["lon"], df["lat"], c=k_labels)
    ax1.set_xlabel("Longitude"); ax1.set_ylabel("Latitude")
    ax1.set_title("K-Means Clusters")
    st.pyplot(fig1)

with c2:
    st.subheader("DBSCAN (lat, lon)")
    fig2, ax2 = plt.subplots()
    sc2 = ax2.scatter(df["lon"], df["lat"], c=d_labels)
    ax2.set_xlabel("Longitude"); ax2.set_ylabel("Latitude")
    ax2.set_title("DBSCAN Clusters")
    st.pyplot(fig2)

st.markdown("---")

# Prophet forecast
if do_forecast:
    st.subheader("Prophet Forecast — Temperature (°C)")
    try:
        fc = try_prophet_forecast(df, out_path="figures/fig_prophet_temp.png", periods=48, freq="H")
        if fc is not None:
            st.image("figures/fig_prophet_temp.png", caption="Temperature forecast with intervals")
            # Scenario application
            st.subheader("Scenarios")
            base_mean = fc["yhat"].tail(24).mean()
            s15 = base_mean + 1.5
            s20 = base_mean + 2.0
            st.write(f"Baseline (next 24h mean): **{base_mean:.2f} °C**")
            st.write(f"+1.5 °C scenario: **{s15:.2f} °C**, +2.0 °C scenario: **{s20:.2f} °C**")
    except Exception as e:
        st.info(f"Prophet not available or failed ({e}). Skipping forecast.")
        st.caption("Install: `pip install prophet` (may take a while).")

st.markdown("---")
st.caption("WGS84 (EPSG:4326). Demo uses tiny cached sample. For live data, wire up src/fetch_weather.py with your API key.")

# -----------------------------
# Future Weather (next 5 days)
# -----------------------------
import matplotlib.pyplot as plt
import streamlit as st
from src.fetch_weather import get_5day_forecast

st.divider()
st.header("Future Weather (next 5 days)")

# Optional toggle so the page stays tidy
show_future = st.checkbox("Show 5-day forecast (3-hourly)", value=True)

if show_future:
    col1, col2, col3 = st.columns([1,1,2])
    with col1:
        lat = st.number_input("Latitude", value=-37.8136, format="%.4f")
    with col2:
        lon = st.number_input("Longitude", value=144.9631, format="%.4f")
    with col3:
        st.caption("Defaults to Melbourne CBD. Any coordinate works.")

    @st.cache_data(ttl=1800)  # 30 minutes
    def _load_forecast(lat, lon):
        return get_5day_forecast(lat=lat, lon=lon)

    try:
        fcast = _load_forecast(lat, lon)
    except Exception as e:
        st.warning(f"Could not load forecast: {e}")
        fcast = None

    if fcast is not None and not fcast.empty:
        # Temp & Humidity (dual-axis)
        st.subheader("Temperature & Humidity (3-hourly)")
        fig1, ax1 = plt.subplots(figsize=(10, 3.2))
        ax1.plot(fcast.index, fcast["temp"], marker="o", linewidth=1.5, label="Temperature (°C)")
        ax1.set_ylabel("°C"); ax1.set_xlabel("Datetime")
        ax2 = ax1.twinx()
        ax2.plot(fcast.index, fcast["humidity"], linestyle="--", linewidth=1.0, label="Humidity (%)")
        ax2.set_ylabel("%")
        ax1.legend(loc="upper left"); ax2.legend(loc="upper right")
        fig1.tight_layout(); st.pyplot(fig1, clear_figure=True)

        # Simulated warming overlays (+1.5 / +2.0)
        st.subheader("Simulated Warming Scenarios")
        fig2, ax = plt.subplots(figsize=(10, 3.2))
        ax.plot(fcast.index, fcast["temp"], color="black", linewidth=1.8, label="Actual")
        ax.plot(fcast.index, fcast["temp"] + 1.5, linestyle="--", linewidth=1.5, label="+1.5 °C")
        ax.plot(fcast.index, fcast["temp"] + 2.0, linestyle="--", linewidth=1.5, label="+2.0 °C")
        ax.set_ylabel("Temperature (°C)"); ax.set_xlabel("Datetime"); ax.legend()
        fig2.tight_layout(); st.pyplot(fig2, clear_figure=True)

        # Rainfall (mm per 3h)
        st.subheader("Rainfall (mm per 3-hour interval)")
        fig3, ax3 = plt.subplots(figsize=(6, 3.0))
        ax3.plot(fcast.index, fcast["rain_mm_3h"], linewidth=1.5)
        ax3.set_ylabel("mm / 3h"); ax3.set_xlabel("Datetime")
        fig3.tight_layout(); st.pyplot(fig3, clear_figure=True)

        with st.expander("Preview forecast table"):
            st.dataframe(fcast.reset_index().rename(columns={"dt": "datetime"}))
    else:
        st.info("Enter a valid lat/lon and ensure OWM_API_KEY is set to fetch the forecast.")

