import pandas as pd
import numpy as np
import os
import json

def generate_materials_data(n_samples=200):
    """
    Generates a high-fidelity Material Science dataset with 5 key dimensions.
    """
    np.random.seed(42)
    materials = [f"M{i:03d}" for i in range(1, n_samples + 1)]
    
    # Define Clusters (High-Performance, Low-Performance, Anomalous)
    cluster = np.random.choice(['High', 'Low', 'Nano-Enhanced'], n_samples, p=[0.4, 0.4, 0.2])
    
    data = []
    for i, c in enumerate(cluster):
        mat = materials[i]
        
        # 1. Causal Drivers
        atomic_struct = np.random.normal(0.8, 0.05) if c in ['High', 'Nano-Enhanced'] else np.random.normal(0.4, 0.1)
        grain_size = np.random.normal(0.75, 0.05) if c == 'High' else (np.random.normal(0.3, 0.1) if c == 'Low' else np.random.normal(0.9, 0.05))
        nano_coating = 1 if c == 'Nano-Enhanced' or (c == 'High' and np.random.rand() > 0.5) else 0
        pressure = np.random.normal(0.65, 0.1) if c in ['High', 'Nano-Enhanced'] else np.random.normal(0.25, 0.1)
        
        # 2. Base Physical Properties (Derived from drivers)
        cond = (atomic_struct * 0.8 + pressure * 0.2) + np.random.normal(0, 0.02)
        strength = (atomic_struct * 0.5 + grain_size * 0.3 + nano_coating * 0.2) + np.random.normal(0, 0.01)
        elasticity = np.random.normal(0.7, 0.05) if c == 'High' else np.random.normal(0.5, 0.1)
        thermal = (nano_coating * 0.6 + atomic_struct * 0.3) + np.random.normal(0, 0.05)
        defect = np.random.normal(0.1, 0.02) if c in ['High', 'Nano-Enhanced'] else np.random.normal(0.7, 0.1)

        # 3. Interventions
        temp = np.random.normal(800, 50) if c in ['High', 'Nano-Enhanced'] else np.random.normal(500, 100)
        time_m = np.random.normal(5, 1) if c in ['High', 'Nano-Enhanced'] else np.random.normal(3, 1)
        doping = np.random.normal(0.1, 0.02) if c in ['High', 'Nano-Enhanced'] else np.random.normal(0.4, 0.05)
        
        # 4. Temporal Dynamics
        cycles = np.random.normal(1000, 100) if c in ['High', 'Nano-Enhanced'] else np.random.normal(400, 50)
        degrad = 0.05 if c in ['High', 'Nano-Enhanced'] else 0.3
        perf_stress = strength * (1 - degrad)
        
        # 5. Network / Interaction
        mix_ratio = np.random.normal(0.7, 0.05) if c in ['High', 'Nano-Enhanced'] else np.random.normal(0.3, 0.1)
        interface_strength = np.random.normal(0.85, 0.05) if c == 'High' else np.random.normal(0.4, 0.1)
        layer_depth = np.random.randint(3, 5) if c in ['High', 'Nano-Enhanced'] else np.random.randint(1, 3)
        
        # 6. Uncertainty
        error = 0.02 if c == 'High' else 0.08
        conf = 0.95 if c == 'High' else 0.7
        
        row = {
            "Material": mat,
            "Conductivity": cond, "Strength": strength, "Elasticity": elasticity, "Thermal_Stability": thermal, "Defect_Score": defect,
            "Atomic_Structure": atomic_struct, "Grain_Size": grain_size, "Nano_Coating": nano_coating, "Pressure_Processing": pressure,
            "Treatment_Temperature": temp, "Treatment_Time": time_m, "Doping_Level": doping,
            "Time_Cycle": cycles, "Degradation_Rate": degrad, "Performance_After_Stress": perf_stress,
            "Composite_Mix_Ratio": mix_ratio, "Interface_Bond_Strength": interface_strength, "Layer_Depth": layer_depth,
            "Measurement_Error": error, "Confidence_Score": conf,
            "Cluster": c # For metadata indexing
        }
        data.append(row)
        
    df = pd.DataFrame(data)
    
    # Metadata
    metadata = {row['Material']: row['Cluster'] for row in data}
    
    return df, metadata

if __name__ == "__main__":
    print("Generating Universal Material Science Dataset...")
    df, meta = generate_materials_data()
    
    os.makedirs("reports", exist_ok=True)
    df.to_csv("reports/materials_test.csv", index=False)
    
    with open("reports/materials_metadata.json", "w") as f:
        json.dump(meta, f, indent=2)
        
    print(f"Data saved to reports/materials_test.csv ({len(df)} samples)")
