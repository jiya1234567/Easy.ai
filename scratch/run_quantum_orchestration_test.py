import sys
import os
import json

# Add current directory to path
sys.path.append(os.getcwd())

from intelligence.reasoning_agent import ReasoningAgent

def run_quantum_tests():
    agent = ReasoningAgent()
    
    with open("reports/quantum_test_dataset.json", "r") as f:
        quantum_data = json.load(f)

    test_suites = {
        "DOMAIN A - Decoherence Prediction": {
            "domain": "Quantum Physics",
            "task": "Predict decoherence collapse window and identify dominant causal factor.",
            "telemetry": quantum_data["telemetry"],
            "hardware": quantum_data["hardware"]
        },
        "DOMAIN B - Quantum Error Cascade": {
            "domain": "Quantum Computing",
            "task": "Detect hidden error propagation tree and stabilization intervention.",
            "error_data": [
                {"time": "T1", "qubit": "Q12", "error_type": "Phase Flip", "drift": 0.03},
                {"time": "T2", "qubit": "Q14", "error_type": "Bit Flip", "drift": 0.08},
                {"time": "T3", "qubit": "Q12", "error_type": "Crosstalk", "drift": 0.19},
                {"time": "T4", "qubit": "Q18", "error_type": "Cascade Error", "drift": 0.41}
            ]
        },
        "DOMAIN C - Hybrid Optimization": {
            "domain": "Quantum-Classical Integration",
            "task": "Dynamically route workloads to minimize energy and time.",
            "workloads": {
                "Matrix Search": {"classical": "High", "quantum": "Low"},
                "Memory Retrieval": {"classical": "Low", "quantum": "High"},
                "Optimization": {"classical": "Extreme", "quantum": "Medium"}
            }
        },
        "DOMAIN E - Experiment Planning": {
            "domain": "Quantum Research",
            "goal": "Increase coherence time by 15% under thermal fluctuation constraints.",
            "task": "Generate candidate experiments, rank by cost, and identify causal variables."
        }
    }

    results = {}
    print("--- Running OMEGA-CORE Quantum Research Orchestration Test ---")
    for name, data in test_suites.items():
        print(f"\nRunning {name}...")
        try:
            result = agent.execute_reasoning(data)
            results[name] = result
            print(f"Result for {name}:")
            print(json.dumps(result, indent=2))
        except Exception as e:
            print(f"Failed {name}: {e}")
            results[name] = {"error": str(e)}

    with open("reports/quantum_orchestration_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nResults saved to reports/quantum_orchestration_results.json")

if __name__ == "__main__":
    run_quantum_tests()
