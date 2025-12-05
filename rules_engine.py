from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Any

import pandas as pd
import yaml
from pathlib import Path


@dataclass
class RuleConfig:
    required_columns: List[str]
    min_tonnage: float
    max_tonnage: float
    allowed_states: List[str]
    product_thresholds: Dict[str, Dict[str, float]]


def load_rule_config(path: str | Path) -> RuleConfig:
    path = Path(path)
    with open(path, "r") as f:
        cfg = yaml.safe_load(f)
    return RuleConfig(
        required_columns=cfg.get("required_columns", []),
        min_tonnage=cfg.get("min_tonnage", 0),
        max_tonnage=cfg.get("max_tonnage", float("inf")),
        allowed_states=cfg.get("allowed_states", []),
        product_thresholds=cfg.get("product_thresholds", {}),
    )


def apply_rules(df: pd.DataFrame, config: RuleConfig) -> pd.DataFrame:
    df = df.copy()
    issues: List[List[str]] = [[] for _ in range(len(df))]

    # Check required columns
    for col in config.required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column in data: {col}")

    # Basic tonnage checks
    for idx, row in df.iterrows():
        row_issues = issues[idx]
        tonnage = row.get("tonnage", None)
        state = str(row.get("state", "")).strip()
        product = str(row.get("product_name", "")).strip().upper()

        if tonnage is None or pd.isna(tonnage):
            row_issues.append("Missing tonnage")
        else:
            try:
                t_val = float(tonnage)
            except (TypeError, ValueError):
                row_issues.append("Non-numeric tonnage")
            else:
                if t_val < config.min_tonnage:
                    row_issues.append("Tonnage below minimum")
                if t_val > config.max_tonnage:
                    row_issues.append("Tonnage above global maximum")
                if t_val == 0:
                    row_issues.append("Zero tonnage")

        # State check
        if config.allowed_states and state not in config.allowed_states:
            row_issues.append("State not in allowed list")

        # Product-specific thresholds
        if product and product in config.product_thresholds and tonnage is not None and not pd.isna(tonnage):
            try:
                t_val = float(tonnage)
            except (TypeError, ValueError):
                pass
            else:
                p_cfg = config.product_thresholds[product]
                p_max = p_cfg.get("max_tonnage")
                if p_max is not None and t_val > p_max:
                    row_issues.append(f"Tonnage above product max ({p_max})")

    df["issues"] = [", ".join(i) if i else "" for i in issues]
    df["has_rule_issue"] = df["issues"].apply(lambda x: bool(x))
    return df
