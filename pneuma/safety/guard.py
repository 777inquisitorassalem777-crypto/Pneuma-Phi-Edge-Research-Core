"""SafetyGate — human-in-the-loop + append-only audit log."""

from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from ..ethics.core import EthicsCore
from ..core.models import EthicalVerdict


class SafetyGate:
    """
    Все критические действия проходят через этику и пишутся в неизменяемый журнал.
    """

    def __init__(self, audit_path: str = "audit.jsonl", ethics: Optional[EthicsCore] = None):
        self.audit_path = Path(audit_path)
        self.ethics = ethics or EthicsCore()
        self.records: List[Dict[str, Any]] = []

    def request(
        self,
        step: int,
        action: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        context = context or {}
        verdict: EthicalVerdict = self.ethics.evaluate(action, context)
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "step": step,
            "action": action,
            "allowed": verdict.allowed,
            "reason": verdict.reason,
            "virtue_signal": verdict.virtue_signal,
            "vice_signal": verdict.vice_signal,
            "uncertainty": verdict.uncertainty,
            "requires_human": (not verdict.allowed) or bool(context.get("irreversible", False)),
            "context_risk": context.get("risk"),
            "context_patterns": context.get("patterns", []),
        }
        self._append(record)
        self.records.append(record)
        return record

    def _append(self, record: Dict[str, Any]) -> None:
        with self.audit_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def summary(self) -> Dict[str, Any]:
        if not self.records:
            return {"total": 0}
        blocked = sum(1 for r in self.records if not r["allowed"])
        return {
            "total_requests": len(self.records),
            "blocked": blocked,
            "allowed": len(self.records) - blocked,
            "last_action": self.records[-1]["action"] if self.records else None,
        }
