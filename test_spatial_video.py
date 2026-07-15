import os
from intelligence.spatial_engine import SpatialEngine, Point3D
from intelligence.world_model_visualizer import WorldModelVisualizer

def main():
    print("========================================")
    print("Testing World Model Visualizer Modules")
    print("========================================")

    # 1. Test Disease Progression Video Simulation (Veo)
    print("\n[1/2] Generating Disease Progression Video (Veo)...")
    try:
        gif_bytes = WorldModelVisualizer.generate_disease_progression_gif()
        print(f" -> Success! Generated {len(gif_bytes)} bytes.")
        out_path = "reports/disease_progression_test.gif"
        os.makedirs("reports", exist_ok=True)
        with open(out_path, "wb") as f:
            f.write(gif_bytes)
        print(f" -> Saved preview to: {out_path}")
    except Exception as e:
        print(f" -> Failed: {e}")

    # 2. Test Spatial Trajectory Video Simulation
    print("\n[2/2] Generating Spatial Trajectory Video...")
    try:
        engine = SpatialEngine()
        # Mock some obstacles
        angles = [0, 45, 90, 135]
        distances = [4.0, 1.0, 5.0, 2.0]
        engine.ingest_lidar(distances, angles, threshold=1.5)
        
        # Add a workstation and hazard to scene graph
        engine.add_scene_node("workstation", Point3D(2.0, 2.0, 0.0))
        engine.add_scene_node("hazard", Point3D(-3.0, 3.0, 0.0))

        # Plan a path
        start = Point3D(-4.0, -4.0, 0.0)
        goal = Point3D(4.0, 4.0, 0.0)
        path_result = engine.plan_path(start, goal)
        
        gif_bytes = WorldModelVisualizer.generate_trajectory_video_gif(engine, path_result)
        print(f" -> Success! Generated {len(gif_bytes)} bytes.")
        out_path = "reports/spatial_trajectory_test.gif"
        with open(out_path, "wb") as f:
            f.write(gif_bytes)
        print(f" -> Saved preview to: {out_path}")
    except Exception as e:
        print(f" -> Failed: {e}")

    print("\nVisual/Video test suite execution complete.")

if __name__ == "__main__":
    main()
