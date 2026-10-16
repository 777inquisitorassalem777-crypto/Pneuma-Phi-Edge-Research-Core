"""
Слой мудрости (Wisdom Layer).
Синтез принципов (по запросу пользователя, без иудаизма и ислама):
христианская этика любви, даосизм, славянская Правда/Кривда,
гуны, И-цзин (перемены), Сунь-цзы, шаманское различение сил.

Это вычислительная метафора, не религия и не откровение.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List
from enum import Enum


class Guna(str, Enum):
    SATTVA = "sattva"   # ясность, гармония
    RAJAS = "rajas"     # активность, страсть
    TAMAS = "tamas"     # инерция, затемнение


@dataclass
class WisdomVector:
    """Вектор Will–Love–Faith–Hope + мудрость."""
    will: float = 0.5
    love: float = 0.5
    faith: float = 0.5
    hope: float = 0.5
    wisdom: float = 0.5
    courage: float = 0.5
    humility: float = 0.5

    def balance(self) -> float:
        return (
            self.wisdom * 0.25
            + self.love * 0.25
            + self.will * 0.15
            + self.faith * 0.10
            + self.hope * 0.10
            + self.courage * 0.08
            + self.humility * 0.07
        )


class WisdomLayer:
    """
    Применяет культурно-философские эвристики к состоянию системы.
    Эпистемический статус: ethical_model_not_doctrine.
    """

    def __init__(self, vector: WisdomVector | None = None):
        self.vector = vector or WisdomVector(
            will=0.55, love=0.70, faith=0.50, hope=0.55,
            wisdom=0.65, courage=0.50, humility=0.60,
        )
        self.history: List[Dict[str, Any]] = []

    def assess_guna(self, risk: float, recovery: float, arousal: float) -> Guna:
        if recovery > 0.6 and risk < 0.35 and arousal < 0.45:
            return Guna.SATTVA
        if arousal > 0.6 or risk > 0.55:
            return Guna.RAJAS
        return Guna.TAMAS

    def counsel(self, risk: float, recovery: float, arousal: float, patterns: List[str]) -> Dict[str, Any]:
        guna = self.assess_guna(risk, recovery, arousal)
        advice: List[str] = []

        # Даосский акцент: ненасилие над процессом, возврат к естественному
        if guna == Guna.RAJAS:
            advice.append("Даосский совет: уменьшить принуждение, вернуться к дыханию и простому действию.")
        if guna == Guna.TAMAS:
            advice.append("Совет ясности: лёгкое движение, свет, контакт — против инерции.")
        if guna == Guna.SATTVA:
            advice.append("Сохранить ясность: не усложнять то, что уже устойчиво.")

        # Христианский акцент: любовь + свобода воли + проверка плодов
        if "moral_erosion_proxy" in patterns or risk > 0.7:
            advice.append(
                "Этический акцент: проверить, сохраняет ли действие достоинство и свободу другого; "
                "плоды дела важнее намерений."
            )

        # Славянский мотив Правды/Кривды
        if "rumination_loop" in patterns:
            advice.append(
                "Мотив Правды: отделить факт от кривого истолкования; "
                "не кормить петлю самооправдания."
            )

        # Сунь-цзы: не сражаться там, где можно избежать
        if risk > 0.65:
            advice.append("Стратегия: не усиливать конфликт; выиграть, сохранив силы и ясность.")

        # И-цзин: перемена
        if recovery < 0.35:
            advice.append("Перемена: текущая фаза — накопление; действие вторично восстановлению.")

        # Шаманский мотив различения «сил»
        if risk > 0.6 and arousal > 0.65:
            advice.append(
                "Различение: отделить внешний шум среды от внутреннего импульса; "
                "не отдавать волю автоматической реакции."
            )

        result = {
            "epistemic_status": "ethical_model_not_doctrine",
            "guna": guna.value,
            "vector_balance": round(self.vector.balance(), 3),
            "vector": {
                "will": self.vector.will,
                "love": self.vector.love,
                "faith": self.vector.faith,
                "hope": self.vector.hope,
                "wisdom": self.vector.wisdom,
            },
            "counsel": advice or ["Сохранять наблюдение без лишней интерпретации."],
            "disclaimer": (
                "Слой мудрости — вычислительная метафора культурных принципов. "
                "Не является религией, откровением или доказательством души."
            ),
        }
        self.history.append(result)
        return result
