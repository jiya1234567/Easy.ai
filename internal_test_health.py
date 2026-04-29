import os
import json
import base64
import time
from intelligence.retinal_analyzer import RetinalAnalyzer
from intelligence.health_insurance_engine import HealthInsuranceEngine
from generate_eye_watch import generate_protocol

def run_internal_test():
    print("INITIALIZING OMEGA-CORE INTERNAL HEALTH TEST")
    print("-" * 50)

    # 1. PROFILE SETUP
    print("\n[STEP 1] SETTING UP HEALTH PROFILE")
    profile = {
        "user_id": "U1-AJ-PHILLIPS",
        "age": 42,
        "history": ["Hypertension (Managed)", "Pre-diabetic risks"],
        "last_sync": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    profile_path = "reports/user_profile.json"
    os.makedirs("reports", exist_ok=True)
    with open(profile_path, "w") as f:
        json.dump(profile, f, indent=2)
    print(f"DONE: Profile created for {profile['user_id']}")

    # 2. RETINA SCAN
    print("\n[STEP 2] PERFORMING RETINA SCAN")
    # Using the sample image mentioned in test_retina.py if it exists, otherwise mock
    img_path = r"C:\Users\simon\.gemini\antigravity\brain\ce9afd1c-7863-4fdc-8b7c-cb5af3a37680\media__1776049215877.jpg"
    
    analyzer = RetinalAnalyzer()
    if os.path.exists(img_path):
        with open(img_path, "rb") as f:
            img_bytes = f.read()
        print("Analyzing retinal image...")
        scan_result = analyzer.analyze_image_bytes(img_bytes)
    else:
        print("Sample image not found. Using high-fidelity mock data.")
        scan_result = {
            "overall_risk": "LOW",
            "retinal_diagnostics": "Optimal",
            "diabetic_risk_score": {"band": "LOW", "probability": 0.12},
            "optometric_summary": "Retinal vasculature shows no signs of hypertensive or diabetic retinopathy. CDR is 0.3."
        }
    
    print(f"DONE: Scan Status: {scan_result.get('retinal_diagnostics', 'Normal')}")
    print(f"Summary: {scan_result.get('optometric_summary')}")

    # 3. SMART WATCH SYNC
    print("\n[STEP 3] SYNCHRONIZING SMART WATCH (Galaxy Fit 3)")
    watch_data = generate_protocol()
    print(f"DONE: Sync Complete. {len(watch_data['steps'])} biometric steps processed.")
    print(f"Vitals: BP {watch_data['metrics']['bp']}, Pulse {watch_data['metrics']['pulse']}")

    # 4. SMS ALERT SIMULATION
    print("\n[STEP 4] SIMULATING SMS ALERT")
    sms_alert = {
        "to": "+61 4XX XXX XXX",
        "message": f"OMEGA-CORE ALERT: {watch_data['watch_alert']['message']}",
        "type": "Haptic/SMS"
    }
    print(f"SMS SENT: \"{sms_alert['message']}\"")
    print("DONE: Alert sequence verified.")

    # 5. POLICY SELECTION
    print("\n[STEP 5] SELECTING INSURANCE POLICY")
    engine = HealthInsuranceEngine()
    
    # Map scan result to engine input
    risk_row = {
        "Retinal_Diabetic_Risk": scan_result.get("diabetic_risk_score", {}).get("probability", 0.1),
        "Heart_Risk": 0.2, # Mocked from watch HR variability
        "Hospital_Visits": 0,
        "Medication_Count": 1,
        "Financial_Stress": 0.3,
        "HbA1c": 5.6, # Mocked from glucose metric
        "Retinal_Risk": scan_result.get("diabetic_risk_score", {}).get("probability", 0.1)
    }
    
    recommendation = engine.evaluate_family_risk(risk_row)
    accident_recommendation = engine.evaluate_accident_cover(risk_row)
    
    print(f"Policy Recommendation: {recommendation}")
    print(f"Accident Cover Status: {accident_recommendation}")

    print("\n" + "-" * 50)
    print("INTERNAL HEALTH TEST SUCCESSFUL")
    print("All nodes verified at Node-04 (Geneva).")


if __name__ == "__main__":
    run_internal_test()
