"""
generate_omega_causal_stress_suite.py
OMEGA-CORE | Causal Transition Stress-Test Suite
Generates 10 high-fidelity CSV datasets modeling continuous mechanistic state transitions under perturbation.
"""
import os
import numpy as np
import pandas as pd

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def generate_suite():
    print("=" * 70)
    print("  OMEGA-CORE | Causal Stress-Test Dataset Suite Generator")
    print("=" * 70)
    
    data_dir = "data/causal_stress_suite"
    ensure_dir(data_dir)
    np.random.seed(42)
    timesteps = 50
    t = np.linspace(0, 1, timesteps)
    
    # ----------------------------------------------------
    # 1. ONCOLOGY EVOLUTION (synthetic_clonal_evolution.csv)
    # ----------------------------------------------------
    print("Generating Oncology Evolution Dataset...")
    # Phased variables: Stable (t: 0-10) -> Mutation (10-20) -> Hypoxia (20-30) -> Drug (30-40) -> Resistance (40-50)
    kras = np.concatenate([np.zeros(10), np.linspace(0, 0.9, 10), np.ones(30)*0.95]) + np.random.normal(0, 0.02, timesteps)
    tp53 = np.concatenate([np.zeros(15), np.linspace(0, 1.0, 15), np.ones(20)]) + np.random.normal(0, 0.02, timesteps)
    oxygen = np.concatenate([np.ones(20)*95.0, np.linspace(95.0, 15.0, 15), np.ones(15)*12.0]) + np.random.normal(0, 1.0, timesteps)
    glucose = np.concatenate([np.ones(10)*5.0, np.linspace(5.0, 45.0, 20), np.ones(20)*48.0]) + np.random.normal(0, 0.8, timesteps)
    immune = np.concatenate([np.ones(15)*80.0, np.linspace(80.0, 10.0, 20), np.ones(15)*8.0]) + np.random.normal(0, 1.5, timesteps)
    therapy = np.concatenate([np.zeros(30), np.linspace(0, 100.0, 10), np.ones(10)*100.0])
    
    # Thermodynamic Metrics
    entropy = np.concatenate([np.ones(10)*0.15, np.linspace(0.15, 0.88, 25), np.linspace(0.88, 0.45, 15)]) + np.random.normal(0, 0.01, timesteps)
    coherence = np.concatenate([np.ones(10)*0.92, np.linspace(0.92, 0.22, 25), np.linspace(0.22, 0.76, 15)]) + np.random.normal(0, 0.01, timesteps)
    emergence = 1.0 - entropy
    bifurcation = np.concatenate([np.zeros(15), np.linspace(0.0, 0.94, 20), np.linspace(0.94, 0.15, 15)])
    reducibility = np.concatenate([np.ones(15)*0.95, np.linspace(0.95, 0.12, 20), np.ones(15)*0.15])
    
    clone_entropy = entropy * 8.0
    resistance_score = np.concatenate([np.zeros(35), np.linspace(0, 95.0, 15)]) + np.random.normal(0, 1.0, timesteps)
    
    onc_df = pd.DataFrame({
        "timestep": [f"t{i+1}" for i in range(timesteps)],
        "state_id": ["Stable"]*10 + ["Mutation"]*10 + ["Hypoxia"]*10 + ["Therapeutic_Pressure"]*10 + ["Resistance_Attractor"]*10,
        "entropy_H": np.clip(entropy, 0, 1),
        "coherence_k": np.clip(coherence, 0, 1),
        "emergence_eta": np.clip(emergence, 0, 1),
        "bifurcation_B": np.clip(bifurcation, 0, 1),
        "reducibility_score": np.clip(reducibility, 0, 1),
        "perturbation": ["None"]*20 + ["Oxygen_Depletion"]*10 + ["Chemotherapy"]*10 + ["Resistance_Escape"]*10,
        "response": ["Homeostasis"]*10 + ["Clonal_Expansion"]*10 + ["Warburg_Shift"]*10 + ["Apoptosis_Attempt"]*10 + ["Pathway_Adaptation"]*10,
        "attractor_state": ["Basal_Homeostasis"]*20 + ["Hypoxic_Niche"]*15 + ["Apoptotic_Collapse"]*5 + ["Clonal_Resistance_Attractor"]*10,
        "KRAS_activation": np.clip(kras, 0, 1),
        "TP53_loss": np.clip(tp53, 0, 1),
        "oxygen_level": np.clip(oxygen, 0, 100),
        "glucose_flux": glucose,
        "immune_pressure": np.clip(immune, 0, 100),
        "therapy_dose": therapy,
        "clone_entropy": np.clip(clone_entropy, 0, 10),
        "resistance_score": np.clip(resistance_score, 0, 100)
    })
    onc_df.to_csv(f"{data_dir}/synthetic_clonal_evolution.csv", index=False)

    # ----------------------------------------------------
    # 2. WEATHER TIPPING (synthetic_cyclone_transition.csv)
    # ----------------------------------------------------
    print("Generating Weather Tipping Dataset...")
    # Calm ocean (0-15) -> Storm emergence (15-30) -> Cyclone lock-in (30-45) -> Chaotic turbulence (45-50)
    press = np.concatenate([np.ones(15)*1013.0, np.linspace(1013.0, 960.0, 20), np.linspace(960.0, 940.0, 15)]) + np.random.normal(0, 1.0, timesteps)
    sst = np.concatenate([np.ones(15)*26.0, np.linspace(26.0, 31.5, 20), np.ones(15)*31.8]) + np.random.normal(0, 0.1, timesteps)
    shear = np.concatenate([np.ones(15)*45.0, np.linspace(45.0, 5.0, 20), np.ones(15)*3.2]) + np.random.normal(0, 0.5, timesteps)
    humidity = np.concatenate([np.ones(15)*60.0, np.linspace(60.0, 98.0, 20), np.ones(15)*99.0]) + np.random.normal(0, 0.8, timesteps)
    
    entropy = np.concatenate([np.ones(15)*0.12, np.linspace(0.12, 0.88, 20), np.ones(15)*0.92]) + np.random.normal(0, 0.01, timesteps)
    coherence = np.concatenate([np.ones(15)*0.10, np.linspace(0.10, 0.94, 20), np.ones(15)*0.96]) + np.random.normal(0, 0.01, timesteps)
    emergence = coherence * 0.95
    bifurcation = np.concatenate([np.zeros(12), np.linspace(0.0, 0.98, 18), np.ones(20)*0.10])
    reducibility = np.concatenate([np.ones(15)*0.92, np.linspace(0.92, 0.08, 20), np.ones(15)*0.05])
    
    wea_df = pd.DataFrame({
        "timestep": [f"t{i+1}" for i in range(timesteps)],
        "state_id": ["Calm"]*15 + ["Storm_Emergence"]*15 + ["Cyclone_LockIn"]*15 + ["Turbulence"]*5,
        "entropy_H": np.clip(entropy, 0, 1),
        "coherence_k": np.clip(coherence, 0, 1),
        "emergence_eta": np.clip(emergence, 0, 1),
        "bifurcation_B": np.clip(bifurcation, 0, 1),
        "reducibility_score": np.clip(reducibility, 0, 1),
        "perturbation": ["None"]*15 + ["Ocean_Thermal_Spike"]*20 + ["Wind_Shear_Collapse"]*15,
        "response": ["Equilibrium"]*15 + ["Vortex_Aggregation"]*20 + ["Rotational_Ignition"]*15,
        "attractor_state": ["Flat_Baric"]*15 + ["Vortex_Tipping"]*15 + ["Stable_Cyclonic_Eye"]*20,
        "pressure_gradient": press,
        "sea_surface_temp": sst,
        "wind_shear": shear,
        "humidity_flux": humidity,
        "vortex_coherence": np.clip(coherence, 0, 1)
    })
    wea_df.to_csv(f"{data_dir}/synthetic_cyclone_transition.csv", index=False)

    # ----------------------------------------------------
    # 3. STOCK MARKET CASCADE (synthetic_flash_crash.csv)
    # ----------------------------------------------------
    print("Generating Stock Market Cascade Dataset...")
    # Stable (0-20) -> Volatility Increase (20-35) -> Feedback Cascade (35-45) -> Crash Isolation (45-50)
    liquidity = np.concatenate([np.ones(20)*100.0, np.linspace(100.0, 10.0, 20), np.ones(10)*2.0]) + np.random.normal(0, 1.0, timesteps)
    volatility = np.concatenate([np.ones(20)*8.0, np.linspace(8.0, 85.0, 20), np.ones(10)*14.0]) + np.random.normal(0, 0.5, timesteps)
    leverage = np.concatenate([np.ones(20)*1.5, np.linspace(1.5, 4.5, 20), np.ones(10)*1.1]) + np.random.normal(0, 0.05, timesteps)
    panic = np.concatenate([np.zeros(20), np.linspace(0.0, 95.0, 20), np.ones(10)*20.0]) + np.random.normal(0, 1.0, timesteps)
    flow = np.concatenate([np.zeros(20), np.linspace(0.0, -1000.0, 20), np.zeros(10)]) + np.random.normal(0, 50.0, timesteps)
    
    entropy = np.concatenate([np.ones(20)*0.25, np.linspace(0.25, 0.94, 20), np.ones(10)*0.15]) + np.random.normal(0, 0.01, timesteps)
    coherence = np.concatenate([np.ones(20)*0.18, np.linspace(0.18, 0.98, 20), np.ones(10)*0.12]) + np.random.normal(0, 0.01, timesteps)
    emergence = coherence * 0.92
    bifurcation = np.concatenate([np.zeros(18), np.linspace(0.0, 0.99, 18), np.ones(14)*0.02])
    reducibility = np.concatenate([np.ones(20)*0.85, np.linspace(0.85, 0.05, 20), np.ones(10)*0.92])
    
    mkt_df = pd.DataFrame({
        "timestep": [f"t{i+1}" for i in range(timesteps)],
        "state_id": ["Stable"]*20 + ["Volatility_Rise"]*15 + ["Feedback_Cascade"]*10 + ["Crash_Isolation"]*5,
        "entropy_H": np.clip(entropy, 0, 1),
        "coherence_k": np.clip(coherence, 0, 1),
        "emergence_eta": np.clip(emergence, 0, 1),
        "bifurcation_B": np.clip(bifurcation, 0, 1),
        "reducibility_score": np.clip(reducibility, 0, 1),
        "perturbation": ["None"]*20 + ["Liquidity_Drain"]*15 + ["Margin_Call_Cascade"]*15,
        "response": ["Equilibrium"]*20 + ["Order_Imbalance"]*15 + ["Algorithmic_Selloff"]*15,
        "attractor_state": ["Stable_Trading"]*20 + ["Volatility_Attractor"]*15 + ["Panic_Attractor"]*15,
        "liquidity": np.clip(liquidity, 0, 100),
        "volatility": np.clip(volatility, 0, 100),
        "leverage": np.clip(leverage, 0, 10),
        "panic_index": np.clip(panic, 0, 100),
        "order_flow": flow
    })
    mkt_df.to_csv(f"{data_dir}/synthetic_flash_crash.csv", index=False)

    # ----------------------------------------------------
    # 4. NEURAL SYNCHRONIZATION (synthetic_neural_sync.csv)
    # ----------------------------------------------------
    print("Generating Neural Synchronization Dataset...")
    # Noise (0-12) -> Partial sync (12-25) -> Global ignition (25-40) -> Desynchronization (40-50)
    firing = np.concatenate([np.ones(12)*12.0, np.linspace(12.0, 95.0, 25), np.linspace(95.0, 5.0, 13)]) + np.random.normal(0, 1.0, timesteps)
    calcium = np.concatenate([np.ones(12)*1.2, np.linspace(1.2, 8.5, 25), np.linspace(8.5, 0.4, 13)]) + np.random.normal(0, 0.1, timesteps)
    sync = np.concatenate([np.ones(12)*0.08, np.linspace(0.08, 0.96, 25), np.ones(13)*0.05]) + np.random.normal(0, 0.01, timesteps)
    balance = np.concatenate([np.ones(12)*1.0, np.linspace(1.0, 0.1, 20), np.linspace(0.1, 2.5, 18)]) + np.random.normal(0, 0.05, timesteps)
    freq = np.concatenate([np.ones(12)*4.0, np.linspace(4.0, 42.0, 25), np.ones(13)*2.0]) + np.random.normal(0, 0.2, timesteps)
    
    entropy = np.concatenate([np.ones(12)*0.88, np.linspace(0.88, 0.12, 25), np.ones(13)*0.95]) + np.random.normal(0, 0.01, timesteps)
    coherence = sync
    emergence = 1.0 - entropy
    bifurcation = np.concatenate([np.zeros(10), np.linspace(0.0, 0.95, 15), np.linspace(0.95, 0.0, 25)])
    reducibility = np.concatenate([np.ones(12)*0.12, np.linspace(0.12, 0.85, 25), np.ones(13)*0.08])
    
    neu_df = pd.DataFrame({
        "timestep": [f"t{i+1}" for i in range(timesteps)],
        "state_id": ["Noise"]*12 + ["Partial_Sync"]*13 + ["Global_Ignition"]*15 + ["Desync"]*10,
        "entropy_H": np.clip(entropy, 0, 1),
        "coherence_k": np.clip(coherence, 0, 1),
        "emergence_eta": np.clip(emergence, 0, 1),
        "bifurcation_B": np.clip(bifurcation, 0, 1),
        "reducibility_score": np.clip(reducibility, 0, 1),
        "perturbation": ["None"]*12 + ["Calcium_Spike"]*23 + ["GABA_Inhibition_Loss"]*15,
        "response": ["Quiescence"]*12 + ["Oscillatory_Rhythm"]*23 + ["Spike_Discharge"]*15,
        "attractor_state": ["Stochastic_Noise"]*12 + ["Oscillatory_Attractor"]*23 + ["Global_Ignition_Lock"]*15,
        "neuron_firing_rate": np.clip(firing, 0, 200),
        "calcium_flux": np.clip(calcium, 0, 20),
        "synchronization": np.clip(sync, 0, 1),
        "inhibitory_balance": np.clip(balance, 0, 5),
        "oscillation_frequency": np.clip(freq, 0, 100)
    })
    neu_df.to_csv(f"{data_dir}/synthetic_neural_sync.csv", index=False)

    # ----------------------------------------------------
    # 5. MOLECULAR PHYSICS (synthetic_binding_dynamics.csv)
    # ----------------------------------------------------
    print("Generating Molecular Physics Dataset...")
    # Follow physical constraints: Delta G, conformational state
    ligand = np.linspace(1e-6, 1e-3, timesteps)
    kd = 1e-4
    fractional_occupancy = ligand / (ligand + kd)
    
    delta_g = -8.314 * 298.15 * np.log(ligand / kd + 1e-9)
    conformational_state = fractional_occupancy * 0.95
    thermal_noise = np.random.normal(0, 0.05, timesteps)
    
    entropy = 1.0 - fractional_occupancy
    coherence = fractional_occupancy
    emergence = fractional_occupancy * 0.85
    bifurcation = 1.0 - np.abs(fractional_occupancy - 0.5)*2 # Maximum instability near Kd midpoint!
    reducibility = np.ones(timesteps) * 0.98  # Highly reducible, compressible analytical kinetics!
    
    mol_df = pd.DataFrame({
        "timestep": [f"t{i+1}" for i in range(timesteps)],
        "state_id": ["Unbound"]*15 + ["Transitioning"]*20 + ["Fully_Bound"]*15,
        "entropy_H": np.clip(entropy, 0, 1),
        "coherence_k": np.clip(coherence, 0, 1),
        "emergence_eta": np.clip(emergence, 0, 1),
        "bifurcation_B": np.clip(bifurcation, 0, 1),
        "reducibility_score": np.clip(reducibility, 0, 1),
        "perturbation": ["Concentration_Ramp"]*timesteps,
        "response": ["Conformational_Shift"]*timesteps,
        "attractor_state": ["Free_Receptor"]*15 + ["Midpoint_State"]*20 + ["Complex_Attractor"]*15,
        "ligand_concentration": ligand,
        "receptor_affinity": np.ones(timesteps) * kd,
        "delta_G": delta_g,
        "conformational_state": np.clip(conformational_state, 0, 1),
        "thermal_noise": thermal_noise
    })
    mol_df.to_csv(f"{data_dir}/synthetic_binding_dynamics.csv", index=False)

    # ----------------------------------------------------
    # 6. MULTISCALE PROPAGATION (synthetic_multiscale_cascade.csv)
    # ----------------------------------------------------
    print("Generating Multiscale Propagation Dataset...")
    # Micro -> Macro propagation: mutation -> metabolic shift -> tissue remodeling -> angiogenesis -> organ dysfunction
    mutation = np.concatenate([np.ones(10)*1.0, np.ones(40)*4.2])
    metabolic = np.concatenate([np.ones(15)*1.0, np.linspace(1.0, 9.2, 15), np.ones(20)*9.5]) + np.random.normal(0, 0.1, timesteps)
    tissue = np.concatenate([np.ones(20)*1.0, np.linspace(1.0, 8.5, 15), np.ones(15)*8.8]) + np.random.normal(0, 0.1, timesteps)
    angio = np.concatenate([np.ones(25)*1.0, np.linspace(1.0, 9.8, 15), np.ones(10)*9.9]) + np.random.normal(0, 0.1, timesteps)
    organ = np.concatenate([np.ones(30)*1.0, np.linspace(1.0, 9.9, 15), np.ones(5)*10.0]) + np.random.normal(0, 0.05, timesteps)
    
    entropy = np.linspace(0.12, 0.94, timesteps)
    coherence = np.linspace(0.94, 0.12, timesteps)
    emergence = 1.0 - entropy
    bifurcation = np.linspace(0.01, 0.98, timesteps)
    reducibility = np.linspace(0.98, 0.02, timesteps)
    
    mul_df = pd.DataFrame({
        "timestep": [f"t{i+1}" for i in range(timesteps)],
        "state_id": ["Micro_Somatic"]*15 + ["Tissue_Remodeling"]*15 + ["Angiogenesis_Factor"]*15 + ["Organ_Dysfunction"]*5,
        "entropy_H": np.clip(entropy, 0, 1),
        "coherence_k": np.clip(coherence, 0, 1),
        "emergence_eta": np.clip(emergence, 0, 1),
        "bifurcation_B": np.clip(bifurcation, 0, 1),
        "reducibility_score": np.clip(reducibility, 0, 1),
        "perturbation": ["Somatic_Mutation"]*15 + ["Metabolic_Rewiring"]*15 + ["Capillary_Sprouting"]*20,
        "response": ["Local_Mitosis"]*15 + ["Stroma_Destabilization"]*15 + ["Systemic_Vascularization"]*20,
        "attractor_state": ["Local_Niche"]*15 + ["Neoplastic_Matrix"]*15 + ["Vascular_Tumor_Attractor"]*20,
        "mutation_count": mutation,
        "metabolic_activity": metabolic,
        "tissue_remodeling_index": tissue,
        "angiogenesis_factor": angio,
        "organ_dysfunction_score": organ
    })
    mul_df.to_csv(f"{data_dir}/synthetic_multiscale_cascade.csv", index=False)

    # ----------------------------------------------------
    # 7. REDUCIBILITY CLASSIFIER (synthetic_reducibility_routing.csv)
    # ----------------------------------------------------
    print("Generating Reducibility Classifier Dataset...")
    # Kepler orbit (reducible), ecosystem collapse (irreducible), tumor (hybrid)
    exp = np.concatenate([np.zeros(15), np.linspace(0.0, 9.5, 20), np.ones(15)*9.8])
    lyapunov = np.concatenate([np.ones(15)*-0.05, np.linspace(-0.05, 2.5, 20), np.ones(15)*2.8])
    dim = np.concatenate([np.ones(15)*1.0, np.linspace(1.0, 3.8, 20), np.ones(15)*4.2])
    
    entropy = np.concatenate([np.ones(15)*0.02, np.linspace(0.02, 0.95, 20), np.ones(15)*0.98])
    coherence = np.concatenate([np.ones(15)*0.99, np.linspace(0.99, 0.05, 20), np.ones(15)*0.02])
    emergence = 1.0 - entropy
    bifurcation = np.concatenate([np.zeros(12), np.linspace(0.0, 0.99, 20), np.ones(18)*0.02])
    reducibility = 1.0 - entropy
    
    red_df = pd.DataFrame({
        "timestep": [f"t{i+1}" for i in range(timesteps)],
        "state_id": ["Reducible_Kepler"]*15 + ["Hybrid_Adaptive"]*20 + ["Irreducible_Collapse"]*15,
        "entropy_H": np.clip(entropy, 0, 1),
        "coherence_k": np.clip(coherence, 0, 1),
        "emergence_eta": np.clip(emergence, 0, 1),
        "bifurcation_B": np.clip(bifurcation, 0, 1),
        "reducibility_score": np.clip(reducibility, 0, 1),
        "perturbation": ["None"]*15 + ["Perturbation_Ingress"]*20 + ["System_Overload"]*15,
        "response": ["Zero_Response"]*15 + ["State_Tracking"]*20 + ["Bifurcation_Unfolding"]*15,
        "attractor_state": ["Analytical_Shortcut"]*15 + ["Adaptive_Manifold"]*20 + ["Irreducible_Unfolding_Basin"]*15,
        "phase_space_expansion": exp,
        "lyapunov_exponent": lyapunov,
        "dimension_growth": dim,
        "router_decision": ["Analytical_Solver"]*15 + ["Hybrid_Solver"]*20 + ["Recursive_Agent_Unfolder"]*15
    })
    red_df.to_csv(f"{data_dir}/synthetic_reducibility_routing.csv", index=False)

    # ----------------------------------------------------
    # 8. HYPERGRAPH CAUSALITY (synthetic_hypergraph_causality.csv)
    # ----------------------------------------------------
    print("Generating Hypergraph Causality Dataset...")
    # Multiway causality {hypoxia, KRAS, immunity, therapy} -> resistance
    h_coupling = np.linspace(0.1, 0.98, timesteps)
    multi_ent = np.linspace(0.2, 0.94, timesteps)
    nl_dep = np.sin(np.linspace(0, np.pi*2, timesteps)) * 0.5 + 0.5
    emergent_coop = h_coupling * nl_dep
    
    entropy = np.linspace(0.12, 0.88, timesteps)
    coherence = np.linspace(0.88, 0.22, timesteps)
    emergence = emergent_coop * 0.92
    bifurcation = h_coupling * 0.95
    reducibility = 1.0 - h_coupling
    
    hyp_df = pd.DataFrame({
        "timestep": [f"t{i+1}" for i in range(timesteps)],
        "state_id": ["Bipartite_Linear"]*15 + ["Multiway_Coupling"]*20 + ["Emergent_Cooperative"]*15,
        "entropy_H": np.clip(entropy, 0, 1),
        "coherence_k": np.clip(coherence, 0, 1),
        "emergence_eta": np.clip(emergence, 0, 1),
        "bifurcation_B": np.clip(bifurcation, 0, 1),
        "reducibility_score": np.clip(reducibility, 0, 1),
        "perturbation": ["Hyperedge_Ingress"]*timesteps,
        "response": ["Cooperative_Shift"]*timesteps,
        "attractor_state": ["Isolated_Nodes"]*15 + ["Dynamic_Hyperedge"]*20 + ["Nonlinear_Attractor"]*15,
        "hyperedge_coupling": h_coupling,
        "multiway_entropy": multi_ent,
        "non_linear_dependency": nl_dep,
        "emergent_cooperative_index": emergent_coop
    })
    hyp_df.to_csv(f"{data_dir}/synthetic_hypergraph_causality.csv", index=False)

    # ----------------------------------------------------
    # 9. JEPA WORLD MODEL (synthetic_jepa_world_model.csv)
    # ----------------------------------------------------
    print("Generating JEPA World Model Dataset...")
    # Predict future latent states without raw pixel reconstruction
    jepa_energy = np.concatenate([np.ones(15)*4.5, np.linspace(4.5, 0.15, 20), np.ones(15)*0.12])
    recon_var = np.concatenate([np.ones(15)*9.8, np.linspace(9.8, 0.05, 20), np.ones(15)*0.02])
    f_entropy = np.concatenate([np.ones(15)*0.95, np.linspace(0.95, 0.14, 20), np.ones(15)*0.10])
    pred_coh = np.concatenate([np.ones(15)*0.05, np.linspace(0.05, 0.94, 20), np.ones(15)*0.96])
    
    entropy = f_entropy
    coherence = pred_coh
    emergence = coherence * 0.98
    bifurcation = 1.0 - pred_coh
    reducibility = np.linspace(0.12, 0.94, timesteps)
    
    jep_df = pd.DataFrame({
        "timestep": [f"t{i+1}" for i in range(timesteps)],
        "state_id": ["Uncalibrated"]*15 + ["JEPA_Energy_Minimization"]*20 + ["Optimal_Latent_Predictor"]*15,
        "entropy_H": np.clip(entropy, 0, 1),
        "coherence_k": np.clip(coherence, 0, 1),
        "emergence_eta": np.clip(emergence, 0, 1),
        "bifurcation_B": np.clip(bifurcation, 0, 1),
        "reducibility_score": np.clip(reducibility, 0, 1),
        "perturbation": ["Gradient_Step"]*timesteps,
        "response": ["Latent_Alignment"]*timesteps,
        "attractor_state": ["High_Variance_State"]*15 + ["Energy_Valley"]*20 + ["JEPA_Optimal_Basin"]*15,
        "latent_prediction_energy": jepa_energy,
        "reconstruction_variance": recon_var,
        "future_state_entropy": f_entropy,
        "predicted_coherence": pred_coh
    })
    jep_df.to_csv(f"{data_dir}/synthetic_jepa_world_model.csv", index=False)

    # ----------------------------------------------------
    # 10. REALITY ANCHOR VALIDATION (synthetic_reality_anchors.csv)
    # ----------------------------------------------------
    print("Generating Reality Anchor Validation Dataset...")
    # Measured outcomes, prediction divergence, manifold drift
    meas = np.concatenate([np.ones(15)*1.1, np.linspace(1.1, 9.8, 20), np.ones(15)*9.9])
    div = np.concatenate([np.ones(15)*0.85, np.linspace(0.85, 0.02, 20), np.ones(15)*0.01])
    drift = np.concatenate([np.ones(15)*0.95, np.linspace(0.95, 0.04, 20), np.ones(15)*0.03])
    unc = np.concatenate([np.ones(15)*0.75, np.linspace(0.75, 0.05, 20), np.ones(15)*0.02])
    
    entropy = np.concatenate([np.ones(15)*0.85, np.linspace(0.85, 0.12, 20), np.ones(15)*0.08])
    coherence = np.concatenate([np.ones(15)*0.08, np.linspace(0.08, 0.95, 20), np.ones(15)*0.96])
    emergence = coherence
    bifurcation = div
    reducibility = np.linspace(0.05, 0.99, timesteps)
    
    rea_df = pd.DataFrame({
        "timestep": [f"t{i+1}" for i in range(timesteps)],
        "state_id": ["Unanchored"]*15 + ["Bayesian_Anchoring"]*20 + ["Empirically_Grounded"]*15,
        "entropy_H": np.clip(entropy, 0, 1),
        "coherence_k": np.clip(coherence, 0, 1),
        "emergence_eta": np.clip(emergence, 0, 1),
        "bifurcation_B": np.clip(bifurcation, 0, 1),
        "reducibility_score": np.clip(reducibility, 0, 1),
        "perturbation": ["Empirical_Measurement"]*timesteps,
        "response": ["Bayesian_Prior_Update"]*timesteps,
        "attractor_state": ["Floating_Manifold"]*15 + ["Anchored_Trajectory"]*20 + ["Empirical_Reality_Basin"]*15,
        "measured_outcome": meas,
        "prediction_divergence": div,
        "manifold_drift": drift,
        "uncertainty": unc
    })
    rea_df.to_csv(f"{data_dir}/synthetic_reality_anchors.csv", index=False)

    print("=" * 70)
    print(f"SUCCESS! Created all 10 causal transition datasets in: {data_dir}")
    print("=" * 70)

if __name__ == "__main__":
    generate_suite()
