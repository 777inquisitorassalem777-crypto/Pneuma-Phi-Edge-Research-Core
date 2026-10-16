"""
Архетипический (гипотетический) слой.

ВАЖНО: всё, что генерирует этот модуль, имеет статус
`archetypal_hypothesis_not_fact`.

Он не утверждает реальность сущностей, душ или «жатвы».
Это культурно-мифологическая модель смысла, подключённая
как опциональный интерпретативный слой.
"""

from __future__ import annotations
from typing import Dict, Any, List
from ..core.models import SensorFrame, PatternReport


class ArchetypalLayer:
    """
    Преобразует наблюдаемые паттерны в язык архетипов
    (низкая/высокая «частота», руминации, уязвимость к «сбору»).
    Все выводы явно помечены как гипотеза.
    """

    def interpret(self, frame: SensorFrame, report: PatternReport) -> Dict[str, Any]:
        # Прокси «частоты» сознания (0–1)
        frequency_proxy = max(0.0, min(1.0,
            (frame.hrv_ms / 90.0) * 0.35
            + (1.0 - frame.subjective_stress / 10.0) * 0.30
            + (frame.focus / 10.0) * 0.20
            + (1.0 - frame.sleep_debt / 10.0) * 0.15
        ))

        # Прокси руминаций
        rumination_proxy = 0.0
        if "rumination_loop" in report.patterns or "persistent_stress_loop" in report.patterns:
            rumination_proxy = 0.7 + (frame.subjective_stress / 10.0) * 0.25
        elif frame.subjective_stress >= 6.0 and frame.focus <= 4.5:
            rumination_proxy = 0.45
        rumination_proxy = min(1.0, rumination_proxy)

        # Уязвимость (для метафоры «сбора»)
        vulnerability = max(0.0, min(1.0,
            (1.0 - frequency_proxy) * 0.5
            + rumination_proxy * 0.35
            + (frame.social_isolation / 10.0) * 0.15
        ))

        # Архетипические метки (только язык)
        labels: List[str] = []
        if frequency_proxy >= 0.70:
            labels.append("high_frequency_state")
        elif frequency_proxy <= 0.32:
            labels.append("low_frequency_state")
        else:
            labels.append("mid_frequency_state")

        if rumination_proxy >= 0.55:
            labels.append("active_rumination")
        if vulnerability >= 0.65:
            labels.append("elevated_vulnerability_metaphor")
        if "moral_erosion_proxy" in report.patterns:
            labels.append("moral_vector_decline_metaphor")

        narrative = self._build_narrative(frequency_proxy, rumination_proxy, vulnerability, labels)

        return {
            "layer": "archetypal",
            "epistemic_status": "archetypal_hypothesis_not_fact",
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

    def _build_narrative(
        self,
        freq: float,
        rum: float,
        vuln: float,
        labels: List[str],
    ) -> str:
        parts = []
        if "low_frequency_state" in labels:
            parts.append(
                "Состояние описывается языком низкой «частоты» сознания "
                "(высокий стресс, сниженный HRV, истощение)."
            )
        if "active_rumination" in labels:
            parts.append(
                "Обнаружена петля повторяющихся негативных мыслей (руминации) — "
                "в архетипической модели это фактор, повышающий уязвимость."
            )
        if "elevated_vulnerability_metaphor" in labels:
            parts.append(
                "Метафора «уязвимости к сбору» активирована. "
                "В научной рамке это означает повышенный риск деструктивных "
                "решений под влиянием стресса и изоляции."
            )
        if not parts:
            parts.append(
                "Архетипический слой не видит выраженных низкочастотных маркеров. "
                "Состояние ближе к устойчивому или восстанавливающемуся."
            )
        return " ".join(parts)
