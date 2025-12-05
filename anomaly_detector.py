from __future__ import annotations

from typing import Optional

import pandas as pd
from sklearn.ensemble import IsolationForest


def detect_anomalies(df: pd.DataFrame, random_state: int = 42) -> pd.DataFrame:
    """Simple anomaly detection over tonnage by product/state.

    This is intentionally lightweight. In a real-world system, you would:
    - Fit on a longer history
    - Use more features (seasonality, region, etc.)
    - Persist and version models
    """
    df = df.copy()
    if "tonnage" not in df.columns:
        raise ValueError("Expected 'tonnage' column in dataframe")

    # Drop rows with missing tonnage for modeling
    model_df = df.dropna(subset=["tonnage"]).copy()
    if model_df.empty:
        df["anomaly_score"] = 0.0
        df["is_anomaly"] = False
        return df

    model_df["tonnage"] = model_df["tonnage"].astype(float)

    iso = IsolationForest(contamination=0.1, random_state=random_state)
    iso.fit(model_df[["tonnage"]])
    scores = iso.decision_function(model_df[["tonnage"]])
    preds = iso.predict(model_df[["tonnage"]])

    model_df["anomaly_score"] = scores
    model_df["is_anomaly"] = preds == -1

    # Merge scores back to full dataframe
    df = df.merge(
        model_df[["anomaly_score", "is_anomaly"]],
        left_index=True,
        right_index=True,
        how="left",
    )
    df["anomaly_score"] = df["anomaly_score"].fillna(0.0)
    df["is_anomaly"] = df["is_anomaly"].fillna(False)
    return df
