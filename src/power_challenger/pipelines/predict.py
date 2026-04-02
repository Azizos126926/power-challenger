from __future__ import annotations

from pathlib import Path

import pandas as pd

from power_challenger.config import ProjectConfig
from power_challenger.data.io import load_climate_xlsx, load_sample_submission, load_train_csv, load_reference_table
from power_challenger.features.climate import merge_climate_daily
from power_challenger.features.metadata import merge_source_metadata
from power_challenger.features.temporal import add_daily_time_features
from power_challenger.models.heuristics import apply_device_scaling, device18_peak_decline_forecast
from power_challenger.utils.serialization import load_pickle
from power_challenger.utils.submission import align_to_sample_submission, merge_predictions


def _build_inference_frame(config: ProjectConfig, sample_submission: pd.DataFrame) -> pd.DataFrame:
    frame = sample_submission.copy()

    source_voltage_path = config.resolve_path("data", "source_voltage_csv")
    source_type_voltage_path = config.resolve_path("data", "source_type_voltage_csv")
    source_voltage = load_reference_table(source_voltage_path)
    source_type_voltage = load_reference_table(source_type_voltage_path)

    frame["Source"] = (
        "consumer_device_"
        + frame["consumer_device"].astype(str)
        + "_data_user_"
        + frame["data_user"].astype(str)
    )
    frame = merge_source_metadata(frame, source_voltage, source_type_voltage)

    climate_path = config.resolve_path("data", "climate_xlsx", default="data/external/Kalam Climate Data.xlsx")
    if climate_path.exists():
        climate_df = load_climate_xlsx(climate_path)
        frame = merge_climate_daily(frame, climate_df)

    frame = add_daily_time_features(frame)
    return frame


def predict_submission_from_config(
    config: ProjectConfig,
    model_path: str | Path,
) -> pd.DataFrame:
    sample_submission = load_sample_submission(config.resolve_path("data", "sample_submission_csv"))
    payload = load_pickle(model_path)
    model = payload["model"]

    inference_frame = _build_inference_frame(config, sample_submission)
    non_device_18 = inference_frame["consumer_device"] != 18
    catboost_predictions = sample_submission.copy()
    catboost_predictions["kwh"] = 0.0
    catboost_predictions.loc[non_device_18, "kwh"] = model.predict(inference_frame.loc[non_device_18]).clip(lower=0)

    train_df = load_train_csv(config.resolve_path("data", "train_csv"))
    heuristic_df = device18_peak_decline_forecast(
        train_df,
        forecast_horizon=int(config.get("inference", "forecast_horizon", default=30)),
        peak_ratio=float(config.get("inference", "device18_peak_ratio", default=1.10)),
        final_ratio=float(config.get("inference", "device18_final_ratio", default=0.13)),
    )

    combined = merge_predictions(catboost_predictions, heuristic_df)
    scaling_rules = config.get("inference", "scaling_rules", default={13: 0.92, 21: 0.90})
    combined = apply_device_scaling(combined, scaling_rules=scaling_rules)
    return align_to_sample_submission(combined, sample_submission)
