from __future__ import annotations

from pathlib import Path
import pickle
from typing import Any


def save_pickle(obj: Any, path: str | Path) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("wb") as fp:
        pickle.dump(obj, fp)


def load_pickle(path: str | Path) -> Any:
    with Path(path).open("rb") as fp:
        return pickle.load(fp)
