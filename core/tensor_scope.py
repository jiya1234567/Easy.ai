import time
import json
import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional


@dataclass
class RoboticsState:
    """Live robotics layer of the global state tensor."""
    joint_positions:     Dict[str, float] = field(default_factory=dict)   # rad
    joint_velocities:    Dict[str, float] = field(default_factory=dict)   # rad/s
    joint_accelerations: Dict[str, float] = field(default_factory=dict)   # rad/s²
    sensor_data:         Dict[str, Any]   = field(default_factory=dict)
    control_params:      Dict[str, Any]   = field(default_factory=dict)
    cad_file:            Optional[str]    = None
    anomaly_flags:       List[str]        = field(default_factory=list)
    timestamp:           float            = field(default_factory=time.time)


@dataclass
class StateTensor:
    """
    OMEGA-CORE | Global State Tensor.
    Aggregates all domain state layers in a single in-process object.
    (Production upgrade path: serialise to Redis for multi-process access.)
    """
    robotics: RoboticsState  = field(default_factory=RoboticsState)
    genomic:  Dict[str, Any] = field(default_factory=dict)
    climate:  Dict[str, Any] = field(default_factory=dict)
    finance:  Dict[str, Any] = field(default_factory=dict)
    cyber:    Dict[str, Any] = field(default_factory=dict)
    timestamp: float         = field(default_factory=time.time)


class TensorScope:
    """
    OMEGA-CORE | TensorScope — Step 3 of the Robotics Pipeline.

    Maintains the live StateTensor and provides:
      - Robotics state ingestion from validated payloads
      - Entropy / predictability scoring (feeds ASSI layer)
      - Coherence tracking across updates
      - Snapshot export for dashboard / audit

    No Kafka dependency: updates are synchronous. In production,
    wrap update_robotics_data() in a Kafka consumer thread.
    """

    def __init__(self):
        self.state = StateTensor()
        self._history: List[dict] = []          # rolling window of snapshots
        self._max_history = 50

    # ------------------------------------------------------------------
    # Ingestion
    # ------------------------------------------------------------------

    def update_robotics_data(self, payload) -> None:
        """
        Ingest a validated RoboticsPayload (or plain dict) into the state tensor.
        Accepts both the dataclass and raw dict forms.
        """
        rs = self.state.robotics

        # Accept dataclass or dict
        if hasattr(payload, "joint_states"):
            joint_states  = payload.joint_states
            sensor_data   = payload.sensor_data
            control_params= payload.control_params
            cad_file      = payload.cad_file
        else:
            joint_states  = payload.get("joint_states", [])
            sensor_data   = payload.get("sensor_data", {})
            control_params= payload.get("control_params", {})
            cad_file      = payload.get("cad_file")

        for js in joint_states:
            if hasattr(js, "joint_id"):
                jid = js.joint_id
                rs.joint_positions[jid]     = js.position
                rs.joint_velocities[jid]    = js.velocity
                rs.joint_accelerations[jid] = js.acceleration
            else:
                jid = js.get("joint_id", "?")
                rs.joint_positions[jid]     = float(js.get("position", 0))
                rs.joint_velocities[jid]    = float(js.get("velocity", 0))
                rs.joint_accelerations[jid] = float(js.get("acceleration", 0))

        rs.sensor_data.update(sensor_data)
        rs.control_params.update(control_params)
        if cad_file:
            rs.cad_file = cad_file
        rs.timestamp = time.time()
        self.state.timestamp = rs.timestamp

        self._snapshot()

    # ------------------------------------------------------------------
    # Analytics
    # ------------------------------------------------------------------

    def compute_joint_entropy(self) -> float:
        """
        Approximate information entropy across joint positions.
        High entropy → chaotic / unconstrained motion.
        """
        rs = self.state.robotics
        if not rs.joint_positions:
            return 0.0
        vals = np.array(list(rs.joint_positions.values()))
        # Normalise to [0,1] relative to ±π
        normed = np.clip((vals + np.pi) / (2 * np.pi), 1e-9, 1 - 1e-9)
        entropy = -np.sum(normed * np.log(normed)) / np.log(len(normed) + 1)
        return float(np.clip(entropy, 0.0, 1.0))

    def compute_coherence(self) -> float:
        """
        Coherence score: inverse of joint velocity variance.
        1.0 = perfectly synchronised joints; 0.0 = chaotic.
        """
        rs = self.state.robotics
        if not rs.joint_velocities:
            return 1.0
        vels = np.array(list(rs.joint_velocities.values()))
        variance = float(np.var(vels))
        return float(np.clip(1.0 / (1.0 + variance * 5), 0.0, 1.0))

    def get_assi_vector(self) -> dict:
        """Return the ASSI input vector for the current robotics state."""
        entropy = self.compute_joint_entropy()
        coherence = self.compute_coherence()
        predictability = float(np.clip(1.0 - entropy * 0.8, 0.0, 1.0))
        instability = float(np.clip(entropy * (1.0 + (1.0 - coherence)), 0.0, 1.0))
        return {
            "entropy": round(entropy, 4),
            "coherence": round(coherence, 4),
            "predictability": round(predictability, 4),
            "instability": round(instability, 4),
            "timestamp": self.state.timestamp,
        }

    # ------------------------------------------------------------------
    # Accessors
    # ------------------------------------------------------------------

    def get_robotics_state(self) -> RoboticsState:
        return self.state.robotics

    def snapshot(self) -> dict:
        """Export the full state tensor as a serialisable dict."""
        rs = self.state.robotics
        return {
            "timestamp": self.state.timestamp,
            "robotics": {
                "joint_positions":     rs.joint_positions,
                "joint_velocities":    rs.joint_velocities,
                "joint_accelerations": rs.joint_accelerations,
                "sensor_data":         rs.sensor_data,
                "control_params":      rs.control_params,
                "cad_file":            rs.cad_file,
                "anomaly_flags":       rs.anomaly_flags,
            },
            "assi_vector": self.get_assi_vector(),
        }

    def get_history(self) -> List[dict]:
        """Return the rolling history of state snapshots (for phase-transition detection)."""
        return list(self._history)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _snapshot(self):
        snap = self.get_assi_vector()
        self._history.append(snap)
        if len(self._history) > self._max_history:
            self._history.pop(0)


if __name__ == "__main__":
    ts = TensorScope()
    sample = {
        "joint_states": [
            {"joint_id": "shoulder", "position": 1.0, "velocity": 0.4, "acceleration": 1.0},
            {"joint_id": "elbow",    "position": -0.5, "velocity": -0.2, "acceleration": 0.5},
        ],
        "sensor_data": {"lidar": [1.2, 0.8, 2.1]},
    }
    ts.update_robotics_data(sample)
    print(json.dumps(ts.snapshot(), indent=2))
