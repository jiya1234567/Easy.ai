import pandas as pd
import numpy as np
import datetime
import os

def generate_city_data(n_days=100):
    """
    Generates synthetic Smart City infrastructure telemetry.
    """
    np.random.seed(42)
    dates = pd.date_range(start="2026-01-01", periods=n_days, freq='D')
    
    data = {
        "Grid_Voltage": np.random.normal(230, 5, n_days),
        "Energy_Demand": np.random.normal(500, 50, n_days),
        "Traffic_Flow_Rate": np.random.normal(80, 10, n_days),
        "Traffic_Load": np.random.normal(0.6, 0.1, n_days),
        "Water_Pressure": np.random.normal(50, 5, n_days),
        "Water_Consumption": np.random.normal(200, 20, n_days),
        "Comms_Latency": np.random.normal(20, 5, n_days),
        "Packet_Rate": np.random.normal(1000, 100, n_days),
        "Sensor_Noise": np.random.uniform(0.01, 0.05, n_days),
        "Anomaly_Score": np.random.uniform(0.05, 0.15, n_days)
    }
    
    # Introduce a simulated "Cascade" incident
    for i in range(80, 85):
        data["Grid_Voltage"][i] = 180 # Brownout
        data["Energy_Demand"][i] = 750 # Spike
        data["Comms_Latency"][i] = 150 # Cascade impact
        data["Traffic_Flow_Rate"][i] = 20 # Traffic jam
        data["Anomaly_Score"][i] = 0.85 # High Alert
    
    df = pd.DataFrame(data, index=dates)
    
    # Ensure reports directory exists
    if not os.path.exists("reports"):
        os.makedirs("reports")
        
    df.to_csv("reports/city_test_data.csv")
    
    # Metadata for Manifold
    metadata = {
        "Grid_Voltage": "Power",
        "Energy_Demand": "Power",
        "Traffic_Flow_Rate": "Transport",
        "Traffic_Load": "Transport",
        "Water_Pressure": "Water",
        "Water_Consumption": "Water",
        "Comms_Latency": "Comms",
        "Packet_Rate": "Comms",
        "Sensor_Noise": "Uncertainty",
        "Anomaly_Score": "Property"
    }
    
    import json
    with open("reports/city_metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
        
    print(f"Generated Smart City data: reports/city_test_data.csv ({n_days} days)")

if __name__ == "__main__":
    generate_city_data()
