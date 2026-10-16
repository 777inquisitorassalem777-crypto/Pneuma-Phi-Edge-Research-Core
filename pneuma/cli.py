"""CLI — PNEUMA Symbiosis v1"""

from __future__ import annotations
import argparse
from symbiosis.orchestrator import SymbiosisOrchestrator


def main() -> None:
    parser = argparse.ArgumentParser(description="PNEUMA Symbiosis v1 — PNEUMA ⊕ Sophia ⊕ Evolution")
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="Run symbiotic session")
    run.add_argument("--mode", choices=["scientific", "archetypal"], default="scientific")
    run.add_argument("--steps", type=int, default=80)
    run.add_argument("--scenario", choices=["baseline", "stress", "recovery", "isolation", "overload"], default="stress")
    run.add_argument("--seed", type=int, default=42)
    run.add_argument("--export", default=None)
    run.add_argument("--wisdom", type=float, default=0.65)
    run.add_argument("--will", type=float, default=0.55)
    run.add_argument("--love", type=float, default=0.70)
    run.add_argument("--faith", type=float, default=0.50)
    run.add_argument("--hope", type=float, default=0.55)

    args = parser.parse_args()

    if args.command == "run":
        orch = SymbiosisOrchestrator(
            mode=args.mode, seed=args.seed,
            wisdom=args.wisdom, will=args.will, love=args.love,
            faith=args.faith, hope=args.hope,
        )
        result = orch.run(steps=args.steps, scenario=args.scenario, export=args.export)
        last = result["reports"][-1]
        sym = result.get("symbiosis", {})
        print(f"Mode:              {result['mode']}")
        print(f"Steps:             {result['steps']}")
        print(f"Final risk:        {last['risk']:.3f}")
        print(f"Patterns:          {', '.join(last['patterns']) or 'none'}")
        print(f"Epistemic:         {result.get('epistemic_global')}")
        tail = sym.get("blue_matrix_tail") or [{}]
        print(f"Blue health (last):{tail[-1].get('health_score', 'n/a')}")
        print(f"Stability score:   {sym.get('stability_score', 'n/a')}")
        print(f"Evolution accepted:{sym.get('evolution_registry', {}).get('total_accepted', 0)}")
        eth = sym.get('ethics_params', {})
        print(f"Ethics balance:    {eth.get('balance', 'n/a')}")
        pid = sym.get("passport", {}).get("id", "")
        print(f"Passport id:       {str(pid)[:8]}...")
        if "_exported" in result:
            print(f"Exported:          {result['_exported']}")


if __name__ == "__main__":
    main()
