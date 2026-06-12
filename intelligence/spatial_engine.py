import math
from dataclasses import dataclass
from typing import List, Tuple, Dict, Any

@dataclass
class Point3D:
    x: float
    y: float
    z: float

@dataclass
class BoundingBox:
    min_pt: Point3D
    max_pt: Point3D

@dataclass
class Obstacle:
    center: Point3D
    radius: float
    severity: str

class SpatialEngine:
    """
    OMEGA-CORE Stage 12: Spatial AI Layer
    Handles 3D geometries, Point Clouds, LiDAR data, Kinematics, and Spatial Navigations.
    Bridges abstract state tensors into physical 3D simulations.
    """
    def __init__(self):
        self.active_obstacles: List[Obstacle] = []
        self.current_trajectory: List[Point3D] = []

    def ingest_lidar(self, distances: List[float], angles_deg: List[float], threshold: float = 1.0) -> List[Obstacle]:
        """
        Converts 1D LiDAR arrays into 3D Spatial Obstacles.
        (Assumes z=0 for 2D plane mapping, easily extensible to 3D).
        """
        self.active_obstacles = []
        for dist, angle in zip(distances, angles_deg):
            if dist < threshold:
                rad = math.radians(angle)
                x = dist * math.cos(rad)
                y = dist * math.sin(rad)
                severity = "CRITICAL" if dist < (threshold * 0.5) else "HIGH"
                obs = Obstacle(center=Point3D(x, y, 0.0), radius=0.2, severity=severity)
                self.active_obstacles.append(obs)
        return self.active_obstacles

    def check_collision(self, position: Point3D, safe_radius: float = 0.5) -> bool:
        """
        Detects physical intersection between the agent and active obstacles.
        """
        for obs in self.active_obstacles:
            dx = position.x - obs.center.x
            dy = position.y - obs.center.y
            dz = position.z - obs.center.z
            distance = math.sqrt(dx**2 + dy**2 + dz**2)
            if distance < (safe_radius + obs.radius):
                return True
        return False

    def optimize_trajectory(self, start: Point3D, goal: Point3D, steps: int = 10) -> Dict[str, Any]:
        """
        Generates a basic linear trajectory, checking for spatial collisions.
        If collision detected, attempts a rudimentary 45-degree evasive maneuver.
        """
        path = []
        collision_risk = False
        cost = 0.0

        for i in range(steps + 1):
            t = i / float(steps)
            current_x = start.x + t * (goal.x - start.x)
            current_y = start.y + t * (goal.y - start.y)
            current_z = start.z + t * (goal.z - start.z)
            pt = Point3D(current_x, current_y, current_z)

            # Check collision at this node
            if self.check_collision(pt):
                collision_risk = True
                # Evasive maneuver (Simple orthogonal shift)
                pt.x += 1.0
                pt.y += 1.0
                cost += 5.0 # Penalty for deviation

            path.append(pt)
            cost += 1.0 # Base cost per step

        return {
            "trajectory": [{"x": p.x, "y": p.y, "z": p.z} for p in path],
            "collision_risk_detected": collision_risk,
            "cost": cost,
            "safety_score": 0.99 if not collision_risk else 0.75
        }

    def compute_bounding_box(self, points: List[Point3D]) -> BoundingBox:
        """
        Calculates the physical boundaries of a molecular structure or point cloud.
        """
        if not points:
            return BoundingBox(Point3D(0,0,0), Point3D(0,0,0))
            
        min_x = min(p.x for p in points)
        min_y = min(p.y for p in points)
        min_z = min(p.z for p in points)
        max_x = max(p.x for p in points)
        max_y = max(p.y for p in points)
        max_z = max(p.z for p in points)

        return BoundingBox(
            Point3D(min_x, min_y, min_z),
            Point3D(max_x, max_y, max_z)
        )
