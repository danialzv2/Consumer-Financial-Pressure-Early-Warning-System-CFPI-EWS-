from app.data_loader import (
    load_historical_data,
    load_forecast_data
)
import numpy as np

hist_df = load_historical_data()
forecast_df = load_forecast_data()
hist_df["date"] = hist_df["date"].dt.strftime("%Y-%m-%d")
forecast_df["date"] = forecast_df["date"].dt.strftime("%Y-%m-%d")

def get_all_states():
    return sorted(hist_df["state"].dropna().unique().tolist())


def get_historical_timeseries(state_name: str):
    
    df = hist_df[hist_df["state"] == state_name].sort_values("date")
    df = df.replace({np.nan: None})
    return df.to_dict(orient="records")

def get_latest_forecast_by_state(state_name: str):
    df = forecast_df[forecast_df["state"] == state_name].sort_values("date")
    df.tail(1)
    return df.to_dict(orient="records")
    
def get_state_dashboard_view(state_name: str):
    return {
        "historical": get_historical_timeseries(state_name),
        "forecast": get_latest_forecast_by_state(state_name)
    }

