"""
Голубая Матрица (Blue Matrix) — полноценная реализация.

Мост между сенсорами (симулятор / железо) и ядром PNEUMA/Sophia.
Нормализует сигналы, фильтрует, агрегирует, считает health_score.

Не утверждает существование «энергетических полей».
ethical_tension — производный мета-сигнал из risk/patterns.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone

from .channels import ChannelSpec, Modality, default_channel_registry
from .filters import ChannelFilterPipeline
from .adapters import SensorAdapter, PneumaFrameAdapter


@dataclass
class SensorReading:
    sensor_id: str
    modality: str
    value: float
    confidence: float
    raw: float = 0.0
    filtered: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    note: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class MatrixSnapshot:
    """Снимок состояния матрицы на один шаг."""
    step: int
    readings: List[SensorReading]
    aggregate: Dict[str, float]
    health_score: float
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "step": self.step,
            "readings": [r.to_dict() for r in self.readings],
            "aggregate": self.aggregate,
            "health_score": self.health_score,
            "timestamp": self.timestamp,
        }


class BlueMatrix:
    """
    Полная реализация Голубой Матрицы.

    Поток:
      adapter.read_raw() -> normalize -> filter -> SensorReading[]
        -> aggregate by modality -> health_score -> MatrixSnapshot
    """

    HEALTH_WEIGHTS = {
        "hrv": 0.28,
        "stress_inv": 0.24,
        "focus": 0.12,
        "isolation_inv": 0.12,
        "ethical_inv": 0.14,
        "env_load_inv": 0.10,
    }

    def __init__(
        self,
        adapter: Optional[SensorAdapter] = None,
        max_history: int = 500,
        enable_filters: bool = True,
        channels: Optional[Dict[str, ChannelSpec]] = None,
    ):
        self.adapter: SensorAdapter = adapter or PneumaFrameAdapter()
        self.max_history = max_history
        self.enable_filters = enable_filters
        self.channels: Dict[str, ChannelSpec] = channels or default_channel_registry()
        self.filters: Dict[str, ChannelFilterPipeline] = {
            cid: ChannelFilterPipeline(use_ma=False, ema_alpha=0.35)
            for cid in self.channels
        }
        self.history: List[MatrixSnapshot] = []
        self._step = 0

    def from_pneuma_frame(self, frame: Any, report: Any = None) -> List[SensorReading]:
        """Обратная совместимость с оркестратором симбиоза."""
        snap = self.ingest(frame=frame, report=report)
        return snap.readings

    def ingest(
        self,
        frame: Any = None,
        report: Any = None,
        raw: Optional[Dict[str, float]] = None,
    ) -> MatrixSnapshot:
        if raw is None:
            raw = self.adapter.read_raw(frame=frame, report=report)

        readings: List[SensorReading] = []
        for sid, spec in self.channels.items():
            if not spec.enabled:
                continue
            if sid not in raw:
                continue
            raw_val = float(raw[sid])
            norm = spec.normalize(raw_val)
            filtered = self.filters[sid].process(norm) if self.enable_filters else norm
            note = ""
            if sid == "ethical_tension":
                note = "derived from risk+patterns, not a physical field"
            readings.append(SensorReading(
                sensor_id=sid,
                modality=spec.modality.value if isinstance(spec.modality, Modality) else str(spec.modality),
                value=round(filtered, 4),
                confidence=spec.confidence,
                raw=raw_val,
                filtered=round(filtered, 4),
                note=note,
            ))

        agg = self.aggregate(readings)
        health = self.health_score(readings)
        snap = MatrixSnapshot(
            step=self._step,
            readings=readings,
            aggregate=agg,
            health_score=round(health, 4),
        )
        self._step += 1
        self.history.append(snap)
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
        return snap

    def aggregate(self, readings: List[SensorReading]) -> Dict[str, float]:
        buckets: Dict[str, List[float]] = {}
        for r in readings:
            buckets.setdefault(r.modality, []).append(r.value)
        return {m: round(sum(vs) / len(vs), 4) for m, vs in buckets.items() if vs}

    def health_score(self, readings: List[SensorReading]) -> float:
        by_id = {r.sensor_id: r.value for r in readings}
        hrv = by_id.get("hrv", 0.5)
        stress = by_id.get("stress", 0.5)
        focus = by_id.get("focus", 0.5)
        isolation = by_id.get("isolation", 0.3)
        ethical = by_id.get("ethical_tension", 0.3)
        env_vals = [by_id[k] for k in ("co2", "noise", "infrasound") if k in by_id]
        env_load = sum(env_vals) / len(env_vals) if env_vals else 0.3

        w = self.HEALTH_WEIGHTS
        score = (
            w["hrv"] * hrv
            + w["stress_inv"] * (1.0 - stress)
            + w["focus"] * focus
            + w["isolation_inv"] * (1.0 - isolation)
            + w["ethical_inv"] * (1.0 - ethical)
            + w["env_load_inv"] * (1.0 - env_load)
        )
        return max(0.0, min(1.0, score))

    def get_channel(self, sensor_id: str) -> Optional[ChannelSpec]:
        return self.channels.get(sensor_id)

    def set_channel_enabled(self, sensor_id: str, enabled: bool) -> None:
        if sensor_id in self.channels:
            self.channels[sensor_id].enabled = enabled

    def calibrate(self, sensor_id: str, raw_min: float, raw_max: float) -> None:
        spec = self.channels.get(sensor_id)
        if spec is None:
            raise KeyError(f"Unknown channel: {sensor_id}")
        spec.raw_min = raw_min
        spec.raw_max = raw_max
        spec.normalizer = None

    def reset_filters(self) -> None:
        for f in self.filters.values():
            f.reset()

    def reset(self) -> None:
        self.history.clear()
        self._step = 0
        self.reset_filters()

    def summary(self) -> Dict[str, Any]:
        if not self.history:
            return {"steps": 0, "avg_health": 0.0}
        scores = [s.health_score for s in self.history]
        return {
            "steps": len(self.history),
            "avg_health": round(sum(scores) / len(scores), 4),
            "min_health": round(min(scores), 4),
            "max_health": round(max(scores), 4),
            "channels_enabled": sum(1 for c in self.channels.values() if c.enabled),
            "epistemic_status": "sensor_normalization_layer_not_metaphysics",
        }

    def last_snapshot(self) -> Optional[MatrixSnapshot]:
        return self.history[-1] if self.history else None
