import json
import time
import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional


# ---------------------------------------------------------------------------
# Data Schemas (Pydantic-free — uses dataclasses to stay within requirements.txt)
# ---------------------------------------------------------------------------

@dataclass
class JointState:
    joint_id: str
    position: float      # radians
    velocity: float      # rad/s
    acceleration: float  # rad/s²
    timestamp: float = field(default_factory=time.time)


@dataclass
class RoboticsPayload:
    robot_id: str
    joint_states: List[JointState] = field(default_factory=list)
    sensor_data: Dict[str, Any] = field(default_factory=dict)
    control_params: Dict[str, Any] = field(default_factory=dict)
    cad_file: Optional[str] = None
    start: Dict[str, float] = field(default_factory=dict)
    goal: Dict[str, float] = field(default_factory=dict)
    obstacles: List[Dict] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Physical constraint tables (UR5-class robot arm defaults)
# ---------------------------------------------------------------------------
JOINT_LIMITS = {
    "position":     {"min": -3.14159, "max": 3.14159},   # ± π rad
    "velocity":     {"min": -2.0,     "max": 2.0},        # rad/s
    "acceleration": {"min": -20.0,    "max": 20.0},       # rad/s²
}

SENSOR_LIMITS = {
    "lidar":   {"min": 0.05, "max": 15.0},   # metres
    "force":   {"min": 0.0,  "max": 150.0},  # Newtons
    "torque":  {"min": -50.0, "max": 50.0},  # N·m
    "camera":  {"min": 0.0,  "max": 1.0},    # normalised brightness
}


class RoboticsValidator:
    """
    OMEGA-CORE | Data Validator — Step 2 of the Robotics Pipeline.

    Validates incoming robotics payloads against:
      1. Schema integrity (required keys, type coercion)
      2. Physical joint constraints
      3. Sensor range limits
      4. Temporal consistency (monotonic timestamps)

    All validation runs with zero extra dependencies.
    """

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def validate(self, raw: dict) -> dict:
        """
        Run full validation suite. Returns:
          status  : 'valid' | 'invalid'
          payload : RoboticsPayload dataclass (when valid)
          errors  : list of error strings (when invalid)
          warnings: list of non-fatal warning strings
        """
        errors = []
        warnings = []

        # --- Schema ---
        schema_result = self._validate_schema(raw, errors)
        if errors:
            return {"status": "invalid", "errors": errors, "warnings": warnings}

        payload = schema_result

        # --- Physics ---
        self._validate_physics(payload, errors, warnings)

        # --- Sensors ---
        self._validate_sensors(payload, warnings)

        # --- Temporal consistency ---
        self._validate_timestamps(payload, warnings)

        if errors:
            return {"status": "invalid", "errors": errors, "warnings": warnings, "payload": payload}

        return {"status": "valid", "errors": [], "warnings": warnings, "payload": payload}

    # ------------------------------------------------------------------
    # Schema validation
    # ------------------------------------------------------------------

    def _validate_schema(self, raw: dict, errors: list) -> Optional[RoboticsPayload]:
        if not isinstance(raw, dict):
            errors.append("Payload must be a JSON object / dict.")
            return None

        robot_id = raw.get("robot_id")
        if not robot_id:
            errors.append("Missing required field: robot_id")
            robot_id = "UNKNOWN"

        joint_states = []
        for js in raw.get("joint_states", []):
            try:
                joint_states.append(JointState(
                    joint_id=str(js.get("joint_id", "?")),
                    position=float(js["position"]),
                    velocity=float(js["velocity"]),
                    acceleration=float(js["acceleration"]),
                    timestamp=float(js.get("timestamp", time.time())),
                ))
            except (KeyError, ValueError, TypeError) as e:
                errors.append(f"Invalid joint_state entry: {e}")

        return RoboticsPayload(
            robot_id=robot_id,
            joint_states=joint_states,
            sensor_data=raw.get("sensor_data", {}),
            control_params=raw.get("control_params", {}),
            cad_file=raw.get("cad_file"),
            start=raw.get("start", {}),
            goal=raw.get("goal", {}),
            obstacles=raw.get("obstacles", []),
        )

    # ------------------------------------------------------------------
    # Physics validation
    # ------------------------------------------------------------------

    def _validate_physics(self, payload: RoboticsPayload, errors: list, warnings: list):
        for js in payload.joint_states:
            lim = JOINT_LIMITS
            if not (lim["position"]["min"] <= js.position <= lim["position"]["max"]):
                errors.append(
                    f"Joint '{js.joint_id}' position {js.position:.3f} rad exceeds ±π limits."
                )
            if not (lim["velocity"]["min"] <= js.velocity <= lim["velocity"]["max"]):
                severity = errors if abs(js.velocity) > 3.0 else warnings
                severity.append(
                    f"Joint '{js.joint_id}' velocity {js.velocity:.3f} rad/s "
                    f"{'exceeds hard limit' if severity is errors else 'approaching limit'}."
                )
            if not (lim["acceleration"]["min"] <= js.acceleration <= lim["acceleration"]["max"]):
                warnings.append(
                    f"Joint '{js.joint_id}' acceleration {js.acceleration:.3f} rad/s² exceeds safe range."
                )

    # ------------------------------------------------------------------
    # Sensor validation
    # ------------------------------------------------------------------

    def _validate_sensors(self, payload: RoboticsPayload, warnings: list):
        for sensor_name, readings in payload.sensor_data.items():
            lim = SENSOR_LIMITS.get(sensor_name.lower())
            if lim is None:
                continue  # Unknown sensor type — skip silently

            values = readings if isinstance(readings, list) else [readings]
            for v in values:
                try:
                    fv = float(v)
                    if not (lim["min"] <= fv <= lim["max"]):
                        warnings.append(
                            f"Sensor '{sensor_name}' reading {fv} is outside expected range "
                            f"[{lim['min']}, {lim['max']}]."
                        )
                except (TypeError, ValueError):
                    warnings.append(f"Sensor '{sensor_name}' contains non-numeric data: {v}")

    # ------------------------------------------------------------------
    # Timestamp consistency
    # ------------------------------------------------------------------

    def _validate_timestamps(self, payload: RoboticsPayload, warnings: list):
        if len(payload.joint_states) < 2:
            return
        ts_vals = [js.timestamp for js in payload.joint_states]
        for i in range(1, len(ts_vals)):
            if ts_vals[i] < ts_vals[i - 1]:
                warnings.append(
                    f"Non-monotonic timestamp at joint_state index {i}: "
                    f"{ts_vals[i]:.3f} < {ts_vals[i-1]:.3f}"
                )
                break


if __name__ == "__main__":
    sample = {
        "robot_id": "UR5-LAB-01",
        "joint_states": [
            {"joint_id": "shoulder", "position": 1.57, "velocity": 0.5, "acceleration": 2.0, "timestamp": 1.0},
            {"joint_id": "elbow",    "position": 0.78, "velocity": 0.3, "acceleration": 1.5, "timestamp": 1.1},
            {"joint_id": "wrist",    "position": 4.00, "velocity": 0.1, "acceleration": 0.5, "timestamp": 1.2},  # bad position
        ],
        "sensor_data": {"lidar": [0.5, 1.2, 0.03], "force": [5.0, 10.0]},  # 0.03 below lidar min
    }
    v = RoboticsValidator()
    result = v.validate(sample)
    print(json.dumps(
        {k: (str(v) if k == "payload" else v) for k, v in result.items()},
        indent=2
    ))
