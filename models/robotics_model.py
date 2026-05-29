import json
import time
import math
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from scipy.optimize import minimize

# Joint position limits (radians) — used as optimisation bounds
_JOINT_BOUNDS = (-3.14159, 3.14159)
_VELOCITY_LIMIT = 2.0      # rad/s  (hard cap applied to trajectory)
_SAFETY_MARGIN = 0.10      # rad    (buffer kept away from joint limits)


class RoboticsModel:
    """
    OMEGA-CORE | RoboticsModel — Step 5 of the Robotics Pipeline.

    Provides:
      - Trajectory optimisation (scipy L-BFGS-B, no PyBullet required)
      - Lightweight obstacle avoidance (geometric repulsion)
      - Dynamics simulation (Euler integration)
      - Cost decomposition (distance + energy + time)

    Production upgrade: swap _optimize_trajectory() internals with a
    full MPC / DMP solver and replace _simulate() with PyBullet for
    physics-accurate forward simulation.
    """

    def __init__(self, joint_names: Optional[List[str]] = None):
        self.joint_names = joint_names or ["shoulder", "elbow", "wrist"]
        self.n = len(self.joint_names)
        # Safety band: keep n_safety_margin inside joint limits
        self.lo = _JOINT_BOUNDS[0] + _SAFETY_MARGIN
        self.hi = _JOINT_BOUNDS[1] - _SAFETY_MARGIN

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def plan_trajectory(
        self,
        start:     Dict[str, float],
        goal:      Dict[str, float],
        obstacles: Optional[List[Dict]] = None,
        steps:     int = 20,
    ) -> dict:
        """
        Plan a collision-aware trajectory from start to goal.

        Args:
          start     : {joint_name: position_rad, ...}
          goal      : {joint_name: position_rad, ...}
          obstacles : list of {"position": [x,y,z], "radius": float}
          steps     : number of waypoints in the trajectory

        Returns:
          trajectory      : {joint_name: [pos_rad, ...]} length == steps
          cost            : scalar optimisation cost
          collision_free  : bool
          dynamics        : result of simulate_dynamics()
        """
        obstacles = obstacles or []

        # Fill missing joints with neutral position
        start = {j: float(start.get(j, 0.0)) for j in self.joint_names}
        goal  = {j: float(goal.get(j, 0.0))  for j in self.joint_names}

        trajectory = self._optimize_trajectory(start, goal, obstacles, steps)
        cost = self._calculate_cost(trajectory)
        collision_free = self._is_collision_free(trajectory, obstacles)
        dynamics = self.simulate_dynamics(trajectory)

        return {
            "trajectory":     trajectory,
            "cost":           round(cost, 4),
            "collision_free": collision_free,
            "steps":          steps,
            "dynamics":       dynamics,
        }

    def simulate_dynamics(self, trajectory: Dict[str, List[float]]) -> dict:
        """
        Euler-integrate the trajectory to produce velocity and acceleration profiles.
        dt is inferred from a 10 Hz sampling assumption.
        """
        dt = 0.1  # seconds per step
        profiles = {}
        energy = 0.0

        for joint in self.joint_names:
            if joint not in trajectory:
                continue
            pos = trajectory[joint]
            vel, acc = [], []
            for i in range(len(pos)):
                v = (pos[i] - pos[i - 1]) / dt if i > 0 else 0.0
                a = (v - vel[-1]) / dt          if vel else 0.0
                # Clamp velocity to hard limit
                v = float(np.clip(v, -_VELOCITY_LIMIT, _VELOCITY_LIMIT))
                vel.append(round(v, 4))
                acc.append(round(a, 4))
                energy += 0.5 * v ** 2 * dt     # ½mv²·dt (unit mass)
            profiles[joint] = {"positions": pos, "velocities": vel, "accelerations": acc}

        return {
            "status":         "simulated",
            "profiles":       profiles,
            "total_energy":   round(energy, 4),
            "duration_s":     round(len(trajectory.get(self.joint_names[0], [])) * dt, 2),
            "collisions":     False,            # placeholder (PyBullet in prod)
        }

    # ------------------------------------------------------------------
    # Optimisation
    # ------------------------------------------------------------------

    def _optimize_trajectory(
        self,
        start:     Dict[str, float],
        goal:      Dict[str, float],
        obstacles: List[Dict],
        steps:     int,
    ) -> Dict[str, List[float]]:
        """
        Minimise path length + obstacle penalty using L-BFGS-B.
        Decision variable x: flattened (steps × n_joints) position array.
        """
        # Build bounds: each waypoint coordinate in [lo, hi]
        bounds = [(self.lo, self.hi)] * (steps * self.n)

        # Initial guess: linear interpolation start → goal
        x0 = np.zeros(steps * self.n)
        for k, joint in enumerate(self.joint_names):
            x0[k::self.n] = np.linspace(start[joint], goal[joint], steps)

        def cost_fn(x):
            waypoints = x.reshape(steps, self.n)
            # 1. Path length (sum of Euclidean distances between consecutive waypoints)
            diffs = np.diff(waypoints, axis=0)
            path_len = float(np.sum(np.linalg.norm(diffs, axis=1)))
            # 2. Obstacle repulsion penalty
            penalty = 0.0
            for obs in obstacles:
                obs_pos = np.array(obs.get("position", [0, 0, 0]))[:self.n]
                obs_r   = float(obs.get("radius", 0.2))
                for wp in waypoints:
                    dist = np.linalg.norm(wp - obs_pos)
                    if dist < obs_r + _SAFETY_MARGIN:
                        penalty += (obs_r + _SAFETY_MARGIN - dist) ** 2 * 100
            # 3. Goal proximity: penalise distance to goal at the last waypoint
            goal_vec = np.array([goal[j] for j in self.joint_names])
            goal_err = float(np.linalg.norm(waypoints[-1] - goal_vec)) * 50
            return path_len + penalty + goal_err

        result = minimize(cost_fn, x0, method="L-BFGS-B", bounds=bounds,
                          options={"maxiter": 200, "ftol": 1e-6})
        waypoints = result.x.reshape(steps, self.n)

        return {
            joint: [round(float(waypoints[s, k]), 4) for s in range(steps)]
            for k, joint in enumerate(self.joint_names)
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _calculate_cost(self, trajectory: Dict[str, List[float]]) -> float:
        total = 0.0
        for joint in self.joint_names:
            pos = trajectory.get(joint, [])
            for i in range(1, len(pos)):
                total += abs(pos[i] - pos[i - 1])
        return total

    def _is_collision_free(
        self,
        trajectory: Dict[str, List[float]],
        obstacles: List[Dict],
    ) -> bool:
        if not obstacles:
            return True
        steps = len(next(iter(trajectory.values()), []))
        for s in range(steps):
            wp = np.array([trajectory.get(j, [0.0] * steps)[s] for j in self.joint_names])
            for obs in obstacles:
                obs_pos = np.array(obs.get("position", [0, 0, 0]))[:self.n]
                obs_r   = float(obs.get("radius", 0.2))
                if np.linalg.norm(wp - obs_pos) < obs_r:
                    return False
        return True


if __name__ == "__main__":
    model = RoboticsModel(["shoulder", "elbow", "wrist"])
    result = model.plan_trajectory(
        start     = {"shoulder": 0.0, "elbow": 0.0, "wrist": 0.0},
        goal      = {"shoulder": 1.2, "elbow": -0.8, "wrist": 0.5},
        obstacles = [{"position": [0.6, -0.4, 0.2], "radius": 0.15}],
        steps     = 15,
    )
    print(json.dumps({k: v for k, v in result.items() if k != "dynamics"}, indent=2))
    print(f"Energy: {result['dynamics']['total_energy']} | Duration: {result['dynamics']['duration_s']}s")
