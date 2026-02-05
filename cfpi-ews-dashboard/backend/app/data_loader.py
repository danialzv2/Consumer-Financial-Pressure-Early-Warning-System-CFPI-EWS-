import pandas as pd

BASE_PATH = "../backend/data"

def load_historical_data():
    """
    Loads historical macro + CFPI data.
    """
    df = pd.read_csv(
        f"{BASE_PATH}/data.csv",
        parse_dates=["date"]
    )
    df.columns = df.columns.str.lower().str.strip()

    return df

def load_forecast_data():
    """
    Loads ML CFPI direction forecast.
    """
    df = pd.read_csv(
        f"{BASE_PATH}/cfpi_direction_forecast.csv",
        parse_dates=["date"]
    )
    df.columns = df.columns.str.lower().str.strip()

    return df
