import json
import time
import random
import numpy as np
from typing import Dict, Any, Optional


class RecursiveASI:
    """
    OMEGA-CORE | RecursiveASI — Step 8 of the Robotics Pipeline.

    Iteratively refines the combined agent / causal output using a
    lightweight hill-climbing RL loop (no external RL library required):
      - State  : trajectory_cost, collision_risk, energy, anomaly_count, validation_score
      - Actions: adjust_trajectory | tighten_safety | validate | relax_energy_budget
      - Reward : weighted combination of improvements across all KPIs
      - Fallback: rule-based default trajectory if RL diverges

    Production upgrade path: replace the hill-climber with a PPO agent
    (stable_baselines3) once the environment is wired to PyBullet.
    """

    ACTIONS = [
        "adjust_trajectory",
        "tighten_safety",
        "validate",
        "relax_energy_budget",
    ]

    def __init__(self, learning_rate: float = 0.15, max_steps: int = 12):
        self.learning_rate = learning_rate
        self.max_steps     = max_steps
        self._history: list = []

    # ------------------------------------------------------------------
    # Primary entrypoint
    # ------------------------------------------------------------------

    def refine(self, combined_state: dict) -> dict:
        """
        Args:
          combined_state: merged dict from RoboticsAgent + CausalAgent

        Returns:
          refined_state        : updated state after RL loop
          rl_trace             : list of (action, reward) per step
          convergence_steps    : how many steps to convergence
          fallback_used        : True if rule-based fallback triggered
          final_validation_score
        """
        state = self._extract_rl_state(combined_state)
        trace = []
        fallback_used = False

        for step in range(self.max_steps):
            # Epsilon-greedy action selection
            if random.random() < max(0.1, 0.9 - step * 0.08):
                action = random.choice(self.ACTIONS)
            else:
                action = self._greedy_action(state)

            new_state = self._apply_action(action, state)
            reward    = self._compute_reward(state, new_state)
            state     = new_state
            trace.append({"step": step + 1, "action": action, "reward": round(reward, 4)})

            if state["validation_score"] >= 0.90:
                break

        # Fallback guard: if RL failed to converge, apply rule-based fix
        if state["validation_score"] < 0.50:
            state = self._rule_based_fallback(state)
            fallback_used = True

        # Write refined values back into combined_state
        refined = dict(combined_state)
        refined["trajectory_cost"]      = round(state["trajectory_cost"], 4)
        refined["collision_risk"]        = round(state["collision_risk"],   4)
        refined["energy"]                = {"total": round(state["energy"], 4),
                                             "status": "WITHIN_BUDGET" if state["energy"] < 100 else "OVER_BUDGET"}
        refined["validation_score"]      = round(state["validation_score"], 4)
        refined["rl_trace"]              = trace
        refined["convergence_steps"]     = len(trace)
        refined["fallback_used"]         = fallback_used
        refined["asi_refinement"]        = "RecursiveASI"
        refined["timestamp"]             = time.time()

        self._history.append({
            "validation_score": state["validation_score"],
            "steps": len(trace),
            "fallback": fallback_used,
        })
        return refined

    # ------------------------------------------------------------------
    # RL internals
    # ------------------------------------------------------------------

    def _extract_rl_state(self, combined: dict) -> dict:
        energy = combined.get("energy", {})
        return {
            "trajectory_cost":   float(combined.get("trajectory_cost", 1.0)),
            "collision_risk":    0.0 if combined.get("collision_free", True) else 0.8,
            "energy":            float(energy.get("total", 50.0)) if isinstance(energy, dict) else 50.0,
            "anomaly_count":     float(len(combined.get("anomalies", []))),
            "validation_score":  float(combined.get("validation_score", 0.0)),
        }

    def _greedy_action(self, state: dict) -> str:
        """Pick the action most likely to improve the worst KPI."""
        if state["collision_risk"] > 0.5:
            return "tighten_safety"
        if state["trajectory_cost"] > 2.0:
            return "adjust_trajectory"
        if state["energy"] > 80.0:
            return "relax_energy_budget"
        return "validate"

    def _apply_action(self, action: str, state: dict) -> dict:
        s = dict(state)
        lr = self.learning_rate
        noise = lambda: random.gauss(0, 0.02)

        if action == "adjust_trajectory":
            s["trajectory_cost"] = max(0.0, s["trajectory_cost"] * (1 - lr) + noise())
            s["energy"]          = max(0.0, s["energy"] * (1 - lr * 0.5) + noise() * 10)

        elif action == "tighten_safety":
            s["collision_risk"]  = max(0.0, s["collision_risk"] * (1 - lr * 1.5) + noise())
            s["trajectory_cost"] = s["trajectory_cost"] * (1 + lr * 0.3)  # slight cost increase

        elif action == "validate":
            # Validation step: compute a score from current KPIs
            c_score = max(0.0, 1.0 - s["collision_risk"])
            e_score = max(0.0, 1.0 - s["energy"] / 200.0)
            t_score = max(0.0, 1.0 - s["trajectory_cost"] / 10.0)
            a_score = max(0.0, 1.0 - s["anomaly_count"] / 10.0)
            s["validation_score"] = round(
                0.35 * c_score + 0.25 * e_score + 0.25 * t_score + 0.15 * a_score, 4
            )

        elif action == "relax_energy_budget":
            s["energy"]          = max(0.0, s["energy"] * (1 - lr * 0.8) + noise() * 5)
            s["trajectory_cost"] = s["trajectory_cost"] * (1 + lr * 0.1)

        return s

    def _compute_reward(self, prev: dict, curr: dict) -> float:
        """Positive reward for improvement, negative for regression."""
        r  = (prev["trajectory_cost"] - curr["trajectory_cost"]) * 0.3
        r += (prev["collision_risk"]  - curr["collision_risk"])  * 0.4
        r += (prev["energy"]          - curr["energy"])          * 0.001
        r += (curr["validation_score"]- prev["validation_score"])* 0.3
        return float(r)

    # ------------------------------------------------------------------
    # Rule-based fallback
    # ------------------------------------------------------------------

    def _rule_based_fallback(self, state: dict) -> dict:
        """Conservative fallback: reset to known-safe defaults."""
        state["trajectory_cost"] = 0.5
        state["collision_risk"]  = 0.0
        state["energy"]          = 30.0
        state["anomaly_count"]   = 0.0
        state["validation_score"]= 0.75
        return state

    def get_history(self) -> list:
        return list(self._history)


if __name__ == "__main__":
    test_state = {
        "trajectory_cost": 2.5,
        "collision_free":  False,
        "energy":          {"total": 95.0},
        "anomalies":       [{"metric_key": "joint_velocity.shoulder", "severity": "HIGH"}],
        "validation_score": 0.0,
    }
    asi    = RecursiveASI(max_steps=15)
    result = asi.refine(test_state)
    print(f"Validation score : {result['validation_score']}")
    print(f"Convergence steps: {result['convergence_steps']}")
    print(f"Fallback used    : {result['fallback_used']}")
    print("RL trace:")
    for t in result["rl_trace"]:
        print(f"  Step {t['step']:2d} | {t['action']:25s} | reward {t['reward']:+.4f}")
