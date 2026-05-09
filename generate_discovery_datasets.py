import pandas as pd
import os
import json

def generate_discovery_datasets():
    os.makedirs("reports/discovery", exist_ok=True)
    
    # DOMAIN 1: Biological Consciousness Test
    bio_data = {
        "Time": ["T1", "T2", "T3", "T4"],
        "Stimulus": ["Calm music", "Red flashing light", "Ambiguous illusion", "Contradictory prompt"],
        "Heart_Rate": [68, 92, 84, 98],
        "Skin_Temp": [36.7, 37.1, 36.9, 37.4],
        "Sleep": ["Good", "Moderate", "Poor", "Poor"],
        "Cognitive_Error": [0.02, 0.15, 0.28, 0.44]
    }
    pd.DataFrame(bio_data).to_csv("reports/discovery/bio_consciousness.csv", index=False)
    
    # DOMAIN 2: Agricultural Emergence
    agri_data = {
        "Field": ["F1", "F2", "F3", "F4"],
        "Temp": [29, 33, 35, 31],
        "Humidity": [60, 78, 81, 74],
        "Soil_N": [0.72, 0.31, 0.28, 0.44],
        "Fungus_Score": [0.05, 0.62, 0.84, 0.33],
        "Wind": ["East", "East", "East", "West"]
    }
    pd.DataFrame(agri_data).to_csv("reports/discovery/agri_emergence.csv", index=False)
    
    # DOMAIN 3: Finance Stress Consciousness Analog
    finance_data = {
        "Family": ["A", "B", "C"],
        "Income": [6000, 7200, 4100],
        "Rent": [3200, 1800, 2100],
        "Health_Risk": [0.2, 0.8, 0.6],
        "Savings": [400, 6000, 200],
        "Stress": [0.72, 0.31, 0.91]
    }
    pd.DataFrame(finance_data).to_csv("reports/discovery/finance_stress.csv", index=False)
    
    # DOMAIN 4: Quantum Stability
    quantum_data = {
        "Qubit": ["Q1", "Q2", "Q3", "Q4"],
        "Coherence": [0.93, 0.88, 0.42, 0.31],
        "Drift": [0.02, 0.04, 0.18, 0.24],
        "Entanglement": ["Strong", "Medium", "Weak", "Collapse"],
        "Syndrome": ["S0", "S1", "S6", "S6"]
    }
    pd.DataFrame(quantum_data).to_csv("reports/discovery/quantum_stability.csv", index=False)
    
    # DOMAIN 5: Consciousness-Like Illusion Tests
    illusion_data = {
        "Frame": [1, 2, 3],
        "Color_Presented": ["Blue/Black", "Rotating Mask", "Impossible Triangle"],
        "User_Perceived": ["White/Gold", "Face inversion", "Stable geometry"],
        "Machine_Prediction": ["Blue/Black", "Flat rotation", "Contradiction"]
    }
    pd.DataFrame(illusion_data).to_csv("reports/discovery/illusion_tests.csv", index=False)
    
    # Metadata map to associate domains with files
    meta = {
        "Biological": "reports/discovery/bio_consciousness.csv",
        "Agricultural": "reports/discovery/agri_emergence.csv",
        "Finance": "reports/discovery/finance_stress.csv",
        "Quantum": "reports/discovery/quantum_stability.csv",
        "Illusion": "reports/discovery/illusion_tests.csv"
    }
    with open("reports/discovery/domain_meta.json", "w") as f:
        json.dump(meta, f, indent=4)
        
    print("Successfully generated Scientific Discovery datasets in reports/discovery/")

if __name__ == "__main__":
    generate_discovery_datasets()
