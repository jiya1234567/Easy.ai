import os
import json
import pandas as pd

def verify_omega_core():
    """
    [MASTER DNA AUDIT]
    Validates all structural and intelligence components of OMEGA-CORE.
    """
    results = {
        "Data Integrity": {},
        "Intelligence Sync": {},
        "Cognitive Memory": {},
        "Final Score": 0.0
    }
    
    # 1. Data Integrity Check (4 Domains)
    domains = ["finance", "bio", "materials", "quantum"]
    data_score = 0
    for d in domains:
        path = f"reports/{d}_test.csv"
        if os.path.exists(path):
            try:
                pd.read_csv(path)
                results["Data Integrity"][d] = "✅ VERIFIED"
                data_score += 1
            except:
                results["Data Integrity"][d] = "❌ CORRUPT"
        else:
            results["Data Integrity"][d] = "❌ MISSING"
    
    # 2. Intelligence Sync Check
    log_path = "reports/discovery_log.json"
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            logs = json.load(f)
            count = len(logs)
            results["Intelligence Sync"]["Surprise Feed"] = f"✅ {count} Discoveries"
            intel_score = 1
    else:
        results["Intelligence Sync"]["Surprise Feed"] = "❌ DISCONNECTED"
        intel_score = 0
        
    # 3. Cognitive Memory Check
    exp_path = "intelligence/experience.json"
    if os.path.exists(exp_path):
        with open(exp_path, "r") as f:
            exp = json.load(f)
            count = len(exp)
            results["Cognitive Memory"]["Episodes"] = f"✅ {count} Episodes"
            cog_score = 1
    else:
        results["Cognitive Memory"]["Episodes"] = "❌ EMPTY"
        cog_score = 0
        
    # 4. Final DNA Fidelity Calculation
    total_score = (data_score/4) * 0.4 + intel_score * 0.3 + cog_score * 0.3
    results["Final Score"] = f"{total_score:.1%}"
    
    return results

if __name__ == "__main__":
    print("--- [OMEGA-CORE] DNA AUDIT INITIALIZED ---")
    audit = verify_omega_core()
    print(json.dumps(audit, indent=2))
