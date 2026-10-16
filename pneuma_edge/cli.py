"""CLI — два режима: scientific и archetypal."""

from __future__ import annotations
import argparse
import json
from pathlib import Path

from .sensors.simulator import SensorSimulator
from .analytics.engine import AnalyticsEngine
from .reflection.module import ReflectionModule
from .reflection.archetypal import ArchetypalLayer
from .safety.guard import SafetyGate
from .reporting.report import ReportBuilder
from .archetypal.war_cycle import WarCycleSimulator


def run_session(
    steps: int,
    scenario: str,
    mode: str,
    export: str | None,
    seed: int,
) -> dict:
    simulator = SensorSimulator(seed=seed, scenario=scenario)
    analytics = AnalyticsEngine()
    reflection = ReflectionModule()
    archetypal = ArchetypalLayer() if mode == "archetypal" else None
    safety = SafetyGate()
    reporter = ReportBuilder()

    frames, reports, reflections, arch_data = [], [], [], []

    for _ in range(steps):
        frame = simulator.next()
        report = analytics.analyze(frame)
        refl = reflection.reflect(frame, report)

        frames.append(frame.to_dict())
        reports.append(report.to_dict())
        reflections.append(refl)

        if archetypal:
            arch = archetypal.interpret(frame, report)
            arch_data.append(arch)

        if report.risk >= 0.75:
            safety.request(frame.step, "pause_and_notify_user", {
                "risk": report.risk,
                "irreversible": False,
                "human_approved": False,
            })

    war_summary = None
    if mode == "archetypal":
        war_sim = WarCycleSimulator(population=80, seed=seed)
        war_summary = war_sim.run(cycles=3)

    result = reporter.build(
        mode=mode,
        scenario=scenario,
        frames=frames,
        reports=reports,
        reflections=reflections,
        archetypal=arch_data if mode == "archetypal" else None,
        war_summary=war_summary,
    )

    if export:
        json_path = export if export.endswith(".json") else export + ".json"
        md_path = json_path.replace(".json", ".md")
        reporter.export(result, json_path, md_path)
        result["_exported"] = {"json": json_path, "markdown": md_path}

    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="PNEUMA-Edge Unified v0.2")
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="Run a session")
    run.add_argument("--mode", choices=["scientific", "archetypal"], default="scientific")
    run.add_argument("--steps", type=int, default=100)
    run.add_argument("--scenario", choices=["baseline", "stress", "recovery", "isolation"], default="baseline")
    run.add_argument("--seed", type=int, default=42)
    run.add_argument("--export", default=None)

    args = parser.parse_args()

    if args.command == "run":
        result = run_session(args.steps, args.scenario, args.mode, args.export, args.seed)
        last = result["reports"][-1]
        print(f"Mode: {result['mode']}")
        print(f"Session complete: {result['steps']} steps")
        print(f"Final risk: {last['risk']:.3f}")
        print(f"Patterns: {', '.join(last['patterns']) or 'none'}")
        if result["mode"] == "archetypal" and result.get("war_cycle_hypothesis"):
            w = result["war_cycle_hypothesis"]
            print(f"[archetypal] total_harvested (metaphor): {w.get('total_harvested')}")
            print(f"[archetypal] epistemic_status: {w.get('epistemic_status')}")
        if "_exported" in result:
            print(f"Exported: {result['_exported']}")


if __name__ == "__main__":
    main()
