from __future__ import annotations

import math

import pandas as pd


def align_to_sample_submission(
    prediction_df: pd.DataFrame,
    sample_submission: pd.DataFrame,
) -> pd.DataFrame:
    base = sample_submission.copy()
    base = base.drop(columns=["kwh"], errors="ignore")
    merged = base.merge(prediction_df[["ID", "kwh"]], on="ID", how="left")
    merged["kwh"] = merged["kwh"].fillna(0).clip(lower=0)
    return merged


def merge_predictions(base_submission: pd.DataFrame, override_df: pd.DataFrame) -> pd.DataFrame:
    merged = base_submission.copy().set_index("ID")
    override = override_df.copy().set_index("ID")
    merged.update(override[["kwh"]])
    return merged.reset_index()


def validate_submission_ids(prediction_df: pd.DataFrame, sample_submission: pd.DataFrame) -> dict[str, set[str]]:
    pred_ids = set(prediction_df["ID"])
    sample_ids = set(sample_submission["ID"])
    return {
        "prediction_only": pred_ids - sample_ids,
        "sample_only": sample_ids - pred_ids,
    }


def rmse(y_true: pd.Series, y_pred: pd.Series) -> float:
    diff = (y_true.astype(float) - y_pred.astype(float)) ** 2
    return math.sqrt(float(diff.mean()))
