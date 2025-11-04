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
