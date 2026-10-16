"""Генерация отчётов JSON + Markdown + данные для визуализации."""

from __future__ import annotations
from typing import Dict, Any, List, Optional
from pathlib import Path
import json
from datetime import datetime, timezone


class ReportBuilder:
    def build(
        self,
        mode: str,
        scenario: str,
        frames: List[dict],
        reports: List[dict],
        reflections: List[dict],
        intuitions: List[dict],
        ethics_log: List[dict],
        archetypal: Optional[List[dict]] = None,
        safety_summary: Optional[dict] = None,
        analytics_summary: Optional[dict] = None,
    ) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "project": "PNEUMA Full",
            "version": "0.4.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "mode": mode,
            "scenario": scenario,
            "steps": len(frames),
            "frames": frames,
            "reports": reports,
            "reflections": reflections,
            "intuitions": intuitions,
            "ethics": ethics_log,
            "visualization": self._viz_data(reports),
            "epistemic_global": "research_platform_not_consciousness",
            "disclaimer": (
                "Система не обладает сознанием, душой или субъективным опытом. "
                "Все архетипические и этические выводы — модели и гипотезы."
            ),
        }
        if safety_summary:
            data["safety_summary"] = safety_summary
        if analytics_summary:
            data["analytics_summary"] = analytics_summary
        if mode == "archetypal" and archetypal:
            data["archetypal_layer"] = archetypal
            data["global_archetypal_disclaimer"] = (
                "Архетипический слой имеет статус archetypal_hypothesis_not_fact "
                "и не утверждает существование душ или сущностей."
            )
        return data

    def _viz_data(self, reports: List[dict]) -> Dict[str, List]:
        return {
            "steps": [r["step"] for r in reports],
            "arousal": [r["arousal"] for r in reports],
            "recovery": [r["recovery"] for r in reports],
            "risk": [r["risk"] for r in reports],
            "coherence": [r.get("coherence", 0) for r in reports],
        }

    def to_markdown(self, data: Dict[str, Any]) -> str:
        lines = [
            f"# PNEUMA Full Report",
            f"- Mode: **{data['mode']}**",
            f"- Scenario: **{data['scenario']}**",
            f"- Steps: **{data['steps']}**",
            f"- Generated: {data.get('generated_at', 'n/a')}",
            f"- Epistemic status: `{data.get('epistemic_global')}`",
            "",
            data.get("disclaimer", ""),
            "",
        ]
        if data.get("reports"):
            last = data["reports"][-1]
            lines += [
                "## Final state",
                f"- Risk: `{last['risk']:.3f}`",
                f"- Arousal: `{last['arousal']:.3f}`",
                f"- Recovery: `{last['recovery']:.3f}`",
                f"- Patterns: {', '.join(last.get('patterns', [])) or 'none'}",
                f"- Interpretation: {last.get('interpretation', '')}",
                "",
            ]
        if data.get("analytics_summary"):
            s = data["analytics_summary"]
            lines += [
                "## Analytics summary",
                f"- Steps analyzed: {s.get('steps_analyzed')}",
                f"- Average risk: {s.get('avg_risk')}",
                f"- Max risk: {s.get('max_risk')}",
                "",
            ]
        if data.get("mode") == "archetypal":
            lines += [
                "## Archetypal layer",
                data.get("global_archetypal_disclaimer", ""),
                "",
            ]
        lines.append("---\n*PNEUMA Full v0.4.0 — research platform, not consciousness*")
        return "\n".join(lines)

    def export(self, data: Dict[str, Any], json_path: str, md_path: Optional[str] = None) -> None:
        Path(json_path).write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        if md_path:
            Path(md_path).write_text(self.to_markdown(data), encoding="utf-8")
