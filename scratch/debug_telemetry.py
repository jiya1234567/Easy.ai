import sys
import os

# Move to the telemetry directory to simulate running from there
os.chdir('telemetry')
sys.path.insert(0, os.getcwd())

print("Current mapping:", os.getcwd())
print("Files:", os.listdir('.'))

try:
    print("Testing imports...")
    import streamlit as st
    import pandas as pd
    import json
    from intelligence.scientific_engine import ScientificEngine
    print("Imports successful!")

    print("Testing ScientificEngine initialization...")
    engine = ScientificEngine(data_path="reports/bio_test.csv", metadata_path="reports/bio_test_metadata.json")
    print("Engine initialized!")

    print("Testing data load...")
    success, msg = engine.load_data()
    print(f"Load Result: {success}, {msg}")

    print("Checking for large files that might cause hangs...")
    reports = os.listdir('reports')
    for f in reports:
        if f.endswith('.csv'):
            size = os.path.getsize(os.path.join('reports', f))
            if size > 1024 * 1024:
                print(f"Large file found: {f} ({size / 1024 / 1024:.2f} MB)")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
