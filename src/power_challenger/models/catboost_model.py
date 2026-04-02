from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pandas as pd


@dataclass
class CatBoostForecaster:
    iterations: int = 12_000
    early_stopping_rounds: int = 100
    random_state: int = 42
    verbose: int = 500
    model: Any | None = None
    feature_names: list[str] = field(default_factory=list)

    def fit(self, train_df: pd.DataFrame, target_col: str = "kwh") -> "CatBoostForecaster":
        try:
            from catboost import CatBoostRegressor
            from sklearn.model_selection import train_test_split
        except ImportError as exc:
            raise ImportError(
                "CatBoost and scikit-learn are required for training. "
                "Install with `pip install catboost scikit-learn`."
            ) from exc

        features = train_df.drop(columns=[target_col, "Date"], errors="ignore")
        if "Source" in features.columns:
            features = features.drop(columns=["Source"])

        features = features.fillna(-1)
        target = train_df[target_col]

        stratify_col = features["consumer_device"] if "consumer_device" in features.columns else None
        x_train, x_valid, y_train, y_valid = train_test_split(
            features,
            target,
            random_state=self.random_state,
            shuffle=True,
            stratify=stratify_col,
        )

        self.feature_names = list(x_train.columns)
        self.model = CatBoostRegressor(
            iterations=self.iterations,
            loss_function="RMSE",
            use_best_model=True,
            early_stopping_rounds=self.early_stopping_rounds,
            verbose=self.verbose,
            random_state=self.random_state,
        )
        self.model.fit(x_train, y_train, eval_set=(x_valid, y_valid))
        return self

    def predict(self, frame: pd.DataFrame) -> pd.Series:
        if self.model is None:
            raise RuntimeError("Model has not been fitted yet.")
        features = frame.copy()
        for col in ["kwh", "ID", "Date", "Source"]:
            if col in features.columns:
                features = features.drop(columns=[col])
        features = features.fillna(-1)
        missing = [col for col in self.feature_names if col not in features.columns]
        if missing:
            for col in missing:
                features[col] = -1
        return pd.Series(self.model.predict(features[self.feature_names]), index=frame.index, name="kwh")
