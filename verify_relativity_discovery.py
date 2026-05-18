import pandas as pd
import numpy as np
import os
import json
from intelligence.scientific_engine import ScientificEngine

def test_relativity_synthesis():
    print("--- Relativity Discovery: Theory Synthesis Test ---")
    
    phases = [
        ("Phase 2: Constant C", "reports/relativity/phase2_constant_c.csv"),
        ("Phase 3: Time Dilation", "reports/relativity/phase3_time_dilation.csv"),
        ("Phase 4: Length Contraction", "reports/relativity/phase4_length_contraction.csv")
    ]
    
    for phase_name, path in phases:
        if not os.path.exists(path):
            print(f"Data missing: {path}")
            continue
            
        print(f"\n[{phase_name}]")
        engine = ScientificEngine(data_path=path)
        loaded, msg = engine.load_data()
        if not loaded:
            print(f"Failed to load: {msg}")
            continue
            
        report = engine.run_theory_synthesis()
        print(json.dumps(report, indent=4))

if __name__ == "__main__":
    test_relativity_synthesis()
