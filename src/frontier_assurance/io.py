from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


def load_structured(path: str | Path) -> dict[str, Any]:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        data = json.loads(text)
    else:
        data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise TypeError(f"Expected mapping at document root: {path}")
    return data
