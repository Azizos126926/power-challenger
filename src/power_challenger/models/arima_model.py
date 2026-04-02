from __future__ import annotations

import pandas as pd


def groupwise_arima_forecast(
    df: pd.DataFrame,
    forecast_horizon: int = 30,
    order: tuple[int, int, int] = (7, 1, 3),
) -> pd.DataFrame:
    try:
        from statsmodels.tsa.arima.model import ARIMA
    except ImportError as exc:
        raise ImportError(
            "statsmodels is required for ARIMA forecasting. Install with `pip install statsmodels`."
        ) from exc

    frame = df.copy()
    frame["Date"] = pd.to_datetime(frame["Date"])
    results: list[pd.DataFrame] = []

    for (consumer_device, data_user), group in frame.groupby(["consumer_device", "data_user"]):
        series = group.sort_values("Date").set_index("Date").asfreq("D")["kwh"].ffill()
        model = ARIMA(series, order=order).fit()
        forecast_values = model.forecast(steps=forecast_horizon)
        forecast_dates = pd.date_range(
            start=series.index.max() + pd.Timedelta(days=1),
            periods=forecast_horizon,
            freq="D",
        )
        forecast_df = pd.DataFrame(
            {
                "ID": [
                    f"{date.strftime('%Y-%m-%d')}_consumer_device_{int(consumer_device)}_data_user_{int(data_user)}"
                    for date in forecast_dates
                ],
                "kwh": forecast_values,
            }
        )
        results.append(forecast_df)

    return pd.concat(results, ignore_index=True)
