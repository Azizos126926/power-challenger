import pandas as pd

from power_challenger.utils.submission import (
    align_to_sample_submission,
    merge_predictions,
    validate_submission_ids,
)


def test_align_to_sample_submission_fills_missing_with_zero():
    predictions = pd.DataFrame(
        {
            "ID": ["2024-10-01_consumer_device_1_data_user_1"],
            "kwh": [2.5],
        }
    )
    sample = pd.DataFrame(
        {
            "ID": [
                "2024-10-01_consumer_device_1_data_user_1",
                "2024-10-02_consumer_device_1_data_user_1",
            ]
        }
    )
    aligned = align_to_sample_submission(predictions, sample)
    assert list(aligned["kwh"]) == [2.5, 0.0]


def test_merge_predictions_overrides_matching_ids():
    base = pd.DataFrame({"ID": ["a", "b"], "kwh": [1.0, 2.0]})
    override = pd.DataFrame({"ID": ["b"], "kwh": [9.0]})
    merged = merge_predictions(base, override)
    assert list(merged["kwh"]) == [1.0, 9.0]


def test_validate_submission_ids_detects_mismatch():
    pred = pd.DataFrame({"ID": ["a", "b"], "kwh": [1, 2]})
    sample = pd.DataFrame({"ID": ["b", "c"]})
    diff = validate_submission_ids(pred, sample)
    assert diff["prediction_only"] == {"a"}
    assert diff["sample_only"] == {"c"}
