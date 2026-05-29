import time
import json
import numpy as np
from typing import Dict, List, Any, Optional
from core.tensor_scope import RoboticsState

# Joint / sensor hard limits (mirrors data_validator.py)
_JOINT_LIMITS = {
    "position":     (-3.14159, 3.14159),
    "velocity":     (-2.0, 2.0),
    "acceleration": (-20.0, 20.0),
}
_SENSOR_LIMITS = {
    "lidar":  (0.05, 15.0),
    "force":  (0.0, 150.0),
    "torque": (-50.0, 50.0),
}

# Severity thresholds: breach > 50 % of range headroom → CRITICAL
_CRIT_FRACTION = 0.5


class AnomalyPropagator:
    """
    OMEGA-CORE | Anomaly Propagator — Step 4 of the Robotics Pipeline.

    Detects threshold breaches and dynamic spikes in the live RoboticsState,
    assigns severity (WARNING / HIGH / CRITICAL), and traces each anomaly
    through a lightweight in-memory causal graph.

    Production upgrade path: replace _causal_graph with a Neo4j-backed
    CausalGraphDB for persistent, multi-domain tracing.
    """

    # Simple in-memory causal graph: source_metric → [downstream_effects]
    _CAUSAL_GRAPH: Dict[str, List[str]] = {
        "joint_position":     ["trajectory_error", "collision_risk"],
        "joint_velocity":     ["collision_risk",   "energy_consumption"],
        "joint_acceleration": ["energy_consumption"],
        "lidar":              ["collision_risk"],
        "force":              ["joint_position",   "trajectory_error"],
        "torque":             ["joint_velocity"],
        "collision_risk":     ["trajectory_error"],
        "energy_consumption": ["trajectory_error"],
    }

    def __init__(self):
        self._anomaly_history: List[dict] = []

    # ------------------------------------------------------------------
    # Primary entrypoint
    # ------------------------------------------------------------------

    def check_robotics_anomalies(self, state: RoboticsState) -> dict:
        """
        Scan the full RoboticsState for anomalies.

        Returns:
          anomalies         : list of anomaly dicts
          propagation_paths : causal traces for each anomaly
          severity_summary  : STABLE | WARNING | HIGH | CRITICAL
          timestamp         : unix timestamp
        """
        anomalies = []

        # --- Joint checks ---
        for jid, pos in state.joint_positions.items():
            a = self._check_value(f"joint_position.{jid}", "position", pos)
            if a: anomalies.append(a)

        for jid, vel in state.joint_velocities.items():
            a = self._check_value(f"joint_velocity.{jid}", "velocity", vel)
            if a: anomalies.append(a)

        for jid, acc in state.joint_accelerations.items():
            a = self._check_value(f"joint_acceleration.{jid}", "acceleration", acc)
            if a: anomalies.append(a)

        # --- Sensor checks ---
        for sensor, readings in state.sensor_data.items():
            lim = _SENSOR_LIMITS.get(sensor.lower())
            if lim is None:
                continue
            vals = readings if isinstance(readings, list) else [readings]
            for v in vals:
                try:
                    fv = float(v)
                    a = self._check_sensor(sensor, fv, lim)
                    if a: anomalies.append(a)
                except (TypeError, ValueError):
                    pass

        # --- Dynamic spike detection (velocity jump between frames) ---
        spike = self._detect_velocity_spike(state)
        if spike:
            anomalies.append(spike)

        # --- Build propagation paths ---
        paths = [self._trace_propagation(a["metric_key"]) for a in anomalies]

        # --- Severity summary ---
        severity = self._overall_severity(anomalies)

        result = {
            "anomalies": anomalies,
            "propagation_paths": paths,
            "severity_summary": severity,
            "anomaly_count": len(anomalies),
            "timestamp": time.time(),
        }
        self._anomaly_history.append(result)
        return result

    # ------------------------------------------------------------------
    # Targeted single-metric trace
    # ------------------------------------------------------------------

    def trace_anomaly(self, metric_key: str, value: float) -> dict:
        """Trace a single known anomaly through the causal graph."""
        root = metric_key.split(".")[0]
        severity = self._severity_for_value(root, value)
        return {
            "metric_key": metric_key,
            "value": value,
            "severity": severity,
            "propagation_path": self._trace_propagation(metric_key),
            "timestamp": time.time(),
        }

    def get_anomaly_history(self) -> List[dict]:
        return list(self._anomaly_history)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _check_value(self, metric_key: str, dim: str, value: float) -> Optional[dict]:
        lo, hi = _JOINT_LIMITS[dim]
        if lo <= value <= hi:
            return None
        headroom = (hi - lo) * _CRIT_FRACTION
        is_crit = (value < lo - headroom) or (value > hi + headroom)
        return {
            "metric_key": metric_key,
            "dimension":  dim,
            "value":      round(value, 4),
            "limits":     {"min": lo, "max": hi},
            "severity":   "CRITICAL" if is_crit else "HIGH",
            "message":    f"{metric_key} = {value:.4f} breaches {dim} limits [{lo}, {hi}].",
        }

    def _check_sensor(self, sensor: str, value: float, limits: tuple) -> Optional[dict]:
        lo, hi = limits
        if lo <= value <= hi:
            return None
        return {
            "metric_key": sensor,
            "dimension":  "reading",
            "value":      round(value, 4),
            "limits":     {"min": lo, "max": hi},
            "severity":   "CRITICAL" if value < lo * 0.5 or value > hi * 1.5 else "WARNING",
            "message":    f"Sensor '{sensor}' reading {value:.4f} outside range [{lo}, {hi}].",
        }

    def _detect_velocity_spike(self, state: RoboticsState) -> Optional[dict]:
        """Flag joints where velocity suddenly exceeds 75 % of the hard limit."""
        spike_threshold = _JOINT_LIMITS["velocity"][1] * 0.75
        for jid, vel in state.joint_velocities.items():
            if abs(vel) > spike_threshold:
                return {
                    "metric_key": f"joint_velocity.{jid}",
                    "dimension":  "spike",
                    "value":      round(vel, 4),
                    "limits":     {"threshold": spike_threshold},
                    "severity":   "CRITICAL",
                    "message":    f"Velocity spike on '{jid}': {vel:.4f} rad/s exceeds {spike_threshold:.2f} rad/s.",
                }
        return None

    def _trace_propagation(self, metric_key: str) -> List[dict]:
        """Walk the causal graph from metric_key, returning a flat edge list."""
        root = metric_key.split(".")[0]
        visited, path = set(), []
        queue = [root]
        while queue:
            node = queue.pop(0)
            if node in visited:
                continue
            visited.add(node)
            for downstream in self._CAUSAL_GRAPH.get(node, []):
                path.append({"source": node, "target": downstream, "type": "CAUSES"})
                if downstream not in visited:
                    queue.append(downstream)
        return path

    def _severity_for_value(self, root: str, value: float) -> str:
        lim_map = {
            "joint_position":     _JOINT_LIMITS["position"],
            "joint_velocity":     _JOINT_LIMITS["velocity"],
            "joint_acceleration": _JOINT_LIMITS["acceleration"],
        }
        lim = lim_map.get(root)
        if lim and not (lim[0] <= value <= lim[1]):
            return "CRITICAL"
        return "WARNING"

    @staticmethod
    def _overall_severity(anomalies: List[dict]) -> str:
        if not anomalies:
            return "STABLE"
        sevs = [a["severity"] for a in anomalies]
        if "CRITICAL" in sevs: return "CRITICAL"
        if "HIGH"     in sevs: return "HIGH"
        return "WARNING"


if __name__ == "__main__":
    from core.tensor_scope import TensorScope
    ts = TensorScope()
    ts.update_robotics_data({
        "joint_states": [
            {"joint_id": "shoulder", "position": 3.50,  "velocity": 1.8,  "acceleration": 5.0},
            {"joint_id": "elbow",    "position": -0.50, "velocity": -0.3, "acceleration": 1.0},
        ],
        "sensor_data": {"lidar": [0.02, 1.2, 3.0]},  # 0.02 below lidar min
    })
    ap = AnomalyPropagator()
    result = ap.check_robotics_anomalies(ts.get_robotics_state())
    print(json.dumps(result, indent=2))
