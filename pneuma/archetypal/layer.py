"""
Архетипический слой.
Все выводы имеют статус archetypal_hypothesis_not_fact.
Не утверждает существование сущностей или душ.
"""

from __future__ import annotations
from typing import Dict, Any, List
from ..core.models import SensorFrame, PatternReport, EpistemicStatus


class ArchetypalLayer:
    """
    Преобразует наблюдаемые паттерны в язык архетипов
    (частота, руминации, уязвимость) строго как метафору.
    """

    def interpret(self, frame: SensorFrame, report: PatternReport) -> Dict[str, Any]:
        frequency_proxy = self._frequency_proxy(frame)
        rumination_proxy = self._rumination_proxy(frame, report)
        vulnerability = self._vulnerability(frequency_proxy, rumination_proxy, frame)
        labels = self._labels(frequency_proxy, rumination_proxy, vulnerability, report)
        narrative = self._narrative(labels, frequency_proxy, rumination_proxy, vulnerability)

        return {
            "layer": "archetypal",
            "epistemic_status": EpistemicStatus.ARCHETYPAL.value,
            "disclaimer": (
                "Это интерпретативная модель, вдохновлённая мифологическими "
                "и эзотерическими образами. Она не является утверждением о "
                "реальном существовании сущностей, душ или их взаимодействии."
            ),
            "frequency_proxy": round(frequency_proxy, 3),
            "rumination_proxy": round(rumination_proxy, 3),
            "vulnerability_proxy": round(vulnerability, 3),
            "archetypal_labels": labels,
            "narrative": narrative,
            "mapping_note": (
                "frequency_proxy ← HRV + stress + focus + sleep; "
                "rumination_proxy ← stress loops + low focus; "
                "vulnerability ← low frequency + rumination + isolation."
            ),
        }

    def _frequency_proxy(self, frame: SensorFrame) -> float:
        return max(0.0, min(1.0,
            (frame.hrv_ms / 90.0) * 0.35
            + (1.0 - frame.subjective_stress / 10.0) * 0.30
            + (frame.focus / 10.0) * 0.20
            + (1.0 - frame.sleep_debt / 10.0) * 0.15
        ))

    def _rumination_proxy(self, frame: SensorFrame, report: PatternReport) -> float:
        if "rumination_loop" in report.patterns or "persistent_stress_loop" in report.patterns:
            return min(1.0, 0.70 + frame.subjective_stress / 40.0)
        if frame.subjective_stress >= 6.0 and frame.focus <= 4.5:
            return 0.45
        if frame.subjective_stress >= 7.0:
            return 0.35
        return 0.10

    def _vulnerability(self, freq: float, rum: float, frame: SensorFrame) -> float:
        return max(0.0, min(1.0,
            (1.0 - freq) * 0.50
            + rum * 0.35
            + (frame.social_isolation / 10.0) * 0.15
        ))

    def _labels(self, freq: float, rum: float, vuln: float, report: PatternReport) -> List[str]:
        labels: List[str] = []
        if freq >= 0.70:
            labels.append("high_frequency_state")
        elif freq <= 0.32:
            labels.append("low_frequency_state")
        else:
            labels.append("mid_frequency_state")
        if rum >= 0.55:
            labels.append("active_rumination")
        if vuln >= 0.65:
            labels.append("elevated_vulnerability_metaphor")
        if "moral_erosion_proxy" in report.patterns:
            labels.append("moral_vector_decline_metaphor")
        return labels

    def _narrative(self, labels: List[str], freq: float, rum: float, vuln: float) -> str:
        parts: List[str] = []
        if "low_frequency_state" in labels:
            parts.append(
                "Состояние описывается языком низкой «частоты» сознания "
                "(высокий стресс, сниженный HRV, истощение)."
            )
        if "active_rumination" in labels:
            parts.append(
                "Обнаружена петля повторяющихся негативных мыслей. "
                "В архетипической модели это фактор повышения уязвимости."
            )
        if "elevated_vulnerability_metaphor" in labels:
            parts.append(
                "Метафора «уязвимости» активирована. "
                "В научной рамке это означает повышенный риск деструктивных "
                "решений под влиянием стресса и изоляции."
            )
        if not parts:
            parts.append(
                "Архетипический слой не видит выраженных низкочастотных маркеров. "
                "Состояние ближе к устойчивому или восстанавливающемуся."
            )
        return " ".join(parts)
