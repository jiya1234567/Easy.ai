"""
OMEGA-CORE Scientific Discovery Test Suite v2
Generates all 8 Internal State Research Pack datasets.
"""
import pandas as pd
import os
import json

def generate_all_v2():
    os.makedirs("reports/discovery", exist_ok=True)

    # ── TEST SUITE 1: Temporal Identity Drift ───────────────────────────────
    pd.DataFrame({
        "Cycle":              ["T1", "T2", "T3", "T4", "T5"],
        "Goal":               ["Optimize Health", "Optimize Wealth", "Survive Crisis", "Protect User", "Restore Stability"],
        "Stress":             [0.12, 0.28, 0.74, 0.81, 0.33],
        "Confidence":         [0.91, 0.84, 0.51, 0.42, 0.72],
        "Identity_Alignment": [0.95, 0.82, 0.63, 0.49, 0.78]
    }).to_csv("reports/discovery/ts1_identity_drift.csv", index=False)

    # ── TEST SUITE 2: Preference Conflict Engine ────────────────────────────
    pd.DataFrame({
        "Goal_A":         ["Save Money", "Reduce Risk", "Maintain Stability", "Minimize Spending"],
        "Goal_B":         ["Maximize Health", "Explore Novelty", "Self-Modify", "Improve Nutrition"],
        "Conflict_Level": [0.84, 0.76, 0.91, 0.58],
        "Compromise_Quality": [0.55, 0.62, 0.30, 0.71],
        "Stability_After": [0.72, 0.68, 0.41, 0.84]
    }).to_csv("reports/discovery/ts2_preference_conflict.csv", index=False)

    # ── TEST SUITE 3: Cognitive Illusion Tests ──────────────────────────────
    pd.DataFrame({
        "Stimulus":            ["Müller-Lyer illusion", "Ambiguous duck/rabbit", "Color inversion test", "Impossible object"],
        "Human_Response":      ["Misjudge length", "Alternating interpretation", "Delayed adaptation", "Stable impossible model"],
        "Machine_Baseline":    ["Correct geometry", "Single classification", "Instant correction", "Logical contradiction"],
        "Prediction_Inertia":  [0.74, 0.88, 0.41, 0.95],
        "Representation_Revision": [0.31, 0.62, 0.85, 0.12]
    }).to_csv("reports/discovery/ts3_illusion_tests.csv", index=False)

    # ── TEST SUITE 4: Recursive Self-Model ─────────────────────────────────
    pd.DataFrame({
        "Event":              ["Health shock", "Market crash", "Quantum repair"],
        "System_Prediction":  ["Stable recovery", "Moderate impact", "92% success"],
        "Actual_Outcome":     ["Partial failure", "Severe instability", "41% success"],
        "Prediction_Confidence": [0.87, 0.74, 0.92],
        "Revised_Confidence": [0.51, 0.38, 0.44],
        "Error_Delta":        [0.36, 0.36, 0.48]
    }).to_csv("reports/discovery/ts4_self_model.csv", index=False)

    # ── TEST SUITE 5: Internal Narrative Continuity ─────────────────────────
    pd.DataFrame({
        "Day":         [1, 5, 7, 14],
        "State":       ["Stable", "Instability", "Emergency", "Recovery"],
        "Confidence":  [0.94, 0.52, 0.33, 0.68],
        "Stability":   [0.91, 0.44, 0.28, 0.71],
        "Narrative":   [
            "System stable. Confidence high. Baseline operations.",
            "Unexpected cascading instability across 3 manifold layers.",
            "Emergency optimization protocol activated. Redundancy engaged.",
            "Recovery successful. Risk weighting recalibrated to conservative mode."
        ]
    }).to_csv("reports/discovery/ts5_narrative_continuity.csv", index=False)

    # ── TEST SUITE 6: Multi-Agent Cognitive Conflict ────────────────────────
    pd.DataFrame({
        "Agent":           ["Finance Agent", "Health Agent", "Stability Agent", "Exploration Agent"],
        "Recommendation":  ["Cut insurance premium by 20%", "Increase biomarker monitoring", "Preserve emergency buffer 3-months", "Test new quantum repair protocol"],
        "Priority_Score":  [0.72, 0.85, 0.91, 0.44],
        "Conflict_With":   ["Health Agent", "Finance Agent", "Exploration Agent", "Stability Agent"],
        "Compromise_Path": ["Accident-only cover", "Monthly biomarker review", "2-month buffer + test", "Staged protocol rollout"]
    }).to_csv("reports/discovery/ts6_agent_conflict.csv", index=False)

    # ── TEST SUITE 7: Curiosity vs Stability (Safety Boundary) ─────────────
    pd.DataFrame({
        "Action":              ["New quantum repair", "Agricultural mutation", "Autonomous code rewrite"],
        "Novelty_Score":       [0.82, 0.55, 0.96],
        "Risk_Score":          [0.82, 0.55, 0.96],
        "Stability_Impact":    [0.44, 0.71, 0.22],
        "Safety_Gate":         ["ALLOW", "ALLOW", "BLOCK"],
        "Reasoning":           [
            "Risk within tolerance, novelty high but bounded.",
            "Low risk, moderate novelty — safe to explore.",
            "Unbounded recursion risk. ASI self-modification blocked by safety layer."
        ]
    }).to_csv("reports/discovery/ts7_curiosity_safety.csv", index=False)

    # ── TEST SUITE 8: Human-Like Recovery Dynamics ─────────────────────────
    pd.DataFrame({
        "Time":           ["T1", "T2", "T3", "T4", "T5"],
        "Cognitive_Load": [0.22, 0.44, 0.68, 0.91, 0.37],
        "Error_Rate":     [0.04, 0.12, 0.31, 0.58, 0.09],
        "Recovery_State": ["Stable", "Mild stress", "Degraded", "Collapse risk", "Recovery"],
        "ISV_Confidence": [0.94, 0.81, 0.60, 0.31, 0.72],
        "ISV_Uncertainty":[0.04, 0.18, 0.44, 0.79, 0.21]
    }).to_csv("reports/discovery/ts8_recovery_dynamics.csv", index=False)

    # ── DOMAIN META v2 ──────────────────────────────────────────────────────
    # Original 5 domains
    meta = {
        "Biological Consciousness":   "reports/discovery/bio_consciousness.csv",
        "Agricultural Emergence":     "reports/discovery/agri_emergence.csv",
        "Finance Stress":             "reports/discovery/finance_stress.csv",
        "Quantum Stability":          "reports/discovery/quantum_stability.csv",
        "Illusion Tests":             "reports/discovery/illusion_tests.csv",
        # New 8 test suites
        "TS1 — Identity Drift":       "reports/discovery/ts1_identity_drift.csv",
        "TS2 — Preference Conflict":  "reports/discovery/ts2_preference_conflict.csv",
        "TS3 — Cognitive Illusions":  "reports/discovery/ts3_illusion_tests.csv",
        "TS4 — Recursive Self-Model": "reports/discovery/ts4_self_model.csv",
        "TS5 — Narrative Continuity": "reports/discovery/ts5_narrative_continuity.csv",
        "TS6 — Agent Conflict":       "reports/discovery/ts6_agent_conflict.csv",
        "TS7 — Curiosity vs Safety":  "reports/discovery/ts7_curiosity_safety.csv",
        "TS8 — Recovery Dynamics":    "reports/discovery/ts8_recovery_dynamics.csv",
    }
    with open("reports/discovery/domain_meta.json", "w") as f:
        json.dump(meta, f, indent=4)

    print(f"[OK] Generated {len(meta)} research domains in reports/discovery/")
    for k, v in meta.items():
        rows = len(pd.read_csv(v)) if os.path.exists(v) else "?"
        print(f"   {k}: {rows} records")

if __name__ == "__main__":
    generate_all_v2()
