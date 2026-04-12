import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

try:
    from simulation.smart_city_simulator import SmartCitySimulator
    from intelligence.scientific_engine import ScientificEngine

    print("--- [VERIFICATION] Starting Smart City Digital Twin Test ---")
    
    # 1. Test Ontology
    engine = ScientificEngine(data_path="reports/city_test_data.csv")
    engine.load_data()
    ontology = engine.get_ontology_map()
    print(f"\n[ONTOLOGY] DRIVERs detected: {len(ontology['DRIVER'])}")
    if "Voltage_Level" in ontology["PROPERTY"] or "Grid_Voltage" in [c for c in ontology["PROPERTY"] if "Grid_Voltage" in c]:
        print("[SUCCESS] Smart City variables correctly mapped in ontology.")
    else:
        # Check if the column is actually there but mapping failed
        cols = engine.data.columns.tolist()
        print(f"[DEBUG] Actual Columns: {cols}")
        print("[FAILURE] Smart City variables missing from ontology.")

    # 2. Test Simulation Cascade
    sim = SmartCitySimulator()
    print("\n[SIMULATION] Injecting Critical Power Failure on Node P...")
    results = sim.inject_shock("P", intensity=1.0)
    
    # Check if Power failure propagated to Comms (C) and Emergency (E)
    comms_risk = results["C"]["cascade_risk"]
    ems_risk = results["E"]["cascade_risk"]
    
    print(f"Comms (C) Cascade Risk: {comms_risk}")
    print(f"Emergency (E) Cascade Risk: {ems_risk}")
    
    if comms_risk > 0.5 and ems_risk > 0.3:
        print("[SUCCESS] Cascading failure propagation verified.")
    else:
        print("[FAILURE] Cascade propagation below expected thresholds.")

    print("\n--- [VERIFICATION COMPLETE] ---")

except Exception as e:
    print(f"\n[FAILURE] Verification failed: {e}")
    sys.exit(1)
