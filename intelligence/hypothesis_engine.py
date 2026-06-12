"""
OMEGA-CORE Stage 9 — Hypothesis Generation Engine
====================================================
Transforms domain observations into ranked, competing scientific hypotheses.
Moves the system from Observe→Predict  to  Observe→Explain→Predict.

Architecture:
    Observation (State Tensor)
        ↓
    HypothesisAgent
        ↓
    Ranked Hypothesis List (confidence, evidence, test protocol)
"""

import json
import random
import datetime
from dataclasses import dataclass, field, asdict
from typing import Any


# ── Domain-specific hypothesis templates ──────────────────────────────────────

HYPOTHESIS_LIBRARY = {
    "oncology": [
        ("Driver mutation activates oncogenic signalling pathway", ["ki67", "mutation_burden", "tumor_cells"]),
        ("Tumour microenvironment hypoxia drives resistance emergence", ["hypoxia", "vegf", "necrosis"]),
        ("Immune checkpoint suppression enables immune evasion", ["pd_l1", "t_cell_infiltration", "cytokines"]),
        ("Metabolic reprogramming (Warburg effect) fuels clonal expansion", ["glucose_uptake", "lactate", "atp"]),
        ("Epigenetic silencing of tumour-suppressor genes", ["methylation", "hdac_activity", "p53"]),
    ],
    "weather": [
        ("Warm sea-surface temperature gradient drives rapid intensification", ["sst", "pressure", "wind"]),
        ("ENSO phase modulates cyclone track and intensity variance", ["enso_index", "pressure", "humidity"]),
        ("Vertical wind shear inhibits convective organisation", ["wind_shear", "cloud_top_temp", "humidity"]),
        ("Moisture convergence at low levels triggers explosive deepening", ["moisture_flux", "pressure", "divergence"]),
    ],
    "macroeconomics": [
        ("Demand-pull inflation driven by excess consumer spending", ["gdp", "inflation", "unemployment"]),
        ("Supply-side cost-push inflation from energy price shocks", ["inflation", "oil_price", "ppi"]),
        ("Monetary policy transmission lag causing persistent inflation", ["cash_rate", "inflation", "credit_growth"]),
        ("Labour market tightness sustaining wage-price spiral dynamics", ["unemployment", "wages", "cpi"]),
    ],
    "longevity": [
        ("Telomere attrition rate predicts biological ageing trajectory", ["telomere_length", "senescent_cells", "age"]),
        ("Senescent cell accumulation drives inflammaging cascade", ["senescent_cells", "il6", "tnf"]),
        ("Mitochondrial dysfunction reduces cellular energy efficiency", ["atp_production", "ros", "nad_levels"]),
        ("Epigenetic clock acceleration predicts disease onset", ["methylation_age", "chronological_age", "dna_damage"]),
    ],
    "graphene_quantum": [
        ("Phonon scattering at elevated temperature causes decoherence", ["temperature_mK", "coherence_time_us", "phonons"]),
        ("Defect density in graphene lattice disrupts qubit fidelity", ["defect_density", "coherence_time_us", "gate_error"]),
        ("Charge noise from substrate coupling limits gate fidelity", ["dielectric_loss", "charge_noise", "coherence_time_us"]),
    ],
    "finance": [
        ("Momentum regime driven by institutional fund flows", ["price_trend", "volume", "sentiment"]),
        ("Mean-reversion signal from oversold RSI divergence", ["rsi", "price", "macd"]),
        ("Macro risk-off triggered by credit spread widening", ["credit_spreads", "vix", "yield_curve"]),
    ],
    "climate": [
        ("CO2 flux variance correlates with ENSO-driven SST anomalies", ["co2_ppm", "sst", "enso_index"]),
        ("Arctic amplification accelerating mid-latitude jet stream disruption", ["arctic_temp", "jet_stream", "polar_vortex"]),
    ],
}

GENERIC_HYPOTHESES = [
    ("Positive feedback loop amplifying the observed signal", []),
    ("Phase transition occurring near observed critical threshold", []),
    ("External perturbation driving system away from equilibrium", []),
]


@dataclass
class Hypothesis:
    id: str
    domain: str
    statement: str
    confidence: float
    evidence_keys: list[str]
    evidence_matched: list[str]
    test_protocol: str
    intervention: str
    rank: int = 0
    timestamp: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class HypothesisSet:
    domain: str
    observation_summary: dict
    hypotheses: list[Hypothesis]
    top_hypothesis: str
    generated_at: str
    state_tensor: dict

    def to_dict(self) -> dict:
        return {
            "domain": self.domain,
            "observation_summary": self.observation_summary,
            "hypotheses": [h.to_dict() for h in self.hypotheses],
            "top_hypothesis": self.top_hypothesis,
            "generated_at": self.generated_at,
            "state_tensor": self.state_tensor,
        }


class HypothesisEngine:
    """
    Stage 9 — Hypothesis Generation Engine.

    Generates ranked, competing hypotheses from a domain observation.
    Each hypothesis carries:
      - Confidence score (0–1)
      - Evidence keys matched from observation
      - Recommended test protocol (SOP reference)
      - Proposed intervention

    Usage:
        engine = HypothesisEngine()
        result = engine.generate("oncology", {"ki67": 0.82, "hypoxia": 0.71})
    """

    def __init__(self):
        self._history: list[HypothesisSet] = []

    # ── State Tensor Calculation ──────────────────────────────────────────────

    def _compute_state_tensor(self, observation: dict) -> dict:
        """Convert raw observations into the universal OMEGA state tensor."""
        values = [v for v in observation.values() if isinstance(v, (int, float))]
        if not values:
            return {"entropy": 0.5, "coherence": 0.5, "emergence": 0.5,
                    "bifurcation": 0.2, "reducibility": 0.6}

        mean_val = sum(values) / len(values)
        variance = sum((v - mean_val) ** 2 for v in values) / len(values)

        entropy     = min(1.0, round(variance * 2 + random.uniform(0.05, 0.15), 3))
        coherence   = round(1.0 - entropy * 0.6 + random.uniform(0.05, 0.1), 3)
        emergence   = round(mean_val * random.uniform(0.5, 0.9), 3)
        bifurcation = round(entropy * random.uniform(0.2, 0.5), 3)
        reducibility = round(1.0 - entropy + random.uniform(-0.05, 0.05), 3)

        return {
            "entropy":      max(0.0, min(1.0, entropy)),
            "coherence":    max(0.0, min(1.0, coherence)),
            "emergence":    max(0.0, min(1.0, emergence)),
            "bifurcation":  max(0.0, min(1.0, bifurcation)),
            "reducibility": max(0.0, min(1.0, reducibility)),
        }

    # ── Evidence Matching ────────────────────────────────────────────────────

    def _match_evidence(self, observation: dict, evidence_keys: list[str]) -> tuple[list[str], float]:
        """Match observation keys to hypothesis evidence requirements."""
        obs_keys_lower = {str(k).lower() for k in observation}
        matched = [k for k in evidence_keys if k.lower() in obs_keys_lower]
        coverage = len(matched) / len(evidence_keys) if evidence_keys else 0.5
        return matched, coverage

    # ── Confidence Scoring ───────────────────────────────────────────────────

    def _score_confidence(self, coverage: float, state_tensor: dict, base: float = None) -> float:
        """Compute confidence from evidence coverage + state tensor signal."""
        base = base or random.uniform(0.55, 0.90)
        signal = state_tensor.get("coherence", 0.5) * 0.3 + coverage * 0.5
        return round(min(0.99, max(0.30, base * 0.4 + signal * 0.6)), 3)

    # ── Test Protocol Generator ──────────────────────────────────────────────

    def _get_test_protocol(self, domain: str, idx: int) -> str:
        protocols = {
            "oncology":          [f"SOP_70_Run_CRISPR_Knockout_Screen_Gene_{idx+1}",
                                   f"SOP_71_Western_Blot_Pathway_Validation",
                                   f"SOP_72_Patient_Cohort_Stratification"],
            "weather":           [f"SOP_60_Satellite_Radiometric_Calibration",
                                   f"SOP_61_Radiosonde_Launch_Profile_{idx+1}"],
            "macroeconomics":    [f"SOP_80_RBA_Policy_Sensitivity_Model",
                                   f"SOP_81_CPI_Component_Decomposition"],
            "longevity":         [f"SOP_90_Telomere_FISH_Measurement",
                                   f"SOP_91_Senescent_Cell_SA_Beta_Gal"],
            "graphene_quantum":  [f"SOP_50_Cryo_Gate_Fidelity_Sweep",
                                   f"SOP_51_Raman_Spectroscopy_Defect_Map"],
            "finance":           [f"SOP_20_Factor_Attribution_Backtest",
                                   f"SOP_21_Risk_Adjusted_Signal_Validation"],
            "climate":           [f"SOP_60_CO2_Flux_Tower_Calibration",
                                   f"SOP_62_ENSO_Index_Correlation_Test"],
        }
        pool = protocols.get(domain, [f"SOP_XX_Experimental_Validation_{idx+1}"])
        return pool[idx % len(pool)]

    def _get_intervention(self, domain: str, hypothesis: str) -> str:
        if "hypoxia" in hypothesis.lower():
            return "Administer bevacizumab anti-VEGF; reduce tumour hypoxia zone"
        if "mutation" in hypothesis.lower() or "oncogen" in hypothesis.lower():
            return "Target driver pathway with tyrosine kinase inhibitor"
        if "immune" in hypothesis.lower():
            return "Deploy PD-1/PD-L1 checkpoint blockade immunotherapy"
        if "inflation" in hypothesis.lower() or "monetary" in hypothesis.lower():
            return "Tighten monetary policy; raise cash rate 25bps"
        if "telomere" in hypothesis.lower():
            return "Initiate senolytic therapy (Dasatinib + Quercetin protocol)"
        if "decoherence" in hypothesis.lower() or "phonon" in hypothesis.lower():
            return "Lower operating temperature to 20mK; redesign substrate isolation"
        if "defect" in hypothesis.lower():
            return "Apply chemical vapour deposition annealing to reduce lattice defects"
        if "cyclone" in hypothesis.lower() or "sst" in hypothesis.lower():
            return "Issue Category 4 alert; evacuate coastal zones within 100km radius"
        if "momentum" in hypothesis.lower():
            return "Enter long position with trailing stop at -2.5% from peak"
        return "Initiate controlled experiment per referenced SOP"

    # ── Main Generate Method ─────────────────────────────────────────────────

    def generate(self, domain: str, observation: dict, max_hypotheses: int = 5) -> HypothesisSet:
        """
        Generate a ranked set of hypotheses from domain + observation.

        Args:
            domain:         e.g. 'oncology', 'weather', 'macroeconomics'
            observation:    dict of observed variables and values
            max_hypotheses: number of competing hypotheses to return

        Returns:
            HypothesisSet with ranked Hypothesis objects
        """
        domain_lower = domain.lower()
        state_tensor = self._compute_state_tensor(observation)
        template_pool = HYPOTHESIS_LIBRARY.get(domain_lower, GENERIC_HYPOTHESES)

        # Add generic fallbacks if pool is small
        combined_pool = template_pool + GENERIC_HYPOTHESES
        selected = combined_pool[:max_hypotheses]

        hypotheses = []
        for idx, (statement, evidence_keys) in enumerate(selected):
            matched, coverage = self._match_evidence(observation, evidence_keys)
            confidence = self._score_confidence(coverage, state_tensor)

            h = Hypothesis(
                id=f"HYP-{domain_lower[:3].upper()}-{idx+1:03d}",
                domain=domain,
                statement=statement,
                confidence=confidence,
                evidence_keys=evidence_keys,
                evidence_matched=matched,
                test_protocol=self._get_test_protocol(domain_lower, idx),
                intervention=self._get_intervention(domain_lower, statement),
                timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            )
            hypotheses.append(h)

        # Rank by confidence descending
        hypotheses.sort(key=lambda h: h.confidence, reverse=True)
        for rank_idx, h in enumerate(hypotheses):
            h.rank = rank_idx + 1

        top = hypotheses[0].statement if hypotheses else "No hypothesis generated"

        result = HypothesisSet(
            domain=domain,
            observation_summary={k: v for k, v in list(observation.items())[:6]},
            hypotheses=hypotheses,
            top_hypothesis=top,
            generated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            state_tensor=state_tensor,
        )
        self._history.append(result)
        return result

    def get_history(self) -> list[dict]:
        return [h.to_dict() for h in self._history]

    def save(self, path: str = "reports/hypothesis_log.json"):
        import os
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(self.get_history(), f, indent=2)


# ── Standalone test ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    engine = HypothesisEngine()
    result = engine.generate("oncology", {
        "tumor_cells": 46000, "ki67": 0.82, "hypoxia": 0.71,
        "pd_l1": 0.6, "t_cell_infiltration": 0.2
    })
    print(json.dumps(result.to_dict(), indent=2))
