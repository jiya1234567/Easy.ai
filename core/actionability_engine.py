import time
import json
from typing import Dict, List, Any, Optional

from core.explainability_engine import ExplainabilityEngine


class ActionabilityEngine:
    """
    OMEGA-CORE | ActionabilityEngine — Step 11 of the Robotics Pipeline.

    Synthesises the outputs of all upstream steps into a prioritised,
    confidence-scored action plan that an operator or downstream
    automation system can act on immediately.

    Actions are ranked by: expected_impact × confidence (descending).
    """

    # Action catalogue: defines what triggers each action and its template
    _ACTION_CATALOGUE = [
        {
            "id":       "halt_replanning",
            "type":     "HALT",
            "trigger":  lambda r: len([a for a in r.get("anomalies", []) if a.get("severity") == "CRITICAL"]) > 0,
            "message":  "CRITICAL anomalies detected — halt execution and re-plan trajectory.",
            "confidence": 0.99,
            "impact":   1.0,
        },
        {
            "id":       "adjust_trajectory",
            "type":     "TRAJECTORY",
            "trigger":  lambda r: float(r.get("trajectory_cost", 0)) > 2.0,
            "message":  "Trajectory cost is elevated — run a secondary optimisation pass.",
            "confidence": 0.88,
            "impact":   0.75,
        },
        {
            "id":       "tighten_safety_margins",
            "type":     "SAFETY",
            "trigger":  lambda r: not r.get("collision_free", True),
            "message":  "Collision risk detected — increase safety margins by 20 %.",
            "confidence": 0.95,
            "impact":   0.90,
        },
        {
            "id":       "recalibrate_lidar",
            "type":     "SENSOR",
            "trigger":  lambda r: any(
                "lidar" in a.get("metric_key", "") for a in r.get("anomalies", [])
            ),
            "message":  "LiDAR anomaly detected — recalibrate sensor and re-validate obstacle map.",
            "confidence": 0.85,
            "impact":   0.80,
        },
        {
            "id":       "reduce_joint_velocity",
            "type":     "KINEMATIC",
            "trigger":  lambda r: any(
                "velocity" in a.get("metric_key", "") and a.get("severity") in ("HIGH", "CRITICAL")
                for a in r.get("anomalies", [])
            ),
            "message":  "Joint velocity anomaly — reduce target velocity by 25 % and re-validate.",
            "confidence": 0.90,
            "impact":   0.70,
        },
        {
            "id":       "expand_rl_budget",
            "type":     "OPTIMISATION",
            "trigger":  lambda r: float(r.get("validation_score", 1.0)) < 0.75,
            "message":  "Validation score below threshold — expand RecursiveASI iteration budget.",
            "confidence": 0.80,
            "impact":   0.60,
        },
        {
            "id":       "reduce_energy_profile",
            "type":     "ENERGY",
            "trigger":  lambda r: (
                isinstance(r.get("energy"), dict) and
                float(r["energy"].get("total", 0)) > 80.0
            ),
            "message":  "Energy consumption elevated — adopt energy-minimising trajectory variant.",
            "confidence": 0.78,
            "impact":   0.55,
        },
        {
            "id":       "proceed_nominal",
            "type":     "PROCEED",
            "trigger":  lambda r: (
                r.get("collision_free", True) and
                float(r.get("validation_score", 0)) >= 0.80 and
                not r.get("anomalies")
            ),
            "message":  "All checks passed — proceed with planned trajectory.",
            "confidence": 0.99,
            "impact":   1.0,
        },
    ]

    def __init__(self):
        self.explainability = ExplainabilityEngine()

    # ------------------------------------------------------------------
    # Primary entrypoint
    # ------------------------------------------------------------------

    def generate_actions(self, refined_state: dict) -> List[dict]:
        """
        Evaluate each catalogue entry against the refined state and
        return all triggered actions (unsorted).
        """
        triggered = []
        causal_graph = refined_state.get("causal_graph")

        for entry in self._ACTION_CATALOGUE:
            try:
                fires = entry["trigger"](refined_state)
            except Exception:
                fires = False

            if fires:
                action = {
                    "id":              entry["id"],
                    "type":            entry["type"],
                    "message":         entry["message"],
                    "confidence":      entry["confidence"],
                    "expected_impact": entry["impact"],
                    "priority_score":  round(entry["impact"] * entry["confidence"], 4),
                    "explanation":     self.explainability.explain_intervention(
                        {"type": entry["id"], "expected_impact": entry["message"],
                         "confidence": entry["confidence"]},
                        causal_graph,
                    ),
                    "timestamp": time.time(),
                }
                triggered.append(action)

        return triggered

    def prioritize_actions(self, actions: List[dict]) -> List[dict]:
        """Sort actions by priority_score descending (highest impact × confidence first)."""
        return sorted(actions, key=lambda x: x["priority_score"], reverse=True)

    def get_action_plan(self, refined_state: dict) -> dict:
        """
        Full action plan: generate + prioritise + annotate with metadata.
        """
        actions = self.generate_actions(refined_state)
        ranked  = self.prioritize_actions(actions)

        primary = ranked[0]["message"] if ranked else "No actions required."

        return {
            "primary_action":   primary,
            "total_actions":    len(ranked),
            "action_plan":      ranked,
            "halt_required":    any(a["type"] == "HALT" for a in ranked),
            "proceed_approved": any(a["type"] == "PROCEED" for a in ranked),
            "timestamp":        time.time(),
        }


if __name__ == "__main__":
    sample_state = {
        "trajectory_cost": 2.8,
        "collision_free":  False,
        "validation_score": 0.65,
        "energy":          {"total": 92.0},
        "anomalies": [
            {"metric_key": "joint_velocity.shoulder", "severity": "HIGH",   "message": "Speed spike."},
            {"metric_key": "lidar.front",             "severity": "CRITICAL","message": "Obstacle too close."},
        ],
        "causal_graph": {
            "edges": [
                {"source": "joint_velocity", "target": "collision_risk",   "weight": 0.80},
                {"source": "collision_risk",  "target": "trajectory_error", "weight": 0.95},
            ]
        },
    }
    engine = ActionabilityEngine()
    plan   = engine.get_action_plan(sample_state)
    print(f"Primary action : {plan['primary_action']}")
    print(f"Total actions  : {plan['total_actions']}")
    print(f"Halt required  : {plan['halt_required']}")
    print("\nRanked plan:")
    for i, a in enumerate(plan["action_plan"], 1):
        print(f"  {i}. [{a['type']}] {a['message']} (score={a['priority_score']})")
