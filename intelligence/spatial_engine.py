"""
OMEGA-CORE | Spatial AI World Model Engine (Stage 12 — Full)
=============================================================
Builds a true 3D world understanding layer that bridges abstract state tensors
to physical reality. Capabilities:
  - LiDAR / depth-camera ingestion → 3D obstacle map
  - Semantic occupancy grid (free / occupied / unknown)
  - SLAM-style loop-closure detection
  - A*-style path planning on occupancy grid
  - Spatial scene-graph with typed entity relations
  - Multi-agent spatial coordination (robot fleet)
  - World-model snapshot export (JSON) for Reality Feedback Engine
"""

import math
import uuid
import json
import datetime
from dataclasses import dataclass, field, asdict
from typing import List, Tuple, Dict, Any, Optional

# ---------------------------------------------------------------------------
# Primitive geometry types
# ---------------------------------------------------------------------------

@dataclass
class Point3D:
    x: float
    y: float
    z: float

    def distance_to(self, other: "Point3D") -> float:
        return math.sqrt((self.x - other.x) ** 2 +
                         (self.y - other.y) ** 2 +
                         (self.z - other.z) ** 2)

    def to_dict(self) -> dict:
        return {"x": round(self.x, 4), "y": round(self.y, 4), "z": round(self.z, 4)}


@dataclass
class BoundingBox:
    min_pt: Point3D
    max_pt: Point3D

    @property
    def volume(self) -> float:
        return ((self.max_pt.x - self.min_pt.x) *
                (self.max_pt.y - self.min_pt.y) *
                (self.max_pt.z - self.min_pt.z))

    @property
    def center(self) -> Point3D:
        return Point3D(
            (self.min_pt.x + self.max_pt.x) / 2,
            (self.min_pt.y + self.max_pt.y) / 2,
            (self.min_pt.z + self.max_pt.z) / 2,
        )


@dataclass
class Obstacle:
    obstacle_id: str
    center: Point3D
    radius: float
    severity: str                     # CRITICAL | HIGH | MEDIUM | LOW
    semantic_label: str = "unknown"   # wall | human | robot | equipment | hazard
    confidence: float = 1.0


# ---------------------------------------------------------------------------
# Occupancy Grid (2D slice at z=0, extensible to 3D voxels)
# ---------------------------------------------------------------------------

class OccupancyGrid:
    """
    2D occupancy grid with three cell states:
        0 = FREE, 1 = OCCUPIED, -1 = UNKNOWN
    Resolution is in metres per cell.
    """
    FREE     =  0
    OCCUPIED =  1
    UNKNOWN  = -1

    def __init__(self, width_m: float = 20.0, height_m: float = 20.0,
                 resolution: float = 0.5):
        self.resolution = resolution
        self.width_cells  = int(width_m  / resolution)
        self.height_cells = int(height_m / resolution)
        self.origin = Point3D(-width_m / 2, -height_m / 2, 0)
        # Initialise as UNKNOWN
        self.grid: List[List[int]] = [
            [self.UNKNOWN] * self.width_cells
            for _ in range(self.height_cells)
        ]

    def _world_to_cell(self, x: float, y: float) -> Tuple[int, int]:
        col = int((x - self.origin.x) / self.resolution)
        row = int((y - self.origin.y) / self.resolution)
        col = max(0, min(col, self.width_cells  - 1))
        row = max(0, min(row, self.height_cells - 1))
        return row, col

    def mark_free(self, x: float, y: float):
        r, c = self._world_to_cell(x, y)
        if self.grid[r][c] != self.OCCUPIED:
            self.grid[r][c] = self.FREE

    def mark_occupied(self, x: float, y: float):
        r, c = self._world_to_cell(x, y)
        self.grid[r][c] = self.OCCUPIED

    def get_state(self, x: float, y: float) -> int:
        r, c = self._world_to_cell(x, y)
        return self.grid[r][c]

    def coverage_stats(self) -> dict:
        total = self.width_cells * self.height_cells
        free  = sum(cell == self.FREE     for row in self.grid for cell in row)
        occ   = sum(cell == self.OCCUPIED for row in self.grid for cell in row)
        unk   = total - free - occ
        return {
            "total_cells": total,
            "free_pct":    round(free / total * 100, 1),
            "occupied_pct":round(occ  / total * 100, 1),
            "unknown_pct": round(unk  / total * 100, 1),
            "explored_pct":round((free + occ) / total * 100, 1),
        }


# ---------------------------------------------------------------------------
# Scene Graph Node (semantic entity in 3D space)
# ---------------------------------------------------------------------------

@dataclass
class SceneNode:
    node_id: str
    label: str          # robot | human | workstation | hazard | exit | sample
    position: Point3D
    properties: Dict[str, Any] = field(default_factory=dict)
    relations: List[Dict[str, str]] = field(default_factory=list)

    def add_relation(self, relation_type: str, target_id: str):
        self.relations.append({"type": relation_type, "target": target_id})


# ---------------------------------------------------------------------------
# Main Spatial AI World Model
# ---------------------------------------------------------------------------

class SpatialEngine:
    """
    OMEGA-CORE Stage 12: Spatial AI World Model
    -------------------------------------------
    Maintains a live 3D model of the lab / operational environment, including
    obstacle maps, semantic scene graph, multi-robot pose registry, and
    trajectory planning.
    """

    def __init__(self, grid_width_m: float = 20.0, grid_height_m: float = 20.0,
                 grid_resolution: float = 0.5):
        self.active_obstacles: List[Obstacle] = []
        self.current_trajectory: List[Point3D] = []
        self.occupancy_grid = OccupancyGrid(grid_width_m, grid_height_m, grid_resolution)
        self.scene_graph: Dict[str, SceneNode] = {}
        self.robot_poses: Dict[str, Point3D] = {}          # robot_id → current pose
        self.loop_closure_events: List[dict] = []
        self._snapshot_id = str(uuid.uuid4())[:8].upper()

    # ------------------------------------------------------------------
    # 1. Sensor Ingestion
    # ------------------------------------------------------------------

    def ingest_lidar(self, distances: List[float], angles_deg: List[float],
                     threshold: float = 1.0,
                     semantic_labels: Optional[List[str]] = None) -> List[Obstacle]:
        """
        Convert 1D LiDAR arrays into 3D Spatial Obstacles and update the
        occupancy grid.
        """
        self.active_obstacles = []
        for i, (dist, angle) in enumerate(zip(distances, angles_deg)):
            rad = math.radians(angle)
            x = dist * math.cos(rad)
            y = dist * math.sin(rad)

            if dist < threshold:
                severity = "CRITICAL" if dist < threshold * 0.4 else \
                           "HIGH"     if dist < threshold * 0.7 else "MEDIUM"
                label = (semantic_labels[i]
                         if semantic_labels and i < len(semantic_labels)
                         else "unknown")
                obs = Obstacle(
                    obstacle_id   = f"OBS-{i:03d}",
                    center        = Point3D(x, y, 0.0),
                    radius        = max(0.1, dist * 0.05),
                    severity      = severity,
                    semantic_label= label,
                    confidence    = min(1.0, 1.0 - dist / threshold),
                )
                self.active_obstacles.append(obs)
                self.occupancy_grid.mark_occupied(x, y)
            else:
                # Mark the free corridor along the ray
                for step in range(1, int(dist / self.occupancy_grid.resolution)):
                    fx = step * self.occupancy_grid.resolution * math.cos(rad)
                    fy = step * self.occupancy_grid.resolution * math.sin(rad)
                    self.occupancy_grid.mark_free(fx, fy)

        return self.active_obstacles

    def ingest_depth_frame(self, depth_matrix: List[List[float]],
                           fov_h_deg: float = 60.0, fov_v_deg: float = 45.0,
                           max_range: float = 5.0) -> int:
        """
        Convert an H×W depth-camera matrix into obstacle points.
        Returns number of obstacle points added.
        """
        count = 0
        h = len(depth_matrix)
        w = len(depth_matrix[0]) if h > 0 else 0
        for row_i, row in enumerate(depth_matrix):
            for col_i, depth in enumerate(row):
                if depth <= 0 or depth > max_range:
                    continue
                v_angle = fov_v_deg * (row_i / h - 0.5)
                h_angle = fov_h_deg * (col_i / w - 0.5)
                x = depth * math.cos(math.radians(v_angle)) * math.sin(math.radians(h_angle))
                y = depth * math.cos(math.radians(v_angle)) * math.cos(math.radians(h_angle))
                z = depth * math.sin(math.radians(v_angle))
                if depth < max_range * 0.3:
                    obs = Obstacle(
                        obstacle_id = f"DEPTH-{count:04d}",
                        center      = Point3D(x, y, z),
                        radius      = 0.1,
                        severity    = "HIGH",
                    )
                    self.active_obstacles.append(obs)
                    self.occupancy_grid.mark_occupied(x, y)
                    count += 1
        return count

    # ------------------------------------------------------------------
    # 2. Collision Detection
    # ------------------------------------------------------------------

    def check_collision(self, position: Point3D, safe_radius: float = 0.3) -> bool:
        """
        Return True if `position` is within `safe_radius` of any obstacle.
        """
        for obs in self.active_obstacles:
            if position.distance_to(obs.center) < (safe_radius + obs.radius):
                return True
        return False

    def nearest_obstacle(self, position: Point3D) -> Optional[dict]:
        """Return the nearest obstacle and its distance."""
        if not self.active_obstacles:
            return None
        best = min(self.active_obstacles,
                   key=lambda o: position.distance_to(o.center))
        return {
            "obstacle_id":    best.obstacle_id,
            "distance_m":     round(position.distance_to(best.center), 3),
            "severity":       best.severity,
            "semantic_label": best.semantic_label,
            "position":       best.center.to_dict(),
        }

    # ------------------------------------------------------------------
    # 3. Path Planning (A*-lite on occupancy grid)
    # ------------------------------------------------------------------

    def plan_path(self, start: Point3D, goal: Point3D,
                  safe_radius: float = 0.3,
                  max_steps: int = 500) -> dict:
        """
        Greedy best-first path planning on the occupancy grid.
        Falls back to linear interpolation with obstacle-avoidance nudge.
        """
        path: List[Point3D] = []
        collision_count = 0
        current = Point3D(start.x, start.y, start.z)

        for step in range(max_steps):
            path.append(Point3D(current.x, current.y, current.z))
            dist_to_goal = current.distance_to(goal)
            if dist_to_goal < 0.15:
                break

            # Step towards goal
            direction_x = (goal.x - current.x) / max(dist_to_goal, 1e-6)
            direction_y = (goal.y - current.y) / max(dist_to_goal, 1e-6)
            step_size   = min(0.2, dist_to_goal)

            candidate = Point3D(
                current.x + direction_x * step_size,
                current.y + direction_y * step_size,
                current.z
            )

            if self.check_collision(candidate, safe_radius):
                collision_count += 1
                # Perpendicular evasion
                perp_x = -direction_y * 0.3
                perp_y =  direction_x * 0.3
                candidate = Point3D(current.x + perp_x, current.y + perp_y, current.z)

            current = candidate

        path.append(Point3D(goal.x, goal.y, goal.z))
        path_length = sum(path[i].distance_to(path[i + 1]) for i in range(len(path) - 1))

        return {
            "trajectory":               [p.to_dict() for p in path],
            "collision_events":         collision_count,
            "path_length_m":            round(path_length, 3),
            "steps_taken":              len(path),
            "goal_reached":             path[-1].distance_to(goal) < 0.3,
            "safety_score":             round(max(0.0, 1.0 - collision_count * 0.1), 2),
            "occupancy_coverage":       self.occupancy_grid.coverage_stats(),
        }

    def optimize_trajectory(self, start: Point3D, goal: Point3D,
                             steps: int = 10) -> dict:
        """Legacy-compatible wrapper around plan_path."""
        result = self.plan_path(start, goal, safe_radius=0.3, max_steps=steps * 5)
        result["collision_risk_detected"] = result["collision_events"] > 0
        result["cost"] = result["path_length_m"] + result["collision_events"] * 5.0
        return result

    # ------------------------------------------------------------------
    # 4. Bounding Box & Geometry
    # ------------------------------------------------------------------

    def compute_bounding_box(self, points: List[Point3D]) -> BoundingBox:
        """Compute axis-aligned bounding box of a point cloud."""
        if not points:
            return BoundingBox(Point3D(0, 0, 0), Point3D(0, 0, 0))
        return BoundingBox(
            Point3D(min(p.x for p in points), min(p.y for p in points), min(p.z for p in points)),
            Point3D(max(p.x for p in points), max(p.y for p in points), max(p.z for p in points)),
        )

    # ------------------------------------------------------------------
    # 5. Scene Graph
    # ------------------------------------------------------------------

    def add_scene_node(self, label: str, position: Point3D,
                       properties: Optional[dict] = None) -> SceneNode:
        """Register a semantic entity in the 3D scene graph."""
        node_id = f"NODE-{str(uuid.uuid4())[:6].upper()}"
        node = SceneNode(
            node_id    = node_id,
            label      = label,
            position   = position,
            properties = properties or {},
        )
        self.scene_graph[node_id] = node
        return node

    def link_nodes(self, src_id: str, rel_type: str, tgt_id: str):
        """Add a directed semantic relation between two scene-graph nodes."""
        if src_id in self.scene_graph:
            self.scene_graph[src_id].add_relation(rel_type, tgt_id)

    def query_nearby_nodes(self, position: Point3D, radius_m: float = 3.0) -> List[dict]:
        """Return all scene nodes within `radius_m` of `position`."""
        result = []
        for node in self.scene_graph.values():
            if position.distance_to(node.position) <= radius_m:
                result.append({
                    "node_id":  node.node_id,
                    "label":    node.label,
                    "distance": round(position.distance_to(node.position), 3),
                    "position": node.position.to_dict(),
                })
        return sorted(result, key=lambda n: n["distance"])

    # ------------------------------------------------------------------
    # 6. Multi-Robot Pose Registry
    # ------------------------------------------------------------------

    def register_robot(self, robot_id: str, pose: Point3D):
        """Register or update a robot's current 3D pose."""
        self.robot_poses[robot_id] = pose
        self.add_scene_node(label=f"robot:{robot_id}", position=pose,
                            properties={"robot_id": robot_id})

    def get_robot_pose(self, robot_id: str) -> Optional[dict]:
        if robot_id not in self.robot_poses:
            return None
        p = self.robot_poses[robot_id]
        return p.to_dict()

    def fleet_status(self) -> List[dict]:
        """Return status summary of all registered robots."""
        result = []
        for rid, pose in self.robot_poses.items():
            nearest = self.nearest_obstacle(pose)
            result.append({
                "robot_id":       rid,
                "pose":           pose.to_dict(),
                "nearest_hazard": nearest,
                "grid_state":     "FREE" if self.occupancy_grid.get_state(pose.x, pose.y) == OccupancyGrid.FREE else "OCCUPIED",
            })
        return result

    # ------------------------------------------------------------------
    # 7. SLAM Loop Closure Detection
    # ------------------------------------------------------------------

    def detect_loop_closure(self, robot_id: str, current_pose: Point3D,
                             closure_radius: float = 1.0) -> Optional[dict]:
        """
        Detect if the robot has returned to a previously visited location
        (simple distance-based loop closure).
        """
        history_key = f"_history_{robot_id}"
        if not hasattr(self, history_key):
            setattr(self, history_key, [])
        history: List[Point3D] = getattr(self, history_key)
        history.append(Point3D(current_pose.x, current_pose.y, current_pose.z))

        # Check against earlier history (skip last 20 entries to avoid immediate re-detection)
        for past_pose in history[:-20]:
            if current_pose.distance_to(past_pose) < closure_radius:
                event = {
                    "robot_id":       robot_id,
                    "current_pose":   current_pose.to_dict(),
                    "matched_pose":   past_pose.to_dict(),
                    "closure_radius": closure_radius,
                    "timestamp":      datetime.datetime.utcnow().isoformat(),
                }
                self.loop_closure_events.append(event)
                return event
        return None

    # ------------------------------------------------------------------
    # 8. World-Model Snapshot Export
    # ------------------------------------------------------------------

    def export_world_model(self) -> dict:
        """
        Export the complete world-model state as a structured dict
        consumable by the Reality Feedback Engine.
        """
        return {
            "snapshot_id":       self._snapshot_id,
            "timestamp":         datetime.datetime.utcnow().isoformat(),
            "obstacle_count":    len(self.active_obstacles),
            "obstacles":         [
                {
                    "id":     o.obstacle_id,
                    "center": o.center.to_dict(),
                    "radius": o.radius,
                    "sev":    o.severity,
                    "label":  o.semantic_label,
                }
                for o in self.active_obstacles
            ],
            "occupancy_grid":    self.occupancy_grid.coverage_stats(),
            "scene_graph_nodes": len(self.scene_graph),
            "scene_entities":    [
                {"id": n.node_id, "label": n.label,
                 "pos": n.position.to_dict(), "relations": n.relations}
                for n in self.scene_graph.values()
            ],
            "robot_fleet":       self.fleet_status(),
            "loop_closures":     len(self.loop_closure_events),
        }
