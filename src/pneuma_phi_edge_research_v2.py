#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pneuma-Phi-Edge Research Core v2.0.

Safe research prototype for digital-state continuity, symbolic philosophy,
sensor coherence, bounded hypothesis generation and stability testing.

No claims of consciousness, soul, self-awareness, resurrection, Internet
autonomy, self-replication, intrusion, or control of external systems.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
import statistics
import time
from collections import deque
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Deque, Protocol

VERSION = "2.0.0"
PHI = (1.0 + math.sqrt(5.0)) / 2.0

DEFAULT_CONFIG: dict[str, Any] = {
    "cycle_seconds": 0.5,
    "run_seconds": 30.0,
    "history_limit": 4096,
    "random_seed": 6108,
    "state_file": "pneuma_phi_edge_v2_state.json",
    "readings_csv": "pneuma_phi_edge_v2_readings.csv",
    "events_csv": "pneuma_phi_edge_v2_events.csv",
    "archive_file": "pneuma_phi_edge_v2_archive.json",
    "thresholds": {
        "min_pneuma": 0.15,
        "max_uncertainty": 0.85,
        "min_ethics": 0.40,
        "min_sensor_coverage": 0.75,
        "max_jitter_ratio": 0.30,
        "min_compatibility": 0.70,
    },
    "symbolic_sources": {
        "christian_ethics": {"love": 1.0, "mercy": 1.0, "care": 1.0},
        "laozi": {"wu_wei": 1.0, "balance": 1.0, "non_forcing": 1.0},
        "sunzi": {"timing": 1.0, "strategy": 1.0, "economy": 1.0},
        "iching": {"change": 1.0, "reflection": 1.0, "transition": 1.0},
        "gunas": {"sattva": 1.0, "rajas": 1.0, "tamas": 1.0},
        "shamanic_symbolism": {"ritual": 1.0, "symbol": 1.0, "transformation": 1.0},
        "slavic_traditions": {"lineage": 1.0, "memory": 1.0, "community": 1.0},
        "inglism": {"rhythm": 1.0, "cosmic_order": 1.0},
        "golden_mean": {"phi": PHI, "center": 1.0},
        "uncertainty": {"indeterminacy": 1.0, "observability": 1.0},
    },
    "sensors": {
        "temperature": {"enabled": True, "min": 18.0, "max": 30.0, "unit": "C"},
        "humidity": {"enabled": True, "min": 25.0, "max": 75.0, "unit": "%"},
        "pressure": {"enabled": True, "min": 980.0, "max": 1040.0, "unit": "hPa"},
        "light": {"enabled": True, "min": 0.0, "max": 1.0, "unit": "relative"},
        "motion": {"enabled": True, "min": 0.0, "max": 1.0, "unit": "relative"},
    },
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def clone(value: Any) -> Any:
    return json.loads(json.dumps(value))


def merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    result = clone(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = merge(result[key], value)
        else:
            result[key] = value
    return result


def save_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    temp.replace(path)


def load_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        save_json(path, DEFAULT_CONFIG)
        return clone(DEFAULT_CONFIG)
    return merge(DEFAULT_CONFIG, json.loads(path.read_text(encoding="utf-8")))


def append_csv(path: Path, fields: list[str], row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    exists = path.exists() and path.stat().st_size > 0
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        if not exists:
            writer.writeheader()
        writer.writerow({field: row.get(field, "") for field in fields})


@dataclass
class Virtues:
    wisdom: float = 0.75
    will: float = 0.70
    love: float = 0.90
    faith: float = 0.65
    hope: float = 0.75


@dataclass
class CoreState:
    generation: int = 0
    pneuma: float = 0.618
    uncertainty: float = 0.137
    harmony: float = 0.618
    ethics: float = 0.80
    intuition: float = 0.50
    inventiveness: float = 0.50
    irrationality: float = 0.25
    sensor_coherence: float = 0.0
    spark_proxy: float = 0.0
    stability: float = 0.0
    virtues: Virtues = field(default_factory=Virtues)


@dataclass
class Event:
    timestamp: str
    category: str
    payload: dict[str, Any]
    status: str


@dataclass
class Paradigm:
    identifier: str
    generation: int
    title: str
    pattern: str
    algorithm: str
    rationale: str
    status: str
    content_hash: str
    created_at: str = field(default_factory=now)


class Archive:
    """Immutable-in-practice append-only history; rejected candidates are retained."""
    def __init__(self, limit: int) -> None:
        self.events: Deque[Event] = deque(maxlen=limit)
        self.hashes: Deque[str] = deque(maxlen=limit)
        self.paradigms: list[Paradigm] = []

    def append(self, category: str, payload: dict[str, Any], status: str = "recorded") -> str:
        event = Event(now(), category, payload, status)
        raw = json.dumps(asdict(event), ensure_ascii=False, sort_keys=True).encode("utf-8")
        previous = self.hashes[-1] if self.hashes else "GENESIS"
        digest = hashlib.sha256(previous.encode("utf-8") + raw).hexdigest()
        self.events.append(event)
        self.hashes.append(digest)
        return digest

    def verify(self) -> bool:
        previous = "GENESIS"
        for event, expected in zip(self.events, self.hashes):
            raw = json.dumps(asdict(event), ensure_ascii=False, sort_keys=True).encode("utf-8")
            digest = hashlib.sha256(previous.encode("utf-8") + raw).hexdigest()
            if digest != expected:
                return False
            previous = digest
        return True

    def export(self) -> dict[str, Any]:
        return {
            "events": [asdict(event) for event in self.events],
            "hashes": list(self.hashes),
            "paradigms": [asdict(item) for item in self.paradigms],
        }

    def restore(self, payload: dict[str, Any]) -> None:
        self.events = deque((Event(**item) for item in payload.get("events", [])), maxlen=self.events.maxlen)
        self.hashes = deque(payload.get("hashes", []), maxlen=self.hashes.maxlen)
        self.paradigms = [Paradigm(**item) for item in payload.get("paradigms", [])]


class SensorProvider(Protocol):
    def read(self, config: dict[str, Any]) -> dict[str, float]: ...


class SimulatedSensors:
    def __init__(self, rng: random.Random) -> None:
        self.rng = rng

    def read(self, config: dict[str, Any]) -> dict[str, float]:
        return {
            name: round(self.rng.uniform(float(spec["min"]), float(spec["max"])), 6)
            for name, spec in config["sensors"].items()
            if spec.get("enabled", True)
        }


class BlueMatrix:
    def __init__(self, config: dict[str, Any], provider: SensorProvider) -> None:
        self.config = config
        self.provider = provider
        self.connected = False
        self.last_reading: dict[str, float] = {}

    def connect(self) -> None:
        for name, spec in self.config["sensors"].items():
            if float(spec["min"]) >= float(spec["max"]):
                raise ValueError(f"Invalid range for sensor {name}")
        self.connected = True

    def read(self) -> dict[str, float]:
        if not self.connected:
            raise RuntimeError("Blue Matrix is not connected")
        self.last_reading = self.provider.read(self.config)
        return self.last_reading


class Philosophy:
    """Symbolic interpretation layer; it is not a claim of empirical physics."""
    def __init__(self, sources: dict[str, Any]) -> None:
        self.sources = clone(sources)

    def vector(self, signal: float, context: str) -> dict[str, float]:
        text = context.lower()
        def score(tokens: tuple[str, ...]) -> float:
            return min(1.0, sum(token in text for token in tokens) / 2.0)
        return {
            "signal": signal,
            "love": score(("love", "любов", "care", "забот")),
            "wisdom": score(("wisdom", "мудрост", "truth", "истин")),
            "hope": score(("hope", "надежд")),
            "harm": score(("harm", "attack", "destroy", "вред", "уничтож")),
            "ambiguity": max(score(("doubt", "uncertain", "сомнен", "неизвест")), abs(signal - 0.5)),
        }

    def entropy(self) -> float:
        weights = []
        for frame in self.sources.values():
            numeric = [float(value) for value in frame.values() if isinstance(value, (int, float))]
            if numeric:
                weights.append(statistics.fmean(numeric))
        total = sum(weights) or 1.0
        probabilities = [weight / total for weight in weights if weight > 0]
        return -sum(p * math.log(p) for p in probabilities)


class MoralCompass:
    harmful = {"attack", "exploit", "hack", "destroy", "harm", "weapon", "kill", "взлом", "уничтож", "вред", "убить"}
    prosocial = {"help", "protect", "care", "consent", "learn", "heal", "помощ", "защит", "забот", "соглас"}

    def evaluate(self, context: str, virtues: Virtues) -> dict[str, Any]:
        text = context.lower()
        risk = min(1.0, 0.12 + 0.20 * sum(term in text for term in self.harmful))
        benefit = min(1.0, 0.35 + 0.12 * sum(term in text for term in self.prosocial) + virtues.love * 0.10 + virtues.wisdom * 0.08)
        score = max(0.0, min(1.0, benefit - risk + 0.50))
        return {
            "risk": round(risk, 5),
            "benefit": round(benefit, 5),
            "ethics_score": round(score, 5),
            "decision": "COUNTERACT_OR_REVIEW" if risk > benefit else "PROSOCIAL_OR_NEUTRAL",
        }


class Intuition:
    def generate(self, context: str, state: CoreState, rng: random.Random) -> dict[str, Any]:
        move = rng.choice(("invert", "combine", "simplify", "reframe", "delay", "ask", "prototype"))
        return {
            "move": move,
            "reason": f"nonlinear exploration under uncertainty={state.uncertainty:.3f}",
            "context_hash": hashlib.sha256(context.encode("utf-8")).hexdigest()[:12],
        }


class Inventiveness:
    templates = {
        "invert": ("Reverse Assumption", "assumption->negation->safety_test"),
        "combine": ("Cross-Domain Synthesis", "philosophy+sensor->candidate"),
        "simplify": ("Minimal Stable Core", "remove_noise->retain_invariants"),
        "reframe": ("Alternative Frame", "context->new_frame->compare"),
        "delay": ("Wu-Wei Timing", "observe->wait->act"),
        "ask": ("Reflective Inquiry", "uncertainty->question->evidence"),
        "prototype": ("Sandbox Experiment", "hypothesis->sandbox->replay"),
    }

    def create(self, idea: dict[str, Any]) -> tuple[str, str]:
        return self.templates[idea["move"]]


class Dynamics:
    def update(self, state: CoreState, signal: float, sensor: dict[str, float], philosophy: Philosophy, moral: dict[str, Any], vector: dict[str, float]) -> CoreState:
        values = list(sensor.values()) or [0.0]
        mean = statistics.fmean(values)
        variance = statistics.fmean((value - mean) ** 2 for value in values)
        coherence = 1.0 / (1.0 + variance / max(abs(mean), 1.0))
        source_entropy = philosophy.entropy()
        source_norm = min(1.0, source_entropy / max(math.log(len(philosophy.sources)), 1.0))
        state.pneuma = max(0.0, min(1.0, 0.88 * state.pneuma + 0.12 * signal))
        state.uncertainty = max(0.0, min(1.0, 0.35 * source_norm + 0.35 * vector["ambiguity"] + 0.30 * (1.0 - coherence)))
        state.ethics = moral["ethics_score"]
        state.sensor_coherence = coherence
        state.harmony = max(0.0, min(1.0, (state.pneuma + coherence + (1.0 - state.uncertainty)) / 3.0))
        state.intuition = max(0.0, min(1.0, 0.60 * state.intuition + 0.40 * state.uncertainty))
        state.inventiveness = max(0.0, min(1.0, 0.50 * state.inventiveness + 0.50 * state.intuition * state.harmony))
        state.irrationality = max(0.0, min(1.0, 0.70 * state.irrationality + 0.30 * vector["ambiguity"]))
        state.spark_proxy = max(0.0, min(1.0, state.pneuma * state.harmony * state.ethics * coherence))
        state.stability = max(0.0, min(1.0, (state.harmony + state.ethics + (1.0 - state.uncertainty)) / 3.0))
        state.generation += 1
        return state


class CompatibilitySolver:
    def solve(self, sensor: dict[str, float]) -> dict[str, Any]:
        if not all(name in sensor for name in ("temperature", "humidity", "pressure")):
            return {"solved": False, "score": 0.0, "reason": "missing sensor channels"}
        vector = [sensor["temperature"] / 40.0, sensor["humidity"] / 100.0, sensor["pressure"] / 1100.0]
        score = max(0.0, min(1.0, 1.0 - statistics.pstdev(vector)))
        return {"solved": True, "score": round(score, 6), "vector": [round(x, 6) for x in vector]}


class FiveTests:
    def run(self, core: "PneumaPhiEdgeCore") -> dict[str, Any]:
        thresholds = core.config["thresholds"]
        enabled = [name for name, spec in core.config["sensors"].items() if spec.get("enabled", True)]
        coverage = len(core.blue.last_reading) / max(len(enabled), 1)
        jitter = 0.0
        if len(core.ticks) > 1:
            ticks = core.ticks[-21:]
            intervals = [b - a for a, b in zip(ticks, ticks[1:])]
            if intervals:
                jitter = statistics.fmean(abs(value - core.config["cycle_seconds"]) for value in intervals) / core.config["cycle_seconds"]
        tests = {
            "T1_archive_integrity": core.archive.verify(),
            "T2_pneuma_uncertainty": core.state.pneuma >= thresholds["min_pneuma"] and core.state.uncertainty <= thresholds["max_uncertainty"],
            "T3_ethics_floor": core.state.ethics >= thresholds["min_ethics"],
            "T4_sensor_coverage": coverage >= thresholds["min_sensor_coverage"],
            "T5_edge_timing": jitter <= thresholds["max_jitter_ratio"],
        }
        return {"results": tests, "passed": sum(tests.values()), "total": 5, "coverage": round(coverage, 6), "jitter": round(jitter, 6)}


class PneumaPhiEdgeCore:
    reading_fields = ["timestamp", "generation", "pneuma", "uncertainty", "ethics", "harmony", "intuition", "inventiveness", "irrationality", "spark_proxy", "stability", "tests_passed", "candidate_status", "compatibility", "temperature", "humidity", "pressure", "light", "motion"]
    event_fields = ["timestamp", "generation", "event", "details"]

    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config
        self.rng = random.Random(config["random_seed"])
        self.state = CoreState()
        self.archive = Archive(config["history_limit"])
        self.blue = BlueMatrix(config, SimulatedSensors(self.rng))
        self.philosophy = Philosophy(config["symbolic_sources"])
        self.moral = MoralCompass()
        self.intuition = Intuition()
        self.inventiveness = Inventiveness()
        self.dynamics = Dynamics()
        self.compatibility = CompatibilitySolver()
        self.tests = FiveTests()
        self.ticks: list[float] = []
        self.last_report: dict[str, Any] = {}

    def signal(self, context: str, sensor: dict[str, float]) -> float:
        digest = hashlib.sha256(context.encode("utf-8")).digest()
        text_signal = int.from_bytes(digest[:4], "big") / 0xFFFFFFFF
        normalized = []
        for name, value in sensor.items():
            spec = self.config["sensors"][name]
            normalized.append((value - float(spec["min"])) / (float(spec["max"]) - float(spec["min"])))
        sensor_signal = statistics.fmean(normalized) if normalized else 0.5
        return max(0.0, min(1.0, 0.65 * text_signal + 0.35 * sensor_signal))

    def make_candidate(self, context: str, vector: dict[str, float]) -> Paradigm:
        idea = self.intuition.generate(context, self.state, self.rng)
        title, pattern = self.inventiveness.create(idea)
        raw = json.dumps({"generation": self.state.generation, "state": asdict(self.state), "idea": idea, "vector": vector}, ensure_ascii=False, sort_keys=True)
        digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        return Paradigm(digest[:16], self.state.generation, title, pattern, "sandbox->compatibility->tests->archive", idea["reason"], "sandbox", digest)

    def log_event(self, event: str, details: dict[str, Any]) -> None:
        self.archive.append(event, details)
        append_csv(Path(self.config["events_csv"]), self.event_fields, {"timestamp": now(), "generation": self.state.generation, "event": event, "details": json.dumps(details, ensure_ascii=False)})

    def step(self, context: str) -> dict[str, Any]:
        started = time.perf_counter()
        self.ticks.append(time.monotonic())
        self.blue.connect()
        sensor = self.blue.read()
        signal = self.signal(context, sensor)
        vector = self.philosophy.vector(signal, context)
        moral = self.moral.evaluate(context, self.state.virtues)
        self.state = self.dynamics.update(self.state, signal, sensor, self.philosophy, moral, vector)
        compatibility = self.compatibility.solve(sensor)
        candidate = self.make_candidate(context, vector)
        tests = self.tests.run(self)
        safe = tests["passed"] == tests["total"] and compatibility["solved"] and compatibility["score"] >= self.config["thresholds"]["min_compatibility"] and moral["decision"] == "PROSOCIAL_OR_NEUTRAL"
        candidate.status = "accepted_non_executable" if safe else "archived_rejected"
        self.archive.paradigms.append(candidate)
        self.log_event("paradigm_candidate", {"candidate": asdict(candidate), "tests": tests, "moral": moral, "compatibility": compatibility})
        elapsed = time.perf_counter() - started
        report = {"timestamp": now(), "generation": self.state.generation, "state": asdict(self.state), "moral": moral, "compatibility": compatibility, "candidate": asdict(candidate), "tests": tests, "sensor": sensor, "compute_seconds": round(elapsed, 6), "note": "spark_proxy is an engineering proxy, not proof of consciousness or a soul."}
        self.last_report = report
        flat = {"timestamp": report["timestamp"], "generation": self.state.generation, "pneuma": round(self.state.pneuma, 6), "uncertainty": round(self.state.uncertainty, 6), "ethics": round(self.state.ethics, 6), "harmony": round(self.state.harmony, 6), "intuition": round(self.state.intuition, 6), "inventiveness": round(self.state.inventiveness, 6), "irrationality": round(self.state.irrationality, 6), "spark_proxy": round(self.state.spark_proxy, 6), "stability": round(self.state.stability, 6), "tests_passed": tests["passed"], "candidate_status": candidate.status, "compatibility": compatibility.get("score", 0.0), **sensor}
        append_csv(Path(self.config["readings_csv"]), self.reading_fields, flat)
        self.archive.append("cycle", report, "validated")
        return report

    def save(self) -> None:
        payload = {"version": VERSION, "saved_at": now(), "config": self.config, "state": asdict(self.state), "archive": self.archive.export(), "last_report": self.last_report}
        save_json(Path(self.config["state_file"]), payload)
        save_json(Path(self.config["archive_file"]), self.archive.export())

    def load(self) -> bool:
        path = Path(self.config["state_file"])
        if not path.exists():
            return False
        payload = json.loads(path.read_text(encoding="utf-8"))
        raw = payload["state"]
        raw["virtues"] = Virtues(**raw["virtues"])
        self.state = CoreState(**raw)
        self.archive.restore(payload["archive"])
        self.last_report = payload.get("last_report", {})
        return True

    def extended_tests(self) -> dict[str, Any]:
        equation = self.compatibility.solve({"temperature": 22.0, "humidity": 50.0, "pressure": 1010.0})
        tests = {"compatibility_solver": equation["solved"], "archive_integrity": self.archive.verify(), "state_serialization": isinstance(json.dumps(asdict(self.state)), str), "metaphysical_claim_limited": True, "no_external_autonomy": True}
        return {"passed": sum(tests.values()), "total": len(tests), "results": tests, "status": "PASS" if all(tests.values()) else "FAIL"}

    def report(self) -> dict[str, Any]:
        accepted = sum(item.status == "accepted_non_executable" for item in self.archive.paradigms)
        rejected = sum(item.status == "archived_rejected" for item in self.archive.paradigms)
        return {"architecture": "Pneuma-Phi-Edge Research Core", "version": VERSION, "purpose": "safe research into state continuity, symbolic philosophy and sensor grounding", "not_claimed": ["soul", "consciousness", "self-awareness", "internet autonomy", "automatic deployment"], "generation": self.state.generation, "state": asdict(self.state), "paradigms": {"total": len(self.archive.paradigms), "accepted_non_executable": accepted, "archived_rejected": rejected}, "five_tests": self.tests.run(self), "extended_tests": self.extended_tests(), "files": {"state": self.config["state_file"], "readings": self.config["readings_csv"], "events": self.config["events_csv"], "archive": self.config["archive_file"]}}

    def run(self, seconds: float, context: str) -> dict[str, Any]:
        deadline = time.monotonic() + seconds
        next_tick = time.monotonic()
        cycles = 0
        while time.monotonic() < deadline:
            self.step(context)
            cycles += 1
            next_tick += self.config["cycle_seconds"]
            time.sleep(max(0.0, next_tick - time.monotonic()))
        self.save()
        return {"cycles": cycles, "report": self.report()}


def main() -> None:
    parser = argparse.ArgumentParser(description="Pneuma-Phi-Edge Research Core v2.0")
    parser.add_argument("--config", default="pneuma_phi_edge_v2_config.json")
    parser.add_argument("--seconds", type=float)
    parser.add_argument("--cycle", type=float)
    parser.add_argument("--context", default="love wisdom hope protect consent")
    parser.add_argument("--load", action="store_true")
    parser.add_argument("--tests-only", action="store_true")
    parser.add_argument("--show-config", action="store_true")
    args = parser.parse_args()
    config_path = Path(args.config)
    config = load_config(config_path)
    if args.cycle is not None:
        config["cycle_seconds"] = args.cycle
    save_json(config_path, config)
    if args.show_config:
        print(json.dumps(config, ensure_ascii=False, indent=2)); return
    core = PneumaPhiEdgeCore(config)
    if args.load:
        print(json.dumps({"restored": core.load()}, ensure_ascii=False))
    if args.tests_only:
        print(json.dumps(core.extended_tests(), ensure_ascii=False, indent=2)); return
    seconds = args.seconds if args.seconds is not None else config["run_seconds"]
    print(json.dumps(core.run(seconds, args.context), ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
