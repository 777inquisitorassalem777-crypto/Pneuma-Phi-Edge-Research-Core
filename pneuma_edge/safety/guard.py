"""SafetyGate — human-in-the-loop + append-only audit."""

from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timezone
from ..ethics.core import EthicsCore


class SafetyGate:
    def __init__(self, audit_path: str = "audit.jsonl"):
        self.audit_path = Path(audit_path)
        self.ethics = EthicsCore()

    def request(self, step: int, action: str, context: dict | None = None) -> dict:
        context = context or {}
        allowed, reason = self.ethics.evaluate(action, context)
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "step": step,
            "action": action,
            "allowed": allowed,
            "reason": reason,
            "context": context,
            "requires_human": not allowed or context.get("irreversible", False),
        }
        self._append(record)
        return record

    def _append(self, record: dict) -> None:
        with self.audit_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
