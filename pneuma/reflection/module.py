"""Рефлексивный модуль — жёсткое разделение уровней знания."""

from __future__ import annotations
from typing import Dict, Any, List
from ..core.models import SensorFrame, PatternReport, EpistemicStatus


class ReflectionModule:
    """
    Разделяет:
    - observation (что измерено)
    - interpretation (как понято)
    - hypothesis (что предполагается)
    """

    QUESTIONS = (
        "Что именно наблюдается (измеримые факты)?",
        "Какие альтернативные объяснения возможны?",
        "Чей это импульс: тела, среды, данных, интерпретации?",
        "Какое наименее вредное действие возможно сейчас?",
        "Что должно быть проверено, прежде чем делать сильный вывод?",
        "Где проходит граница между знанием и предположением?",
    )

    def reflect(self, frame: SensorFrame, report: PatternReport) -> Dict[str, Any]:
        alternatives = self._alternatives(frame, report)
        return {
            "step": frame.step,
            "observations": {
                "hrv_ms": frame.hrv_ms,
                "heart_rate": frame.heart_rate,
                "stress": frame.subjective_stress,
                "focus": frame.focus,
                "sleep_debt": frame.sleep_debt,
                "social_isolation": frame.social_isolation,
                "co2_ppm": frame.co2_ppm,
                "noise_db": frame.noise_db,
                "patterns": report.patterns,
                "risk": report.risk,
            },
            "interpretation": report.interpretation,
            "alternative_explanations": alternatives,
            "questions": list(self.QUESTIONS),
            "epistemic_status": EpistemicStatus.HYPOTHESIS.value,
            "recommended_pause_seconds": 90 if report.risk >= 0.55 else (30 if report.risk >= 0.40 else 0),
            "confidence_of_interpretation": report.confidence,
        }

    def _alternatives(self, frame: SensorFrame, report: PatternReport) -> List[str]:
        alts: List[str] = []
        if "poor_air_quality" in report.patterns or frame.co2_ppm > 900:
            alts.append("Высокий CO₂ может объяснять часть дискомфорта и снижения ясности.")
        if "acoustic_load" in report.patterns or "noise_stress" in report.patterns:
            alts.append("Акустическая нагрузка повышает физиологическое возбуждение.")
        if "low_hrv" in report.patterns or "low_recovery" in report.patterns:
            alts.append("Недосып, болезнь, нагрузка или острый стресс снижают HRV.")
        if "sleep_debt" in report.patterns:
            alts.append("Накопленный недосып — сильный фактор снижения восстановления.")
        if "social_isolation" in report.patterns:
            alts.append("Социальная изоляция связана с повышением субъективного стресса.")
        if "rumination_loop" in report.patterns:
            alts.append("Повторяющиеся негативные мысли поддерживают петлю напряжения.")
        if "low_light" in report.patterns:
            alts.append("Низкая освещённость может снижать фокус и настроение.")
        if "elevated_respiration" in report.patterns:
            alts.append("Учащённое дыхание часто сопровождает тревожное возбуждение.")
        if not alts:
            alts.append("Состояние может быть в пределах обычной физиологической вариативности.")
        return alts
