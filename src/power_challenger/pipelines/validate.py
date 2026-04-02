from __future__ import annotations

import pandas as pd

from power_challenger.config import ProjectConfig
from power_challenger.features.temporal import add_daily_time_features
from power_challenger.models.catboost_model import CatBoostForecaster
from power_challenger.models.heuristics import device18_peak_decline_forecast
from power_challenger.pipelines.training import build_training_frame
from power_challenger.utils.submission import rmse


def holdout_backtest(
    config: ProjectConfig,
    split_date: str = "2024-09-13",
) -> dict[str, float]:
    full_train = build_training_frame(config)
    split = pd.to_datetime(split_date)

    train_df = full_train[full_train["Date"] <= split].copy()
    valid_df = full_train[full_train["Date"] > split].copy()
    if valid_df.empty:
        raise ValueError("No validation rows found after split_date.")

    model = CatBoostForecaster(
        iterations=int(config.get("model", "catboost", "iterations", default=4000)),
        early_stopping_rounds=int(config.get("model", "catboost", "early_stopping_rounds", default=100)),
        random_state=int(config.get("model", "catboost", "random_state", default=42)),
        verbose=int(config.get("model", "catboost", "verbose", default=500)),
    ).fit(train_df)

    preds = model.predict(valid_df).clip(lower=0)
    metrics = {"catboost_rmse": rmse(valid_df["kwh"], preds)}

    return metrics
