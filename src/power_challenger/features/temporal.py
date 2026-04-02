from __future__ import annotations

import numpy as np
import pandas as pd


def add_daily_time_features(df: pd.DataFrame, date_col: str = "Date") -> pd.DataFrame:
    frame = df.copy()
    frame[date_col] = pd.to_datetime(frame[date_col])
    date_series = frame[date_col]

    frame["year"] = date_series.dt.year
    frame["month"] = date_series.dt.month
    frame["day"] = date_series.dt.day
    frame["week_of_year"] = date_series.dt.isocalendar().week.astype(int)
    frame["quarter"] = date_series.dt.quarter
    frame["day_of_week"] = date_series.dt.dayofweek
    frame["is_weekend"] = (date_series.dt.dayofweek >= 5).astype(int)

    frame["day_of_week_sin"] = np.sin(2 * np.pi * frame["day_of_week"] / 7)
    frame["day_of_week_cos"] = np.cos(2 * np.pi * frame["day_of_week"] / 7)

    frame["month_sin"] = np.sin(2 * np.pi * frame["month"] / 12)
    frame["month_cos"] = np.cos(2 * np.pi * frame["month"] / 12)

    frame["week_of_year_sin"] = np.sin(2 * np.pi * frame["week_of_year"] / 52)
    frame["week_of_year_cos"] = np.cos(2 * np.pi * frame["week_of_year"] / 52)

    frame["quarter_sin"] = np.sin(2 * np.pi * frame["quarter"] / 4)
    frame["quarter_cos"] = np.cos(2 * np.pi * frame["quarter"] / 4)
    return frame


def add_group_lag_features(
    df: pd.DataFrame,
    group_cols: list[str],
    target_col: str = "kwh",
    lags: tuple[int, ...] = (1, 7, 14, 30),
) -> pd.DataFrame:
    frame = df.copy().sort_values(group_cols + ["Date"])
    for lag in lags:
        frame[f"{target_col}_lag_{lag}"] = frame.groupby(group_cols)[target_col].shift(lag)
    return frame
