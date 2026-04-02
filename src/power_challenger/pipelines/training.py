from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from power_challenger.config import ProjectConfig
from power_challenger.data.io import load_climate_xlsx, load_reference_table, load_train_csv
from power_challenger.features.climate import merge_climate_daily
from power_challenger.features.metadata import merge_source_metadata
from power_challenger.features.temporal import add_daily_time_features
from power_challenger.models.catboost_model import CatBoostForecaster
from power_challenger.utils.serialization import save_pickle


@dataclass
class TrainingArtifacts:
    model: CatBoostForecaster
    training_frame: pd.DataFrame


def build_training_frame(config: ProjectConfig) -> pd.DataFrame:
    train_path = config.resolve_path("data", "train_csv")
    frame = load_train_csv(train_path)

    source_voltage_path = config.resolve_path("data", "source_voltage_csv")
    source_type_voltage_path = config.resolve_path("data", "source_type_voltage_csv")
    source_voltage = load_reference_table(source_voltage_path)
    source_type_voltage = load_reference_table(source_type_voltage_path)
    frame = merge_source_metadata(frame, source_voltage, source_type_voltage)

    climate_path = config.resolve_path("data", "climate_xlsx", default="data/external/Kalam Climate Data.xlsx")
    if climate_path.exists():
        climate_df = load_climate_xlsx(climate_path)
        frame = merge_climate_daily(frame, climate_df)

    frame = add_daily_time_features(frame)

    excluded_devices = set(config.get("training", "excluded_devices", default=[18]))
    if excluded_devices:
        frame = frame[~frame["consumer_device"].isin(excluded_devices)].copy()

    high_sources = set(config.get("training", "high_kwh_sources", default=[]))
    cutoff_date = pd.to_datetime(config.get("training", "cutoff_date_for_high_sources", default="2024-08-24"))
    if high_sources:
        frame = frame[~((frame["Source"].isin(high_sources)) & (frame["Date"] < cutoff_date))].copy()

    return frame


def train_catboost_from_config(config: ProjectConfig) -> TrainingArtifacts:
    frame = build_training_frame(config)
    model = CatBoostForecaster(
        iterations=int(config.get("model", "catboost", "iterations", default=12_000)),
        early_stopping_rounds=int(config.get("model", "catboost", "early_stopping_rounds", default=100)),
        random_state=int(config.get("model", "catboost", "random_state", default=42)),
        verbose=int(config.get("model", "catboost", "verbose", default=500)),
    ).fit(frame)
    return TrainingArtifacts(model=model, training_frame=frame)


def persist_training_artifacts(artifacts: TrainingArtifacts, output_path: str | Path) -> None:
    payload = {
        "model": artifacts.model,
        "feature_names": artifacts.model.feature_names,
    }
    save_pickle(payload, output_path)
