"""
OMEGA-CORE Stage 10 — Counterfactual Engine
============================================
Forks the digital twin into parallel reality branches and simulates
divergent outcomes from different interventions.

Answers: "What if?"

Architecture:
    Current State
        ↓
    CounterfactualEngine.fork(branches)
        ↓
    Parallel Branch Simulations
        ↓
    {branch_a: outcome, branch_b: outcome, ...}
"""

import json
import random
import datetime
from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass
class Branch:
    id: str
    name: str
    intervention: str
    initial_state: dict
    final_state: dict
    trajectory: list[dict]
    outcome_label: str
    outcome_score: float
    steps: int
    recommendation: str
    timestamp: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class CounterfactualResult:
    domain: str
    scenario: str
    branches: list[Branch]
    best_branch: str
    worst_branch: str
    divergence_score: float
    summary: str
    generated_at: str

    def to_dict(self) -> dict:
        return {
            "domain": self.domain,
            "scenario": self.scenario,
            "branches": [b.to_dict() for b in self.branches],
            "best_branch": self.best_branch,
            "worst_branch": self.worst_branch,
            "divergence_score": self.divergence_score,
            "summary": self.summary,
            "generated_at": self.generated_at,
        }


# ── Domain-specific transition dynamics ───────────────────────────────────────

BRANCH_TEMPLATES = {
    "oncology": [
        {
            "name": "Drug A — EGFR Inhibitor",
            "intervention": "Erlotinib 150mg/day (EGFR-targeted therapy)",
            "dynamics": {"tumor_cells": -0.35, "ki67": -0.40, "hypoxia": -0.15},
            "outcome_bias": 0.78,
        },
        {
            "name": "Drug B — Anti-VEGF",
            "intervention": "Bevacizumab 15mg/kg q3w (anti-angiogenic)",
            "dynamics": {"tumor_cells": -0.20, "ki67": -0.25, "hypoxia": -0.45},
            "outcome_bias": 0.65,
        },
        {
            "name": "Drug C — Immunotherapy",
            "intervention": "Pembrolizumab 200mg q3w (PD-1 checkpoint blockade)",
            "dynamics": {"tumor_cells": -0.15, "ki67": -0.10, "hypoxia": 0.05},
            "outcome_bias": 0.58,
        },
        {
            "name": "No Treatment (Control)",
            "intervention": "Watchful waiting — no systemic therapy",
            "dynamics": {"tumor_cells": 0.30, "ki67": 0.20, "hypoxia": 0.25},
            "outcome_bias": 0.15,
        },
    ],
    "weather": [
        {
            "name": "Early Evacuation",
            "intervention": "Mandatory evacuation order 48h before landfall",
            "dynamics": {"casualties": -0.90, "infrastructure_damage": -0.20},
            "outcome_bias": 0.89,
        },
        {
            "name": "Shelter-in-Place",
            "intervention": "Community shelter reinforcement + emergency supplies",
            "dynamics": {"casualties": -0.50, "infrastructure_damage": -0.10},
            "outcome_bias": 0.60,
        },
        {
            "name": "No Intervention",
            "intervention": "No pre-emptive action taken",
            "dynamics": {"casualties": 0.50, "infrastructure_damage": 0.60},
            "outcome_bias": 0.10,
        },
    ],
    "macroeconomics": [
        {
            "name": "Rate Hike +50bps",
            "intervention": "RBA raises cash rate from 4.35% to 4.85%",
            "dynamics": {"inflation": -0.30, "gdp": -0.20, "unemployment": 0.15},
            "outcome_bias": 0.62,
        },
        {
            "name": "Rate Hold",
            "intervention": "RBA holds cash rate steady at 4.35%",
            "dynamics": {"inflation": -0.05, "gdp": 0.05, "unemployment": 0.02},
            "outcome_bias": 0.55,
        },
        {
            "name": "Rate Cut -25bps",
            "intervention": "RBA cuts cash rate to 4.10% to stimulate growth",
            "dynamics": {"inflation": 0.15, "gdp": 0.10, "unemployment": -0.10},
            "outcome_bias": 0.40,
        },
        {
            "name": "Fiscal Stimulus",
            "intervention": "Government stimulus package AUD $15B infrastructure",
            "dynamics": {"inflation": 0.20, "gdp": 0.30, "unemployment": -0.25},
            "outcome_bias": 0.50,
        },
    ],
    "longevity": [
        {
            "name": "Senolytic Therapy",
            "intervention": "Dasatinib + Quercetin 3-day pulse monthly",
            "dynamics": {"senescent_cells": -0.35, "telomere_length": 0.05},
            "outcome_bias": 0.72,
        },
        {
            "name": "NAD+ Restoration",
            "intervention": "NMN 500mg/day + Resveratrol 250mg/day",
            "dynamics": {"senescent_cells": -0.15, "telomere_length": 0.08},
            "outcome_bias": 0.65,
        },
        {
            "name": "Caloric Restriction",
            "intervention": "20% caloric restriction with balanced micronutrients",
            "dynamics": {"senescent_cells": -0.20, "telomere_length": 0.03},
            "outcome_bias": 0.60,
        },
        {
            "name": "No Intervention",
            "intervention": "Standard of care — no longevity intervention",
            "dynamics": {"senescent_cells": 0.20, "telomere_length": -0.10},
            "outcome_bias": 0.20,
        },
    ],
    "graphene_quantum": [
        {
            "name": "Reduce Temperature 20mK",
            "intervention": "Lower dilution fridge to 20mK operating point",
            "dynamics": {"coherence_time_us": 0.60, "defect_density": 0.0},
            "outcome_bias": 0.85,
        },
        {
            "name": "Substrate Redesign",
            "intervention": "Replace SiO2 with hBN substrate for lower dielectric loss",
            "dynamics": {"coherence_time_us": 0.45, "defect_density": -0.40},
            "outcome_bias": 0.78,
        },
        {
            "name": "Annealing Treatment",
            "intervention": "Rapid thermal anneal at 400°C to heal lattice defects",
            "dynamics": {"coherence_time_us": 0.20, "defect_density": -0.60},
            "outcome_bias": 0.65,
        },
        {
            "name": "No Change (Baseline)",
            "intervention": "Continue at current operating conditions",
            "dynamics": {"coherence_time_us": 0.0, "defect_density": 0.0},
            "outcome_bias": 0.35,
        },
    ],
}

OUTCOME_LABELS = {
    (0.80, 1.00): "✅ Strong Positive Response",
    (0.60, 0.80): "🔶 Moderate Improvement",
    (0.40, 0.60): "⚠️ Marginal Effect",
    (0.20, 0.40): "🔴 Minimal Benefit",
    (0.00, 0.20): "❌ Adverse / No Effect",
}


def _outcome_label(score: float) -> str:
    for (lo, hi), label in OUTCOME_LABELS.items():
        if lo <= score <= hi:
            return label
    return "Unknown"


class CounterfactualEngine:
    """
    Stage 10 — Counterfactual Engine.

    Forks the current state into parallel intervention branches and
    simulates each trajectory, returning ranked outcomes.

    Usage:
        engine = CounterfactualEngine()
        result = engine.fork("oncology", "Cancer progression intervention",
                             {"tumor_cells": 46000, "ki67": 0.82})
    """

    def __init__(self, simulation_steps: int = 6):
        self.steps = simulation_steps
        self._history: list[CounterfactualResult] = []

    def _simulate_trajectory(self, initial: dict, dynamics: dict) -> list[dict]:
        """Simulate a state trajectory over N steps given delta dynamics."""
        trajectory = [initial.copy()]
        current = {k: float(v) if isinstance(v, (int, float)) else v
                   for k, v in initial.items()}

        for step in range(self.steps):
            next_state = {}
            for key, val in current.items():
                if not isinstance(val, (int, float)):
                    next_state[key] = val
                    continue
                delta_pct = dynamics.get(key, 0.0)
                noise = random.uniform(-0.03, 0.03)
                next_val = val * (1 + delta_pct / self.steps + noise)
                next_state[key] = round(max(0.0, next_val), 4)
            current = next_state
            trajectory.append(current.copy())

        return trajectory

    def _recommendation(self, domain: str, branch_name: str, outcome_score: float) -> str:
        if outcome_score >= 0.75:
            return f"DEPLOY: {branch_name} shows strong predicted efficacy. Proceed to clinical/operational phase."
        elif outcome_score >= 0.55:
            return f"TRIAL: {branch_name} shows moderate effect. Recommend Phase 2 validation study."
        elif outcome_score >= 0.35:
            return f"MONITOR: {branch_name} shows marginal benefit. Continue data collection before committing."
        else:
            return f"AVOID: {branch_name} predicted adverse or insufficient outcome. Seek alternative strategy."

    def fork(self, domain: str, scenario: str, initial_state: dict) -> CounterfactualResult:
        """
        Fork the current domain state into all available intervention branches.

        Args:
            domain:        domain key (oncology, weather, macroeconomics, etc.)
            scenario:      human-readable description of the decision point
            initial_state: current observed state as dict

        Returns:
            CounterfactualResult with all branch simulations ranked
        """
        templates = BRANCH_TEMPLATES.get(domain.lower(), [
            {"name": "Intervention A", "intervention": "Apply standard intervention",
             "dynamics": {}, "outcome_bias": 0.6},
            {"name": "No Intervention", "intervention": "Do nothing",
             "dynamics": {}, "outcome_bias": 0.3},
        ])

        branches = []
        for idx, tmpl in enumerate(templates):
            trajectory = self._simulate_trajectory(initial_state, tmpl["dynamics"])
            final = trajectory[-1]
            outcome_score = round(
                tmpl["outcome_bias"] * 0.7 + random.uniform(0.0, 0.3), 3
            )

            branch = Branch(
                id=f"CF-{domain[:3].upper()}-{idx+1:02d}",
                name=tmpl["name"],
                intervention=tmpl["intervention"],
                initial_state=initial_state,
                final_state=final,
                trajectory=trajectory,
                outcome_label=_outcome_label(outcome_score),
                outcome_score=outcome_score,
                steps=self.steps,
                recommendation=self._recommendation(domain, tmpl["name"], outcome_score),
                timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            )
            branches.append(branch)

        branches.sort(key=lambda b: b.outcome_score, reverse=True)

        best  = branches[0].name if branches else "N/A"
        worst = branches[-1].name if branches else "N/A"

        scores = [b.outcome_score for b in branches]
        divergence = round(max(scores) - min(scores), 3) if len(scores) > 1 else 0.0

        summary = (
            f"Across {len(branches)} branches, '{best}' yields the highest predicted "
            f"outcome score ({branches[0].outcome_score:.2f}). "
            f"Branch divergence: {divergence:.3f} — "
            f"{'High' if divergence > 0.4 else 'Moderate' if divergence > 0.2 else 'Low'} sensitivity to intervention choice."
        )

        result = CounterfactualResult(
            domain=domain,
            scenario=scenario,
            branches=branches,
            best_branch=best,
            worst_branch=worst,
            divergence_score=divergence,
            summary=summary,
            generated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        )
        self._history.append(result)
        return result

    def get_history(self) -> list[dict]:
        return [r.to_dict() for r in self._history]

    def save(self, path: str = "reports/counterfactual_log.json"):
        import os
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(self.get_history(), f, indent=2)


if __name__ == "__main__":
    engine = CounterfactualEngine()
    result = engine.fork("oncology", "Stage 3 NSCLC treatment decision",
                         {"tumor_cells": 46000, "ki67": 0.82, "hypoxia": 0.71})
    print(json.dumps(result.to_dict(), indent=2))
