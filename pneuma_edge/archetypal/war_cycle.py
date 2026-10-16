"""
Симулятор циклов 70–100 лет (гипотетический).
Явно помечен как archetypal_hypothesis_not_fact.
"""

from __future__ import annotations
from typing import List, Dict, Any
from dataclasses import dataclass
import random
from .entities import HumanSoul, LowFrequencyEntity, LightEntity


@dataclass
class CycleResult:
    cycle: int
    year: int
    war_occurred: bool
    deaths: int
    harvested: int
    avg_human_frequency: float
    notes: str


class WarCycleSimulator:
    """
    Модель «исторической закономерности» войн + метафора сбора душ.
    Не является утверждением реальной метафизики.
    """

    def __init__(self, population: int = 120, seed: int = 42):
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
        war = years >= 100 or (years >= 70 and self.rng.random() < (years - 70) / 30)
        deaths = harvested = 0

        if war:
            for h in self.humans:
                if not h.body_alive:
                    continue
                risk = 0.15 + (1 - h.frequency) * 0.25 + h.rumination_level * 0.2
                if self.rng.random() < risk:
                    h.die()
                    deaths += 1
                    for lf in self.low:
                        if lf.harvest(h):
                            harvested += 1
                            break

        # Светлые «поддерживают»
        for l in self.light:
            for h in self.humans:
                if h.body_alive and h.frequency < 0.6:
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
            avg_human_frequency=round(avg_f, 4),
            notes=notes,
        )
        self.history.append(result)
        return result

    def run(self, cycles: int = 4) -> Dict[str, Any]:
        results = [self.run_cycle(self.rng.randint(75, 95)) for _ in range(cycles)]
        return {
            "epistemic_status": "archetypal_hypothesis_not_fact",
            "disclaimer": "Модель циклов и «жатвы» — культурно-мифологическая гипотеза, не факт.",
            "cycles": [
                {
                    "cycle": r.cycle,
                    "year": r.year,
                    "war": r.war_occurred,
                    "deaths": r.deaths,
                    "harvested": r.harvested,
                    "avg_freq": r.avg_human_frequency,
                    "notes": r.notes,
                }
                for r in results
            ],
            "total_harvested": sum(len(e.harvested_souls) for e in self.low),
            "living": sum(1 for h in self.humans if h.body_alive),
        }
