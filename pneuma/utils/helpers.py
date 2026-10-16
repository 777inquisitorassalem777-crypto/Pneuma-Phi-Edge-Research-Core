"""Вспомогательные утилиты."""

from __future__ import annotations
from typing import Any, Dict, List
import json
from pathlib import Path


def deep_get(d: Dict[str, Any], path: str, default: Any = None) -> Any:
    cur: Any = d
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return default
        cur = cur[part]
    return cur


def save_json(data: Any, path: str) -> None:
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_json(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sliding_average(values: List[float], window: int) -> List[float]:
    if window <= 0 or not values:
        return []
    result = []
    for i in range(len(values)):
        start = max(0, i - window + 1)
        chunk = values[start:i + 1]
        result.append(sum(chunk) / len(chunk))
    return result


def clamp(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, value))
