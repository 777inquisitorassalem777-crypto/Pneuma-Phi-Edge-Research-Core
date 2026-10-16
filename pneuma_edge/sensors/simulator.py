"""Расширенный симулятор сенсоров."""

import math
import random
from ..core.models import SensorFrame


class SensorSimulator:
    """
    Детерминированный симулятор среды и психофизиологии.
    Не является медицинским устройством.
    """

    SCENARIOS = ("baseline", "stress", "recovery", "isolation")

    def __init__(self, seed: int = 42, scenario: str = "baseline"):
        if scenario not in self.SCENARIOS:
            raise ValueError(f"Unknown scenario: {scenario}")
        self.rng = random.Random(seed)
        self.step = 0
        self.scenario = scenario
        self.base_hrv = {
            "baseline": 62.0,
            "stress": 34.0,
            "recovery": 78.0,
            "isolation": 48.0,
        }[scenario]

    def next(self) -> SensorFrame:
        t = self.step * 0.5
        wave = math.sin(t / 7.0) * 6 + math.sin(t / 23.0) * 3
        noise = self.rng.uniform(-2.5, 2.5)

        if self.scenario == "stress":
            hrv = max(12.0, self.base_hrv + wave * 0.4 + noise)
            stress = min(10.0, 6.8 + wave * 0.08 + self.rng.uniform(-0.4, 0.4))
            focus = max(0.0, 3.8 + wave * 0.05 + self.rng.uniform(-0.5, 0.5))
            sleep_debt = min(10.0, 5.5 + self.rng.uniform(-0.5, 0.8))
            isolation = min(10.0, 3.0 + self.rng.uniform(-0.3, 0.6))
            co2 = 950 + wave * 8 + self.rng.uniform(-30, 40)
            infrasound = 42 + wave * 0.4 + self.rng.uniform(-2, 3)
            noise_db = 48 + self.rng.uniform(-3, 5)
        elif self.scenario == "recovery":
            hrv = max(25.0, self.base_hrv + wave + noise)
            stress = max(0.0, 1.8 + wave * 0.04 + self.rng.uniform(-0.3, 0.3))
            focus = min(10.0, 8.2 + wave * 0.04 + self.rng.uniform(-0.4, 0.4))
            sleep_debt = max(0.0, 1.2 + self.rng.uniform(-0.4, 0.4))
            isolation = max(0.0, 1.0 + self.rng.uniform(-0.3, 0.3))
            co2 = 620 + wave * 4 + self.rng.uniform(-20, 20)
            infrasound = 32 + self.rng.uniform(-2, 2)
            noise_db = 28 + self.rng.uniform(-2, 3)
        elif self.scenario == "isolation":
            hrv = max(18.0, self.base_hrv + wave * 0.5 + noise)
            stress = min(10.0, 5.5 + wave * 0.07 + self.rng.uniform(-0.4, 0.5))
            focus = max(0.0, 4.5 + wave * 0.05 + self.rng.uniform(-0.6, 0.4))
            sleep_debt = min(10.0, 4.0 + self.rng.uniform(-0.5, 0.7))
            isolation = min(10.0, 7.5 + self.rng.uniform(-0.5, 0.8))
            co2 = 780 + wave * 6 + self.rng.uniform(-25, 30)
            infrasound = 36 + self.rng.uniform(-2, 3)
            noise_db = 32 + self.rng.uniform(-2, 4)
        else:  # baseline
            hrv = max(20.0, self.base_hrv + wave * 0.7 + noise)
            stress = max(0.0, min(10.0, 3.8 + wave * 0.06 + self.rng.uniform(-0.5, 0.5)))
            focus = max(0.0, min(10.0, 6.2 + wave * 0.05 + self.rng.uniform(-0.5, 0.5)))
            sleep_debt = max(0.0, 2.0 + self.rng.uniform(-0.6, 0.6))
            isolation = max(0.0, 2.0 + self.rng.uniform(-0.5, 0.5))
            co2 = 700 + wave * 5 + self.rng.uniform(-25, 25)
            infrasound = 34 + self.rng.uniform(-2, 2)
            noise_db = 34 + self.rng.uniform(-3, 3)

        frame = SensorFrame(
            step=self.step,
            timestamp=round(t, 3),
            hrv_ms=round(hrv, 2),
            heart_rate=round(max(48.0, 108.0 - hrv * 0.52 + self.rng.uniform(-3, 3)), 1),
            temperature_c=round(22.0 + wave * 0.08 + self.rng.uniform(-0.4, 0.4), 2),
            humidity_pct=round(45.0 + wave * 0.3 + self.rng.uniform(-3, 3), 1),
            co2_ppm=round(max(400.0, co2), 0),
            magnetic_ut=round(45.0 + self.rng.uniform(-1.5, 1.5), 2),
            electrostatic_v=round(120.0 + self.rng.uniform(-15, 15), 1),
            infrasound_db=round(max(20.0, infrasound), 1),
            ambient_light_lux=round(max(50.0, 280 + wave * 15 + self.rng.uniform(-40, 40)), 0),
            noise_db=round(max(20.0, noise_db), 1),
            subjective_stress=round(max(0.0, min(10.0, stress)), 2),
            focus=round(max(0.0, min(10.0, focus)), 2),
            sleep_debt=round(max(0.0, min(10.0, sleep_debt)), 2),
            social_isolation=round(max(0.0, min(10.0, isolation)), 2),
        )
        self.step += 1
        return frame
