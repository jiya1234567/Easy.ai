import pandas as pd
import numpy as np
import os

class HealthInsuranceEngine:
    def __init__(self, data_dir="reports"):
        self.data_dir = data_dir
        self.family_test_path = os.path.join(data_dir, "health_family_test.csv")
        self.biomarker_test_path = os.path.join(data_dir, "health_biomarker_test.csv")
        self.accident_test_path = os.path.join(data_dir, "health_accident_test.csv")
        self.family_cost_test_path = os.path.join(data_dir, "health_family_cost_test.csv")

    def load_family_data(self):
        if os.path.exists(self.family_test_path):
            return pd.read_csv(self.family_test_path)
        return pd.DataFrame()

    def load_biomarker_data(self):
        if os.path.exists(self.biomarker_test_path):
            return pd.read_csv(self.biomarker_test_path)
        return pd.DataFrame()

    def load_accident_data(self):
        if os.path.exists(self.accident_test_path):
            return pd.read_csv(self.accident_test_path)
        return pd.DataFrame()

    def load_family_cost_data(self):
        if os.path.exists(self.family_cost_test_path):
            return pd.read_csv(self.family_cost_test_path)
        return pd.DataFrame()

    def evaluate_family_risk(self, row):
        # High Risk Logic
        if row.get('Retinal_Diabetic_Risk', 0) > 0.70 or \
           row.get('Heart_Risk', 0) > 0.65 or \
           row.get('Hospital_Visits', 0) >= 2 or \
           row.get('Medication_Count', 0) >= 3:
            return "Keep hospital cover and diabetes-related extras."
        # Low Risk with High Financial Stress
        elif row.get('Financial_Stress', 0) > 0.80:
            return "Recommend reduce or remove expensive extras cover."
        else:
            return "Recommend basic hospital-only policy."

    def evaluate_biomarker_risk(self, row):
        abnormal_count = 0
        
        # High Risk conditions
        if row.get('HbA1c', 0) > 6.5 or \
           row.get('eGFR', 100) < 60 or \
           row.get('Retinal_Diabetic_Risk', 0) > 0.70 or \
           row.get('Smartwatch_Heart_Risk', 0) > 0.65 or \
           row.get('CRP', 0) > 10 or \
           row.get('Systolic_BP', 0) > 150:
            return "HIGH RISK if any critical marker is abnormal."

        # Medium Risk logic (mild abnormalities)
        if 5.7 <= row.get('HbA1c', 0) <= 6.5:
            abnormal_count += 1
        if 60 <= row.get('eGFR', 100) <= 90:
            abnormal_count += 1
        if 0.3 <= row.get('Retinal_Diabetic_Risk', 0) <= 0.70:
            abnormal_count += 1
        if 0.3 <= row.get('Smartwatch_Heart_Risk', 0) <= 0.65:
            abnormal_count += 1
        if 3 <= row.get('CRP', 0) <= 10:
            abnormal_count += 1
        if 130 <= row.get('Systolic_BP', 0) <= 150:
            abnormal_count += 1
            
        if abnormal_count >= 2:
            return "MEDIUM RISK if 2 or more markers are mildly abnormal."
            
        return "LOW RISK only if nearly all markers remain in the normal range."
    
    def evaluate_accident_cover(self, row):
        # Recommendation logic for accident-only insurance based on biomarkers
        if row.get('HbA1c', 0) > 7.0 or row.get('eGFR', 100) < 60 or row.get('Systolic_BP', 0) > 150 or row.get('Retinal_Risk', 0) > 0.70:
            return "CRITICAL: Full insurance and specialist care required"
        elif row.get('HbA1c', 0) >= 6.0 or row.get('Retinal_Risk', 0) > 0.4:
            return "WARNING: Keep accident cover but add GP monitoring"
        elif row.get('HbA1c', 0) >= 5.7 or row.get('Retinal_Risk', 0) > 0.15:
            return "WATCH: App alerts every 3 months"
        else:
            return "SAFE: Accident-only cover sufficient"
