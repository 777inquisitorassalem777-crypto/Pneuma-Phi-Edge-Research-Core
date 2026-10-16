"""Симулятор руминаций (гипотетический)."""

from __future__ import annotations
from typing import List
from dataclasses import dataclass
import random
from .entities import HumanSoul


@dataclass
class RuminationEvent:
    step: int
    intensity: float
    frequency_before: float
    frequency_after: float
    rumination_level: float


class RuminationSimulator:
    def __init__(self, seed: int = 7):
        self.rng = random.Random(seed)

    def simulate(self, soul: HumanSoul, steps: int = 20, base_intensity: float = 0.08) -> List[RuminationEvent]:
        events = []
        for step in range(1, steps + 1):
            intensity = min(0.25, base_intensity * self.rng.uniform(0.6, 1.4))
            before = soul.frequency
            soul.apply_rumination(intensity)
            events.append(RuminationEvent(
                step=step,
                intensity=round(intensity, 4),
                frequency_before=round(before, 4),
                frequency_after=round(soul.frequency, 4),
                rumination_level=round(soul.rumination_level, 4),
            ))
            if self.rng.random() < 0.12:
                soul.shift_frequency(+0.015)
                soul.rumination_level = max(0.0, soul.rumination_level - 0.05)
        return events
