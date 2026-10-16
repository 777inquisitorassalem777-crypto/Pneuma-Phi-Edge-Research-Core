"""Тесты симбиоза."""

from symbiosis.orchestrator import SymbiosisOrchestrator
from sophia.blue_matrix.matrix import BlueMatrix
from sophia.wisdom.layer import WisdomLayer
from sophia.evolution.loop import EvolutionLoop
from sophia.passport.identity import Passport
from pneuma.sensors.simulator import SensorSimulator
from pneuma.analytics.engine import AnalyticsEngine


def test_blue_matrix():
    sim = SensorSimulator(seed=1, scenario="stress")
    eng = AnalyticsEngine()
    blue = BlueMatrix()
    f = sim.next()
    r = eng.analyze(f)
    readings = blue.from_pneuma_frame(f, r)
    assert len(readings) >= 5
    assert 0 <= blue.health_score(readings) <= 1


def test_wisdom_counsel():
    w = WisdomLayer()
    out = w.counsel(0.7, 0.3, 0.8, ["rumination_loop"])
    assert out["epistemic_status"] == "ethical_model_not_doctrine"
    assert "guna" in out


def test_evolution_cycle():
    evo = EvolutionLoop(data_dir="/tmp/evo_test")
    report = evo.cycle({"risk": 0.8, "patterns": ["rumination_loop", "moral_erosion_proxy"]})
    assert report.candidates_total >= 1
    assert report.epistemic_status == "research_loop_not_consciousness"


def test_passport():
    p = Passport(name="test")
    p.update_from_session(10, 0.6, 1, 2, {"wisdom": 0.7}, "note")
    assert p.total_steps == 10
    assert p.epistemic_status == "identity_record_not_soul"


def test_orchestrator_scientific():
    orch = SymbiosisOrchestrator(mode="scientific", seed=3)
    result = orch.run(steps=15, scenario="baseline")
    assert result["mode"] == "scientific"
    assert "symbiosis" in result
    assert result["symbiosis"]["epistemic_status"] == "research_platform_not_consciousness"


def test_orchestrator_archetypal():
    orch = SymbiosisOrchestrator(mode="archetypal", seed=4)
    result = orch.run(steps=15, scenario="stress")
    assert result["mode"] == "archetypal"
    assert "archetypal_layer" in result


def test_stability_score_present():
    orch = SymbiosisOrchestrator(mode="scientific", seed=11)
    result = orch.run(steps=20, scenario="recovery")
    sym = result["symbiosis"]
    assert "stability_score" in sym
    assert 0.0 <= sym["stability_score"] <= 1.0
    assert "ethics_params" in sym
    assert "balance" in sym["ethics_params"]


def test_evolution_dedupes():
    evo = EvolutionLoop(data_dir="/tmp/evo_dedupe_test")
    r1 = evo.cycle({"risk": 0.8, "patterns": ["rumination_loop"]})
    n1 = evo.registry_summary()["total_accepted"]
    r2 = evo.cycle({"risk": 0.8, "patterns": ["rumination_loop"]})
    n2 = evo.registry_summary()["total_accepted"]
    # second cycle should not inflate registry with identical texts
    assert n2 <= n1 + 1


def test_blue_matrix_history_bounded():
    from pneuma.sensors.simulator import SensorSimulator
    from pneuma.analytics.engine import AnalyticsEngine
    sim = SensorSimulator(seed=1, scenario="baseline")
    eng = AnalyticsEngine()
    blue = BlueMatrix(max_history=5)
    for _ in range(12):
        f = sim.next()
        r = eng.analyze(f)
        blue.from_pneuma_frame(f, r)
    assert len(blue.history) <= 5
