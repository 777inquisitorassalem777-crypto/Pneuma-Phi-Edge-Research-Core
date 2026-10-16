"""
Passport — устойчивый снимок состояния/идентичности сессии.
Не «душа», а версионируемый паспорт параметров и истории решений.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import json
from pathlib import Path
import uuid


@dataclass
class Passport:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "pneuma-agent"
    version: str = "1.0"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    wisdom_vector: Dict[str, float] = field(default_factory=dict)
    ethics_balance: float = 0.5
    total_steps: int = 0
    blocked_actions: int = 0
    evolution_accepted: int = 0
    notes: List[str] = field(default_factory=list)
    epistemic_status: str = "identity_record_not_soul"

    def update_from_session(
        self,
        steps: int,
        ethics_balance: float,
        blocked: int,
        evolution_accepted: int,
        wisdom_vector: Optional[Dict[str, float]] = None,
        note: str = "",
    ) -> None:
        self.total_steps += steps
        self.ethics_balance = ethics_balance
        self.blocked_actions += blocked
        self.evolution_accepted += evolution_accepted
        if wisdom_vector:
            self.wisdom_vector = wisdom_vector
        if note:
            self.notes.append(f"{datetime.now(timezone.utc).isoformat()}: {note}")

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def save(self, path: str) -> None:
        Path(path).write_text(
            json.dumps(self.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8"
        )

    @classmethod
    def load(cls, path: str) -> "Passport":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
