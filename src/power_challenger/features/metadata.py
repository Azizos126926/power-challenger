from __future__ import annotations

import pandas as pd


def merge_source_metadata(
    df: pd.DataFrame,
    source_voltage: pd.DataFrame | None = None,
    source_type_voltage: pd.DataFrame | None = None,
) -> pd.DataFrame:
    frame = df.copy()
    if source_voltage is not None and "Source" in frame.columns:
        frame = frame.merge(source_voltage, on="Source", how="left")
    if source_type_voltage is not None and "Source" in frame.columns:
        frame = frame.merge(source_type_voltage, on="Source", how="left")
    return frame
