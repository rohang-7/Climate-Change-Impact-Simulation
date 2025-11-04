import pandas as pd
import numpy as np

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "feels_like_c" not in df and {"temp_c","humidity"}.issubset(df.columns):
        # crude approximation if feels_like not present
        df["feels_like_c"] = df["temp_c"] + 0.33*df["humidity"]/100.0 * 5.0
    # time features
    if "datetime" in df.columns:
        df["hour"] = pd.to_datetime(df["datetime"]).dt.hour
        df["dayofweek"] = pd.to_datetime(df["datetime"]).dt.dayofweek
    # clip outliers lightly for demo
    for c in ["temp_c","feels_like_c","humidity"]:
        if c in df.columns:
            df[c] = df[c].clip(lower=df[c].quantile(0.01), upper=df[c].quantile(0.99))
    return df
