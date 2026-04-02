from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(slots=True)
class ProjectConfig:
    raw: dict[str, Any]
    root: Path

    def resolve_path(self, *keys: str, default: str | None = None) -> Path:
        value: Any = self.raw
        for key in keys:
            if not isinstance(value, dict) or key not in value:
                if default is None:
                    raise KeyError(" -> ".join(keys))
                return (self.root / default).resolve()
            value = value[key]
        if value is None:
            if default is None:
                raise KeyError(" -> ".join(keys))
            value = default
        return (self.root / str(value)).resolve()

    def get(self, *keys: str, default: Any = None) -> Any:
        value: Any = self.raw
        for key in keys:
            if not isinstance(value, dict) or key not in value:
                return default
            value = value[key]
        return value


def load_config(path: str | Path) -> ProjectConfig:
    config_path = Path(path).resolve()
    raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    return ProjectConfig(raw=raw, root=config_path.parent.parent)
