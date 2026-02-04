import pandas as pd
from data_merging import merging
import numpy as np

def preprocessing():  

    cleaned_data = merging()

    ROLLING_Z_WINDOW = 24        # months
    SMOOTHING_WINDOW = 3         # months

    WEIGHTS = {
        "fuel": 0.30,
        "inflation": 0.35,
        "fx": 0.20,
        "policy": 0.15
    }

    CFPI_MIN = 0
    CFPI_MAX = 100


    ################################# Feature Engineering #################################

    def rolling_zscore(series, window):
        mean = series.rolling(window).mean()
        std = series.rolling(window).std()
        return (series - mean) / std


    def compute_fuel_pressure(df):
        fuel_price = (
            0.5 * df["ron95_budi95"] +
            0.3 * df["diesel"] +
            0.2 * df["ron97"]
        )

        fuel_mom_change = fuel_price.pct_change()
        fuel_pressure = rolling_zscore(fuel_mom_change, window=6)

        return fuel_pressure



    def compute_inflation_pressure(df):
        cpi_change = df["index"].pct_change(periods=12)  # YoY inflation
        inflation_pressure = rolling_zscore(cpi_change, window=6)

        return inflation_pressure


    def compute_fx_pressure(df):
        fx = df["USD"]
        fx_change_3m = fx.pct_change(periods=3)

        fx_pressure = rolling_zscore(fx_change_3m, window=6)
        return fx_pressure


    def compute_policy_pressure(df):
        opr_change = df["Rate"].diff()

        policy_pressure = (opr_change > 0).astype(int)
        return policy_pressure

    ################################# Index construction logic  #################################


    def scale_to_100(series):
        min_val = series.min()
        max_val = series.max()
        return 100 * (series - min_val) / (max_val - min_val)


    def compute_cfpi(df):
        df = df.sort_values("date").copy()

        df["fuel_pressure"] = compute_fuel_pressure(df)
        df["inflation_pressure"] = compute_inflation_pressure(df)
        df["fx_pressure"] = compute_fx_pressure(df)
        df["policy_pressure"] = compute_policy_pressure(df)

        df["raw_cfpi"] = (
            WEIGHTS["fuel"] * df["fuel_pressure"] +
            WEIGHTS["inflation"] * df["inflation_pressure"] +
            WEIGHTS["fx"] * df["fx_pressure"] +
            WEIGHTS["policy"] * df["policy_pressure"]
        )

        df["raw_cfpi"] = df["raw_cfpi"].rolling(SMOOTHING_WINDOW, min_periods=1).mean()

        df["cfpi"] = scale_to_100(df["raw_cfpi"])
        df["cfpi"] = df["cfpi"].clip(CFPI_MIN, CFPI_MAX)

        df["cfpi_trend"] = df["cfpi"].diff()

        df["risk_flag"] = pd.cut(
            df["cfpi"],
            bins=[-np.inf, 30, 60, 80, np.inf],
            labels=["Low", "Moderate", "High", "Severe"]
        )

        return df


    # INPUT_PATH = "../data/cleaned_data.csv"
    # OUTPUT_PATH = "outputs/cfpi_daily.csv"

    # df = pd.read_csv(INPUT_PATH, parse_dates=["date"])
    cleaned_data["date"] = pd.to_datetime(cleaned_data["date"])

    result = (
        cleaned_data
        .groupby("state", group_keys=False)
        .apply(compute_cfpi)
        .reset_index(drop=True)
    )

    return result
