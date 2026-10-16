"""
Цикл мета-эволюции (упрощённый).
Генерирует кандидатов (правила/паттерны/гипотезы), валидирует, сохраняет.
Не является самосознанием. Только управляемый исследовательский цикл.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import uuid
import json
from pathlib import Path


@dataclass
class Candidate:
    id: str
    kind: str          # rule | pattern | algorithm | hypothesis
    payload: Dict[str, Any]
    scores: Dict[str, float] = field(default_factory=dict)
    accepted: bool = False
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class EvolutionReport:
    cycle_id: str
    candidates_total: int
    accepted: int
    rejected: int
    notes: str
    epistemic_status: str = "research_loop_not_consciousness"


class EvolutionLoop:
    """
    Один цикл: наблюдение → извлечение признаков → генерация кандидатов → валидация → реестр.
    """

    def __init__(self, data_dir: str = "evolution_data", threshold: float = 0.65):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.threshold = threshold
        self.registry: List[Candidate] = []
        self.memory: List[Dict[str, Any]] = []
        self._load()

    def _load(self) -> None:
        reg = self.data_dir / "registry.json"
        if reg.exists():
            try:
                raw = json.loads(reg.read_text(encoding="utf-8"))
                self.registry = [Candidate(**x) for x in raw]
            except Exception:
                self.registry = []

    def _save(self) -> None:
        path = self.data_dir / "registry.json"
        path.write_text(
            json.dumps([c.to_dict() for c in self.registry], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def cycle(self, observation: Dict[str, Any]) -> EvolutionReport:
        self.memory.append(observation)
        if len(self.memory) > 200:
            self.memory = self.memory[-200:]
        features = self._extract(observation)
        candidates = self._generate(features, observation)
        accepted = 0
        existing_keys = {
            (c.kind, str(c.payload.get("text", ""))[:80]) for c in self.registry
        }
        for c in candidates:
            ok, scores = self._validate(c, observation)
            c.scores = scores
            c.accepted = ok
            key = (c.kind, str(c.payload.get("text", ""))[:80])
            if ok and key not in existing_keys:
                self.registry.append(c)
                existing_keys.add(key)
                accepted += 1
            elif ok:
                c.accepted = False  # duplicate
        self._save()
        return EvolutionReport(
            cycle_id=str(uuid.uuid4())[:8],
            candidates_total=len(candidates),
            accepted=accepted,
            rejected=len(candidates) - accepted,
            notes="Мета-цикл завершён. Кандидаты — гипотезы, не законы природы. Дубликаты отфильтрованы.",
        )

    def _extract(self, obs: Dict[str, Any]) -> Dict[str, Any]:
        patterns = obs.get("patterns", [])
        risk = float(obs.get("risk", 0.0))
        return {
            "pattern_count": len(patterns),
            "has_rumination": "rumination_loop" in patterns,
            "has_moral_erosion": "moral_erosion_proxy" in patterns,
            "high_risk": risk >= 0.65,
            "risk": risk,
        }

    def _generate(self, features: Dict[str, Any], obs: Dict[str, Any]) -> List[Candidate]:
        cands: List[Candidate] = []
        base = {"source_risk": features["risk"], "patterns": obs.get("patterns", [])}

        cands.append(Candidate(
            id=str(uuid.uuid4())[:8], kind="hypothesis",
            payload={**base, "text": "При высоком risk приоритет — восстановление, не интерпретация."},
        ))
        if features.get("has_rumination"):
            cands.append(Candidate(
                id=str(uuid.uuid4())[:8], kind="pattern",
                payload={**base, "text": "Руминации снижаются через телесное прерывание, а не анализ."},
            ))
        if features.get("has_moral_erosion"):
            cands.append(Candidate(
                id=str(uuid.uuid4())[:8], kind="rule",
                payload={**base, "text": "При moral_erosion_proxy — обязательная пауза и human review."},
            ))
        cands.append(Candidate(
            id=str(uuid.uuid4())[:8], kind="algorithm",
            payload={**base, "text": "Периодически пересчитывать ethical balance при смене сценария."},
        ))
        return cands

    def _validate(self, candidate: Candidate, obs: Dict[str, Any]) -> tuple[bool, Dict[str, float]]:
        # Простая эвристическая валидация
        scores = {
            "usefulness": 0.75,
            "stability": 0.70,
            "reproducibility": 0.70,
            "ethics": 0.85,
            "compatibility": 0.80,
        }
        if candidate.kind == "hypothesis" and float(obs.get("risk", 0)) < 0.3:
            scores["usefulness"] = 0.55
        accepted = all(v >= self.threshold for v in scores.values())
        return accepted, scores

    def registry_summary(self) -> Dict[str, Any]:
        by_kind: Dict[str, int] = {}
        for c in self.registry:
            by_kind[c.kind] = by_kind.get(c.kind, 0) + 1
        return {
            "total_accepted": len(self.registry),
            "by_kind": by_kind,
            "epistemic_status": "research_registry_not_truth",
        }
