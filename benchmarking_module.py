import time
import os
import json
import pandas as pd
import numpy as np
from intelligence.scientific_engine import ScientificEngine

def run_benchmarks():
    print("--- OMEGA-CORE PERFORMANCE BENCHMARK INITIALIZED ---")
    print("-" * 50)
    
    results = {}
    
    # 1. Data Loading Benchmark
    start = time.time()
    engine = ScientificEngine()
    loaded, msg = engine.load_data()
    results['Data Loading (ms)'] = (time.time() - start) * 1000
    print(f"Data Loading: {results['Data Loading (ms)']:.2f}ms | {msg}")
    
    if not loaded:
        print("Error: Benchmark aborted due to missing data.")
        return

    # 2. Manifold Computation Benchmark (PCA)
    start = time.time()
    engine.compute_manifold(method='PCA', n_components=3)
    results['PCA Projection 3D (ms)'] = (time.time() - start) * 1000
    print(f"PCA Projection (3D): {results['PCA Projection 3D (ms)']:.2f}ms")

    # 3. Manifold Stability Test
    start = time.time()
    stability = engine.compute_stability()
    results['Stability Test (ms)'] = (time.time() - start) * 1000
    print(f"Stability Index ({stability:.4f}): {results['Stability Test (ms)']:.2f}ms")

    # 4. Reducibility / Explained Variance
    start = time.time()
    reducibility = engine.compute_reducibility()
    results['Reducibility Test (ms)'] = (time.time() - start) * 1000
    print(f"Reducibility Score ({reducibility:.4f}): {results['Reducibility Test (ms)']:.2f}ms")

    # 5. Causal Graph Discovery
    start = time.time()
    G = engine.discover_causality()
    results['Causal Discovery (ms)'] = (time.time() - start) * 1000
    print(f"Causal Discovery ({len(G.edges())} paths): {results['Causal Discovery (ms)']:.2f}ms")

    # 6. Memory Usage (Approx)
    import sys
    if engine.data is not None:
        results['Memory Occupation (MB)'] = engine.data.memory_usage(deep=True).sum() / (1024 * 1024)
        print(f"Memory Footprint: {results['Memory Occupation (MB)']:.2f} MB")

    print("-" * 50)
    print("FINAL BENCHMARK SUMMARY SAVED TO reports/benchmark_report.json")
    
    os.makedirs("reports", exist_ok=True)
    with open("reports/benchmark_report.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run_benchmarks()
