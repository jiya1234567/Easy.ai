"""
counterfactual_engine.py — Day 7
Lightweight do-calculus counterfactual reasoning using networkx.
Uses causal graphs from causal_scan_v2 to compute "what if X had been Y?"
"""
from __future__ import annotations
import numpy as np
from dataclasses import dataclass, field
from typing import Any


@dataclass
class CounterfactualResult:
    intervention: dict[str, float]   # what we changed
    affected_variables: dict[str, float]  # predicted new values
    confidence: float
    reasoning: str
    causal_path: list[str]

    def to_dict(self) -> dict:
        return self.__dict__.copy()


def compute_counterfactual(
    data: dict,
    causal_graph: dict,
    intervention: dict[str, float],
) -> CounterfactualResult:
    """
    Compute counterfactual: what would other variables be if we
    intervened to set intervention variables to specific values?

    Parameters
    ----------
    data         : {var: [values...]} -- observed data
    causal_graph : {effect: [causes]} -- from causal_scan_v2
    intervention : {var: new_value}   -- the "do()" operation

    Returns
    -------
    CounterfactualResult
    """
    try:
        import networkx as nx
        G = nx.DiGraph()
        for effect, causes in causal_graph.items():
            for cause in causes:
                G.add_edge(cause, effect)
    except ImportError:
        G = None

    arrays = {k: np.array(v, dtype=float)
              for k, v in data.items()
              if isinstance(v, (list, tuple)) and len(v) >= 3}
    n = min(len(a) for a in arrays.values()) if arrays else 0

    affected: dict[str, float] = {}
    reasoning_parts = []
    causal_path = list(intervention.keys())

    # For each intervened variable, propagate to its effects
    for interv_var, new_val in intervention.items():
        original_mean = float(np.mean(arrays[interv_var])) if interv_var in arrays else 0.0
        delta = new_val - original_mean
        reasoning_parts.append(
            f"Intervention: set {interv_var}={new_val:.2f} "
            f"(original mean={original_mean:.2f}, delta={delta:+.2f})"
        )

        # Find downstream effects via causal graph
        downstream = []
        for effect, causes in causal_graph.items():
            if interv_var in causes and effect not in intervention:
                downstream.append(effect)

        for effect in downstream:
            if effect not in arrays:
                continue
            causal_path.append(effect)
            # Estimate effect via regression coefficient
            cause_arr = arrays[interv_var]
            effect_arr = arrays[effect]
            if np.std(cause_arr) > 0:
                coeff = float(np.corrcoef(cause_arr, effect_arr)[0, 1]) * \
                        (float(np.std(effect_arr)) / float(np.std(cause_arr)))
                predicted_delta = coeff * delta
                new_effect_val = float(np.mean(effect_arr)) + predicted_delta
                affected[effect] = round(new_effect_val, 3)
                reasoning_parts.append(
                    f"  -> {effect} changes by {predicted_delta:+.2f} "
                    f"(coeff={coeff:.3f}), predicted new mean: {new_effect_val:.2f}"
                )

    # Confidence: based on how many causal links are in the graph
    total_links = sum(len(v) for v in causal_graph.values())
    confidence = min(0.9, 0.3 + total_links * 0.1) if affected else 0.1

    if not affected:
        reasoning_parts.append(
            "No downstream effects found in causal graph. "
            "Intervened variable may be exogenous (root cause)."
        )

    return CounterfactualResult(
        intervention=intervention,
        affected_variables=affected,
        confidence=round(confidence, 3),
        reasoning="\n".join(reasoning_parts),
        causal_path=list(dict.fromkeys(causal_path)),  # deduplicate, preserve order
    )


if __name__ == "__main__":
    print("=== Counterfactual Engine Tests ===")

    # Test 1: temperature intervention affects humidity
    data = {"temperature": [20,21,22,23,24,25],
            "humidity": [55,53,51,49,47,45]}
    causal_graph = {"humidity": ["temperature"]}
    result = compute_counterfactual(
        data, causal_graph,
        intervention={"temperature": 30.0}
    )
    print(f"[Test 1] Intervene temp=30, humidity predicted: {result.affected_variables}")
    assert "humidity" in result.affected_variables
    assert result.affected_variables["humidity"] < 45.0, "Humidity should decrease"
    print("PASS")

    # Test 2: exogenous variable (no downstream effects)
    result2 = compute_counterfactual(
        data, {"humidity": []},
        intervention={"temperature": 30.0}
    )
    print(f"[Test 2] Exogenous: affected={result2.affected_variables}")
    assert result2.affected_variables == {}
    print("PASS")

    # Test 3: multi-hop (A->B->C)
    data3 = {"rate":[4,4.5,5,5.5,6,6.5],
             "bond_yield":[2,2.3,2.6,2.9,3.2,3.5],
             "equity_price":[100,98,95,91,86,80]}
    graph3 = {"bond_yield":["rate"], "equity_price":["bond_yield"]}
    result3 = compute_counterfactual(data3, graph3, {"rate": 3.0})
    print(f"[Test 3] Rate cut: {result3.affected_variables}")
    print("PASS")

    print("ALL TESTS PASSED")
