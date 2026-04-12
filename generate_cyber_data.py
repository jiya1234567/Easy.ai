import pandas as pd
import numpy as np
import os
import json

def generate_cyber_data(n_steps=1000, n_nodes=5):
    """
    Generates high-fidelity, adversarial cybersecurity dataset.
    Features include network state, causal drivers, attack vectors, and multi-agent layers.
    """
    np.random.seed(42)
    nodes = [f"N{i}" for i in range(1, n_nodes + 1)]
    
    # Base configuration for nodes
    # Some nodes are more vulnerable (lower patch level, higher privilege)
    node_configs = {
        "N1": {"patch": 0.90, "priv": 0.2, "ports": 5},
        "N2": {"patch": 0.88, "priv": 0.25, "ports": 6},
        "N3": {"patch": 0.30, "priv": 0.9, "ports": 20}, # Vulnerable Target
        "N4": {"patch": 0.35, "priv": 0.85, "ports": 18}, # Vulnerable Target
        "N5": {"patch": 0.92, "priv": 0.2, "ports": 4}
    }
    
    data = {}
    dates = pd.date_range(end='2026-04-11', periods=n_steps, freq='min')
    
    for node in nodes:
        cfg = node_configs[node]
        
        # 1. Causal Driver Layer (Static/Slowly changing)
        patch_level = np.full(n_steps, cfg["patch"]) + np.random.normal(0, 0.005, n_steps)
        user_priv = np.full(n_steps, cfg["priv"])
        open_ports = np.full(n_steps, cfg["ports"])
        ext_conn = np.random.randint(5, 15, n_steps) if cfg["patch"] > 0.5 else np.random.randint(50, 100, n_steps)
        
        # 2. Base Network State (CORE SIGNAL)
        # Normal traffic
        traffic = np.random.normal(1200, 50, n_steps)
        entropy = np.random.normal(0.85, 0.02, n_steps)
        logins = np.random.poisson(2, n_steps)
        cpu = np.random.normal(0.4, 0.05, n_steps)
        
        # 3. Attack / Intervention Layer
        # Inject attack on N3 and N4 around middle
        attack_mask = np.zeros(n_steps)
        attack_start, attack_end = 400, 600
        attack_mask[attack_start:attack_end] = 1.0
        
        payload_intensity = np.zeros(n_steps)
        if node in ["N3", "N4"]:
            payload_intensity[attack_start:attack_end] = np.random.uniform(0.7, 1.0, attack_end - attack_start)
            
            # Attack impact
            traffic[attack_start:attack_end] *= (1 + payload_intensity[attack_start:attack_end] * 2)
            entropy[attack_start:attack_end] *= 0.5 # Low entropy packets
            logins[attack_start:attack_end] += np.random.poisson(20, attack_end - attack_start)
            cpu[attack_start:attack_end] = np.clip(cpu[attack_start:attack_end] + payload_intensity[attack_start:attack_end] * 0.5, 0, 1)
            
        # 4. Anomaly Score (Outcome)
        anomaly_score = (payload_intensity * 0.8) + (cpu * 0.2) + np.random.normal(0, 0.05, n_steps)
        anomaly_score = np.clip(anomaly_score, 0, 1)
        
        # 5. Time Dynamics
        anomaly_growth = np.gradient(anomaly_score)
        system_degradation = np.cumsum(anomaly_score) / np.max(np.cumsum(anomaly_score) + 1)
        
        # 6. Network Graph / Lateral Movement Risk
        influence = np.random.normal(0.4, 0.1, n_steps)
        lateral_risk = (1.0 - patch_level) * user_priv * (1.0 + payload_intensity)
        lateral_risk = np.clip(lateral_risk, 0, 1)
        
        # 7. Uncertainty + Confidence
        confidence = 0.95 - (anomaly_score * 0.2) + np.random.normal(0, 0.01, n_steps)
        fp_rate = 0.05 + (anomaly_score * 0.1)
        noise = np.random.normal(0.02, 0.005, n_steps)
        
        # 8. Defense / Response
        firewall = np.random.normal(0.9, 0.05, n_steps) if cfg["patch"] > 0.5 else np.random.normal(0.5, 0.1, n_steps)
        resp_time = np.random.randint(1, 3, n_steps) if cfg["patch"] > 0.5 else np.random.randint(8, 12, n_steps)
        
        # Populate data
        data[f"{node}_Traffic_Volume"] = traffic
        data[f"{node}_Packet_Entropy"] = entropy
        data[f"{node}_Failed_Logins"] = logins
        data[f"{node}_CPU_Usage"] = cpu
        data[f"{node}_Anomaly_Score"] = anomaly_score
        data[f"{node}_Patch_Level"] = patch_level
        data[f"{node}_User_Privilege_Level"] = user_priv
        data[f"{node}_Open_Ports"] = open_ports
        data[f"{node}_External_Connections"] = ext_conn
        data[f"{node}_Payload_Intensity"] = payload_intensity
        data[f"{node}_Anomaly_Growth"] = anomaly_growth
        data[f"{node}_System_Degradation"] = system_degradation
        data[f"{node}_Influence_Score"] = influence
        data[f"{node}_Lateral_Movement_Risk"] = lateral_risk
        data[f"{node}_Detection_Confidence"] = confidence
        data[f"{node}_False_Positive_Rate"] = fp_rate
        data[f"{node}_Sensor_Noise"] = noise
        data[f"{node}_Firewall_Strength"] = firewall
        data[f"{node}_Response_Time"] = resp_time

    df = pd.DataFrame(data, index=dates)
    
    # Metadata for classification in Manifold
    metadata = {}
    for col in df.columns:
        node_id = col.split("_")[0]
        metadata[col] = f"Node {node_id}"
        
    return df, metadata

if __name__ == "__main__":
    print("Generating Cybersecurity Universal Test Data...")
    df, meta = generate_cyber_data()
    
    os.makedirs("reports", exist_ok=True)
    df.to_csv("reports/cyber_test_advanced.csv", index=True)
    
    with open("reports/cyber_test_metadata.json", "w") as f:
        json.dump(meta, f, indent=2)
        
    print(f"Dataset generated: reports/cyber_test_advanced.csv ({len(df)} steps, {len(df.columns)} signals)")
    print("Metadata saved to reports/cyber_test_metadata.json")
