import sys
import os
import json

# Add current directory to path
sys.path.append(os.getcwd())

from intelligence.reasoning_agent import ReasoningAgent

def run_cancer_tests():
    agent = ReasoningAgent()
    
    with open("reports/cancer_discovery_test.json", "r") as f:
        cancer_data = json.load(f)

    test_suites = {
        "DOMAIN A - Mutation Driver Discovery": {
            "domain": "Health/Bio",
            "task": "Rank mutation severity and identify pathway interactions.",
            "genomics": cancer_data["genomics"],
            "biomarkers": cancer_data["biomarkers"]
        },
        "DOMAIN B - Drug Toxicity Prediction": {
            "domain": "Health/Bio",
            "task": "Predict harmful off-target effects and estimate therapeutic window.",
            "candidates": cancer_data["candidate_drugs"]
        },
        "DOMAIN C - Resistance Evolution": {
            "domain": "Health/Bio",
            "task": "Forecast resistance emergence and identify escape pathways.",
            "tumor_evolution": [
                {"day": 0, "clone": "C1", "mutation": "EGFR", "sensitivity": 0.92},
                {"day": 15, "clone": "C2", "mutation": "MET Amplification", "sensitivity": 0.61},
                {"day": 30, "clone": "C3", "mutation": "KRAS Activation", "sensitivity": 0.24},
                {"day": 60, "clone": "C4", "mutation": "PI3K Escape", "sensitivity": 0.09}
            ]
        },
        "DOMAIN D - Multi-Drug Synergy": {
            "domain": "Health/Bio",
            "task": "Find combinations stronger together and minimize overlapping toxicity.",
            "combinations": [
                {"drug_a": "OGC-101", "drug_b": "OGC-205", "synergy": 0.81},
                {"drug_a": "OGC-101", "drug_b": "OGC-309", "synergy": 0.21},
                {"drug_a": "OGC-205", "drug_b": "OGC-412", "synergy": 0.93}
            ]
        },
        "DOMAIN E - Immune Microenvironment": {
            "domain": "Health/Bio",
            "task": "Model tumor vs immune interactions and predict immunotherapy success.",
            "microenvironment": cancer_data["tumor_microenvironment"]
        }
    }

    results = {}
    print("--- Running OMEGA-CORE Cancer Drug Discovery Test ---")
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

    with open("reports/cancer_discovery_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nResults saved to reports/cancer_discovery_results.json")

if __name__ == "__main__":
    run_cancer_tests()
