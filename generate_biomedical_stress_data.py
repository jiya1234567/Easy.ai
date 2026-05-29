import json
import os
import numpy as np

# Ensure directory exists
output_dir = "data/biomedical_stress_cohorts"
os.makedirs(output_dir, exist_ok=True)

def generate_patient(patient_id, disease_type):
    """
    Generates a multimodal longitudinal patient trajectory based on disease type.
    """
    # Timeline states mapping
    if disease_type == "Breast Cancer":
        timeline = [{"t": 1, "state": "stable"}, {"t": 2, "state": "adaptive"}, {"t": 3, "state": "clonal_expansion"}, {"t": 4, "state": "critical_transition"}]
        labs = {"CRP": round(np.random.normal(5.0, 1.0), 1), "CA15_3": round(np.random.normal(35.0, 5.0), 1)}
        genomics = {"BRCA1": 1, "TP53": int(np.random.choice([0, 1])), "PIK3CA": 1, "PRS_score": round(np.random.uniform(0.8, 0.99), 2)}
        imaging = {"tumor_density": round(np.random.uniform(0.6, 0.9), 2), "vascularity": round(np.random.uniform(0.5, 0.8), 2)}
        entropy = round(np.random.uniform(0.7, 0.95), 2)
        coherence = round(np.random.uniform(0.1, 0.3), 2)
        reducibility = round(np.random.uniform(0.05, 0.2), 2) # Irreducible
    elif disease_type == "Cardiovascular":
        timeline = [{"t": 1, "state": "stable"}, {"t": 2, "state": "inflammation"}, {"t": 3, "state": "plaque_instability"}, {"t": 4, "state": "critical_transition"}]
        labs = {"LDL": round(np.random.normal(160, 20), 1), "CRP": round(np.random.normal(8.0, 2.0), 1)}
        genomics = {"APOE": 1, "PCSK9": int(np.random.choice([0, 1])), "PRS_score": round(np.random.uniform(0.7, 0.9), 2)}
        imaging = {"arterial_calcification": round(np.random.uniform(0.5, 0.85), 2), "plaque_vulnerability": round(np.random.uniform(0.6, 0.9), 2)}
        entropy = round(np.random.uniform(0.5, 0.75), 2)
        coherence = round(np.random.uniform(0.3, 0.6), 2)
        reducibility = round(np.random.uniform(0.3, 0.6), 2) # Hybrid
    elif disease_type == "Diabetes":
        timeline = [{"t": 1, "state": "stable"}, {"t": 2, "state": "insulin_resistance"}, {"t": 3, "state": "metabolic_tipping"}, {"t": 4, "state": "critical_transition"}]
        labs = {"HbA1c": round(np.random.normal(7.5, 0.8), 1), "FastingGlucose": round(np.random.normal(130, 15), 1)}
        genomics = {"TCF7L2": 1, "PRS_score": round(np.random.uniform(0.6, 0.85), 2)}
        imaging = {"hepatic_fat": round(np.random.uniform(0.3, 0.7), 2), "pancreatic_volume": round(np.random.uniform(0.4, 0.8), 2)}
        entropy = round(np.random.uniform(0.6, 0.85), 2)
        coherence = round(np.random.uniform(0.2, 0.5), 2)
        reducibility = round(np.random.uniform(0.1, 0.4), 2) # Irreducible
    else: # Prostate / Colorectal
        timeline = [{"t": 1, "state": "stable"}, {"t": 2, "state": "adaptive"}, {"t": 3, "state": "unstable"}, {"t": 4, "state": "critical_transition"}]
        labs = {"TumorMarker": round(np.random.normal(10.0, 2.0), 1)}
        genomics = {"KRAS": 1, "PRS_score": round(np.random.uniform(0.5, 0.9), 2)}
        imaging = {"lesion_size": round(np.random.uniform(0.2, 0.6), 2)}
        entropy = round(np.random.uniform(0.6, 0.9), 2)
        coherence = round(np.random.uniform(0.2, 0.5), 2)
        reducibility = round(np.random.uniform(0.2, 0.5), 2)

    return {
        "state_tensor": {
            "patient_id": patient_id,
            "timepoint": "t4",
            "entropy_H": entropy,
            "coherence_k": coherence,
            "emergence_eta": round(np.random.uniform(0.5, 0.9), 2),
            "bifurcation_B": round(np.random.uniform(0.7, 0.95), 2),
            "reducibility_R": reducibility
        },
        "multimodal_features": {
            "genomics": genomics,
            "labs": labs,
            "imaging": imaging
        },
        "temporal_trajectory": {
            "timeline": timeline
        }
    }

if __name__ == "__main__":
    print("Generating OMEGA Biomedical Stress Test Cohorts...")
    np.random.seed(42)

    cohorts = {
        "Cardiovascular": [],
        "Diabetes": [],
        "Breast Cancer": [],
        "Prostate Cancer": [],
        "Colorectal Cancer": []
    }

    # Generate 50 patients per cohort
    for disease in cohorts.keys():
        for i in range(50):
            pid = f"{disease[:2].upper()}_{str(i).zfill(3)}"
            cohorts[disease].append(generate_patient(pid, disease))
            
    # Save cohorts to JSON
    for disease, patients in cohorts.items():
        filename = disease.replace(" ", "_").lower() + "_cohort.json"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w") as f:
            json.dump(patients, f, indent=2)
        print(f"Generated: {filepath} ({len(patients)} patients)")

    print("✅ All Biomedical Stress Test Data Generated Successfully.")
