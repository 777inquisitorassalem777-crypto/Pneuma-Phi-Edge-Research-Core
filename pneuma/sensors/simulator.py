"""Расширенный симулятор сенсоров (физика + физиология)."""

from __future__ import annotations
import math
import random
from typing import Optional
from ..core.models import SensorFrame


class SensorSimulator:
    """
    Детерминированный симулятор.
    Не является медицинским устройством.
    Поддерживает сценарии: baseline, stress, recovery, isolation, overload.
    """

    SCENARIOS = ("baseline", "stress", "recovery", "isolation", "overload")

    def __init__(self, seed: int = 42, scenario: str = "baseline"):
        if scenario not in self.SCENARIOS:
            raise ValueError(f"Unknown scenario: {scenario}. Choose from {self.SCENARIOS}")
        self.rng = random.Random(seed)
        self.step = 0
        self.scenario = scenario
        self._base_hrv = {
            "baseline": 62.0, "stress": 34.0, "recovery": 78.0,
            "isolation": 48.0, "overload": 28.0,
        }[scenario]
        self._history: list[SensorFrame] = []

    def next(self) -> SensorFrame:
        t = self.step * 0.5
        wave = math.sin(t / 7.0) * 6.0 + math.sin(t / 23.0) * 3.0
        noise = self.rng.uniform(-2.5, 2.5)
        slow = math.sin(t / 41.0) * 2.0

        params = self._scenario_params(wave, noise, slow)
        frame = SensorFrame(
            step=self.step,
            timestamp=round(t, 3),
            hrv_ms=round(params["hrv"], 2),
            heart_rate=round(max(48.0, 108.0 - params["hrv"] * 0.52 + self.rng.uniform(-3, 3)), 1),
            temperature_c=round(22.0 + wave * 0.08 + self.rng.uniform(-0.4, 0.4), 2),
            humidity_pct=round(45.0 + wave * 0.3 + self.rng.uniform(-3, 3), 1),
            co2_ppm=round(max(400.0, params["co2"]), 0),
            infrasound_db=round(max(20.0, params["infrasound"]), 1),
            noise_db=round(max(20.0, params["noise_db"]), 1),
            ambient_light_lux=round(max(50.0, 280 + wave * 15 + self.rng.uniform(-40, 40)), 0),
            magnetic_ut=round(45.0 + self.rng.uniform(-1.8, 1.8), 2),
            electrostatic_v=round(120.0 + self.rng.uniform(-18, 18), 1),
            subjective_stress=round(max(0.0, min(10.0, params["stress"])), 2),
            focus=round(max(0.0, min(10.0, params["focus"])), 2),
            sleep_debt=round(max(0.0, min(10.0, params["sleep_debt"])), 2),
            social_isolation=round(max(0.0, min(10.0, params["isolation"])), 2),
            body_temperature_c=round(36.4 + self.rng.uniform(-0.3, 0.5) + (0.3 if params["stress"] > 6 else 0), 2),
            respiration_rate=round(max(8.0, 12.0 + params["stress"] * 0.6 + self.rng.uniform(-1, 1)), 1),
        )
        self._history.append(frame)
        self.step += 1
        return frame

    def _scenario_params(self, wave: float, noise: float, slow: float) -> dict:
        s = self.scenario
        if s == "stress":
            return {
                "hrv": max(12.0, self._base_hrv + wave * 0.4 + noise),
                "stress": min(10.0, 6.8 + wave * 0.08 + self.rng.uniform(-0.4, 0.4)),
                "focus": max(0.0, 3.8 + wave * 0.05 + self.rng.uniform(-0.5, 0.5)),
                "sleep_debt": min(10.0, 5.5 + self.rng.uniform(-0.5, 0.8)),
                "isolation": min(10.0, 3.0 + self.rng.uniform(-0.3, 0.6)),
                "co2": 950 + wave * 8 + self.rng.uniform(-30, 40),
                "infrasound": 42 + wave * 0.4 + self.rng.uniform(-2, 3),
                "noise_db": 48 + self.rng.uniform(-3, 5),
            }
        if s == "recovery":
            return {
                "hrv": max(25.0, self._base_hrv + wave + noise),
                "stress": max(0.0, 1.8 + wave * 0.04 + self.rng.uniform(-0.3, 0.3)),
                "focus": min(10.0, 8.2 + wave * 0.04 + self.rng.uniform(-0.4, 0.4)),
                "sleep_debt": max(0.0, 1.2 + self.rng.uniform(-0.4, 0.4)),
                "isolation": max(0.0, 1.0 + self.rng.uniform(-0.3, 0.3)),
                "co2": 620 + wave * 4 + self.rng.uniform(-20, 20),
                "infrasound": 32 + self.rng.uniform(-2, 2),
                "noise_db": 28 + self.rng.uniform(-2, 3),
            }
        if s == "isolation":
            return {
                "hrv": max(18.0, self._base_hrv + wave * 0.5 + noise),
                "stress": min(10.0, 5.5 + wave * 0.07 + self.rng.uniform(-0.4, 0.5)),
                "focus": max(0.0, 4.5 + wave * 0.05 + self.rng.uniform(-0.6, 0.4)),
                "sleep_debt": min(10.0, 4.0 + self.rng.uniform(-0.5, 0.7)),
                "isolation": min(10.0, 7.5 + self.rng.uniform(-0.5, 0.8)),
                "co2": 780 + wave * 6 + self.rng.uniform(-25, 30),
                "infrasound": 36 + self.rng.uniform(-2, 3),
                "noise_db": 32 + self.rng.uniform(-2, 4),
            }
        if s == "overload":
            return {
                "hrv": max(10.0, self._base_hrv + wave * 0.3 + noise - 4),
                "stress": min(10.0, 8.2 + wave * 0.1 + self.rng.uniform(-0.3, 0.5)),
                "focus": max(0.0, 2.5 + wave * 0.03 + self.rng.uniform(-0.6, 0.3)),
                "sleep_debt": min(10.0, 7.5 + self.rng.uniform(-0.4, 0.6)),
                "isolation": min(10.0, 4.5 + self.rng.uniform(-0.4, 0.7)),
                "co2": 1100 + wave * 10 + self.rng.uniform(-40, 50),
                "infrasound": 48 + wave * 0.5 + self.rng.uniform(-2, 4),
                "noise_db": 58 + self.rng.uniform(-4, 6),
            }
        # baseline
        return {
            "hrv": max(20.0, self._base_hrv + wave * 0.7 + noise),
            "stress": max(0.0, min(10.0, 3.8 + wave * 0.06 + self.rng.uniform(-0.5, 0.5))),
            "focus": max(0.0, min(10.0, 6.2 + wave * 0.05 + self.rng.uniform(-0.5, 0.5))),
            "sleep_debt": max(0.0, 2.0 + self.rng.uniform(-0.6, 0.6)),
            "isolation": max(0.0, 2.0 + self.rng.uniform(-0.5, 0.5)),
            "co2": 700 + wave * 5 + self.rng.uniform(-25, 25),
            "infrasound": 34 + self.rng.uniform(-2, 2),
            "noise_db": 34 + self.rng.uniform(-3, 3),
        }

    def reset(self, scenario: Optional[str] = None, seed: Optional[int] = None) -> None:
        if scenario:
            if scenario not in self.SCENARIOS:
                raise ValueError(f"Unknown scenario: {scenario}")
            self.scenario = scenario
            self._base_hrv = {
                "baseline": 62.0, "stress": 34.0, "recovery": 78.0,
                "isolation": 48.0, "overload": 28.0,
            }[scenario]
        if seed is not None:
            self.rng = random.Random(seed)
        self.step = 0
        self._history.clear()

    @property
    def history(self) -> list[SensorFrame]:
        return list(self._history)
