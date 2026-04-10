import sys, os, json
import pandas as pd
import numpy as np
sys.path.append(os.getcwd())
from intelligence.scientific_engine import ScientificEngine

def run_road_test():
    tests = [
        {
            "name": "DNA SEQUENCE TEST",
            "file": "reports/dna_sequence_test.csv",
            "target": "Mutation_Score",
            "desc": "Detecting Healthy vs Mutated clusters"
        },
        {
            "name": "PROTEIN FEATURE SPACE",
            "file": "reports/protein_features_test.csv",
            "target": "Binding_Affinity",
            "desc": "Detecting folding families"
        },
        {
            "name": "DRUG-TARGET SIMULATION",
            "file": "reports/drug_test.csv",
            "target": "Toxicity_Index",
            "desc": "Detecting Good vs Bad drugs"
        }
    ]
    
    print("="*60)
    print("OMEGA-CORE SCIENTIFIC ROAD TEST: FEATURE & CAUSATION")
    print("="*60)
    
    for test in tests:
        print(f"\nRUNNING: {test['name']}")
        print(f"FILE: {test['file']}")
        print(f"GOAL: {test['desc']}")
        
        if not os.path.exists(test['file']):
            print(f"Error: {test['file']} missing. Skipping.")
            continue
            
        engine = ScientificEngine(data_path=test['file'])
        engine.load_data()
        
        # 1. Silhouette Score (Clustering Fidelity)
        try:
            sil_score = engine.compute_silhouette(n_clusters=2)
            print(f"Silhouette Score: {sil_score:.4f}")
        except Exception as e:
            print(f"Silhouette Score: Error {e}")
            
        # 2. Feature Importance
        print(f"Feature Importance (Target: {test['target']}):")
        importance = engine.compute_feature_importance(target_col=test['target'])
        for f, v in sorted(importance.items(), key=lambda x: x[1], reverse=True)[:3]:
            print(f"   - {f}: {v:.4f}")
            
        # 3. Causal Discovery
        print("Hypothesized Causal Paths:")
        G = engine.discover_causality(threshold=0.4)
        if len(G.edges()) > 0:
            for u, v in G.edges():
                print(f"   - {u} -> {v} (Weight: {G[u][v]['weight']:.2f})")
        else:
            print("   - No significant paths detected.")
            
        print("-" * 30)

    print("\n" + "="*60)
    print("ROAD TEST COMPLETE")
    print("="*60)

if __name__ == "__main__":
    run_road_test()
