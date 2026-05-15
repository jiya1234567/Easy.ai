import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_semiconductor_data(n_samples=200):
    """
    Generates synthetic data for the 'Sensing meets Semiconductors' domain.
    Models the relationship between chip hardware, environment, and sensor SNR.
    """
    np.random.seed(42)
    start_date = datetime.now() - timedelta(days=n_samples)
    dates = [start_date + timedelta(days=i) for i in range(n_samples)]
    
    # Fundamental Semiconductor Parameters (Drivers)
    thermal_stability = np.random.normal(298, 2, n_samples) # K (Ambient ~25C)
    doping_consistency = np.random.normal(0.95, 0.02, n_samples) # Index
    gate_leakage = np.random.normal(10, 2, n_samples) # nA
    
    # Interaction Layer (Smart Sensing - NSSN)
    # SNR is high when thermal stability is high (low temp) and leakage is low
    snr_uplink = (30 - (thermal_stability - 298) * 0.5 - (gate_leakage - 10) * 0.8) + np.random.normal(0, 1, n_samples)
    quantum_efficiency = (0.85 * doping_consistency) + np.random.normal(0, 0.05, n_samples)
    
    # Edge Computing Metrics (S3B)
    inference_latency = (5 + (thermal_stability - 298) * 0.2 + (1.0 - quantum_efficiency) * 2) + np.random.normal(0, 0.5, n_samples)
    power_consumption = (150 + (gate_leakage * 5)) + np.random.normal(0, 10, n_samples) # mW
    
    # Derived Stability Metric
    system_fidelity = (snr_uplink / 30.0) * (1.0 / (inference_latency / 5.0))
    
    df = pd.DataFrame({
        'Date': dates,
        'Thermal_Stability': thermal_stability,
        'Doping_Consistency': doping_consistency,
        'Gate_Leakage': gate_leakage,
        'SNR_Uplink': snr_uplink,
        'Quantum_Efficiency': quantum_efficiency,
        'Inference_Latency': inference_latency,
        'Power_Consumption': power_consumption,
        'System_Fidelity': system_fidelity
    })
    
    df.set_index('Date', inplace=True)
    
    output_dir = "reports"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_path = os.path.join(output_dir, "semiconductor_sensing_test.csv")
    df.to_csv(output_path)
    print(f"Dataset generated: {output_path}")
    return output_path

if __name__ == "__main__":
    generate_semiconductor_data()
