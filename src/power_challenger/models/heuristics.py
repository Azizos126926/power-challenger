from __future__ import annotations

import numpy as np
import pandas as pd


def device18_peak_decline_forecast(
    df: pd.DataFrame,
    forecast_horizon: int = 30,
    peak_ratio: float = 1.10,
    final_ratio: float = 0.13,
) -> pd.DataFrame:
    working = df.copy()
    working["Date"] = pd.to_datetime(working["Date"])
    device_data = working[working["consumer_device"] == 18].copy()
    forecasts: list[pd.DataFrame] = []

    for data_user, user_group in device_data.groupby("data_user"):
        user_group = user_group.sort_values("Date")
        last_val = float(user_group["kwh"].iloc[-1])
        peak_val = last_val * peak_ratio
        final_val = last_val * final_ratio

        phase_1 = np.linspace(last_val, peak_val, 4)
        phase_2 = np.array([peak_val])
        decline_days = forecast_horizon - len(phase_1) - len(phase_2)
        phase_3 = np.linspace(peak_val, final_val, decline_days)
        forecast_values = np.concatenate([phase_1, phase_2, phase_3])

        forecast_dates = pd.date_range(
            start=user_group["Date"].max() + pd.Timedelta(days=1),
            periods=forecast_horizon,
            freq="D",
        )

        forecasts.append(
            pd.DataFrame(
                {
                    "ID": [
                        f"{date.strftime('%Y-%m-%d')}_consumer_device_18_data_user_{int(data_user)}"
                        for date in forecast_dates
                    ],
                    "kwh": forecast_values,
                }
            )
        )

    if not forecasts:
        return pd.DataFrame(columns=["ID", "kwh"])
    return pd.concat(forecasts, ignore_index=True)


def apply_device_scaling(
    submission: pd.DataFrame,
    scaling_rules: dict[int, float] | None = None,
) -> pd.DataFrame:
    rules = scaling_rules or {13: 0.92, 21: 0.90}
    frame = submission.copy()
    extracted = frame["ID"].str.extract(r"consumer_device_(\d+)_data_user_")
    frame["consumer_device"] = extracted[0].astype(int)
    for device, scale in rules.items():
        mask = frame["consumer_device"] == int(device)
        frame.loc[mask, "kwh"] = frame.loc[mask, "kwh"] * float(scale)
    return frame.drop(columns=["consumer_device"])
