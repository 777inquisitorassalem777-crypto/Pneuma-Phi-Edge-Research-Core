"""
Описание каналов Голубой Матрицы: модальности, нормализация, калибровка.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Dict, Optional, Any
from enum import Enum


class Modality(str, Enum):
    PHYSIOLOGY = "physiology"
    ENVIRONMENT = "environment"
    SOCIAL = "social"
    META = "meta"
    PROPRIOCEPTION = "proprioception"
    ACOUSTIC = "acoustic"


@dataclass
class ChannelSpec:
    """Спецификация одного сенсорного канала."""
    sensor_id: str
    modality: Modality
    confidence: float = 0.8
    # Функция нормализации: raw -> [0, 1]
    # Если None — значение уже нормализовано
    normalizer: Optional[Callable[[float], float]] = None
    unit: str = ""
    description: str = ""
    enabled: bool = True
    # Калибровочные точки (raw_min, raw_max) для линейной шкалы
    raw_min: float = 0.0
    raw_max: float = 1.0

    def normalize(self, raw: float) -> float:
        if self.normalizer is not None:
            return max(0.0, min(1.0, float(self.normalizer(raw))))
        # Линейная калибровка
        span = self.raw_max - self.raw_min
        if span <= 0:
            return 0.0
        return max(0.0, min(1.0, (raw - self.raw_min) / span))


def _clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


def default_channel_registry() -> Dict[str, ChannelSpec]:
    """Реестр каналов по умолчанию (PNEUMA SensorFrame + meta)."""
    return {
        "hrv": ChannelSpec(
            sensor_id="hrv",
            modality=Modality.PHYSIOLOGY,
            confidence=0.90,
            normalizer=lambda v: _clamp01(v / 100.0),
            unit="ms",
            description="Heart rate variability (RMSSD-like proxy)",
            raw_min=10.0,
            raw_max=100.0,
        ),
        "heart_rate": ChannelSpec(
            sensor_id="heart_rate",
            modality=Modality.PHYSIOLOGY,
            confidence=0.88,
            normalizer=lambda v: _clamp01((v - 40.0) / 80.0),
            unit="bpm",
            description="Heart rate",
            raw_min=40.0,
            raw_max=120.0,
        ),
        "stress": ChannelSpec(
            sensor_id="stress",
            modality=Modality.PHYSIOLOGY,
            confidence=0.85,
            normalizer=lambda v: _clamp01(v / 10.0),
            unit="0-10",
            description="Subjective stress",
        ),
        "focus": ChannelSpec(
            sensor_id="focus",
            modality=Modality.PHYSIOLOGY,
            confidence=0.80,
            normalizer=lambda v: _clamp01(v / 10.0),
            unit="0-10",
            description="Subjective focus / attention",
        ),
        "sleep_debt": ChannelSpec(
            sensor_id="sleep_debt",
            modality=Modality.PHYSIOLOGY,
            confidence=0.80,
            normalizer=lambda v: _clamp01(v / 10.0),
            unit="0-10",
            description="Accumulated sleep debt proxy",
        ),
        "respiration": ChannelSpec(
            sensor_id="respiration",
            modality=Modality.PHYSIOLOGY,
            confidence=0.75,
            normalizer=lambda v: _clamp01((v - 8.0) / 20.0),
            unit="breaths/min",
            description="Respiration rate",
            raw_min=8.0,
            raw_max=28.0,
        ),
        "isolation": ChannelSpec(
            sensor_id="isolation",
            modality=Modality.SOCIAL,
            confidence=0.75,
            normalizer=lambda v: _clamp01(v / 10.0),
            unit="0-10",
            description="Social isolation proxy",
        ),
        "co2": ChannelSpec(
            sensor_id="co2",
            modality=Modality.ENVIRONMENT,
            confidence=0.70,
            normalizer=lambda v: _clamp01((v - 400.0) / 1200.0),
            unit="ppm",
            description="CO2 concentration",
            raw_min=400.0,
            raw_max=1600.0,
        ),
        "noise": ChannelSpec(
            sensor_id="noise",
            modality=Modality.ACOUSTIC,
            confidence=0.70,
            normalizer=lambda v: _clamp01(v / 80.0),
            unit="dB",
            description="Ambient noise level",
            raw_min=20.0,
            raw_max=80.0,
        ),
        "infrasound": ChannelSpec(
            sensor_id="infrasound",
            modality=Modality.ACOUSTIC,
            confidence=0.65,
            normalizer=lambda v: _clamp01(v / 60.0),
            unit="dB",
            description="Infrasound level",
            raw_min=20.0,
            raw_max=60.0,
        ),
        "light": ChannelSpec(
            sensor_id="light",
            modality=Modality.ENVIRONMENT,
            confidence=0.65,
            normalizer=lambda v: _clamp01(v / 500.0),
            unit="lux",
            description="Ambient light",
            raw_min=0.0,
            raw_max=500.0,
        ),
        "temperature": ChannelSpec(
            sensor_id="temperature",
            modality=Modality.ENVIRONMENT,
            confidence=0.70,
            normalizer=lambda v: _clamp01((v - 15.0) / 20.0),
            unit="°C",
            description="Ambient temperature",
            raw_min=15.0,
            raw_max=35.0,
        ),
        "humidity": ChannelSpec(
            sensor_id="humidity",
            modality=Modality.ENVIRONMENT,
            confidence=0.70,
            normalizer=lambda v: _clamp01(v / 100.0),
            unit="%",
            description="Relative humidity",
        ),
        "ethical_tension": ChannelSpec(
            sensor_id="ethical_tension",
            modality=Modality.META,
            confidence=0.60,
            normalizer=lambda v: _clamp01(v),
            unit="0-1",
            description="Derived ethical tension (from risk/patterns), not a physical field",
        ),
    }
