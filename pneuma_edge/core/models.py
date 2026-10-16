"""Расширенные модели данных."""

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any


@dataclass
class SensorFrame:
    step: int
    timestamp: float
    # Физиология
    hrv_ms: float
    heart_rate: float
    # Среда
    temperature_c: float
    humidity_pct: float
    co2_ppm: float
    magnetic_ut: float
    electrostatic_v: float
    infrasound_db: float
    ambient_light_lux: float = 300.0
    noise_db: float = 35.0
    # Субъективные / прокси
    subjective_stress: float = 4.0
    focus: float = 6.0
    sleep_debt: float = 0.0          # 0–10
    social_isolation: float = 0.0    # 0–10

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PatternReport:
    step: int
    arousal: float
    recovery: float
    coherence: float
    risk: float
    patterns: List[str] = field(default_factory=list)
    interpretation: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Decision:
    step: int
    action: str
    approved: bool
    reason: str
    uncertainty: float
    source: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
