import pandas as pd
import matplotlib.pyplot as plt

def try_prophet_forecast(df, out_path="figures/fig_prophet_temp.png", periods=48, freq="H"):
    try:
        from prophet import Prophet
    except Exception:
        print("Prophet not installed; skipping forecast.")
        return None

    if "datetime" not in df or "temp_c" not in df:
        raise ValueError("DataFrame must contain 'datetime' and 'temp_c' columns")

    ds = pd.DataFrame({
        "ds": pd.to_datetime(df["datetime"]),
        "y": df["temp_c"].astype(float)
    }).dropna()

    model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=True)
    model.fit(ds)
    future = model.make_future_dataframe(periods=periods, freq=freq)
    fc = model.predict(future)

    fig = model.plot(fc)
    plt.title("Prophet Forecast – Temperature (°C)")
    fig.savefig(out_path, dpi=160, bbox_inches="tight")
    plt.close(fig)
    return fc
