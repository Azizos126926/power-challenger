from __future__ import annotations

from pathlib import Path

import pandas as pd


def parse_source_columns(df: pd.DataFrame, source_col: str = "Source") -> pd.DataFrame:
    frame = df.copy()
    extracted = frame[source_col].str.extract(r"consumer_device_(\d+)_data_user_(\d+)")
    frame["consumer_device"] = extracted[0].astype("Int64")
    frame["data_user"] = extracted[1].astype("Int64")
    return frame


def parse_submission_id(df: pd.DataFrame, id_col: str = "ID") -> pd.DataFrame:
    frame = df.copy()
    frame["Date"] = pd.to_datetime(frame[id_col].str.extract(r"(\d{4}-\d{2}-\d{2})")[0])
    extracted = frame[id_col].str.extract(r"consumer_device_(\d+)_data_user_(\d+)")
    frame["consumer_device"] = extracted[0].astype("Int64")
    frame["data_user"] = extracted[1].astype("Int64")
    return frame


def load_train_csv(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["Date"] = pd.to_datetime(df["Date"])
    return parse_source_columns(df)


def load_climate_xlsx(path: str | Path) -> pd.DataFrame:
    df = pd.read_excel(path)
    if "Date Time" not in df.columns:
        raise ValueError("Climate file must contain a 'Date Time' column.")
    df["Date Time"] = pd.to_datetime(df["Date Time"])
    return df


def load_sample_submission(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    return parse_submission_id(df)


def load_reference_table(path: str | Path) -> pd.DataFrame:
    return pd.read_csv(path)
