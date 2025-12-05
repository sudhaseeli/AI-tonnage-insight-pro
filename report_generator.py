from __future__ import annotations

from typing import Dict, Any

import pandas as pd


def build_issue_explanation(row: pd.Series) -> str:
    messages = []
    if row.get("has_rule_issue"):
        messages.append(f"Rule issues: {row.get('issues')}")
    if bool(row.get("is_anomaly", False)):
        score = row.get("anomaly_score", 0.0)
        messages.append(f"Anomaly flagged (score={score:.3f})")
    if not messages:
        return "No issues detected"
    return " | ".join(messages)


def summarize_issues(df: pd.DataFrame) -> Dict[str, Any]:
    summary = {}
    summary["total_rows"] = len(df)
    summary["rows_with_rule_issues"] = int(df["has_rule_issue"].sum())
    summary["rows_with_anomalies"] = int(df["is_anomaly"].sum())
    summary["rows_with_any_issue"] = int(
        ((df["has_rule_issue"]) | (df["is_anomaly"])).sum()
    )
    return summary


def annotate_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["explanation"] = df.apply(build_issue_explanation, axis=1)
    df["has_any_issue"] = df["has_rule_issue"] | df["is_anomaly"]
    return df
