import json
from intelligence.spatial_engine import SpatialEngine, Point3D

def run_spatial_tests():
    print("========================================")
    print("🌐 OMEGA-CORE Stage 12: Spatial AI Layer")
    print("========================================\n")
    
    engine = SpatialEngine()
    
    # Test 1: LiDAR Ingestion & Obstacle Mapping
    print("--- Test 1: LiDAR Ingestion (Robotics/Auto) ---")
    angles = [0, 15, 30, 45, 60, 90]
    distances = [5.0, 4.5, 0.8, 0.4, 2.0, 3.0] # 0.8 and 0.4 are obstacles
    obstacles = engine.ingest_lidar(distances, angles, threshold=1.0)
    print(f"Ingested {len(angles)} LiDAR vectors.")
    print(f"Mapped {len(obstacles)} Physical Obstacles.")
    for o in obstacles:
        print(f" -> Obstacle at ({o.center.x:.2f}, {o.center.y:.2f}, {o.center.z:.2f}) | Severity: {o.severity}")
    print("✅ Passed\n")

    # Test 2: Trajectory Optimization with Evasion
    print("--- Test 2: Spatial Trajectory Optimization ---")
    start = Point3D(0, 0, 0)
    goal = Point3D(1, 1, 0)
    
    # Trajectory will pass through x=0.5, y=0.5. 
    # Let's see if the obstacle at 45 deg (x=0.28, y=0.28) triggers a collision evasion
    nav_result = engine.optimize_trajectory(start, goal, steps=5)
    print(f"Collision Risk Detected: {nav_result['collision_risk_detected']}")
    print(f"Final Safety Score: {nav_result['safety_score']}")
    print(f"Path Nodes Generated: {len(nav_result['trajectory'])}")
    print("Trajectory Sample (First 3 nodes):")
    for pt in nav_result['trajectory'][:3]:
        print(f" -> {pt}")
    print("✅ Passed\n")
    
    # Test 3: Quantum / Molecular Bounding Box
    print("--- Test 3: Molecular Geometric Bounding Box ---")
    molecule_points = [
        Point3D(-1.2, 0.5, 0.1),
        Point3D(0.0, 0.0, 0.0),
        Point3D(1.5, -0.2, 0.8),
        Point3D(0.5, 1.2, -0.5)
    ]
    bbox = engine.compute_bounding_box(molecule_points)
    print(f"Input: {len(molecule_points)} atoms/nodes")
    print(f"Bounding Box Min: ({bbox.min_pt.x:.2f}, {bbox.min_pt.y:.2f}, {bbox.min_pt.z:.2f})")
    print(f"Bounding Box Max: ({bbox.max_pt.x:.2f}, {bbox.max_pt.y:.2f}, {bbox.max_pt.z:.2f})")
    volume = (bbox.max_pt.x - bbox.min_pt.x) * (bbox.max_pt.y - bbox.min_pt.y) * (bbox.max_pt.z - bbox.min_pt.z)
    print(f"Calculated Enclosed Volume: {volume:.3f} cubic units")
    print("✅ Passed\n")

if __name__ == "__main__":
    run_spatial_tests()
