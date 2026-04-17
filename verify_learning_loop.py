import json
from intelligence.scientific_engine import ScientificEngine

def test_learning_loop():
    print("--- Test: OMEGA-CORE Post-Harvest Learning Loop ---")
    
    # Initialize with Ag data (which has Projected_Yield and Actual_Yield)
    engine = ScientificEngine(data_path="reports/agri_test_suite.csv")
    engine.load_data()
    
    print("Initializing Causal Discovery...")
    engine.discover_causality()
    
    # Check initial weights for Projected_Yield
    target = "Projected_Yield"
    drivers = [u for u, v in engine.causal_graph.edges() if v == target]
    
    print(f"Target: {target}")
    for u in drivers:
        print(f"  Driver: {u} | Initial Weight: {engine.causal_graph[u][target]['weight']:.4f}")
        
    print("\nRunning Learning Loop (Ingesting Ground Truth)...")
    success, audit = engine.learn_from_ground_truth()
    
    if success:
        print("PASS: Learning iteration complete.")
        for item in audit:
            print(f"  {item['driver']}: {item['old_weight']} -> {item['new_weight']} (Delta: {item['delta']})")
    else:
        print(f"FAIL: {audit}")

if __name__ == "__main__":
    test_learning_loop()
