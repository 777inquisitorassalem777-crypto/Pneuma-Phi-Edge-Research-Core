"""Расширенные модели данных PNEUMA Full."""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional
from enum import Enum


class EpistemicStatus(str, Enum):
    OBSERVATION = "observation"
    INTERPRETATION = "interpretation"
    HYPOTHESIS = "hypothesis_not_fact"
    ARCHETYPAL = "archetypal_hypothesis_not_fact"
    ETHICAL_MODEL = "ethical_model_not_doctrine"
    GENERATED = "generated_hypothesis_not_fact"


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
    infrasound_db: float
    noise_db: float
    ambient_light_lux: float
    magnetic_ut: float = 45.0
    electrostatic_v: float = 120.0
    # Субъективные / прокси
    subjective_stress: float = 4.0
    focus: float = 6.0
    sleep_debt: float = 0.0
    social_isolation: float = 0.0
    # Дополнительно
    body_temperature_c: float = 36.6
    respiration_rate: float = 14.0

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
    confidence: float = 0.7

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class EthicalParameters:
    """Параметры этического выбора: мудрость, воля, любовь."""
    wisdom: float = 0.5      # 0..1 — учёт последствий и смирение
    will: float = 0.5        # 0..1 — сила выбора
    love: float = 0.5        # 0..1 — ориентация на сохранение живого
    courage: float = 0.5
    humility: float = 0.5

    def balance(self) -> float:
        """Общий этический баланс."""
        return (self.wisdom * 0.30 + self.will * 0.20 + self.love * 0.30 +
                self.courage * 0.10 + self.humility * 0.10)


@dataclass
class EthicalVerdict:
    action: str
    allowed: bool
    reason: str
    virtue_signal: float
    vice_signal: float
    uncertainty: float
    parameters_used: Optional[EthicalParameters] = None
    epistemic_status: str = EpistemicStatus.ETHICAL_MODEL.value

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        if self.parameters_used:
            d["parameters_used"] = asdict(self.parameters_used)
        return d


@dataclass
class DecisionRecord:
    step: int
    action: str
    verdict: EthicalVerdict
    context: Dict[str, Any] = field(default_factory=dict)
    human_override: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "step": self.step,
            "action": self.action,
            "verdict": self.verdict.to_dict(),
            "context": self.context,
            "human_override": self.human_override,
        }
