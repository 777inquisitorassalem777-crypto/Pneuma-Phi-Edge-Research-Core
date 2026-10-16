"""
Голубая Матрица — мост между физическими/симулированными сенсорами
и ядром PNEUMA / Sophia.

Не утверждает существование «энергетических полей».
Нормализует измеримые сигналы в единый формат.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
import math


@dataclass
class SensorReading:
    sensor_id: str
    modality: str
    value: float          # обычно 0..1 или -1..1
    confidence: float
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    note: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class BlueMatrix:
    """
    Интерфейс «Голубая Матрица».
    В реальной системе — драйверы датчиков.
    Здесь — нормализация кадров PNEUMA SensorFrame + мета-сигналы.
    """

    def __init__(self, max_history: int = 500):
        self.history: List[List[SensorReading]] = []
        self.max_history = max_history
        self.active = {
            "hrv": 0.9,
            "stress": 0.85,
            "focus": 0.8,
            "co2": 0.7,
            "noise": 0.7,
            "light": 0.65,
            "isolation": 0.75,
            "ethical_tension": 0.6,  # производный мета-сигнал, не «поле»
        }

    def from_pneuma_frame(self, frame: Any, report: Any = None) -> List[SensorReading]:
        """Преобразует SensorFrame PNEUMA в показания Голубой Матрицы."""
        readings: List[SensorReading] = []

        def add(sid: str, modality: str, value: float, conf: float, note: str = ""):
            readings.append(SensorReading(
                sensor_id=sid, modality=modality,
                value=round(max(0.0, min(1.0, value)), 4),
                confidence=conf, note=note,
            ))

        # Физиология
        add("hrv", "physiology", min(1.0, frame.hrv_ms / 100.0), self.active["hrv"])
        add("stress", "physiology", frame.subjective_stress / 10.0, self.active["stress"])
        add("focus", "physiology", frame.focus / 10.0, self.active["focus"])
        add("sleep_debt", "physiology", frame.sleep_debt / 10.0, 0.8)
        add("isolation", "social", frame.social_isolation / 10.0, self.active["isolation"])

        # Среда
        add("co2", "environment", min(1.0, max(0.0, (frame.co2_ppm - 400) / 1200.0)), self.active["co2"])
        add("noise", "environment", min(1.0, frame.noise_db / 80.0), self.active["noise"])
        add("light", "environment", min(1.0, frame.ambient_light_lux / 500.0), self.active["light"])
        add("infrasound", "environment", min(1.0, frame.infrasound_db / 60.0), 0.65)

        # Мета-сигнал этического напряжения (производный, не мистика)
        ethical_tension = 0.3
        if report is not None:
            ethical_tension = min(1.0, report.risk * 0.7 + (0.3 if "moral_erosion_proxy" in report.patterns else 0.0))
        add("ethical_tension", "meta", ethical_tension, self.active["ethical_tension"],
            note="derived from risk + patterns, not a physical field")

        self.history.append(readings)
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
        return readings

    def aggregate(self, readings: List[SensorReading]) -> Dict[str, float]:
        """Сводка по модальностям."""
        buckets: Dict[str, List[float]] = {}
        for r in readings:
            buckets.setdefault(r.modality, []).append(r.value)
        return {m: sum(vs) / len(vs) for m, vs in buckets.items()}

    def health_score(self, readings: List[SensorReading]) -> float:
        """Простой интегральный показатель «устойчивости» 0..1."""
        agg = self.aggregate(readings)
        # высокий stress/isolation/ethical_tension → ниже health
        stress = agg.get("physiology", 0.5)
        # invert stress-like signals roughly
        hrv_like = next((r.value for r in readings if r.sensor_id == "hrv"), 0.5)
        stress_v = next((r.value for r in readings if r.sensor_id == "stress"), 0.5)
        isol = next((r.value for r in readings if r.sensor_id == "isolation"), 0.3)
        eth = next((r.value for r in readings if r.sensor_id == "ethical_tension"), 0.3)
        score = (
            hrv_like * 0.35
            + (1.0 - stress_v) * 0.30
            + (1.0 - isol) * 0.15
            + (1.0 - eth) * 0.20
        )
        return max(0.0, min(1.0, score))
