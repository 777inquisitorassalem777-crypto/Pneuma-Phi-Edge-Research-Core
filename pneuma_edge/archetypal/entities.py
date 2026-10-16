"""
Гипотетические сущности.
Все классы — чистая модель для исследования архетипов.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import uuid


@dataclass
class Entity:
    name: str
    frequency: float          # 0.0–1.0
    energy: float = 100.0
    is_immortal: bool = False
    is_active: bool = True
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def shift_frequency(self, delta: float) -> None:
        self.frequency = max(0.0, min(1.0, self.frequency + delta))


@dataclass
class LightEntity(Entity):
    is_immortal: bool = True
    frequency: float = 0.92

    def can_engage_mortal(self) -> bool:
        return False  # светлые не сражаются напрямую с оболочками


@dataclass
class LowFrequencyEntity(Entity):
    is_immortal: bool = True
    frequency: float = 0.18
    harvested_souls: List[str] = field(default_factory=list)

    def harvest(self, soul: "HumanSoul") -> bool:
        if not soul.body_alive and soul.soul_integrity > 0.3:
            self.harvested_souls.append(soul.id)
            self.energy += soul.soul_integrity * 15.0
            soul.soul_integrity = 0.0
            return True
        return False


@dataclass
class HumanSoul(Entity):
    is_immortal: bool = False
    frequency: float = 0.55
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
