"""Расширенный аналитический движок."""

from __future__ import annotations
from typing import List, Dict, Any
from ..core.models import SensorFrame, PatternReport


class AnalyticsEngine:
    """
    Вычисляет arousal, recovery, coherence, risk и детектирует паттерны.
    Все выводы — наблюдения и интерпретации, не диагнозы.
    """

    def __init__(self, window: int = 12):
        self.window = window
        self.hrv_history: List[float] = []
        self.stress_history: List[float] = []
        self.focus_history: List[float] = []
        self.risk_history: List[float] = []

    def analyze(self, frame: SensorFrame) -> PatternReport:
        self.hrv_history.append(frame.hrv_ms)
        self.stress_history.append(frame.subjective_stress)
        self.focus_history.append(frame.focus)

        arousal = self._normalize(
            (frame.subjective_stress / 10.0) * 0.50
            + (1.0 - min(frame.hrv_ms / 80.0, 1.0)) * 0.28
            + (frame.sleep_debt / 10.0) * 0.12
            + (frame.respiration_rate - 12) / 20.0 * 0.10
        )
        recovery = self._normalize(
            (frame.hrv_ms / 90.0) * 0.42
            + (1.0 - frame.subjective_stress / 10.0) * 0.28
            + (1.0 - frame.sleep_debt / 10.0) * 0.20
            + (frame.focus / 10.0) * 0.10
        )
        coherence = self._normalize(
            (frame.focus / 10.0) * 0.60
            + (1.0 - abs(frame.respiration_rate - 12) / 15.0) * 0.25
            + (frame.hrv_ms / 100.0) * 0.15
        )
        risk = self._compute_risk(frame, recovery, arousal)
        self.risk_history.append(risk)
        patterns = self._detect_patterns(frame, recovery, arousal, coherence)

        if not patterns:
            interpretation = "Значимых деструктивных паттернов не обнаружено."
        else:
            interpretation = (
                "Обнаружены состояния, требующие паузы, границ и восстановления. "
                "Это наблюдение, а не диагноз и не утверждение о внешнем вмешательстве."
            )

        return PatternReport(
            step=frame.step,
            arousal=round(arousal, 3),
            recovery=round(recovery, 3),
            coherence=round(coherence, 3),
            risk=round(risk, 3),
            patterns=patterns,
            interpretation=interpretation,
            confidence=self._confidence(patterns),
        )

    @staticmethod
    def _normalize(value: float) -> float:
        return max(0.0, min(1.0, value))

    def _compute_risk(self, frame: SensorFrame, recovery: float, arousal: float) -> float:
        hrv_drop = 0.0
        if len(self.hrv_history) >= 10:
            baseline = sum(self.hrv_history[-10:-5]) / 5.0
            current = sum(self.hrv_history[-5:]) / 5.0
            hrv_drop = max(0.0, (baseline - current) / max(baseline, 1.0))

        environmental_load = (
            max(0.0, (frame.co2_ppm - 800.0) / 1000.0)
            + max(0.0, (frame.infrasound_db - 40.0) / 30.0)
            + max(0.0, (frame.noise_db - 45.0) / 25.0)
            + max(0.0, (100.0 - frame.ambient_light_lux) / 200.0)
        )
        social_load = frame.social_isolation / 10.0
        physiological_strain = max(0.0, (frame.respiration_rate - 16) / 15.0)

        return self._normalize(
            arousal * 0.36
            + (1.0 - recovery) * 0.24
            + hrv_drop * 0.12
            + min(environmental_load, 1.0) * 0.14
            + social_load * 0.08
            + physiological_strain * 0.06
        )

    def _detect_patterns(self, frame: SensorFrame, recovery: float, arousal: float, coherence: float) -> List[str]:
        patterns: List[str] = []
        if arousal >= 0.65:
            patterns.append("high_arousal")
        if frame.subjective_stress >= 7.0:
            patterns.append("subjective_distress")
        if recovery <= 0.30:
            patterns.append("low_recovery")
        if frame.hrv_ms <= 35.0:
            patterns.append("low_hrv")
        if frame.focus <= 3.0:
            patterns.append("attention_depletion")
        if coherence <= 0.30:
            patterns.append("low_coherence")
        if frame.co2_ppm >= 1000.0:
            patterns.append("poor_air_quality")
        if frame.infrasound_db >= 45.0:
            patterns.append("acoustic_load")
        if frame.noise_db >= 50.0:
            patterns.append("noise_stress")
        if frame.sleep_debt >= 6.0:
            patterns.append("sleep_debt")
        if frame.social_isolation >= 7.0:
            patterns.append("social_isolation")
        if frame.ambient_light_lux < 100.0:
            patterns.append("low_light")
        if frame.respiration_rate >= 20.0:
            patterns.append("elevated_respiration")

        if len(self.stress_history) >= self.window:
            recent = self.stress_history[-self.window:]
            if sum(1 for x in recent if x >= 6.0) >= int(self.window * 0.65):
                patterns.append("persistent_stress_loop")
            if (sum(1 for x in recent if x >= 5.5) >= int(self.window * 0.7)
                    and frame.focus <= 4.5):
                patterns.append("rumination_loop")

        if (frame.subjective_stress >= 6.5 and frame.focus <= 4.0
                and frame.social_isolation >= 5.0):
            patterns.append("moral_erosion_proxy")

        if len(self.risk_history) >= 8:
            if sum(1 for r in self.risk_history[-8:] if r >= 0.6) >= 6:
                patterns.append("sustained_high_risk")

        return patterns

    def _confidence(self, patterns: List[str]) -> float:
        if not patterns:
            return 0.85
        base = 0.70
        if "persistent_stress_loop" in patterns or "rumination_loop" in patterns:
            base += 0.10
        if len(patterns) >= 4:
            base += 0.05
        return min(0.95, base)

    def summary(self) -> Dict[str, Any]:
        if not self.risk_history:
            return {"status": "no_data"}
        return {
            "steps_analyzed": len(self.risk_history),
            "avg_risk": round(sum(self.risk_history) / len(self.risk_history), 3),
            "max_risk": round(max(self.risk_history), 3),
            "avg_hrv": round(sum(self.hrv_history) / len(self.hrv_history), 2) if self.hrv_history else 0,
            "avg_stress": round(sum(self.stress_history) / len(self.stress_history), 2) if self.stress_history else 0,
        }
