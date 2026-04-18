import json
import os
import pandas as pd
from intelligence.scientific_engine import ScientificEngine
from intelligence.agri_intelligence import AgriIntelligence

def verify_weather_manifold_tear():
    print("--- Audit: Weather/Fire Manifold Tear Detection ---")
    engine = ScientificEngine(data_path="reports/weather_propagation_b.csv")
    engine.load_data()
    
    # Check Stability
    stability = engine.compute_stability(window_size=3)
    print(f"Computed System Stability: {stability:.4f}")
    
    # Check Reducibility
    reducibility = engine.compute_reducibility()
    print(f"Computed System Reducibility: {reducibility:.4f}")
    
    # Expected results for Day 5 Heatwave (Synthetic)
    # Since we can't easily iterate time segments in the base engine, we look at global metrics
    if stability < 0.6:
        print("PASS: System detected high volatility (Manifold Tear potential).")
    else:
        print("FAIL: Stability metric too high for extreme heatwave scenario.")

def verify_agri_asi_logic():
    print("\n--- Audit: Agriculture ASI End-to-End Logic ---")
    agri = AgriIntelligence()
    report = agri.generate_farmer_report(plot_id="Field_001")
    
    print(f"Report Generated: {report['Title']}")
    print(f"Diagnosis: {report['Health_Audit']['Diagnosis']} (Severity: {report['Health_Audit']['Severity']})")
    print(f"Yield Prediction: {report['Intelligence_Forecast']['Predicted_Yield']}")
    print(f"Weather Risk: {report['Intelligence_Forecast']['Weather_Alert']}")
    
    # Validations
    if report["Health_Audit"]["Diagnosis"] == "Gray Leaf Spot":
        print("PASS: CropVision correctly identified corn disease.")
    if "Manifold Tear" in report["Intelligence_Forecast"]["Weather_Alert"]:
        print("PASS: Yield prediction correctly coupled with environmental manifold tear.")
    if "ROI" in report["Prescription"]["Economic_Alternative"]:
        print("PASS: Economic optimization prioritized ROI.")

if __name__ == "__main__":
    verify_weather_manifold_tear()
    verify_agri_asi_logic()
