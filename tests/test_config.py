from pathlib import Path

from power_challenger.config import load_config


def test_load_config_and_resolve_paths():
    config = load_config("configs/default.yaml")
    train_path = config.resolve_path("data", "train_csv")
    assert train_path.name == "aggday.csv"
    assert train_path.exists()
