import json
import time
import numpy as np
from typing import Dict, List, Any, Optional

from core.assi_sensing_engine import ASSISensingEngine
from models.robotics_model import RoboticsModel
from core.tensor_scope import RoboticsState

_SAFETY_MARGIN_POS = 0.10   # rad
_SAFETY_MARGIN_VEL = 0.20   # rad/s
_JOINT_POS_LIMIT   = 3.14159
_JOINT_VEL_LIMIT   = 2.0


class RoboticsAgent:
    """
    OMEGA-CORE | RoboticsAgent — Step 6 of the Robotics Pipeline.

    Layers domain intelligence on top of the RoboticsModel output:
      1. Applies safety margins to clamp the optimised trajectory
      2. Runs ASSI classification on the live state
      3. Adds energy budget feedback
      4. Detects post-optimisation anomalies (second-pass quality gate)
      5. Generates a concise action summary

    Integrates directly with ASSISensingEngine (already in the codebase).
    """

    def __init__(self, joint_names: Optional[List[str]] = None):
        self.joint_names = joint_names or ["shoulder", "elbow", "wrist"]
        self.model = RoboticsModel(self.joint_names)
        self.assi  = ASSISensingEngine()

    # ------------------------------------------------------------------
    # Primary entrypoint
    # ------------------------------------------------------------------

    def process(self, input_data: dict, anomaly_report: dict) -> dict:
        """
        Args:
          input_data     : validated payload dict with keys: start, goal, obstacles,
                           sensor_data (vision_entropy, touch_entropy, smell_entropy optional)
          anomaly_report : output of AnomalyPropagator.check_robotics_anomalies()

        Returns a rich result dict ready for CausalAgent / RecursiveASI.
        """
        start     = input_data.get("start", {})
        goal      = input_data.get("goal", {})
        obstacles = input_data.get("obstacles", [])
        steps     = int(input_data.get("steps", 20))

        # --- Step 5: Plan trajectory ---
        plan = self.model.plan_trajectory(start, goal, obstacles, steps)
        raw_traj = plan["trajectory"]

        # --- Apply safety margins ---
        safe_traj = self._apply_safety_margins(raw_traj)

        # --- Re-simulate dynamics on the safe trajectory ---
        safe_dynamics = self.model.simulate_dynamics(safe_traj)

        # --- ASSI classification ---
        assi_result = self._classify_environment(input_data)

        # --- Energy budget check ---
        energy = safe_dynamics.get("total_energy", 0.0)
        energy_status = "WITHIN_BUDGET" if energy < 100.0 else "OVER_BUDGET"

        # --- Post-optimisation anomaly check ---
        post_anomalies = self._post_check_anomalies(safe_traj)

        # --- Merge incoming anomalies with post-optimisation ones ---
        all_anomalies = (anomaly_report.get("anomalies", []) or []) + post_anomalies

        # --- Action summary ---
        action_summary = self._build_action_summary(
            plan, safe_dynamics, assi_result, energy_status, all_anomalies
        )

        return {
            "agent":          "RoboticsAgent",
            "trajectory":     safe_traj,
            "trajectory_cost": plan["cost"],
            "collision_free": plan["collision_free"],
            "dynamics":       safe_dynamics,
            "assi":           assi_result,
            "energy":         {"total": energy, "status": energy_status},
            "anomalies":      all_anomalies,
            "action_summary": action_summary,
            "timestamp":      time.time(),
        }

    # ------------------------------------------------------------------
    # Safety margin application
    # ------------------------------------------------------------------

    def _apply_safety_margins(self, trajectory: Dict[str, List[float]]) -> Dict[str, List[float]]:
        clamped = {}
        lo = -_JOINT_POS_LIMIT + _SAFETY_MARGIN_POS
        hi =  _JOINT_POS_LIMIT - _SAFETY_MARGIN_POS
        for joint, positions in trajectory.items():
            clamped[joint] = [
                round(float(np.clip(p, lo, hi)), 4)
                for p in positions
            ]
        return clamped

    # ------------------------------------------------------------------
    # ASSI environment classification
    # ------------------------------------------------------------------

    def _classify_environment(self, input_data: dict) -> dict:
        sensor_data = input_data.get("sensor_data", {})

        # Pull multi-modal entropy values if supplied; else estimate from sensor variance
        v_ent = float(sensor_data.get("vision_entropy",  self._estimate_entropy(sensor_data.get("camera", [0.5]))))
        t_ent = float(sensor_data.get("touch_entropy",   self._estimate_entropy(sensor_data.get("force",  [5.0]))))
        s_ent = float(sensor_data.get("smell_entropy",   self._estimate_entropy(sensor_data.get("gas",    [0.1]))))

        classification, g_ent, pred, inst = self.assi.classify_robotic_system(v_ent, t_ent, s_ent)
        return {
            "classification": classification,
            "global_entropy": round(g_ent, 4),
            "predictability": round(pred, 4),
            "instability":    round(inst, 4),
            "inputs": {"vision_entropy": v_ent, "touch_entropy": t_ent, "smell_entropy": s_ent},
        }

    @staticmethod
    def _estimate_entropy(readings) -> float:
        """Rough entropy estimate from sensor variance when explicit entropy not supplied."""
        vals = readings if isinstance(readings, list) else [readings]
        if not vals:
            return 0.5
        arr = np.array([float(v) for v in vals], dtype=float)
        if arr.std() == 0:
            return 0.1
        # Normalise variance to [0, 1]
        return float(np.clip(arr.std() / (arr.mean() + 1e-9), 0.0, 1.0))

    # ------------------------------------------------------------------
    # Post-optimisation quality gate
    # ------------------------------------------------------------------

    def _post_check_anomalies(self, trajectory: Dict[str, List[float]]) -> List[dict]:
        anomalies = []
        lo = -_JOINT_POS_LIMIT + _SAFETY_MARGIN_POS
        hi =  _JOINT_POS_LIMIT - _SAFETY_MARGIN_POS
        for joint, positions in trajectory.items():
            for i, p in enumerate(positions):
                if not (lo <= p <= hi):
                    anomalies.append({
                        "metric_key": f"post_opt.{joint}.step_{i}",
                        "value":      round(p, 4),
                        "severity":   "HIGH",
                        "message":    f"Post-optimisation: {joint} at step {i} = {p:.4f} outside safe band.",
                    })
        return anomalies

    # ------------------------------------------------------------------
    # Action summary
    # ------------------------------------------------------------------

    def _build_action_summary(
        self,
        plan: dict,
        dynamics: dict,
        assi: dict,
        energy_status: str,
        anomalies: List[dict],
    ) -> dict:
        crit = [a for a in anomalies if a.get("severity") == "CRITICAL"]
        return {
            "trajectory_status":   "SAFE" if plan["collision_free"] else "COLLISION_RISK",
            "assi_classification": assi["classification"],
            "energy_status":       energy_status,
            "critical_anomalies":  len(crit),
            "total_anomalies":     len(anomalies),
            "recommended_action":  (
                "HALT — CRITICAL anomalies detected. Re-plan required."
                if crit else
                "PROCEED — Trajectory validated and within safety margins."
            ),
        }


if __name__ == "__main__":
    agent = RoboticsAgent()
    sample_input = {
        "start":     {"shoulder": 0.0, "elbow": 0.0, "wrist": 0.0},
        "goal":      {"shoulder": 1.2, "elbow": -0.8, "wrist": 0.5},
        "obstacles": [{"position": [0.6, -0.4, 0.2], "radius": 0.15}],
        "sensor_data": {
            "vision_entropy": 0.35,
            "touch_entropy":  0.50,
            "smell_entropy":  0.20,
            "lidar": [0.8, 1.2, 2.0],
        },
    }
    result = agent.process(sample_input, {"anomalies": []})
    print(json.dumps({k: v for k, v in result.items() if k != "trajectory"}, indent=2))
