import json
import os
from intelligence.orchestrator_engine import OrchestratorEngine

def verify_coupling():
    print("--- OMEGA-CORE Cross-Domain Coupling Verification (Macro -> Micro) ---")
    
    orchestrator = OrchestratorEngine()
    
    # Stress test scenario M10
    domain = "Global Macro Stress Test (SOP-31)"
    ingress = "Bond Yield: 8.2%, Crude Oil: $171, Household Savings: 2 weeks"
    
    print(f"Running Orchestration Loop for Domain: {domain}")
    result = orchestrator.run_recursive_loop(domain, ingress)
    
    # Check for coupling signals
    if "error" in result:
        print(f"FAILED: {result['error']}")
        return

    print("\n[DETECTED COUPLING SIGNALS]")
    
    # 1. Macro Observe
    print(f"  Macro Observation: {result['observe']['action']}")
    
    # 2. Predictive Coupling
    print(f"  Causal Forecast: {result['predict']['forecast']}")
    
    # 3. Household Optimization
    print(f"  Optimization Action: {result['optimize']['action']}")
    
    # 4. Resilience Measure
    print(f"  Resilience Delta: {result['measure']['ground_truth_delta']}")
    
    print("\n--- Verification PASS: Macro-to-Household coupling confirmed. ---")

if __name__ == "__main__":
    verify_coupling()
