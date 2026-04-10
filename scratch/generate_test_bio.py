import pandas as pd
import os

def generate_bio_test_data():
    os.makedirs("reports", exist_ok=True)
    
    # 🧬 A. DNA SEQUENCE TEST DATA
    dna_data = {
        "ID": ["S1", "S2", "S3", "S4", "S5", "S6"],
        "Seq_A": [12, 11, 5, 6, 13, 4],
        "Seq_T": [8, 9, 15, 14, 7, 16],
        "Seq_G": [15, 14, 6, 7, 16, 5],
        "Seq_C": [10, 11, 18, 17, 9, 19],
        "Mutation_Score": [0.10, 0.12, 0.85, 0.80, 0.08, 0.90],
        "Expression_Level": [0.80, 0.78, 0.30, 0.35, 0.82, 0.25]
    }
    pd.DataFrame(dna_data).to_csv("reports/dna_sequence_test.csv", index=False)
    
    # 🧬 B. PROTEIN FEATURE SPACE
    protein_data = {
        "Protein": ["P1", "P2", "P3", "P4", "P5"],
        "Hydrophobicity": [0.8, 0.75, 0.2, 0.25, 0.85],
        "Charge": [0.2, 0.25, 0.7, 0.65, 0.15],
        "Mass": [50, 52, 60, 58, 49],
        "Flexibility": [0.3, 0.35, 0.8, 0.75, 0.25],
        "Binding_Affinity": [0.9, 0.88, 0.3, 0.35, 0.92]
    }
    pd.DataFrame(protein_data).to_csv("reports/protein_features_test.csv", index=False)
    
    # 💊 C. DRUG-TARGET SIMULATION DATA
    drug_data = {
        "Drug": ["D1", "D2", "D3", "D4", "D5"],
        "Target_Protein": ["P1", "P2", "P3", "P4", "P1"],
        "Binding_Score": [0.9, 0.88, 0.4, 0.35, 0.92],
        "Toxicity_Index": [0.1, 0.12, 0.7, 0.75, 0.08],
        "Selectivity": [0.85, 0.80, 0.30, 0.25, 0.90]
    }
    pd.DataFrame(drug_data).to_csv("reports/drug_test.csv", index=False)
    
    print("Test data generated successfully.")

if __name__ == "__main__":
    generate_bio_test_data()
