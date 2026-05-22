import json
import numpy as np

def classify_system(entropy, predictability, instability):
    """
    Classifies a system based on ASSI Framework:
    - Reducible: low entropy, high predictability, low instability
    - Irreducible: high entropy, low predictability, high instability
    - Hybrid: transitional/mixed entropy, moderate predictability, phase transitions
    - Emergent: adaptive entropy, hidden-state predictability, structured instability
    """
    if entropy < 0.3 and predictability > 0.8 and instability < 0.2:
        return "Reducible"
    elif entropy > 0.7 and predictability < 0.3 and instability > 0.7:
        return "Irreducible"
    elif entropy >= 0.7 and predictability >= 0.4 and 0.2 < instability < 0.8:
        # High entropy but structured predictability = emergent
        return "Emergent / Biological"
    elif 0.3 <= entropy <= 0.7 and 0.3 <= predictability <= 0.8:
        return "Hybrid (Transitioning)"
    else:
        return "Unknown / Unclassified"

def run_assi_benchmark():
    print("==========================================================")
    print("       CLASSIFICATION BENCHMARK: ASSI FRAMEWORK           ")
    print("==========================================================")
    
    test_cases = [
        # Reducible
        {"company": "Advanced Navigation", "domain": "Inertial Navigation", "entropy": 0.1, "predictability": 0.95, "instability": 0.05, "expected": "Reducible"},
        {"company": "Extel Technologies", "domain": "Signal Processing", "entropy": 0.2, "predictability": 0.9, "instability": 0.1, "expected": "Reducible"},
        {"company": "Thermal Dawn", "domain": "Thermal Gradients", "entropy": 0.15, "predictability": 0.85, "instability": 0.1, "expected": "Reducible"},
        
        # Irreducible
        {"company": "Unleash Live", "domain": "Dynamic Scene Understanding", "entropy": 0.85, "predictability": 0.15, "instability": 0.9, "expected": "Irreducible"},
        {"company": "Ocius", "domain": "Ocean Systems / Turbulence", "entropy": 0.9, "predictability": 0.1, "instability": 0.95, "expected": "Irreducible"},
        {"company": "Carbonix", "domain": "Atmospheric Turbulence", "entropy": 0.88, "predictability": 0.2, "instability": 0.85, "expected": "Irreducible"},
        
        # Hybrid
        {"company": "Q-CTRL", "domain": "Quantum Control vs Noise", "entropy": 0.5, "predictability": 0.6, "instability": 0.4, "expected": "Hybrid"},
        {"company": "Samsara Eco", "domain": "Chemical to Biological Adaptation", "entropy": 0.6, "predictability": 0.5, "instability": 0.5, "expected": "Hybrid"},
        {"company": "HydGene Renewables", "domain": "Thermodynamics to Grid Adaptation", "entropy": 0.55, "predictability": 0.65, "instability": 0.45, "expected": "Hybrid"},
        
        # Emergent / Biological
        {"company": "CREATE Medicines", "domain": "Adaptive Biochemistry", "entropy": 0.75, "predictability": 0.45, "instability": 0.4, "expected": "Emergent"},
        {"company": "Skin2Neuron", "domain": "Cellular Differentiation", "entropy": 0.7, "predictability": 0.5, "instability": 0.35, "expected": "Emergent"}
    ]

    results = []
    passed = 0
    
    for case in test_cases:
        classification = classify_system(case["entropy"], case["predictability"], case["instability"])
        
        # Check if classification matches the expected category (roughly)
        is_match = False
        if "Reducible" in classification and "Reducible" in case["expected"]:
            is_match = True
        elif "Irreducible" in classification and "Irreducible" in case["expected"]:
            is_match = True
        elif "Hybrid" in classification and "Hybrid" in case["expected"]:
            is_match = True
        elif "Emergent" in classification and "Emergent" in case["expected"]:
            is_match = True
            
        if is_match: passed += 1
            
        print(f"Company: {case['company']}")
        print(f"Domain:  {case['domain']}")
        print(f"Metrics: Entropy={case['entropy']}, Predictability={case['predictability']}, Instability={case['instability']}")
        print(f"Class:   {classification} (Expected: {case['expected']})")
        print(f"Match:   {'[PASS]' if is_match else '[FAIL]'}")
        print("-" * 50)
        
        results.append({
            "company": case["company"],
            "classification": classification,
            "match": is_match
        })

    print(f"\nFinal Score: {passed}/{len(test_cases)} Passed")
    if passed == len(test_cases):
        print("Universal Sensing Benchmark: VALIDATED")
    else:
        print("Universal Sensing Benchmark: REQUIRES TUNING")

if __name__ == "__main__":
    run_assi_benchmark()
