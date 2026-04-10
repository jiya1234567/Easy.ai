import sys, os
import pandas as pd
sys.path.append(os.getcwd())
from intelligence.scientific_engine import ScientificEngine

print("--- Testing Causal Discovery (DNA Dataset) ---")
engine = ScientificEngine(data_path="reports/dna_sequence_test.csv")
engine.load_data()

print("\n--- Feature Importance (Target: Expression_Level) ---")
importance = engine.compute_feature_importance(target_col="Expression_Level")
for f, v in importance.items():
    print(f"{f}: {v:.4f}")

print("\n--- Causal Graph ---")
G = engine.discover_causality()
for u, v in G.edges():
    print(f"{u} -> {v} (Weight: {G[u][v]['weight']:.4f})")

print("\n--- Silhouette Score ---")
score = engine.compute_silhouette()
print(f"Silhouette Score: {score:.4f}")

if "Mutation_Score" in str(G.edges()):
    print("\n✅ Causal Agent logic verified.")
else:
    print("\n❌ Causal Agent failed to detect key mechanisms.")
