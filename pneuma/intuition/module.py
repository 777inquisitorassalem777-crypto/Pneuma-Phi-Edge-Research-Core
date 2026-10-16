"""
Модуль интуиции и изобретательности.
Генерирует нестандартные, но проверяемые гипотезы.
Не является мистическим озарением.
"""

from __future__ import annotations
from typing import List, Dict, Any, Optional
import random
from ..core.models import SensorFrame, PatternReport, EpistemicStatus


class IntuitionModule:
    """
    «Интуиция» = комбинаторная генерация гипотез + фильтрация по проверяемости.
    """

    def __init__(self, seed: int = 13):
        self.rng = random.Random(seed)
        self.memory: List[Dict[str, Any]] = []
        self.hypothesis_bank = self._build_bank()

    def _build_bank(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": "env_co2",
                "trigger": lambda f, r: f.co2_ppm > 900,
                "text": (
                    "Повышенный CO₂ может объяснять часть субъективного напряжения "
                    "через лёгкую гиперкапнию и снижение когнитивной ясности. "
                    "Стоит проверить вентиляцию как независимый фактор."
                ),
                "testable": True,
            },
            {
                "id": "env_noise",
                "trigger": lambda f, r: f.noise_db > 48 or f.infrasound_db > 44,
                "text": (
                    "Акустическая нагрузка (шум / инфразвук) повышает физиологическое "
                    "возбуждение. Снижение звукового фона — простой и проверяемый шаг."
                ),
                "testable": True,
            },
            {
                "id": "env_light",
                "trigger": lambda f, r: f.ambient_light_lux < 150,
                "text": (
                    "Низкая освещённость коррелирует со снижением фокуса и повышением "
                    "сонливости. Проверка освещения — быстрый эксперимент."
                ),
                "testable": True,
            },
            {
                "id": "sleep_debt",
                "trigger": lambda f, r: f.sleep_debt >= 5.5 or "sleep_debt" in r.patterns,
                "text": (
                    "Накопленный недосып — один из самых сильных факторов снижения HRV "
                    "и роста стресса. Приоритет восстановления сна выше сложных интерпретаций."
                ),
                "testable": True,
            },
            {
                "id": "rumination",
                "trigger": lambda f, r: "rumination_loop" in r.patterns or "persistent_stress_loop" in r.patterns,
                "text": (
                    "Петля руминаций поддерживается сниженным HRV и недосыпом. "
                    "Прерывание через тело (медленное дыхание, движение, холодная вода) "
                    "часто эффективнее продолжения анализа."
                ),
                "testable": True,
            },
            {
                "id": "isolation",
                "trigger": lambda f, r: f.social_isolation >= 6.0,
                "text": (
                    "Социальная изоляция усиливает субъективный стресс и снижает "
                    "восстановление. Даже краткий безопасный контакт может сдвинуть состояние."
                ),
                "testable": True,
            },
            {
                "id": "low_recovery",
                "trigger": lambda f, r: r.recovery < 0.35,
                "text": (
                    "Низкое восстановление — первичный сигнал. "
                    "Любые сложные (в том числе метафизические) интерпретации вторичны "
                    "до восстановления базовых ресурсов."
                ),
                "testable": True,
            },
            {
                "id": "archetypal_low_freq",
                "trigger": lambda f, r: r.risk > 0.60,
                "text": (
                    "[архетипическая гипотеза] Состояние описывается языком «низкой частоты». "
                    "Это метафора качества сознания (стресс + истощение), "
                    "а не утверждение о существовании сущностей."
                ),
                "testable": False,
            },
            {
                "id": "body_first",
                "trigger": lambda f, r: True,
                "text": (
                    "Возможно, полезно временно снизить информационную нагрузку "
                    "и вернуться к простому наблюдению за дыханием и контактом с поверхностью."
                ),
                "testable": True,
            },
            {
                "id": "uncertainty",
                "trigger": lambda f, r: r.confidence < 0.75,
                "text": (
                    "Уверенность интерпретации умеренная. "
                    "Принцип неопределённости: лучше сохранить несколько рабочих гипотез, "
                    "чем зафиксировать одну преждевременно."
                ),
                "testable": True,
            },
        ]

    def generate(
        self,
        frame: SensorFrame,
        report: PatternReport,
        max_hypotheses: int = 3,
    ) -> Dict[str, Any]:
        candidates = []
        for item in self.hypothesis_bank:
            try:
                if item["trigger"](frame, report):
                    candidates.append(item)
            except Exception:
                continue

        if not candidates:
            candidates = [self.hypothesis_bank[-2]]  # body_first fallback

        # Приоритет проверяемым
        testable = [c for c in candidates if c.get("testable", True)]
        non_testable = [c for c in candidates if not c.get("testable", True)]
        ordered = testable + non_testable

        k = min(max_hypotheses, len(ordered))
        chosen = self.rng.sample(ordered, k=k) if len(ordered) > k else ordered

        result = {
            "epistemic_status": EpistemicStatus.GENERATED.value,
            "hypotheses": [
                {
                    "id": c["id"],
                    "text": c["text"],
                    "testable": c.get("testable", True),
                }
                for c in chosen
            ],
            "note": (
                "Интуитивный модуль создаёт проверяемые предположения, "
                "а не откровения и не утверждения о душе."
            ),
            "memory_size": len(self.memory),
        }
        self.memory.append(result)
        return result

    def clear_memory(self) -> None:
        self.memory.clear()
