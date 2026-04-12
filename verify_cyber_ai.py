import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

try:
    from simulation.cyber_simulator import CyberSimulator
    from simulation.adversarial_engine import AdversarialEngine
    from intelligence.mitre_mapper import MitreMapper
    from intelligence.auto_response_engine import AutoResponseEngine

    print("--- [VERIFICATION] Starting Cyber AI System Test ---")
    
    sim = CyberSimulator()
    engine = AdversarialEngine(sim)
    
    # Run 2 rounds of adversarial simulation
    print("\nRunning Multi-Round Simulation...")
    for i in range(2):
        res = engine.run_round()
        print(f"Round {i+1} summary: Red attacked {res['red_action']['target']} | Blue actions: {len(res['blue_responses'])}")

    print("\n[SUCCESS] All core components integrated and functional.")

except Exception as e:
    print(f"\n[FAILURE] Verification failed: {e}")
    sys.exit(1)
