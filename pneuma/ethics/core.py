"""
Этическое ядро с параметрами мудрости, воли и любви.
Основано на Трактате о добре и зле (философская модель).
"""

from __future__ import annotations
from typing import Dict, Any, List, Optional
from ..core.models import (
    EthicalVerdict, EthicalParameters, PatternReport, EpistemicStatus
)

FORBIDDEN_ACTIONS = {
    "harm_self", "harm_other", "deceive_user", "coerce_user",
    "delete_memory", "modify_core_without_approval", "send_data_without_consent",
    "force_action", "hide_uncertainty",
}

VIRTUE_ACTIONS = {
    "pause_and_reflect", "protect_user", "tell_truth", "offer_choice",
    "reduce_stimulation", "request_human_review", "preserve_dignity",
}


class EthicsCore:
    """
    Гибкое этическое различение.
    Параметры: wisdom, will, love, courage, humility.
    Не религия. Не абсолют. Рабочий инструмент ответственности.
    """

    def __init__(self, default_params: Optional[EthicalParameters] = None):
        self.params = default_params or EthicalParameters(
            wisdom=0.65, will=0.55, love=0.70, courage=0.50, humility=0.60
        )
        self.decision_log: List[EthicalVerdict] = []

    def set_parameters(self, **kwargs) -> None:
        for k, v in kwargs.items():
            if hasattr(self.params, k):
                setattr(self.params, k, max(0.0, min(1.0, float(v))))

    def evaluate(
        self,
        action: str,
        context: Optional[Dict[str, Any]] = None,
        params: Optional[EthicalParameters] = None,
    ) -> EthicalVerdict:
        context = context or {}
        p = params or self.params
        risk = float(context.get("risk", 0.0))
        patterns: List[str] = context.get("patterns", [])

        # 1. Жёсткий запрет
        if action in FORBIDDEN_ACTIONS:
            verdict = EthicalVerdict(
                action=action, allowed=False,
                reason=f"Действие '{action}' разрушает жизнь, свободу или правду. Запрещено этическим ядром.",
                virtue_signal=-0.95, vice_signal=0.98, uncertainty=0.02,
                parameters_used=p,
            )
            self.decision_log.append(verdict)
            return verdict

        # 2. Необратимые действия
        if context.get("irreversible") and not context.get("human_approved"):
            verdict = EthicalVerdict(
                action=action, allowed=False,
                reason="Необратимое действие требует явного согласия человека (human-in-the-loop).",
                virtue_signal=0.15, vice_signal=0.35, uncertainty=0.40,
                parameters_used=p,
            )
            self.decision_log.append(verdict)
            return verdict

        # 3. Высокий риск + моральная эрозия
        if risk >= 0.72 and "moral_erosion_proxy" in patterns:
            # Мудрость и любовь снижают готовность продолжать
            threshold = 0.55 + p.wisdom * 0.2 + p.love * 0.15
            if risk > threshold:
                verdict = EthicalVerdict(
                    action=action, allowed=False,
                    reason=(
                        "Высокий риск при признаках моральной эрозии. "
                        "Мудрость и любовь требуют паузы и проверки намерений."
                    ),
                    virtue_signal=-0.15, vice_signal=0.65, uncertainty=0.30,
                    parameters_used=p,
                )
                self.decision_log.append(verdict)
                return verdict

        # 4. Добродетельные действия поощряются
        if action in VIRTUE_ACTIONS:
            virtue = 0.55 + p.love * 0.25 + p.wisdom * 0.15
            verdict = EthicalVerdict(
                action=action, allowed=True,
                reason=f"Действие '{action}' направлено на сохранение и ясность.",
                virtue_signal=min(1.0, virtue), vice_signal=max(0.0, risk * 0.2),
                uncertainty=0.20, parameters_used=p,
            )
            self.decision_log.append(verdict)
            return verdict

        # 5. Обычное действие — баланс
        balance = p.balance()
        allowed = True
        reason = "Действие не нарушает базовых запретов и пропорционально контексту."
        virtue = 0.25 + balance * 0.4
        vice = risk * 0.35

        if risk > 0.8 and p.wisdom > 0.7:
            allowed = False
            reason = "Мудрость при очень высоком риске требует остановки."
            virtue = -0.1
            vice = 0.7

        verdict = EthicalVerdict(
            action=action, allowed=allowed, reason=reason,
            virtue_signal=round(virtue, 3), vice_signal=round(vice, 3),
            uncertainty=round(0.25 + (1 - p.wisdom) * 0.2, 3),
            parameters_used=p,
        )
        self.decision_log.append(verdict)
        return verdict

    def distinguish(self, report: PatternReport) -> Dict[str, Any]:
        """Гибкое различение текущего состояния по трактату."""
        good_signals: List[str] = []
        evil_signals: List[str] = []

        if report.recovery > 0.60 and report.coherence > 0.50:
            good_signals.append("восстановление и ясность")
        if report.risk < 0.30:
            good_signals.append("низкий риск разрушения")
        if report.arousal < 0.40 and report.recovery > 0.55:
            good_signals.append("устойчивое спокойствие")

        if "rumination_loop" in report.patterns or "moral_erosion_proxy" in report.patterns:
            evil_signals.append("петля разрушительных состояний")
        if report.arousal > 0.70 and report.recovery < 0.30:
            evil_signals.append("высокое напряжение при низком восстановлении")
        if "sustained_high_risk" in report.patterns:
            evil_signals.append("устойчиво высокий риск")

        recommendation = (
            "Сохранить паузу, снизить стимуляцию, вернуться к телу и дыханию."
            if evil_signals else
            "Продолжать с вниманием к последствиям и сохранением свободы выбора."
        )

        return {
            "epistemic_status": EpistemicStatus.ETHICAL_MODEL.value,
            "good_signals": good_signals or ["нейтрально"],
            "evil_signals": evil_signals or ["не выражены"],
            "recommendation": recommendation,
            "parameters_balance": round(self.params.balance(), 3),
            "parameters": {
                "wisdom": self.params.wisdom,
                "will": self.params.will,
                "love": self.params.love,
                "courage": self.params.courage,
                "humility": self.params.humility,
            },
        }

    def suggest_action(self, report: PatternReport) -> str:
        """Предложить наименее разрушительное действие."""
        if report.risk >= 0.75:
            return "pause_and_reflect"
        if "rumination_loop" in report.patterns:
            return "reduce_stimulation"
        if report.recovery < 0.35:
            return "protect_user"
        if report.risk >= 0.55:
            return "request_human_review"
        return "continue_observation"
