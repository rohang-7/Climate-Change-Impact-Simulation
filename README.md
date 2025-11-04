
#  Climate Change Impact Simulation (Melbourne, Australia)

This project analyzes real-time and historical weather data to simulate and visualize the **impact of climate change in Melbourne**.  
Using live data from the **OpenWeatherMap API**, it explores temperature variations, rainfall trends, and urban heat zones — applying **machine learning (DBSCAN & KMeans)** and **forecasting (Prophet)** to predict climate patterns and identify risk-prone regions.

The goal is to help understand how +1.5°C and +2.0°C global warming scenarios could affect city-level climate dynamics, guiding sustainability and resilience planning.
For the original notebook and report PDF, see docs:
###  PDF - https://drive.google.com/file/d/1rocu_2cXfBJ0hv2FvzIJS3kDmnJoTQT4/view?usp=sharing
###  PYTHON NOTEBOOK - https://drive.google.com/file/d/1s3Y-wWnGVfmtHFROr_9_GmzHpjcXQMrL/view?usp=sharing
---

## Project Overview

- Collected and cleaned live weather data from **OpenWeatherMap API** (JSON-based).  
- Built a dataset combining **temperature, humidity, rainfall, wind, and pressure** metrics.  
- Applied **DBSCAN clustering** to detect **heatwave-prone and cool zones** across Melbourne.  
- Forecasted temperature and rainfall using **Facebook Prophet** (time-series forecasting).  
- Simulated **warming scenarios (+1.5°C and +2.0°C)** aligned with IPCC climate targets.  
- Created **interactive visualizations and heatmaps** for spatial and temporal insights.

---

## Key Findings

- **Urban Heat Zones:** Detected clusters of elevated temperature, primarily in dense suburbs.  
- **Tree Coverage Impact:** Areas with higher vegetation (urban forests) showed lower heat intensity.  
- **Rainfall Forecast:** The Prophet model predicts variable rainfall trends with potential decline post-2030.  
- **Temperature Trend:** Notable +1.8°C increase simulated across Melbourne by 2050 under high-emission scenarios.  
- **Heat Index:** "Feels-like" temperatures rise significantly beyond measured values, highlighting humidity’s role.  

This project showed how **data, weather APIs, and analytics** can reveal crucial insights about our planet’s future.

---

## Tools & Libraries

- **Python:** pandas, numpy, matplotlib, seaborn  
- **Geospatial:** geopandas, folium, shapely  
- **Clustering:** scikit-learn (DBSCAN, KMeans)  
- **Forecasting:** Prophet  
- **Data Source:** OpenWeatherMap API  
- **Environment:** Google Colab / Jupyter Notebook  

---

## How to Run

1. Clone this repository:
   ```bash
   git clone https://github.com/rohang-7/Climate-Change-Impact-Simulation.git
   cd Climate-Change-Impact-Simulation



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

## Streamlit app 
Run an interactive demo locally:

```bash
streamlit run streamlit_app.py
```

Controls (left sidebar):
- **K-Means**: choose `k`
- **DBSCAN**: tune `eps` and `min_samples`
- **Forecast**: toggle Prophet forecast (skips gracefully if Prophet not installed)

---

