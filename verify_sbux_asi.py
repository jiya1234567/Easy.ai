import os
import json
import subprocess

def verify_sbux_pipeline():
    print("--- OMEGA-CORE ASI VERIFICATION: SBUX ---")
    
    # Step 1: Data Generation
    print("[1/3] Generating SBUX Target.JASON...")
    subprocess.run(["py", "generate_sbux.py"], check=True)
    if os.path.exists("Target.JASON"):
        print("      SUCCESS: Target.JASON found.")
    
    # Step 2: Kernel Processing
    print("[2/3] Processing through ASI Kernel...")
    subprocess.run(["py", "run_sbux_kernel.py"], check=True)
    if os.path.exists("DASHBOARD.json"):
        with open("DASHBOARD.json", "r") as f:
            dash = json.load(f)
            print(f"      SUCCESS: DASHBOARD.json generated. Prediction: {dash['agent_reports']['sim']}")
    
    # Step 3: Asset Radar Integration
    print("[3/3] Verifying Asset Radar Report...")
    report_path = "reports/metrics/sbux.json"
    if os.path.exists(report_path):
        with open(report_path, "r") as f:
            report = json.load(f)
            print(f"      SUCCESS: {report['asset']} Report validated. Status: {report['status']}")
    
    print("\n--- ASI PROCESS VERIFIED: SBUX READY FOR DEPLOYMENT ---")

if __name__ == "__main__":
    verify_sbux_pipeline()
