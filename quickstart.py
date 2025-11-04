import argparse
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from src.clean import engineer_features
from src.cluster import run_kmeans, run_dbscan
from src.forecasting import try_prophet_forecast

FIG_DIR = "figures"
DATA_PATH = "data/sample_weather.csv"

def ensure_dirs():
    os.makedirs(FIG_DIR, exist_ok=True)

def load_sample():
    df = pd.read_csv(DATA_PATH, parse_dates=["datetime"])
    return df

def plot_kmeans(df, labels, fname):
    plt.figure()
    plt.scatter(df["lon"], df["lat"], c=labels)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("K-Means Clusters (sample)")
    plt.savefig(os.path.join(FIG_DIR, fname), dpi=160, bbox_inches="tight")
    plt.close()

def plot_dbscan(df, labels, fname):
    plt.figure()
    plt.scatter(df["lon"], df["lat"], c=labels)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("DBSCAN Clusters (sample)")
    plt.savefig(os.path.join(FIG_DIR, fname), dpi=160, bbox_inches="tight")
    plt.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--forecast", action="store_true", help="Run Prophet forecast if available")
    parser.add_argument("--cluster", action="store_true", help="Run clustering (KMeans + DBSCAN)")
    args = parser.parse_args()

    ensure_dirs()
    df = load_sample()
    df_feat = engineer_features(df)

    if args.cluster:
        # K-Means on spatial coords (+ temperature) as demo
        k_labels = run_kmeans(df_feat, k=3, use_cols=["lat","lon","temp_c"])
        plot_kmeans(df_feat, k_labels, "fig_kmeans_clusters.png")

        # DBSCAN on standardized lat/lon
        d_labels = run_dbscan(df_feat, eps=0.12, min_samples=5, use_cols=["lat","lon"])
        plot_dbscan(df_feat, d_labels, "fig_dbscan_clusters.png")

    if args.forecast:
        # Prophet (graceful if not installed)
        try_prophet_forecast(df_feat, out_path=os.path.join(FIG_DIR, "fig_prophet_temp.png"))

if __name__ == "__main__":
    main()
