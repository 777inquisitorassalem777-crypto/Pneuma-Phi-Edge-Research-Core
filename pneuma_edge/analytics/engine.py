"""Улучшенный аналитический движок."""

from typing import List
from ..core.models import SensorFrame, PatternReport


class AnalyticsEngine:
    def __init__(self):
        self.hrv_history: List[float] = []
        self.stress_history: List[float] = []
        self.focus_history: List[float] = []

    def analyze(self, frame: SensorFrame) -> PatternReport:
        self.hrv_history.append(frame.hrv_ms)
        self.stress_history.append(frame.subjective_stress)
        self.focus_history.append(frame.focus)

        arousal = self._normalize(
            (frame.subjective_stress / 10.0) * 0.55
            + (1.0 - min(frame.hrv_ms / 80.0, 1.0)) * 0.30
            + (frame.sleep_debt / 10.0) * 0.15
        )
        recovery = self._normalize(
            (frame.hrv_ms / 90.0) * 0.45
            + (1.0 - frame.subjective_stress / 10.0) * 0.30
            + (1.0 - frame.sleep_debt / 10.0) * 0.25
        )
        coherence = self._normalize(frame.focus / 10.0)
        risk = self._compute_risk(frame, recovery, arousal)
        patterns = self._detect_patterns(frame, recovery, arousal)

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
        )

    @staticmethod
    def _normalize(value: float) -> float:
        return max(0.0, min(1.0, value))

    def _compute_risk(self, frame: SensorFrame, recovery: float, arousal: float) -> float:
        hrv_drop = 0.0
        if len(self.hrv_history) >= 10:
            baseline = sum(self.hrv_history[-10:-5]) / 5
            current = sum(self.hrv_history[-5:]) / 5
            hrv_drop = max(0.0, (baseline - current) / max(baseline, 1.0))

        environmental_load = (
            max(0.0, (frame.co2_ppm - 800.0) / 1000.0)
            + max(0.0, (frame.infrasound_db - 40.0) / 30.0)
            + max(0.0, (frame.noise_db - 45.0) / 25.0)
        )
        social_load = frame.social_isolation / 10.0

        return self._normalize(
            arousal * 0.40
            + (1 - recovery) * 0.25
            + hrv_drop * 0.12
            + min(environmental_load, 1.0) * 0.13
            + social_load * 0.10
        )

    def _detect_patterns(self, frame: SensorFrame, recovery: float, arousal: float) -> list:
        patterns = []
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

        # Руминативная петля (прокси)
        if len(self.stress_history) >= 12:
            recent = self.stress_history[-12:]
            if sum(1 for x in recent if x >= 6.0) >= 8:
                patterns.append("persistent_stress_loop")
            if sum(1 for x in recent if x >= 5.5) >= 9 and frame.focus <= 4.5:
                patterns.append("rumination_loop")

        # Моральная эрозия (прокси: высокий стресс + низкий фокус + изоляция)
        if (frame.subjective_stress >= 6.5 and frame.focus <= 4.0
                and frame.social_isolation >= 5.0):
            patterns.append("moral_erosion_proxy")

        return patterns
