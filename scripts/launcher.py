#!/usr/bin/env python3
"""
PNEUMA Symbiosis — точка входа для Windows / CLI.

Использование:
  python scripts/launcher.py
  python scripts/launcher.py --mode archetypal --steps 60 --scenario stress
  PNEUMA-Symbiosis.exe   (после сборки PyInstaller)
"""

from __future__ import annotations
import sys
import os
from pathlib import Path

# Корень проекта в PYTHONPATH
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.chdir(ROOT)


def main(argv: list[str] | None = None) -> int:
    argv = list(argv if argv is not None else sys.argv[1:])

    # Без аргументов — короткая демо-сессия
    if not argv:
        argv = [
            "run",
            "--mode", "scientific",
            "--steps", "40",
            "--scenario", "baseline",
            "--export", "session_out.json",
        ]
    elif argv and argv[0] != "run" and not argv[0].startswith("-"):
        pass
    elif argv and argv[0].startswith("--"):
        argv = ["run"] + argv

    # Подмена sys.argv для argparse в pneuma.cli
    sys.argv = ["pneuma"] + argv

    try:
        from pneuma.cli import main as cli_main
        cli_main()
        return 0
    except SystemExit as e:
        return int(e.code or 0)
    except Exception as exc:
        print(f"[PNEUMA] Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
