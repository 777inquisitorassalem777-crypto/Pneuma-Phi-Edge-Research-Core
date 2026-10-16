"""Рефлексивный модуль — разделяет факт, интерпретацию и гипотезу."""

from ..core.models import SensorFrame, PatternReport


class ReflectionModule:
    QUESTIONS = (
        "Что именно наблюдается?",
        "Какие альтернативные объяснения возможны?",
        "Чей это импульс: мой, среды, данных или чужого влияния?",
        "Какое наименее вредное действие возможно сейчас?",
        "Что должно быть проверено, прежде чем делать вывод?",
    )

    def reflect(self, frame: SensorFrame, report: PatternReport) -> dict:
        alternatives = []
        if "poor_air_quality" in report.patterns:
            alternatives.append("Высокий CO₂ может объяснять часть дискомфорта.")
        if "acoustic_load" in report.patterns or "noise_stress" in report.patterns:
            alternatives.append("Шумовая / акустическая нагрузка может повышать напряжение.")
        if "low_hrv" in report.patterns or "low_recovery" in report.patterns:
            alternatives.append("Недосып, болезнь, нагрузка или стресс могут снижать HRV.")
        if "sleep_debt" in report.patterns:
            alternatives.append("Накопленный недосып — сильный фактор снижения восстановления.")
        if "social_isolation" in report.patterns:
            alternatives.append("Социальная изоляция связана с повышением субъективного стресса.")
        if "rumination_loop" in report.patterns:
            alternatives.append("Повторяющиеся негативные мысли (руминации) могут поддерживать петлю напряжения.")
        if not alternatives:
            alternatives.append("Состояние может быть в пределах обычной вариативности.")

        return {
            "step": frame.step,
            "observations": {
                "hrv_ms": frame.hrv_ms,
                "stress": frame.subjective_stress,
                "focus": frame.focus,
                "sleep_debt": frame.sleep_debt,
                "social_isolation": frame.social_isolation,
                "patterns": report.patterns,
            },
            "interpretation": report.interpretation,
            "alternative_explanations": alternatives,
            "questions": list(self.QUESTIONS),
            "epistemic_status": "hypothesis_not_fact",
            "recommended_pause_seconds": 90 if report.risk >= 0.55 else 0,
        }
