"""
Адаптеры источников данных для Голубой Матрицы.

- PneumaFrameAdapter: из SensorFrame симулятора
- DictAdapter: из произвольного словаря raw-значений
- StubHardwareAdapter: заготовка под реальные датчики
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class SensorAdapter(ABC):
    """Базовый адаптер → словарь {sensor_id: raw_value}."""

    @abstractmethod
    def read_raw(self, frame: Any = None, report: Any = None) -> Dict[str, float]:
        ...


class PneumaFrameAdapter(SensorAdapter):
    """Читает поля PNEUMA SensorFrame (+ risk/patterns из report)."""

    def read_raw(self, frame: Any = None, report: Any = None) -> Dict[str, float]:
        if frame is None:
            return {}
        raw: Dict[str, float] = {
            "hrv": float(getattr(frame, "hrv_ms", 50.0)),
            "heart_rate": float(getattr(frame, "heart_rate", 70.0)),
            "stress": float(getattr(frame, "subjective_stress", 4.0)),
            "focus": float(getattr(frame, "focus", 6.0)),
            "sleep_debt": float(getattr(frame, "sleep_debt", 2.0)),
            "respiration": float(getattr(frame, "respiration_rate", 14.0)),
            "isolation": float(getattr(frame, "social_isolation", 2.0)),
            "co2": float(getattr(frame, "co2_ppm", 700.0)),
            "noise": float(getattr(frame, "noise_db", 35.0)),
            "infrasound": float(getattr(frame, "infrasound_db", 34.0)),
            "light": float(getattr(frame, "ambient_light_lux", 300.0)),
            "temperature": float(getattr(frame, "temperature_c", 22.0)),
            "humidity": float(getattr(frame, "humidity_pct", 45.0)),
        }
        # Meta: ethical tension from analytics report
        tension = 0.3
        if report is not None:
            risk = float(getattr(report, "risk", 0.0))
            patterns = list(getattr(report, "patterns", []) or [])
            tension = min(1.0, risk * 0.7 + (0.3 if "moral_erosion_proxy" in patterns else 0.0))
        raw["ethical_tension"] = tension
        return raw


class DictAdapter(SensorAdapter):
    """Произвольный словарь raw-значений."""

    def __init__(self, data: Optional[Dict[str, float]] = None):
        self.data = data or {}

    def read_raw(self, frame: Any = None, report: Any = None) -> Dict[str, float]:
        return dict(self.data)

    def update(self, data: Dict[str, float]) -> None:
        self.data.update(data)


class StubHardwareAdapter(SensorAdapter):
    """
    Заготовка под реальные датчики (Polar, CO2, микрофон и т.д.).
    Сейчас возвращает нейтральные значения; замените read_raw на драйверы.
    """

    def __init__(self):
        self._last: Dict[str, float] = {
            "hrv": 55.0,
            "heart_rate": 72.0,
            "stress": 3.0,
            "focus": 6.0,
            "co2": 650.0,
            "noise": 32.0,
            "light": 280.0,
            "ethical_tension": 0.2,
        }

    def read_raw(self, frame: Any = None, report: Any = None) -> Dict[str, float]:
        # TODO: подключить реальные SDK / serial / BLE
        return dict(self._last)

    def inject(self, **kwargs: float) -> None:
        """Для тестов и ручной подстановки."""
        self._last.update(kwargs)
