"""
Гипотетический симулятор циклов 70–100 лет.
Статус: archetypal_hypothesis_not_fact.
Не утверждает реальной метафизики.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any
import random
import uuid


@dataclass
class Entity:
    name: str
    frequency: float
    energy: float = 100.0
    is_immortal: bool = False
    is_active: bool = True
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def shift_frequency(self, delta: float) -> None:
        self.frequency = max(0.0, min(1.0, self.frequency + delta))


@dataclass
class HumanSoul(Entity):
    is_immortal: bool = False
    soul_integrity: float = 1.0
    body_alive: bool = True
    moral_vector: float = 0.5
    rumination_level: float = 0.0

    def die(self) -> None:
        self.body_alive = False
        self.is_active = False
        self.frequency = max(0.1, self.frequency - 0.05 * self.rumination_level)

    def apply_rumination(self, intensity: float) -> None:
        self.rumination_level = min(1.0, self.rumination_level + intensity)
        self.shift_frequency(-0.04 * intensity)
        self.moral_vector = max(-1.0, self.moral_vector - 0.03 * intensity)


@dataclass
class LowFrequencyEntity(Entity):
    is_immortal: bool = True
    frequency: float = 0.18
    harvested: List[str] = field(default_factory=list)

    def harvest(self, soul: HumanSoul) -> bool:
        if not soul.body_alive and soul.soul_integrity > 0.3:
            self.harvested.append(soul.id)
            self.energy += soul.soul_integrity * 15.0
            soul.soul_integrity = 0.0
            return True
        return False


@dataclass
class LightEntity(Entity):
    is_immortal: bool = True
    frequency: float = 0.92

    def can_engage_mortal(self) -> bool:
        return False


@dataclass
class CycleResult:
    cycle: int
    year: int
    war_occurred: bool
    deaths: int
    harvested: int
    avg_frequency: float
    notes: str


class WarCycleSimulator:
    """
    Модель «исторической закономерности» + метафора сбора.
    Явно гипотетическая.
    """

    def __init__(self, population: int = 100, seed: int = 42):
        self.rng = random.Random(seed)
        self.humans = [
            HumanSoul(
                name=f"H-{i}",
                frequency=self.rng.uniform(0.35, 0.75),
                moral_vector=self.rng.uniform(-0.3, 0.6),
                rumination_level=self.rng.uniform(0.0, 0.35),
            )
            for i in range(population)
        ]
        self.low = [LowFrequencyEntity(name=f"LF-{i}") for i in range(5)]
        self.light = [LightEntity(name=f"L-{i}") for i in range(4)]
        self.year = 0
        self.history: List[CycleResult] = []

    def run_cycle(self, years: int = 85) -> CycleResult:
        self.year += years
        war = years >= 100 or (years >= 70 and self.rng.random() < (years - 70) / 30.0)
        deaths = harvested = 0

        if war:
            for h in self.humans:
                if not h.body_alive:
                    continue
                risk = 0.15 + (1.0 - h.frequency) * 0.25 + h.rumination_level * 0.20
                if self.rng.random() < risk:
                    h.die()
                    deaths += 1
                    for lf in self.low:
                        if lf.harvest(h):
                            harvested += 1
                            break

        for light in self.light:
            for h in self.humans:
                if h.body_alive and h.frequency < 0.60:
                    h.shift_frequency(+0.02)

        alive = [h for h in self.humans if h.body_alive]
        avg_f = sum(h.frequency for h in alive) / len(alive) if alive else 0.0
        notes = "Война (гипотеза). Жатва как метафора." if war else "Спокойный период."
        result = CycleResult(
            cycle=len(self.history) + 1,
            year=self.year,
            war_occurred=war,
            deaths=deaths,
            harvested=harvested,
            avg_frequency=round(avg_f, 4),
            notes=notes,
        )
        self.history.append(result)
        return result

    def run(self, cycles: int = 4) -> Dict[str, Any]:
        results = [self.run_cycle(self.rng.randint(75, 95)) for _ in range(cycles)]
        return {
            "epistemic_status": "archetypal_hypothesis_not_fact",
            "disclaimer": (
                "Модель циклов и «жатвы» — культурно-мифологическая гипотеза, не факт. "
                "Не утверждает существования сущностей или бессмертных душ."
            ),
            "cycles": [
                {
                    "cycle": r.cycle,
                    "year": r.year,
                    "war": r.war_occurred,
                    "deaths": r.deaths,
                    "harvested": r.harvested,
                    "avg_freq": r.avg_frequency,
                    "notes": r.notes,
                }
                for r in results
            ],
            "total_harvested_metaphor": sum(len(e.harvested) for e in self.low),
            "living": sum(1 for h in self.humans if h.body_alive),
        }
