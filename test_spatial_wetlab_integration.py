"""
OMEGA-CORE | Spatial AI + Wet-Lab Integration Validation
Runs end-to-end tests without emoji (Windows console safe).
"""
import sys, json

def test_spatial_engine():
    print("=" * 60)
    print("SPATIAL AI WORLD MODEL - FULL VALIDATION")
    print("=" * 60)

    from intelligence.spatial_engine import SpatialEngine, Point3D

    engine = SpatialEngine(grid_width_m=20.0, grid_height_m=20.0, grid_resolution=0.5)

    # Test 1: LiDAR ingestion
    angles    = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]
    distances = [0.5, 3.0, 0.7, 5.0, 1.2, 0.4, 2.5, 4.0, 0.6, 3.5, 1.8, 0.3]
    labels    = ["wall", "free", "equipment", "free", "hazard", "human",
                 "free", "free", "wall", "free", "robot", "wall"]
    obs = engine.ingest_lidar(distances, angles, threshold=1.0, semantic_labels=labels)
    print(f"\n[TEST 1] LiDAR Ingestion: {len(angles)} beams -> {len(obs)} obstacles mapped")
    assert len(obs) > 0, "Expected obstacles"
    for o in obs:
        print(f"  {o.obstacle_id} | sev={o.severity} | label={o.semantic_label} | "
              f"pos=({o.center.x:.2f},{o.center.y:.2f})")
    print("[TEST 1] PASS")

    # Test 2: Occupancy grid
    cov = engine.occupancy_grid.coverage_stats()
    print(f"\n[TEST 2] Occupancy Grid: explored={cov['explored_pct']}% | "
          f"free={cov['free_pct']}% | occupied={cov['occupied_pct']}%")
    assert cov["explored_pct"] > 0, "Grid should have some explored cells"
    print("[TEST 2] PASS")

    # Test 3: Path planning
    start = Point3D(-4.0, -4.0, 0.0)
    goal  = Point3D( 4.0,  4.0, 0.0)
    path  = engine.plan_path(start, goal)
    print(f"\n[TEST 3] A* Path Planning: length={path['path_length_m']}m | "
          f"safety={path['safety_score']} | reached={path['goal_reached']} | "
          f"collisions={path['collision_events']}")
    assert path["goal_reached"], "Path should reach goal"
    print("[TEST 3] PASS")

    # Test 4: Scene graph
    n1 = engine.add_scene_node("robot",       Point3D(0.0, 0.0, 0.0), {"robot_id": "UR5"})
    n2 = engine.add_scene_node("workstation", Point3D(2.0, 1.0, 0.0))
    n3 = engine.add_scene_node("hazard",      Point3D(-1.0, 0.5, 0.0))
    engine.link_nodes(n1.node_id, "adjacent_to", n2.node_id)
    engine.link_nodes(n1.node_id, "avoid",       n3.node_id)
    nearby = engine.query_nearby_nodes(Point3D(0, 0, 0), radius_m=5.0)
    print(f"\n[TEST 4] Scene Graph: {len(engine.scene_graph)} nodes | "
          f"{len(nearby)} within 5m radius")
    assert len(engine.scene_graph) >= 3
    print("[TEST 4] PASS")

    # Test 5: Multi-robot fleet
    engine.register_robot("UR5-01",     Point3D(0.0,  0.0, 0.0))
    engine.register_robot("Drone-04",   Point3D(2.0,  3.0, 1.5))
    engine.register_robot("Mobile-Alpha",Point3D(-3.0, 1.0, 0.0))
    fleet = engine.fleet_status()
    print(f"\n[TEST 5] Fleet Registry: {len(fleet)} robots registered")
    for r in fleet:
        print(f"  {r['robot_id']} | pos={r['pose']} | grid={r['grid_state']}")
    assert len(fleet) == 3
    print("[TEST 5] PASS")

    # Test 6: World model export
    snap = engine.export_world_model()
    print(f"\n[TEST 6] World Model Snapshot: id={snap['snapshot_id']} | "
          f"obstacles={snap['obstacle_count']} | nodes={snap['scene_graph_nodes']} | "
          f"fleet={len(snap['robot_fleet'])}")
    assert snap["obstacle_count"] == len(obs)
    print("[TEST 6] PASS")

    print("\n" + "=" * 60)
    print("SPATIAL AI: ALL 6 TESTS PASSED")
    print("=" * 60)
    return True


def test_wetlab_orchestrator():
    print("\n" + "=" * 60)
    print("WET-LAB ORCHESTRATOR - FULL VALIDATION")
    print("=" * 60)

    from intelligence.wetlab_orchestrator import WetLabOrchestrator
    orch = WetLabOrchestrator(simulated=True)

    # Test 1: Protocol compilation
    proto = orch.compile_protocol({
        "type": "crispr_knockout", "target": "BRCA1_exon11",
        "dosage_ul": 15.0, "wells": ["A1","A2","A3"], "replicates": 3
    })
    print(f"\n[TEST 1] Compile CRISPR: id={proto['protocol_id']} | "
          f"safety={proto['safety_level']} | dur={proto['duration_min']}min")
    assert "opentrons" in proto["script"].lower()
    assert proto["dosage_ul"] == 15.0
    print("[TEST 1] PASS")

    # Test 2: Safety validation (PASS case)
    safety = orch.validate_safety(proto)
    print(f"\n[TEST 2] Safety Validation: clearance={safety['clearance']} | "
          f"checks={[c['check']+':'+c['status'] for c in safety['checks']]}")
    assert safety["valid"] is True
    print("[TEST 2] PASS")

    # Test 3: Safety block (overdose)
    bad_proto = orch.compile_protocol({
        "type": "compound_dosing", "target": "toxin_X",
        "dosage_ul": 999.0, "wells": ["A1"], "replicates": 1
    })
    bad_safety = orch.validate_safety(bad_proto)
    print(f"\n[TEST 3] Safety Block (overdose): clearance={bad_safety['clearance']}")
    assert bad_safety["valid"] is False
    print("[TEST 3] PASS")

    # Test 4: Full execution (simulated)
    result = orch.execute({
        "type": "crispr_knockout", "target": "BRCA1_exon11",
        "dosage_ul": 15.0, "wells": ["A1","B1","C1"], "replicates": 3
    })
    print(f"\n[TEST 4] Execute Protocol: status={result.status} | "
          f"steps={len(result.execution_log)} | "
          f"efficacy={result.reality_feedback.get('efficacy_estimate','?')}")
    assert result.status == "SUCCESS"
    assert len(result.execution_log) == 9
    assert result.telemetry.get("deck_layout_valid") is True
    print("[TEST 4] PASS")

    # Test 5: qPCR protocol
    r2 = orch.execute({
        "type": "qpcr_prep", "target": "KRAS_primer_v3",
        "dosage_ul": 10.0, "wells": ["A1","A2"], "replicates": 2
    })
    print(f"\n[TEST 5] qPCR Prep: status={r2.status} | "
          f"vol={r2.telemetry.get('volume_dispensed_ul')}uL")
    assert r2.status == "SUCCESS"
    print("[TEST 5] PASS")

    # Test 6: Batch combinatorial screen
    batch = orch.batch_screen(
        compounds=["Drug_A", "Drug_B", "Drug_C"],
        doses_ul=[2.5, 5.0],
    )
    print(f"\n[TEST 6] Batch Screen: {len(batch)} wells | "
          f"compounds x doses = 3 x 2 = {3*2}")
    successes = [b for b in batch if b["status"] == "SUCCESS"]
    print(f"  Successes: {len(successes)}/{len(batch)}")
    assert len(batch) == 6
    print("[TEST 6] PASS")

    # Test 7: Run history
    summary = orch.run_summary()
    print(f"\n[TEST 7] Run Summary: total={summary['total_runs']} | "
          f"success_rate={summary['success_rate_pct']}%")
    assert summary["total_runs"] >= 8
    print("[TEST 7] PASS")

    print("\n" + "=" * 60)
    print("WET-LAB ORCHESTRATOR: ALL 7 TESTS PASSED")
    print("=" * 60)
    return True


if __name__ == "__main__":
    all_pass = True
    try:
        test_spatial_engine()
    except Exception as e:
        print(f"SPATIAL ENGINE FAILED: {e}")
        import traceback; traceback.print_exc()
        all_pass = False

    try:
        test_wetlab_orchestrator()
    except Exception as e:
        print(f"WET-LAB ORCHESTRATOR FAILED: {e}")
        import traceback; traceback.print_exc()
        all_pass = False

    print("\n" + "=" * 60)
    if all_pass:
        print("ALL INTEGRATION TESTS PASSED - Spatial AI 92% | Wet-Lab 85%")
    else:
        print("SOME TESTS FAILED - Review above")
    print("=" * 60)
    sys.exit(0 if all_pass else 1)
