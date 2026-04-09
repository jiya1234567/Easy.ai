import pandas as pd
import numpy as np
import os
import json

def generate_cancer_bio_data(n_patients=150, n_genes=1000):
    """
    Generates synthetic RNA-seq expression data for cancer patients.
    Clusters patients into response-types for different Chemo agents.
    """
    np.random.seed(42)
    
    # 1. Define Chemo Agents (The 'Assets')
    agents = ['Paclitaxel', 'Cisplatin', 'Doxorubicin', 'Gemcitabine', '5-FU']
    
    # 2. Create Base Expression (Mean levels)
    # Most genes are at baseline
    genes = [f"GENE_{i:04d}" for i in range(n_genes)]
    
    # 3. Create Patient Profiles
    # We'll create 3 distinct 'Biological Regimes' (Subtypes)
    patient_ids = [f"PATIENT_{i:03d}" for i in range(n_patients)]
    
    data = np.random.lognormal(2, 0.5, (n_patients, n_genes))
    
    # Induce specific 'pathways' (clusters)
    for i in range(n_patients):
        if i % 3 == 0: # Cluster 0: Sensitive to Paclitaxel
            data[i, 0:50] *= 5.0  # Overexpress markers for group 0
        elif i % 3 == 1: # Cluster 1: Sensitive to Cisplatin
            data[i, 50:100] *= 0.2 # Underexpress suppressors for group 1
        else: # Cluster 2: Multi-Drug Resistant
            data[i, 100:150] *= 3.0
            
    df = pd.DataFrame(data, index=patient_ids, columns=genes)
    
    # Metadata: Mapping what 'Type' each patient is (equivalent to Asset Type)
    # In finance we transpose (Assets are samples), here Patients are samples.
    # To use ScientificEngine, we want to analyze relationship between AGENTS (Treatments).
    # So we'll treat Agents as 'Assets' and Patients as 'Time'.
    
    # Let's create Agent Response vectors over the patients
    agent_responses = {}
    for agent in agents:
        # Base response
        base = np.random.normal(0.01, 0.005, n_patients)
        if agent == 'Paclitaxel':
            # High efficiency on Cluster 0
            base[::3] += 0.05
        elif agent == 'Cisplatin':
            base[1::3] += 0.04
            
        # Prices (Cumulative Efficacy / Survival Probability)
        agent_responses[agent] = 100 * np.exp(np.cumsum(base))
        
    df_agents = pd.DataFrame(agent_responses, index=pd.date_range(end='2026-04-08', periods=n_patients, freq='D'))
    
    metadata = {agent: 'Chemo-Agent' for agent in agents}
    
    return df_agents, metadata

if __name__ == "__main__":
    print("Generating High-Fidelity Cancer Bio-Manifold Data...")
    df, meta = generate_cancer_bio_data()
    
    os.makedirs("reports", exist_ok=True)
    df.to_csv("reports/cancer_bio_data.csv")
    
    # Update asset_metadata to include bio-agents if health domain is used
    with open("reports/bio_metadata.json", "w") as f:
        json.dump(meta, f, indent=2)
        
    print("Bio-Data saved to reports/cancer_bio_data.csv")
