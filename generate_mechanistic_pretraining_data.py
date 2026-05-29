import os
import pandas as pd
import numpy as np

# Ensure directory exists
output_dir = "data/mechanistic_pretraining"
os.makedirs(output_dir, exist_ok=True)

def generate_reducible_trajectory(n_steps=1000):
    """
    Simulates a Reducible system (e.g. Orbital Mechanics, Simple Circuits)
    Highly predictable, low entropy, constant coherence, zero emergence.
    """
    t = np.linspace(0, 10, n_steps)
    
    # Simple harmonic oscillator behavior
    entropy_H = np.random.normal(0.1, 0.01, n_steps)  # Low disorder
    coherence_k = 0.9 + np.sin(t) * 0.05             # High synchronization
    emergence_eta = np.zeros(n_steps)                # No emergence
    bifurcation_B = np.zeros(n_steps)                # No tipping points
    
    # Reducibility score is near 1.0 (highly compressible/predictable)
    reducibility_score = 0.95 + np.random.normal(0, 0.01, n_steps)
    
    return pd.DataFrame({
        "timestep": np.arange(n_steps),
        "state_id": ["STABLE_ORBIT"] * n_steps,
        "entropy_H": entropy_H,
        "coherence_k": coherence_k,
        "emergence_eta": emergence_eta,
        "bifurcation_B": bifurcation_B,
        "reducibility_score": np.clip(reducibility_score, 0, 1)
    })

def generate_irreducible_transition(n_steps=1000):
    """
    Simulates an Irreducible system undergoing a phase transition 
    (e.g., Normal Tissue -> Hypoxia -> Tumor Emergence -> Metastasis).
    """
    t = np.linspace(0, 10, n_steps)
    df = pd.DataFrame()
    df["timestep"] = np.arange(n_steps)
    
    # Phase 1: Normal State (t=0 to t=300)
    # Phase 2: Perturbation / Hypoxia (t=300 to t=600)
    # Phase 3: Bifurcation / Tumor Emergence (t=600 to t=1000)
    
    state_id = []
    entropy_H = []
    coherence_k = []
    emergence_eta = []
    bifurcation_B = []
    reducibility_score = []
    
    for i in range(n_steps):
        if i < 300:
            state_id.append("NORMAL_STATE")
            entropy_H.append(np.random.normal(0.2, 0.02))
            coherence_k.append(np.random.normal(0.8, 0.05))
            emergence_eta.append(0.0)
            bifurcation_B.append(0.05)
            reducibility_score.append(0.8) # Somewhat predictable
        elif i < 600:
            state_id.append("PERTURBATION_HYPOXIA")
            # Entropy rises as system destabilizes
            entropy_H.append(np.random.normal(0.5, 0.1) + (i-300)*0.001)
            # Coherence drops as normal syncing fails
            coherence_k.append(np.random.normal(0.5, 0.1) - (i-300)*0.001)
            emergence_eta.append(np.random.normal(0.2, 0.05))
            bifurcation_B.append(np.random.normal(0.6, 0.1)) # Approaching tipping point
            reducibility_score.append(0.4) # Harder to predict
        else:
            state_id.append("EMERGENT_TUMOR_STATE")
            # Entropy stabilizes at a higher state
            entropy_H.append(np.random.normal(0.7, 0.05))
            # New pathogenic coherence emerges
            coherence_k.append(np.random.normal(0.9, 0.02))
            # High emergence metric
            emergence_eta.append(np.random.normal(0.9, 0.05))
            # Past the bifurcation
            bifurcation_B.append(0.95)
            reducibility_score.append(0.1) # Totally irreducible, requires step-by-step
            
    df["state_id"] = state_id
    df["entropy_H"] = entropy_H
    df["coherence_k"] = coherence_k
    df["emergence_eta"] = emergence_eta
    df["bifurcation_B"] = bifurcation_B
    df["reducibility_score"] = reducibility_score
    
    return df

def generate_irreducible_cyber(n_steps=1000):
    """
    Simulates a Cybersecurity zero-day exploit propagation.
    Sudden loss of coherence and massive entropy spike.
    """
    t = np.linspace(0, 10, n_steps)
    df = pd.DataFrame({"timestep": np.arange(n_steps)})
    
    state_id = []
    entropy_H = []
    coherence_k = []
    emergence_eta = []
    bifurcation_B = []
    reducibility_score = []
    
    for i in range(n_steps):
        if i < 400: # Normal network traffic
            state_id.append("NORMAL_TRAFFIC")
            entropy_H.append(np.random.normal(0.1, 0.01))
            coherence_k.append(np.random.normal(0.95, 0.01))
            emergence_eta.append(0.0)
            bifurcation_B.append(0.0)
            reducibility_score.append(0.9)
        elif i < 500: # Zero-day injected, spreading
            state_id.append("ZERO_DAY_PROPAGATION")
            entropy_H.append(np.random.normal(0.6, 0.2)) # Massive noise
            coherence_k.append(np.random.normal(0.4, 0.1)) # Desync of auth servers
            emergence_eta.append(np.random.normal(0.4, 0.1))
            bifurcation_B.append(np.random.normal(0.8, 0.1))
            reducibility_score.append(0.2)
        else: # Full network collapse / botnet emergence
            state_id.append("BOTNET_EMERGENCE")
            entropy_H.append(np.random.normal(0.8, 0.05))
            coherence_k.append(np.random.normal(0.8, 0.02)) # Malicious coherence
            emergence_eta.append(np.random.normal(0.95, 0.02))
            bifurcation_B.append(1.0)
            reducibility_score.append(0.05) # Total chaos
            
    df["state_id"] = state_id
    df["entropy_H"] = entropy_H
    df["coherence_k"] = coherence_k
    df["emergence_eta"] = emergence_eta
    df["bifurcation_B"] = bifurcation_B
    df["reducibility_score"] = reducibility_score
    return df

def generate_irreducible_city(n_steps=1000):
    """
    Simulates a Smart City power grid cascading failure.
    """
    df = pd.DataFrame({"timestep": np.arange(n_steps)})
    state_id, entropy_H, coherence_k, emergence_eta, bifurcation_B, reducibility_score = [], [], [], [], [], []
    
    for i in range(n_steps):
        if i < 700: # Grid stable
            state_id.append("GRID_STABLE")
            entropy_H.append(np.random.normal(0.15, 0.02))
            coherence_k.append(np.random.normal(0.9, 0.02))
            emergence_eta.append(0.0)
            bifurcation_B.append(0.1)
            reducibility_score.append(0.85)
        else: # Cascading failure
            state_id.append("CASCADING_FAILURE")
            entropy_H.append(np.random.normal(0.9, 0.1)) # Max entropy
            coherence_k.append(np.random.normal(0.1, 0.1)) # Zero sync (blackout)
            emergence_eta.append(np.random.normal(0.1, 0.05))
            bifurcation_B.append(1.0)
            reducibility_score.append(0.0)
            
    df["state_id"] = state_id
    df["entropy_H"] = entropy_H
    df["coherence_k"] = coherence_k
    df["emergence_eta"] = emergence_eta
    df["bifurcation_B"] = bifurcation_B
    df["reducibility_score"] = reducibility_score
    return df

if __name__ == "__main__":
    print("Generating Mechanistic Pretraining Datasets...")
    
    # 1. Generate Reducible Orbit Dataset
    reducible_df = generate_reducible_trajectory(1000)
    path_red = os.path.join(output_dir, "pretrain_reducible_orbit.csv")
    reducible_df.to_csv(path_red, index=False)
    print(f"Generated: {path_red}")
    
    # 2. Generate Irreducible Tumor Dataset
    irreducible_df = generate_irreducible_transition(1000)
    path_irr = os.path.join(output_dir, "pretrain_irreducible_tumor.csv")
    irreducible_df.to_csv(path_irr, index=False)
    print(f"Generated: {path_irr}")

    # 3. Generate Cyber Dataset
    cyber_df = generate_irreducible_cyber(1000)
    path_cyb = os.path.join(output_dir, "pretrain_irreducible_cyber.csv")
    cyber_df.to_csv(path_cyb, index=False)
    print(f"Generated: {path_cyb}")

    # 4. Generate City Dataset
    city_df = generate_irreducible_city(1000)
    path_cit = os.path.join(output_dir, "pretrain_irreducible_city.csv")
    city_df.to_csv(path_cit, index=False)
    print(f"Generated: {path_cit}")
    
    print("\nPretraining Data Ready. Structure conforms to:")
    print("timestep | state_id | entropy_H | coherence_k | emergence_eta | bifurcation_B | reducibility_score")
