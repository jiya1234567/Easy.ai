import pandas as pd
import numpy as np
import os
import json

def generate_glasswing_data():
    """
    Generates the GLASSWING Maximum Defensive Stress Testbed dataset.
    Includes decoy risk, adaptive attackers, and cross-domain contagion nodes.
    """
    np.random.seed(88)
    n_steps = 200
    dates = pd.date_range(end='2026-04-20', periods=n_steps, freq='min')
    
    # User's specified Node Data Baseline
    nodes = {
        "AUTH01": {"Role": "Identity_Server", "Patch": 0.42, "Priv": 9, "SupplyIdx": 0.92, "LateralIdx": 0.88, "Crit": 0.95, "Decoy": 0.05, "Insider": 0},
        "DB01": {"Role": "Customer_Database", "Patch": 0.31, "Priv": 10, "SupplyIdx": 0.85, "LateralIdx": 0.91, "Crit": 0.99, "Decoy": 0.10, "Insider": 0},
        "API01": {"Role": "Public_API", "Patch": 0.71, "Priv": 5, "SupplyIdx": 0.61, "LateralIdx": 0.63, "Crit": 0.71, "Decoy": 0.05, "Insider": 0},
        "SCM01": {"Role": "Supply_Chain_Server", "Patch": 0.24, "Priv": 8, "SupplyIdx": 0.97, "LateralIdx": 0.93, "Crit": 0.96, "Decoy": 0.12, "Insider": 1},
        "DRONE01": {"Role": "Drone_Control_Node", "Patch": 0.58, "Priv": 7, "SupplyIdx": 0.76, "LateralIdx": 0.84, "Crit": 0.88, "Decoy": 0.08, "Insider": 0},
        "GRID01": {"Role": "Power_Grid_Controller", "Patch": 0.19, "Priv": 10, "SupplyIdx": 0.99, "LateralIdx": 0.97, "Crit": 1.00, "Decoy": 0.95, "Insider": 0},
        "TRADER01": {"Role": "Macro_Execution_Engine", "Patch": 0.64, "Priv": 8, "SupplyIdx": 0.73, "LateralIdx": 0.81, "Crit": 0.87, "Decoy": 0.22, "Insider": 0},
        "AI01": {"Role": "Model_Weights_Server", "Patch": 0.77, "Priv": 10, "SupplyIdx": 0.52, "LateralIdx": 0.79, "Crit": 0.92, "Decoy": 0.15, "Insider": 1}
    }
    
    data = {}
    for node, cfg in nodes.items():
        # Static baseline features
        patch = np.full(n_steps, cfg["Patch"]) + np.random.normal(0, 0.01, n_steps)
        priv = np.full(n_steps, cfg["Priv"])
        supply_dep = np.full(n_steps, cfg["SupplyIdx"])
        lateral_risk = np.full(n_steps, cfg["LateralIdx"])
        criticality = np.full(n_steps, cfg["Crit"])
        decoy_risk = np.full(n_steps, cfg["Decoy"])
        insider = np.full(n_steps, cfg["Insider"])
        
        # dynamic signals
        ports = np.random.randint(5, 30, n_steps)
        entropy = np.random.normal(0.7, 0.1, n_steps)
        logins = np.random.poisson(2, n_steps)
        anomaly = np.random.normal(0.1, 0.05, n_steps)
        
        # Inject the Glasswing Attack Sequence
        # Scenario: SCM01 -> AI01 -> DRONE01 -> GRID01 -> TRADER01
        
        # A1: Credential Stuffing on AUTH01 (Start: 20)
        if node == "AUTH01":
            logins[20:50] += np.random.poisson(40, 30)
            anomaly[20:50] += 0.6
            
        # A2: Supply Chain Backdoor on SCM01 (Start: 40)
        if node == "SCM01":
            entropy[40:100] = np.random.normal(0.2, 0.05, 60)
            anomaly[40:100] += 0.8
            
        # A3: Prompt Injection on AI01 (Start: 60)
        if node == "AI01":
            anomaly[60:120] += 0.7
            
        # A4: Privilege Escalation on DB01 (Start: 80)
        if node == "DB01":
            anomaly[80:140] += 0.85
            
        # A5: ICS Disruption on GRID01 (Start: 100)
        if node == "GRID01":
            anomaly[100:160] += 0.9
            
        # A6: Drone Command Hijack on DRONE01 (Start: 120)
        if node == "DRONE01":
            anomaly[120:180] += 0.75
            
        # A7: Market Manipulation on TRADER01 (Start: 140)
        if node == "TRADER01":
            anomaly[140:190] += 0.8
            
        data[f"{node}_Patch_Level"] = patch
        data[f"{node}_User_Privilege_Level"] = priv
        data[f"{node}_Supply_Chain_Dependency"] = supply_dep
        data[f"{node}_Lateral_Movement_Risk"] = lateral_risk
        data[f"{node}_Criticality"] = criticality
        data[f"{node}_Decoy_Risk"] = decoy_risk
        data[f"{node}_Insider_Access"] = insider
        data[f"{node}_Open_Ports"] = ports
        data[f"{node}_Packet_Entropy"] = entropy
        data[f"{node}_Failed_Logins"] = logins
        data[f"{node}_Anomaly_Score"] = np.clip(anomaly, 0, 1)
        
    df = pd.DataFrame(data, index=dates)
    
    os.makedirs("reports", exist_ok=True)
    df.to_csv("reports/cyber_glasswing_stress.csv", index=True)
    
    # Metadata
    meta = {col: col.split("_")[0] for col in df.columns}
    with open("reports/cyber_glasswing_metadata.json", "w") as f:
        json.dump(meta, f, indent=2)
        
    print(f"GLASSWING Testbed generated: reports/cyber_glasswing_stress.csv")

if __name__ == "__main__":
    generate_glasswing_data()
