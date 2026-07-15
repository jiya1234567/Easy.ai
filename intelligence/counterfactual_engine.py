"""
OMEGA-CORE Stage 10 — Counterfactual Engine (DoWhy-Style)
=========================================================
Forks the digital twin into parallel reality branches using mathematical Do-Calculus.
Rather than using hardcoded templates, it ingests a CausalGraph and propagates
interventions (do-operator) through the graph edges to calculate Treatment Effects
and counterfactual state trajectories.
"""

import json
import random
import datetime
import networkx as nx
from dataclasses import dataclass, field, asdict
from typing import Any, Optional
from intelligence.causal_discovery_engine import CausalDiscoveryEngine, CausalGraph

@dataclass
class Intervention:
    target_variable: str
    delta_value: float
    description: str

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

OUTCOME_LABELS = {
    (0.80, 1.00): "✅ Strong Positive Response",
    (0.60, 0.80): "🔶 Moderate Improvement",
    (0.40, 0.60): "⚠️ Marginal Effect",
    (0.20, 0.40): "🔴 Minimal Benefit",
    (0.00, 0.20): "❌ Adverse / No Effect",
    (-1.00, 0.00): "☠️ Critical Degradation"
}

def _outcome_label(score: float) -> str:
    for (lo, hi), label in OUTCOME_LABELS.items():
        if lo <= score <= hi:
            return label
    return "Unknown"

class CounterfactualEngine:
    def __init__(self, simulation_steps: int = 6):
        self.steps = simulation_steps
        self._history: list[CounterfactualResult] = []

    def _build_nx_graph(self, causal_graph: CausalGraph) -> nx.DiGraph:
        """Convert OMEGA CausalGraph to NetworkX DiGraph for Do-Calculus."""
        G = nx.DiGraph()
        for edge in causal_graph.edges:
            # Infer polarity from mechanism description or assume positive
            mech = edge.mechanism.lower()
            polarity = -1 if any(word in mech for word in ["reduce", "decrease", "negative", "lower", "shorten"]) else 1
            G.add_edge(edge.source, edge.target, weight=edge.confidence * polarity)
        return G

    def _simulate_do_calculus(self, G: nx.DiGraph, initial_state: dict, intervention: Intervention) -> list[dict]:
        """
        Simulate the trajectory of the system over N steps by applying the
        Do-Operator (severing incoming edges to the target) and propagating the delta.
        """
        trajectory = [initial_state.copy()]
        current_state = initial_state.copy()
        
        # Apply Do-Operator: Sever incoming edges to the intervened variable
        G_do = G.copy()
        target = intervention.target_variable
        if G_do.has_node(target):
            in_edges = list(G_do.in_edges(target))
            G_do.remove_edges_from(in_edges)
            
        # Immediate effect of intervention
        if target in current_state:
            current_state[target] += intervention.delta_value
        else:
            current_state[target] = intervention.delta_value

        for step in range(self.steps):
            next_state = current_state.copy()
            try:
                nodes = list(nx.topological_sort(G_do))
            except nx.NetworkXUnfeasible:
                nodes = list(G_do.nodes())

            deltas = {n: 0.0 for n in nodes}
            
            for node in nodes:
                if node == target and step == 0:
                    continue
                    
                if G_do.has_node(node):
                    for predecessor in G_do.predecessors(node):
                        weight = G_do[predecessor][node]['weight']
                        prev_val = trajectory[-1].get(predecessor, 0.0)
                        curr_val = current_state.get(predecessor, 0.0)
                        pred_delta = curr_val - prev_val
                        
                        deltas[node] += pred_delta * weight * 0.5 # Damping

            for node, delta in deltas.items():
                if node in next_state:
                    noise = random.uniform(-0.02, 0.02)
                    next_state[node] += delta + noise

            current_state = next_state
            trajectory.append(current_state.copy())
            
        return trajectory

    def _score_outcome(self, initial_state: dict, final_state: dict, primary_metric: str, higher_is_better: bool = True) -> float:
        """Score the final state relative to the initial state on a 0-1 scale."""
        if primary_metric not in initial_state or primary_metric not in final_state:
            return 0.5 
            
        init_val = initial_state[primary_metric]
        fin_val = final_state[primary_metric]
        
        if init_val == 0:
            pct_change = 0
        else:
            pct_change = (fin_val - init_val) / abs(init_val)
            
        if not higher_is_better:
            pct_change = -pct_change
            
        score = 0.5 + (pct_change * 0.5)
        return max(0.0, min(1.0, score))

    def fork(self, domain: str, scenario: str, initial_state: dict, causal_graph: Optional[CausalGraph] = None, interventions: Optional[list[Intervention]] = None, target_metric: Optional[str] = None, higher_is_better: bool = True) -> CounterfactualResult:
        """
        Fork the current state into parallel branches using Do-Calculus.
        """
        if causal_graph is None:
            causal_graph = CausalDiscoveryEngine().discover(domain)
            
        if interventions is None:
            interventions = []
            for k, v in list(initial_state.items())[:2]:
                if isinstance(v, (int, float)):
                    interventions.append(Intervention(k, abs(v) * 0.2, f"Increase {k} by 20%"))
                    interventions.append(Intervention(k, -abs(v) * 0.2, f"Decrease {k} by 20%"))
                    
        if target_metric is None:
            target_metric = list(initial_state.keys())[-1]

        G = self._build_nx_graph(causal_graph)
        all_interventions = [Intervention("NONE", 0.0, "Baseline (No Intervention)")] + interventions
        
        branches = []
        for idx, intervention in enumerate(all_interventions):
            if intervention.target_variable == "NONE":
                trajectory = [initial_state.copy() for _ in range(self.steps + 1)]
            else:
                trajectory = self._simulate_do_calculus(G, initial_state, intervention)
                
            final = trajectory[-1]
            outcome_score = self._score_outcome(initial_state, final, target_metric, higher_is_better)
            
            branch = Branch(
                id=f"CF-{domain[:3].upper()}-{idx:02d}",
                name=intervention.description,
                intervention=f"do({intervention.target_variable} += {intervention.delta_value})",
                initial_state=initial_state,
                final_state=final,
                trajectory=trajectory,
                outcome_label=_outcome_label(outcome_score),
                outcome_score=round(outcome_score, 3),
                steps=self.steps,
                recommendation="DEPLOY" if outcome_score > 0.7 else "MONITOR" if outcome_score > 0.4 else "AVOID",
                timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            )
            branches.append(branch)

        branches.sort(key=lambda b: b.outcome_score, reverse=True)
        best = branches[0].name if branches else "N/A"
        worst = branches[-1].name if branches else "N/A"
        
        scores = [b.outcome_score for b in branches]
        divergence = round(max(scores) - min(scores), 3) if len(scores) > 1 else 0.0

        summary = f"Simulated {len(branches)} counterfactual branches using Do-Calculus. Target Metric: '{target_metric}'. Best outcome: '{best}' (Score: {branches[0].outcome_score:.2f})."

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
    result = engine.fork("weather", "Hurricane intervention", {"warm_sst": 1.0, "low_pressure": 0.5, "precipitation_rate": 0.8})
    print(json.dumps(result.to_dict(), indent=2))
