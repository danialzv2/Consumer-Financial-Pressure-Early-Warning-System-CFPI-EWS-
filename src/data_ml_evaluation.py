
import pandas as pd
import numpy as np
import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import roc_auc_score, classification_report

MODEL_PATH = "../Consumer-Financial-Pressure-Early-Warning-System-CFPI-EWS-/models/cfpi_direction_model.pkl"

def ml_evaluation(data):

    FEATURE_COLS = [
        "fuel_pressure",
        "index",
        "fx_pressure",
        "policy_pressure",
        "cfpi_momentum_1m",
        "cfpi_momentum_3m",
        "cfpi_volatility_3m"
    ]

    def add_ml_features(df):
        """
        Adds ML features needed for CFPI direction prediction
        """
        df = df.sort_values(["state", "date"]).copy()

        df["cfpi_momentum_1m"] = df.groupby("state")["cfpi"].diff(1)
        df["cfpi_momentum_3m"] = df.groupby("state")["cfpi"].diff(3)

        df["cfpi_volatility_3m"] = (
            df.groupby("state")["cfpi"]
            .rolling(3)
            .std()
            .reset_index(level=0, drop=True)
        )

        return df


    def predict_direction(df):
        bundle = joblib.load(MODEL_PATH)
        model = bundle["model"]

        df = add_ml_features(df)

        df = df.sort_values(["state", "date"]).copy()
        latest = df.groupby("state").tail(1)

        X_latest = latest[FEATURE_COLS].dropna()
        probs = model.predict_proba(X_latest)[:, 1]

        output = latest.loc[X_latest.index, ["date", "state", "cfpi"]].copy()
        output["prob_cfpi_up_next_month"] = probs
        output["direction_signal"] = (
            output["prob_cfpi_up_next_month"] > 0.6
        ).map({True: "Likely Increase", False: "Stable / Decrease"})

        return output

    final = predict_direction(data)
    
    return final

