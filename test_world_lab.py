import json
import os
import sys

from intelligence.hypothesis_engine import HypothesisEngine
from intelligence.counterfactual_engine import CounterfactualEngine
from intelligence.causal_discovery_engine import CausalDiscoveryEngine
from intelligence.theory_engine import TheoryEngine

# Provided Test Data
TEST_DATASETS = {
    "finance_rates": [
        {"quarter": "Q1", "cash_rate": 4.10, "inflation": 3.2, "gdp_growth": 2.7, "unemployment": 4.1},
        {"quarter": "Q2", "cash_rate": 4.60, "inflation": 4.1, "gdp_growth": 1.8, "unemployment": 4.8},
        {"quarter": "Q3", "cash_rate": 5.10, "inflation": 4.8, "gdp_growth": 0.9, "unemployment": 5.7}
    ],
    "cancer_evolution": [
        {"day": 0, "tumor_cells": 1000, "hypoxia": 0.2, "egfr_activity": 0.8},
        {"day": 30, "tumor_cells": 2500, "hypoxia": 0.5, "egfr_activity": 0.9},
        {"day": 60, "tumor_cells": 6000, "hypoxia": 0.8, "egfr_activity": 1.0}
    ],
    "drug_discovery": [
        {"compound": "A", "binding_affinity": 0.55, "toxicity": 0.75},
        {"compound": "B", "binding_affinity": 0.89, "toxicity": 0.22},
        {"compound": "C", "binding_affinity": 0.62, "toxicity": 0.48}
    ],
    "longevity_telomere": [
        {"age": 40, "telomere_length": 8.5, "telomerase": 0.15, "cancer_risk": 0.05},
        {"age": 60, "telomere_length": 6.8, "telomerase": 0.18, "cancer_risk": 0.08},
        {"age": 80, "telomere_length": 5.1, "telomerase": 0.22, "cancer_risk": 0.12}
    ],
    "neural_network": [
        {"time": 0, "firing_rate": 22, "synchrony": 0.2},
        {"time": 50, "firing_rate": 34, "synchrony": 0.5},
        {"time": 100, "firing_rate": 61, "synchrony": 0.9}
    ],
    "weather": [
        {"hour": 0, "pressure": 1008, "wind": 30},
        {"hour": 12, "pressure": 990, "wind": 70},
        {"hour": 24, "pressure": 960, "wind": 130}
    ],
    "quantum_gravity": [
        {"scale": "macro", "curvature": 0.01},
        {"scale": "meso", "curvature": 0.50},
        {"scale": "planck", "curvature": 0.99}
    ],
    "string_theory": [
        {"vacuum": "A", "dimensions": 10, "stability": 0.9},
        {"vacuum": "B", "dimensions": 11, "stability": 0.4},
        {"vacuum": "C", "dimensions": 26, "stability": 0.1}
    ]
}

def map_domain_to_components(domain_key):
    if "finance" in domain_key: return "macroeconomics"
    if "cancer" in domain_key or "drug" in domain_key: return "oncology"
    if "longevity" in domain_key: return "longevity"
    if "weather" in domain_key: return "weather"
    if "quantum" in domain_key or "string" in domain_key: return "graphene_quantum"
    return "oncology" # fallback

def main():
    print("=" * 80)
    print("OMEGA WORLD LAB TEST SUITE")
    print("Executing full cognitive pipeline across all provided datasets.")
    print("=" * 80 + "\n")
    
    hypothesis_engine = HypothesisEngine()
    counterfactual_engine = CounterfactualEngine()
    causal_engine = CausalDiscoveryEngine()
    theory_engine = TheoryEngine()
    
    for domain_key, dataset in TEST_DATASETS.items():
        print(f"[{domain_key.upper()}] Loading Data Streams...")
        
        # Use final state in dataset for hypothesis generation
        latest_observation = dataset[-1]
        
        # Map test domain to component domains
        mapped_domain = map_domain_to_components(domain_key)
        
        # 1. Hypothesis Generation
        hyp_res = hypothesis_engine.generate(mapped_domain, latest_observation)
        top_hyp = hyp_res.top_hypothesis
        print(f"  → Stage 9  (Hypothesis): {top_hyp}")
        
        # 2. Counterfactual Simulation
        cf_res = counterfactual_engine.fork(mapped_domain, f"Intervention for {domain_key}", latest_observation)
        best_cf = cf_res.best_branch
        print(f"  → Stage 10 (Counterfactual): Recommended Intervention: {best_cf} (Score: {cf_res.branches[0].outcome_score})")
        
        # 3. Causal Discovery
        causal_res = causal_engine.discover(mapped_domain, latest_observation)
        nodes = len(causal_res.nodes)
        print(f"  → Stage 11 (Causal Graph): Identified {nodes} causal nodes and relations.")
        
        # 4. Theory Generation
        theory_res = theory_engine.synthesize_theory(domain_key, top_hyp, nodes, best_cf)
        print(f"  → Stage 16 (World Lab Theory Synthesis):")
        print(f"      Theory: {theory_res.active_theories[0].name}")
        print(f"      Falsification Criteria: {theory_res.active_theories[0].falsification_criteria}")
        print("-" * 80)

if __name__ == "__main__":
    main()
