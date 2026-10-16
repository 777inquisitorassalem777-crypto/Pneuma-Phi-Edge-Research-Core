"""
Оркестратор симбиоза:
PNEUMA (sensors→analytics→reflection→ethics→intuition→archetypal)
  ⊕ Sophia (Blue Matrix, Wisdom, Evolution, Passport)
"""

from __future__ import annotations
from typing import Dict, Any, Optional, List
from pneuma.sensors.simulator import SensorSimulator
from pneuma.analytics.engine import AnalyticsEngine
from pneuma.reflection.module import ReflectionModule
from pneuma.intuition.module import IntuitionModule
from pneuma.ethics.core import EthicsCore
from pneuma.core.models import EthicalParameters
from pneuma.archetypal.layer import ArchetypalLayer
from pneuma.safety.guard import SafetyGate
from pneuma.reporting.report import ReportBuilder
from sophia.blue_matrix.matrix import BlueMatrix
from sophia.wisdom.layer import WisdomLayer, WisdomVector
from sophia.evolution.loop import EvolutionLoop
from sophia.passport.identity import Passport


class SymbiosisOrchestrator:
    """
    Единая точка запуска симбиоза.
    Эпистемический статус всей системы: research_platform_not_consciousness.
    """

    def __init__(
        self,
        mode: str = "scientific",
        seed: int = 42,
        wisdom: float = 0.65,
        will: float = 0.55,
        love: float = 0.70,
        faith: float = 0.50,
        hope: float = 0.55,
    ):
        self.mode = mode
        self.sim = SensorSimulator(seed=seed, scenario="baseline")
        self.analytics = AnalyticsEngine()
        self.reflection = ReflectionModule()
        self.intuition = IntuitionModule(seed=seed)
        self.ethics = EthicsCore(EthicalParameters(wisdom=wisdom, will=will, love=love))
        self.archetypal = ArchetypalLayer() if mode == "archetypal" else None
        self.safety = SafetyGate(ethics=self.ethics)
        self.blue = BlueMatrix()
        self.wisdom = WisdomLayer(WisdomVector(
            will=will, love=love, faith=faith, hope=hope, wisdom=wisdom,
        ))
        self.evolution = EvolutionLoop()
        self.passport = Passport(name="pneuma-sophia-symbiosis")
        self.reporter = ReportBuilder()

    def run(
        self,
        steps: int = 80,
        scenario: str = "stress",
        export: Optional[str] = None,
    ) -> Dict[str, Any]:
        self.sim.reset(scenario=scenario)
        frames, reports, reflections, intuitions, ethics_log = [], [], [], [], []
        arch_data, blue_data, wisdom_data, evo_reports = [], [], [], []

        for _ in range(steps):
            frame = self.sim.next()
            report = self.analytics.analyze(frame)
            refl = self.reflection.reflect(frame, report)
            intu = self.intuition.generate(frame, report)
            eth = self.ethics.distinguish(report)
            suggested = self.ethics.suggest_action(report)
            verdict = self.ethics.evaluate(suggested, {
                "risk": report.risk, "patterns": report.patterns,
            })

            # Blue Matrix
            readings = self.blue.from_pneuma_frame(frame, report)
            health = self.blue.health_score(readings)
            blue_summary = {
                "aggregate": self.blue.aggregate(readings),
                "health_score": round(health, 3),
                "readings_count": len(readings),
            }

            # Wisdom
            counsel = self.wisdom.counsel(
                report.risk, report.recovery, report.arousal, report.patterns,
            )

            # Адаптивная подстройка этических параметров от health + guna
            # (не «магия», а простой feedback loop)
            guna = counsel.get("guna", "rajas")
            if health < 0.35:
                self.ethics.set_parameters(
                    wisdom=min(1.0, self.ethics.params.wisdom + 0.02),
                    humility=min(1.0, self.ethics.params.humility + 0.02),
                )
            elif health > 0.7 and guna == "sattva":
                self.ethics.set_parameters(
                    will=min(1.0, self.ethics.params.will + 0.01),
                )

            # Evolution cycle periodically
            if frame.step % 20 == 19:
                evo = self.evolution.cycle({
                    "risk": report.risk,
                    "patterns": report.patterns,
                    "step": frame.step,
                })
                evo_reports.append(evo.__dict__)

            # Archetypal
            if self.archetypal:
                arch_data.append(self.archetypal.interpret(frame, report))

            if report.risk >= 0.75:
                self.safety.request(frame.step, "pause_and_notify_user", {
                    "risk": report.risk, "patterns": report.patterns,
                })

            frames.append(frame.to_dict())
            reports.append(report.to_dict())
            reflections.append(refl)
            intuitions.append(intu)
            ethics_log.append({**eth, "suggested": suggested, "verdict": verdict.to_dict()})
            blue_data.append(blue_summary)
            wisdom_data.append(counsel)

        # Passport update
        safety_sum = self.safety.summary()
        self.passport.update_from_session(
            steps=steps,
            ethics_balance=self.ethics.params.balance(),
            blocked=safety_sum.get("blocked", 0),
            evolution_accepted=self.evolution.registry_summary().get("total_accepted", 0),
            wisdom_vector={
                "will": self.wisdom.vector.will,
                "love": self.wisdom.vector.love,
                "faith": self.wisdom.vector.faith,
                "hope": self.wisdom.vector.hope,
                "wisdom": self.wisdom.vector.wisdom,
            },
            note=f"session mode={self.mode} scenario={scenario}",
        )

        result = self.reporter.build(
            mode=self.mode,
            scenario=scenario,
            frames=frames,
            reports=reports,
            reflections=reflections,
            intuitions=intuitions,
            ethics_log=ethics_log,
            archetypal=arch_data if self.mode == "archetypal" else None,
            safety_summary=safety_sum,
            analytics_summary=self.analytics.summary(),
        )

        # Symbiosis extensions
        # Интегральный показатель устойчивости симбиоза
        health_scores = [b.get("health_score", 0.5) for b in blue_data] or [0.5]
        avg_health = sum(health_scores) / len(health_scores)
        avg_risk = (self.analytics.summary() or {}).get("avg_risk", 0.5)
        stability = max(0.0, min(1.0, avg_health * 0.6 + (1.0 - float(avg_risk)) * 0.4))

        result["symbiosis"] = {
            "blue_matrix_tail": blue_data[-3:] if blue_data else [],
            "wisdom_tail": wisdom_data[-3:] if wisdom_data else [],
            "evolution_reports": evo_reports,
            "evolution_registry": self.evolution.registry_summary(),
            "passport": self.passport.to_dict(),
            "stability_score": round(stability, 3),
            "avg_blue_health": round(avg_health, 3),
            "ethics_params": {
                "wisdom": self.ethics.params.wisdom,
                "will": self.ethics.params.will,
                "love": self.ethics.params.love,
                "humility": self.ethics.params.humility,
                "balance": round(self.ethics.params.balance(), 3),
            },
            "epistemic_status": "research_platform_not_consciousness",
            "symbiosis_disclaimer": (
                "Симбиоз PNEUMA ⊕ Sophia ⊕ Evolution — исследовательская архитектура. "
                "Не создаёт души, сознания или самосознания. "
                "Все «искры» — символические показатели связности параметров."
            ),
        }

        if export:
            json_path = export if export.endswith(".json") else export + ".json"
            md_path = json_path.replace(".json", ".md")
            self.reporter.export(result, json_path, md_path)
            self.passport.save(json_path.replace(".json", "_passport.json"))
            result["_exported"] = {"json": json_path, "markdown": md_path}

        return result
