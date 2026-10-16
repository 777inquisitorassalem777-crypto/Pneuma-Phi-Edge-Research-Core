"""Тесты объединённого проекта."""

from pneuma_edge.sensors.simulator import SensorSimulator
from pneuma_edge.analytics.engine import AnalyticsEngine
from pneuma_edge.reflection.module import ReflectionModule
from pneuma_edge.reflection.archetypal import ArchetypalLayer
from pneuma_edge.archetypal.war_cycle import WarCycleSimulator
from pneuma_edge.archetypal.rumination import RuminationSimulator
from pneuma_edge.archetypal.entities import HumanSoul
from pneuma_edge.cli import run_session


def test_sensor_scenarios():
    for sc in ("baseline", "stress", "recovery", "isolation"):
        sim = SensorSimulator(seed=1, scenario=sc)
        frame = sim.next()
        assert frame.hrv_ms > 0
        assert 0 <= frame.subjective_stress <= 10


def test_analytics_patterns():
    sim = SensorSimulator(seed=2, scenario="stress")
    eng = AnalyticsEngine()
    for _ in range(30):
        report = eng.analyze(sim.next())
    assert isinstance(report.patterns, list)
    assert 0 <= report.risk <= 1


def test_reflection_status():
    sim = SensorSimulator(seed=3)
    eng = AnalyticsEngine()
    ref = ReflectionModule()
    frame = sim.next()
    report = eng.analyze(frame)
    refl = ref.reflect(frame, report)
    assert refl["epistemic_status"] == "hypothesis_not_fact"


def test_archetypal_layer_disclaimer():
    sim = SensorSimulator(seed=4, scenario="stress")
    eng = AnalyticsEngine()
    layer = ArchetypalLayer()
    frame = sim.next()
    report = eng.analyze(frame)
    arch = layer.interpret(frame, report)
    assert arch["epistemic_status"] == "archetypal_hypothesis_not_fact"
    assert "disclaimer" in arch


def test_war_cycle_hypothesis():
    sim = WarCycleSimulator(population=40, seed=5)
    summary = sim.run(cycles=2)
    assert summary["epistemic_status"] == "archetypal_hypothesis_not_fact"
    assert "total_harvested" in summary


def test_rumination():
    soul = HumanSoul(name="T", frequency=0.6)
    sim = RuminationSimulator(seed=6)
    events = sim.simulate(soul, steps=8)
    assert len(events) == 8
    assert events[-1].rumination_level > 0


def test_cli_scientific():
    result = run_session(steps=20, scenario="baseline", mode="scientific", export=None, seed=7)
    assert result["mode"] == "scientific"
    assert "archetypal_layer" not in result


def test_cli_archetypal():
    result = run_session(steps=15, scenario="stress", mode="archetypal", export=None, seed=8)
    assert result["mode"] == "archetypal"
    assert "archetypal_layer" in result
    assert result["war_cycle_hypothesis"]["epistemic_status"] == "archetypal_hypothesis_not_fact"
