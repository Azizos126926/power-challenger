import pytest
import pandas as pd

from power_challenger.models.heuristics import (
    apply_device_scaling,
    device18_peak_decline_forecast,
)


def test_device18_peak_decline_forecast_builds_expected_rows():
    df = pd.DataFrame(
        {
            "Source": ["consumer_device_18_data_user_1"] * 3,
            "Date": ["2024-01-01", "2024-01-02", "2024-01-03"],
            "kwh": [10.0, 11.0, 12.0],
            "consumer_device": [18, 18, 18],
            "data_user": [1, 1, 1],
        }
    )
    forecast = device18_peak_decline_forecast(df, forecast_horizon=6)
    assert len(forecast) == 6
    assert forecast.iloc[0]["ID"].startswith("2024-01-04_consumer_device_18_data_user_1")
    assert forecast["kwh"].iloc[0] == 12.0


def test_apply_device_scaling_scales_target_devices_only():
    submission = pd.DataFrame(
        {
            "ID": [
                "2024-01-01_consumer_device_13_data_user_1",
                "2024-01-01_consumer_device_8_data_user_1",
            ],
            "kwh": [10.0, 10.0],
        }
    )
    scaled = apply_device_scaling(submission, {13: 0.92})
    assert scaled["kwh"].iloc[0] == pytest.approx(9.2)
    assert scaled["kwh"].iloc[1] == 10.0
