# Climate Change Impact Simulation — Melbourne

Real-time Melbourne climate analytics: **API-driven dataset → Prophet forecasts → DBSCAN/K-Means heat‑risk mapping → +1.5 °C/+2 °C scenario testing.**

## Why this repo
Urban heat and rainfall volatility are rising issues for councils and planners. This project ingests **live weather** from OpenWeatherMap, builds **time-series forecasts** (Prophet), detects **urban heat clusters** (DBSCAN/K‑Means), and explores **warming scenarios** (+1.5 °C / +2 °C) to highlight risk hot-spots and potential adaptation levers (trees, cool roofs, heat-health planning).

---

## Project structure
```
.
├── README.md
├── requirements.txt
├── .env.example
├── quickstart.py                 # runs on sample data end-to-end (no API key needed)
├── src/
│   ├── fetch_weather.py          # live API ingestion (OpenWeatherMap)
│   ├── clean.py                  # cleaning & feature engineering
│   ├── forecasting.py            # Prophet utilities
│   └── cluster.py                # DBSCAN + K-Means helpers
├── data/
│   └── sample_weather.csv        # tiny cached sample for reproducibility
├── figures/                      # output charts (saved here by quickstart.py)
│   └── .gitkeep
└── notebooks/
    └── (optional notebooks)
```

---

## Quick start (no API key needed)
1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the end-to-end sample**
   ```bash
   python quickstart.py
   ```

3. **See outputs**
   - Figures saved to `./figures/`:
     - `fig_prophet_temp.png` (if Prophet available)
     - `fig_kmeans_clusters.png`
     - `fig_dbscan_clusters.png`

> The sample uses a tiny CSV (`data/sample_weather.csv`) so anyone can reproduce plots without credentials.

---

## Live data (optional)
To pull fresh observations:
1. Get a free API key from OpenWeatherMap.
2. Create a `.env` file using the template below and add your key:
   ```bash
   cp .env.example .env
   ```
3. In your code, call `src/fetch_weather.py:fetch_openweather()` to retrieve data for a city or coordinates.

**.env.example**
```ini
OWM_API_KEY=YOUR_KEY_HERE
OWM_BASE_URL=https://api.openweathermap.org/data/2.5/weather
DEFAULT_CITY=Melbourne,AU
```

---

## Methods in 60 seconds
- **Forecasting (Prophet)**: daily/Hourly temperature `y ~ trend + seasonality`; 95% CI; configurable horizon.  
- **K‑Means**: k chosen via elbow/silhouette (default `k=3`); features include temp, humidity, “feels_like”, and (optionally) lat/lon.  
- **DBSCAN**: density-based clusters on standardized spatial features (default `eps=0.12`, `min_samples=10` after scaling).  
- **Scenarios**: baseline vs **+1.5 °C** and **+2 °C** (applied additively to forecast mean) to examine relative risk shifts.

> CRS: inputs are assumed in WGS84 (`EPSG:4326`) when mapping geolocated points.

---

## Reproduce the figures
```bash
# Prophet forecast (skips gracefully if Prophet not installed)
python quickstart.py --forecast

# Spatial clustering (K-Means + DBSCAN)
python quickstart.py --cluster

# All steps
python quickstart.py --forecast --cluster
```

---

## Results (example highlights — replace with your latest):
- **Urban heat zones** coincide with lower tree/vegetation coverage and denser built form.
- **“Feels-like” temperature** escalates faster than dry-bulb temperature on humid days.
- **2050 warming scenario** (high-emission sim) shows ~**+1.8 °C** mean temperature increase; rainfall **variance widens**.

---

## References
- IPCC Assessment Reports (AR6), WG1 Climate Change 2021 (for warming context)  
- OpenWeatherMap API docs (data dictionary & endpoints)  
- Ester et al. (1996) “A Density-Based Algorithm for Discovering Clusters in Large Spatial Databases with Noise” (DBSCAN)

---

## License
MIT

---

## Streamlit app (optional UI)
Run an interactive demo locally:

```bash
streamlit run streamlit_app.py
```

Controls (left sidebar):
- **K-Means**: choose `k`
- **DBSCAN**: tune `eps` and `min_samples`
- **Forecast**: toggle Prophet forecast (skips gracefully if Prophet not installed)

---

## LinkedIn assets
Inside `POSTS.md` you'll find:
- A polished LinkedIn post (text + tags)
- 3 one-line **image captions**
- Alt-text for accessibility
