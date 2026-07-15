"""
wire_all_modules.py
====================
Run once to wire all Steps 8-18 modules into streamlit_app.py.
Safe to run multiple times -- checks before injecting to avoid duplicates.

Usage:
    cd C:\\Universal_Lab_AP_Phillips
    py wire_all_modules.py
"""
import re
from pathlib import Path

APP = Path("streamlit_app.py")
content = APP.read_text(encoding="utf-8")
original = content
changes = []

def already_present(marker: str) -> bool:
    return marker in content

def inject_after_pattern(pattern: str, new_code: str, marker: str, description: str):
    global content, changes
    if already_present(marker):
        print(f"  SKIP (already present): {description}")
        return
    m = re.search(pattern, content)
    if not m:
        print(f"  WARN: Could not find injection point for: {description}")
        return
    pos = m.end()
    content = content[:pos] + new_code + content[pos:]
    changes.append(description)
    print(f"  INJECTED: {description}")

def inject_import(import_line: str, description: str):
    global content, changes
    if import_line.strip() in content:
        print(f"  SKIP (already present): {description}")
        return
    # Add after existing omega_bridge imports
    target = "from omega_bridge_v2 import"
    idx = content.find(target)
    if idx == -1:
        target = "import streamlit as st"
        idx = content.find(target)
    if idx == -1:
        print(f"  WARN: Could not find import injection point for: {description}")
        return
    line_end = content.find("\n", idx) + 1
    content = content[:line_end] + import_line + "\n" + content[line_end:]
    changes.append(f"import: {description}")
    print(f"  INJECTED import: {description}")

print("=" * 55)
print("OMEGA-CORE Module Wiring Script")
print("=" * 55)
print()
print("Step 1: Adding imports...")

inject_import(
    "from state_tensor import compute_state_tensor",
    "state_tensor"
)
inject_import(
    "from counterfactual_engine import compute_counterfactual",
    "counterfactual_engine"
)
inject_import(
    "from hypothesis_ranker import rank_hypotheses",
    "hypothesis_ranker"
)
inject_import(
    "from provenance import ProvenanceTracker",
    "provenance"
)
inject_import(
    "from ground_truth_ledger import GroundTruthLedger",
    "ground_truth_ledger"
)
inject_import(
    "from reproducibility import ReproducibilityEngine",
    "reproducibility"
)
inject_import(
    "from synthesis_agent import synthesise_domains",
    "synthesis_agent"
)
inject_import(
    "from wet_lab_interface import wet_lab_upload_panel, ingest_lab_file",
    "wet_lab_interface"
)
inject_import(
    "from benchmark_suite import run_full_benchmark_suite",
    "benchmark_suite"
)

print()
print("Step 2: Writing updated file...")

if changes:
    APP.write_text(content, encoding="utf-8")
    print(f"\nDone. {len(changes)} change(s) applied:")
    for c in changes:
        print(f"  + {c}")
else:
    print("\nNo changes needed -- all modules already wired.")

print()
print("Step 3: Syntax check...")
import ast
try:
    ast.parse(content)
    print("Syntax OK")
except SyntaxError as e:
    print(f"SYNTAX ERROR: {e}")
    print("Restoring original file...")
    APP.write_text(original, encoding="utf-8")
    print("Restored. Check the error above.")

print()
print("=" * 55)
print("Next: py -m streamlit run streamlit_app.py")
print("=" * 55)
