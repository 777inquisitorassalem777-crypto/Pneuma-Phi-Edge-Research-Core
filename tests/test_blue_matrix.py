"""Тесты полной реализации Blue Matrix."""

from sophia.blue_matrix import (
    BlueMatrix, DictAdapter, StubHardwareAdapter, PneumaFrameAdapter,
    MovingAverage, ExponentialSmoothing, SpikeReject, default_channel_registry,
)
from pneuma.sensors.simulator import SensorSimulator
from pneuma.analytics.engine import AnalyticsEngine


def test_default_channels():
    reg = default_channel_registry()
    assert "hrv" in reg
    assert "ethical_tension" in reg
    assert 0 <= reg["hrv"].normalize(50) <= 1


def test_filters():
    ma = MovingAverage(3)
    assert ma.push(1.0) == 1.0
    assert abs(ma.push(3.0) - 2.0) < 1e-6
    ema = ExponentialSmoothing(0.5)
    v1 = ema.push(0.0)
    v2 = ema.push(1.0)
    assert 0 < v2 < 1
    sp = SpikeReject(0.3)
    assert sp.push(0.5) == 0.5
    assert sp.push(0.9) == 0.5  # rejected


def test_dict_adapter_ingest():
    raw = {"hrv": 60, "stress": 3, "focus": 7, "co2": 700, "noise": 30, "ethical_tension": 0.2}
    m = BlueMatrix(adapter=DictAdapter(raw), enable_filters=False)
    snap = m.ingest()
    assert len(snap.readings) >= 5
    assert 0 <= snap.health_score <= 1
    assert "physiology" in snap.aggregate or len(snap.aggregate) >= 1


def test_pneuma_frame_path():
    sim = SensorSimulator(seed=1, scenario="stress")
    eng = AnalyticsEngine()
    m = BlueMatrix()
    f = sim.next()
    r = eng.analyze(f)
    readings = m.from_pneuma_frame(f, r)
    assert any(x.sensor_id == "hrv" for x in readings)
    assert any(x.sensor_id == "ethical_tension" for x in readings)
    eth = next(x for x in readings if x.sensor_id == "ethical_tension")
    assert "derived" in eth.note


def test_health_higher_in_recovery():
    sim_s = SensorSimulator(seed=2, scenario="stress")
    sim_r = SensorSimulator(seed=2, scenario="recovery")
    eng_s, eng_r = AnalyticsEngine(), AnalyticsEngine()
    m_s, m_r = BlueMatrix(enable_filters=False), BlueMatrix(enable_filters=False)
    for _ in range(15):
        fs, fr = sim_s.next(), sim_r.next()
        m_s.ingest(frame=fs, report=eng_s.analyze(fs))
        m_r.ingest(frame=fr, report=eng_r.analyze(fr))
    assert m_r.summary()["avg_health"] > m_s.summary()["avg_health"]


def test_calibrate_and_disable():
    m = BlueMatrix(adapter=DictAdapter({"hrv": 50}), enable_filters=False)
    m.calibrate("hrv", 0, 200)
    m.set_channel_enabled("noise", False)
    snap = m.ingest(raw={"hrv": 100, "noise": 40})
    ids = [r.sensor_id for r in snap.readings]
    assert "hrv" in ids
    assert "noise" not in ids


def test_history_bound():
    m = BlueMatrix(adapter=DictAdapter({"hrv": 50, "stress": 2}), max_history=5, enable_filters=False)
    for _ in range(12):
        m.ingest()
    assert len(m.history) <= 5


def test_stub_hardware():
    stub = StubHardwareAdapter()
    stub.inject(hrv=70, stress=2)
    m = BlueMatrix(adapter=stub, enable_filters=False)
    snap = m.ingest()
    assert snap.health_score > 0.4


def test_orchestrator_still_works():
    from symbiosis.orchestrator import SymbiosisOrchestrator
    orch = SymbiosisOrchestrator(mode="scientific", seed=5)
    result = orch.run(steps=12, scenario="baseline")
    assert "symbiosis" in result
    assert result["symbiosis"]["avg_blue_health"] >= 0
