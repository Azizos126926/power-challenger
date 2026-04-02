from __future__ import annotations

import pandas as pd


CLIMATE_AGGREGATIONS = {
    "Temperature (°C)": "mean",
    "Dewpoint Temperature (°C)": "mean",
    "U Wind Component (m/s)": "mean",
    "V Wind Component (m/s)": "mean",
    "Total Precipitation (mm)": "sum",
    "Snowfall (mm)": "sum",
    "Snow Cover (%)": "mean",
}


def aggregate_climate_daily(climate_df: pd.DataFrame) -> pd.DataFrame:
    working = climate_df.copy()
    working["Date Time"] = pd.to_datetime(working["Date Time"])
    daily = (
        working.groupby(working["Date Time"].dt.date)
        .agg(CLIMATE_AGGREGATIONS)
        .reset_index()
        .rename(columns={"Date Time": "Date"})
    )
    daily["Date"] = pd.to_datetime(daily["Date"])
    return daily


def merge_climate_daily(base_df: pd.DataFrame, climate_df: pd.DataFrame) -> pd.DataFrame:
    merged = base_df.copy()
    merged["Date"] = pd.to_datetime(merged["Date"])
    daily = aggregate_climate_daily(climate_df)
    return merged.merge(daily, on="Date", how="left")
