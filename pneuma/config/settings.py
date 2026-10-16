"""Конфигурация PNEUMA Full."""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Dict, Any


@dataclass
class EthicsConfig:
    wisdom: float = 0.65
    will: float = 0.55
    love: float = 0.70
    courage: float = 0.50
    humility: float = 0.60


@dataclass
class RuntimeConfig:
    default_mode: str = "scientific"
    default_scenario: str = "baseline"
    default_steps: int = 100
    default_seed: int = 42
    audit_path: str = "audit.jsonl"
    ethics: EthicsConfig = field(default_factory=EthicsConfig)
    risk_pause_threshold: float = 0.75
    risk_review_threshold: float = 0.55

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


DEFAULT_CONFIG = RuntimeConfig()
