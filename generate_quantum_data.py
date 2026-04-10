import pandas as pd
import numpy as np
import os
import json

def generate_quantum_data(n_samples=200):
    """
    Generates a high-fidelity Quantum Computing dataset.
    """
    np.random.seed(42)
    qubits = [f"Q_{i:03d}" for i in range(1, n_samples + 1)]
    
    # Define Clusters (Stable, Noisy, Entangled-Node)
    cluster = np.random.choice(['Stable', 'Noisy', 'Entangled'], n_samples, p=[0.5, 0.3, 0.2])
    
    data = []
    for i, c in enumerate(cluster):
        qb = qubits[i]
        
        # 1. Causal Drivers
        mag_bias = np.random.normal(0.5, 0.05) if c == 'Stable' else np.random.normal(0.8, 0.1)
        pulse_dur = np.random.normal(0.9, 0.05) if c in ['Stable', 'Entangled'] else np.random.normal(0.4, 0.1)
        vacuum = np.random.normal(0.95, 0.02) if c == 'Stable' else np.random.normal(0.6, 0.1)
        
        # 2. Base Properties
        coherence = (pulse_dur * 0.7 + vacuum * 0.3) + np.random.normal(0, 0.01)
        fidelity = (coherence * 0.8 + (1-mag_bias) * 0.2) + np.random.normal(0, 0.01)
        stability = np.random.normal(0.9, 0.05) if c == 'Stable' else np.random.normal(0.4, 0.1)
        phase_shift = np.random.normal(0.01, 0.005) if c == 'Stable' else np.random.normal(0.1, 0.02)
        
        # 3. Interventions
        laser = np.random.normal(0.8, 0.05) if c in ['Stable', 'Entangled'] else np.random.normal(0.4, 0.1)
        cryo = np.random.normal(15, 2) # mK
        microwave = np.random.normal(5.0, 0.5) # GHz
        
        # 4. Dynamics
        decoherence = 0.02 if c == 'Stable' else 0.15
        relaxation = np.random.normal(50, 5) if c == 'Stable' else np.random.normal(20, 5)
        
        # 5. Network
        entanglement = np.random.normal(0.95, 0.02) if c == 'Entangled' else np.random.normal(0.3, 0.1)
        coupler = np.random.normal(0.8, 0.05) if c == 'Entangled' else np.random.normal(0.2, 0.05)
        
        # 6. Uncertainty
        readout_error = 0.01 if c == 'Stable' else 0.05
        confidence = 0.99 if c == 'Stable' else 0.8
        
        row = {
            "Qubit": qb,
            "Coherence_Time": coherence, "Fidelity": fidelity, "Qubit_Stability": stability, "Phase_Shift": phase_shift,
            "Magnetic_Bias": mag_bias, "Pulse_Duration": pulse_dur, "Vacuum_Pressure": vacuum,
            "Laser_Intensity": laser, "Cryo_Temperature": cryo, "Microwave_Frequency": microwave,
            "Decoherence_Rate": decoherence, "Relaxation_Time": relaxation,
            "Entanglement_Entropy": entanglement, "Coupler_Strength": coupler,
            "Readout_Error": readout_error, "Confidence_Score": confidence,
            "Cluster": c
        }
        data.append(row)
        
    df = pd.DataFrame(data)
    metadata = {row['Qubit']: row['Cluster'] for row in data}
    return df, metadata

if __name__ == "__main__":
    print("Generating Universal Quantum Computing Dataset...")
    df, meta = generate_quantum_data()
    os.makedirs("reports", exist_ok=True)
    df.to_csv("reports/quantum_test.csv", index=False)
    with open("reports/quantum_metadata.json", "w") as f:
        json.dump(meta, f, indent=2)
    print(f"Quantum Data saved to reports/quantum_test.csv ({len(df)} samples)")
