import json
import os
from datetime import datetime
from core.assi_sensing_engine import ASSISensingEngine

def generate_assi_research_data():
    """
    Generates a unified dataset for ASSI (Adaptive System State Intelligence) research.
    It combines standard corporate/system domains and multi-modal robotic domains,
    classifies them using the core engine, and saves the output for dashboard integration.
    """
    print("Initializing ASSI Research Data Generation...")
    
    research_dataset = {
        "metadata": {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "framework": "OMEGA-CORE ASSI Engine",
            "version": "1.0",
            "total_cases": 0
        },
        "standard_domains": [],
        "robotic_domains": []
    }

    # 1. Standard Domains (Single Modality)
    standard_cases = [
        {"company": "Advanced Navigation", "domain": "Inertial Navigation", "entropy": 0.1, "predictability": 0.95, "instability": 0.05},
        {"company": "Extel Technologies", "domain": "Signal Processing", "entropy": 0.2, "predictability": 0.9, "instability": 0.1},
        {"company": "Thermal Dawn", "domain": "Thermal Gradients", "entropy": 0.15, "predictability": 0.85, "instability": 0.1},
        {"company": "Unleash Live", "domain": "Dynamic Scene Understanding", "entropy": 0.85, "predictability": 0.15, "instability": 0.9},
        {"company": "Ocius", "domain": "Ocean Systems / Turbulence", "entropy": 0.9, "predictability": 0.1, "instability": 0.95},
        {"company": "Carbonix", "domain": "Atmospheric Turbulence", "entropy": 0.88, "predictability": 0.2, "instability": 0.85},
        {"company": "Q-CTRL", "domain": "Quantum Control vs Noise", "entropy": 0.5, "predictability": 0.6, "instability": 0.4},
        {"company": "Samsara Eco", "domain": "Chemical to Biological Adaptation", "entropy": 0.6, "predictability": 0.5, "instability": 0.5},
        {"company": "HydGene Renewables", "domain": "Thermodynamics to Grid Adaptation", "entropy": 0.55, "predictability": 0.65, "instability": 0.45},
        {"company": "CREATE Medicines", "domain": "Adaptive Biochemistry", "entropy": 0.75, "predictability": 0.45, "instability": 0.4},
        {"company": "Skin2Neuron", "domain": "Cellular Differentiation", "entropy": 0.7, "predictability": 0.5, "instability": 0.35}
    ]

    for case in standard_cases:
        classification = ASSISensingEngine.classify_system(
            case["entropy"], case["predictability"], case["instability"]
        )
        case["assi_classification"] = classification
        research_dataset["standard_domains"].append(case)

    # 2. Robotic Domains (Multi-Modal)
    robotic_cases = [
        {
            "scenario": "Automated High-Throughput Pipetting",
            "vision_entropy": 0.1, "touch_entropy": 0.05, "smell_entropy": 0.0
        },
        {
            "scenario": "Rigid Crystal Sorting",
            "vision_entropy": 0.15, "touch_entropy": 0.1, "smell_entropy": 0.0
        },
        {
            "scenario": "Volcanic Gas Plume Tracking",
            "vision_entropy": 0.95, "touch_entropy": 0.50, "smell_entropy": 0.90
        },
        {
            "scenario": "Deep Ocean Fluid Sampling",
            "vision_entropy": 0.60, "touch_entropy": 0.95, "smell_entropy": 0.85
        },
        {
            "scenario": "Soft-Polymer Tactile Manipulation",
            "vision_entropy": 0.3, "touch_entropy": 0.65, "smell_entropy": 0.4
        },
        {
            "scenario": "Catalytic Reaction Monitoring (Bio-Reactor)",
            "vision_entropy": 0.7, "touch_entropy": 0.2, "smell_entropy": 0.6
        },
        {
            "scenario": "Live Tissue Microsurgery",
            "vision_entropy": 0.75, "touch_entropy": 0.7, "smell_entropy": 0.8
        },
        {
            "scenario": "Forest Ecosystem Canopy Navigation",
            "vision_entropy": 0.8, "touch_entropy": 0.75, "smell_entropy": 0.9
        }
    ]

    for case in robotic_cases:
        classification, g_ent, pred, instab = ASSISensingEngine.classify_robotic_system(
            case["vision_entropy"], case["touch_entropy"], case["smell_entropy"]
        )
        case["assi_classification"] = classification
        case["global_entropy"] = round(g_ent, 4)
        case["computed_predictability"] = round(pred, 4)
        case["computed_instability"] = round(instab, 4)
        research_dataset["robotic_domains"].append(case)

    research_dataset["metadata"]["total_cases"] = len(standard_cases) + len(robotic_cases)

    # 3. Save to data directory
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "assi_research_data.json")
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(research_dataset, f, indent=4)
        
    print(f"Success! Processed {research_dataset['metadata']['total_cases']} total research cases.")
    print(f"Unified JSON test data written to: {output_path}")
    print("Ready for research analysis.")

if __name__ == "__main__":
    generate_assi_research_data()
