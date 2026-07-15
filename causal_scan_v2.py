"""
causal_scan_v2.py
==================
Upgraded causal discovery tool for the OMEGA harness.

Replaces the simple pairwise correlation in harness.py with:
1. Same-timestep correlation (original behaviour, preserved)
2. Lag-1 and Lag-2 tests   -> does A PRECEDE B? (causal lead)
3. Hyperedge detection     -> does (A AND B) jointly drive C?
4. Regime change detection -> does the relationship flip mid-series?
5. Trend extraction        -> rising / falling / flat / volatile
6. Irreducibility flag     -> variables that resist explanation

Output is a structured dict the Hypothesis Agent and Discovery Planner
can use to generate mechanistically grounded hypotheses rather than
just noting "A correlates with B".

Drop-in replacement: register as "causal_scan" in ToolRegistry.
Same function signature as the original (data: dict, **_) -> dict,
so no changes needed anywhere else in the harness.
"""

from __future__ import annotations
import numpy as np


def causal_scan_v2(data: dict, **_) -> dict:
    """
    Upgraded causal discovery scan.

    Parameters
    ----------
    data : dict  {variable_name: [numeric values ...]}

    Returns
    -------
    dict with keys: variables, n_observations, trends,
    same_step_correlations, lag_leads, lag_details, hyperedges,
    regime_changes, irreducible_variables, candidate_causal_graph,
    summary
    """
    if not data:
        return {"error": "no data provided"}

    variables = [k for k, v in data.items()
                 if isinstance(v, (list, tuple)) and len(v) >= 4]
    if len(variables) < 2:
        return {"variables": variables, "error": "need at least 2 variables with 4+ points"}

    arrays = {v: np.array(data[v], dtype=float) for v in variables}
    n = min(len(a) for a in arrays.values())
    arrays = {v: a[:n] for v, a in arrays.items()}

    # Guard against zero-variance (constant) columns -- corrcoef on a
    # constant array produces NaN/warnings, not a crash, but we want
    # clean output. Track them and exclude from correlation-based checks
    # while still reporting them as a flat trend.
    zero_variance = {v for v, a in arrays.items() if np.std(a) == 0}

    THRESH = 0.50
    LAG_BOOST = 0.05

    # ── 1. Trends ─────────────────────────────────────────────────
    trends: dict[str, str] = {}
    for v, a in arrays.items():
        slope = np.polyfit(np.arange(n), a, 1)[0]
        std = np.std(a)
        mean = np.mean(a) if np.mean(a) != 0 else 1e-9
        cv = std / abs(mean)
        if cv > 0.25 and abs(slope) < std * 0.1:
            trends[v] = "volatile"
        elif slope > std * 0.05:
            trends[v] = "rising"
        elif slope < -std * 0.05:
            trends[v] = "falling"
        else:
            trends[v] = "flat"

    # ── 2. Same-step correlations ─────────────────────────────────
    same_step: dict[str, float] = {}
    for i, va in enumerate(variables):
        for vb in variables[i + 1:]:
            if va in zero_variance or vb in zero_variance:
                continue
            r = float(np.corrcoef(arrays[va], arrays[vb])[0, 1])
            if abs(r) >= THRESH:
                same_step[f"{va}<->{vb}"] = round(r, 3)

    # ── 3. Lag tests (A leads B by 1 or 2 steps) ─────────────────
    lag_leads: dict[str, list[str]] = {v: [] for v in variables}
    lag_details: dict[str, dict] = {}
    for va in variables:
        for vb in variables:
            if va == vb:
                continue
            if va in zero_variance or vb in zero_variance:
                continue
            a, b = arrays[va], arrays[vb]
            r0 = abs(float(np.corrcoef(a, b)[0, 1]))
            best_lag, best_r = 0, r0
            for lag in (1, 2):
                if n > lag + 2:
                    r_lag = abs(float(np.corrcoef(a[:-lag], b[lag:])[0, 1]))
                    if r_lag > best_r + LAG_BOOST:
                        best_lag, best_r = lag, r_lag
            if best_lag > 0 and best_r >= THRESH:
                lag_leads[va].append(vb)
                lag_details[f"{va}->{vb}"] = {
                    "lag_steps": best_lag,
                    "lag_r": round(best_r, 3),
                    "same_step_r": round(r0, 3),
                }

    # ── 4. Hyperedge detection ────────────────────────────────────
    hyperedges: list[dict] = []
    for vc in variables:
        if vc in zero_variance:
            continue
        c = arrays[vc]
        for i, va in enumerate(variables):
            if va == vc or va in zero_variance:
                continue
            for vb in variables[i + 1:]:
                if vb == vc or vb in zero_variance:
                    continue
                a, b = arrays[va], arrays[vb]
                ra = abs(float(np.corrcoef(a, c)[0, 1]))
                rb = abs(float(np.corrcoef(b, c)[0, 1]))
                joint = (a - a.mean()) * (b - b.mean())
                if joint.std() > 0:
                    rj = abs(float(np.corrcoef(joint, c)[0, 1]))
                    if rj >= THRESH and rj > ra + 0.15 and rj > rb + 0.15:
                        hyperedges.append({
                            "drivers": [va, vb],
                            "target": vc,
                            "joint_r": round(rj, 3),
                            "solo_r": {va: round(ra, 3), vb: round(rb, 3)},
                        })

    # ── 5. Regime change detection ────────────────────────────────
    regime_changes: list[str] = []
    mid = n // 2
    for i, va in enumerate(variables):
        for vb in variables[i + 1:]:
            if va in zero_variance or vb in zero_variance:
                continue
            a, b = arrays[va], arrays[vb]
            if mid < 3:
                continue
            r_first = float(np.corrcoef(a[:mid], b[:mid])[0, 1])
            r_second = float(np.corrcoef(a[mid:], b[mid:])[0, 1])
            if abs(r_first) >= THRESH and abs(r_second) >= THRESH:
                if r_first * r_second < 0:
                    regime_changes.append(
                        f"{va}<->{vb}: r flips {r_first:+.2f} -> {r_second:+.2f} at step {mid}"
                    )

    # ── 6. Irreducibility flag ────────────────────────────────────
    irreducible: list[str] = []
    for v in variables:
        if v in zero_variance:
            continue
        a = arrays[v]
        max_r = 0.0
        for v2 in variables:
            if v2 != v and v2 not in zero_variance:
                r = abs(float(np.corrcoef(a, arrays[v2])[0, 1]))
                max_r = max(max_r, r)
        if max_r < THRESH and n > 4:
            ac1 = float(np.corrcoef(a[:-1], a[1:])[0, 1])
            if abs(ac1) < 0.3:
                irreducible.append(v)

    # ── 7. Candidate causal graph ──────────────────────────────────
    causal_graph: dict[str, list[str]] = {v: [] for v in variables}
    for cause, effects in lag_leads.items():
        for effect in effects:
            if cause not in causal_graph[effect]:
                causal_graph[effect].append(cause)
    for key in same_step:
        va, vb = key.split("<->")
        if not causal_graph[va] and not causal_graph[vb]:
            causal_graph[vb].append(va)

    # ── 8. Human-readable summary ──────────────────────────────────
    summary: list[str] = []
    for key, r in same_step.items():
        va, vb = key.split("<->")
        direction = "positive" if r > 0 else "negative"
        strength = "strong" if abs(r) > 0.8 else "moderate"
        summary.append(f"{va} and {vb} have a {strength} {direction} relationship (r={r})")
    for cause, effects in lag_leads.items():
        for effect in effects:
            d = lag_details.get(f"{cause}->{effect}", {})
            summary.append(
                f"{cause} LEADS {effect} by {d.get('lag_steps', '?')} step(s) "
                f"(r={d.get('lag_r', '?')}) -- suggests {cause} may CAUSE {effect}"
            )
    for he in hyperedges:
        summary.append(
            f"HYPEREDGE: {he['drivers']} jointly drive {he['target']} "
            f"(joint r={he['joint_r']}) -- neither alone is sufficient"
        )
    for rc in regime_changes:
        summary.append(f"REGIME CHANGE detected: {rc}")
    for irr in irreducible:
        summary.append(f"IRREDUCIBLE: {irr} shows no stable causal relationship -- may be exogenous/random")
    for cv in zero_variance:
        summary.append(f"CONSTANT: {cv} did not vary in this dataset -- held fixed, cannot test as a cause or effect here")

    return {
        "variables": variables,
        "n_observations": n,
        "trends": trends,
        "held_constant": sorted(zero_variance),
        "same_step_correlations": same_step,
        "lag_leads": {k: v for k, v in lag_leads.items() if v},
        "lag_details": lag_details,
        "hyperedges": hyperedges,
        "regime_changes": regime_changes,
        "irreducible_variables": irreducible,
        "candidate_causal_graph": causal_graph,
        "summary": summary,
    }


# ── Self-test ─────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Test 1: simple lag relationship (A leads B by 1 step) ===")
    n = 30
    a = [float(i % 10) for i in range(n)]
    b = [0.0] + a[:-1]  # B is A shifted by 1 -> A leads B by 1 step
    result = causal_scan_v2({"a": a, "b": b})
    print("Lag leads:", result["lag_leads"])
    print("Summary:", result["summary"])
    assert "a" in result["lag_leads"], "FAILED: should detect a leads b"
    print("PASS\n")

    print("=== Test 2: hyperedge (C depends on A*B jointly, not on either alone) ===")
    import random
    random.seed(42)
    rng = np.random.default_rng(42)
    a2 = rng.normal(0, 1, 40)
    b2 = rng.normal(0, 1, 40)
    c2 = (a2 - a2.mean()) * (b2 - b2.mean()) + rng.normal(0, 0.1, 40)
    result2 = causal_scan_v2({"a2": a2.tolist(), "b2": b2.tolist(), "c2": c2.tolist()})
    print("Hyperedges found:", result2["hyperedges"])
    print("Same-step corr (should be weak/absent for a2,c2 and b2,c2):", result2["same_step_correlations"])
    print("PASS (hyperedge logic executes without error)\n")

    print("=== Test 3: regime change (correlation flips sign mid-series) ===")
    n3 = 40
    x3 = list(range(n3))
    y3 = [i for i in range(n3 // 2)] + [n3 // 2 - i for i in range(n3 // 2)]
    result3 = causal_scan_v2({"x3": x3, "y3": y3})
    print("Regime changes:", result3["regime_changes"])
    assert len(result3["regime_changes"]) > 0, "FAILED: should detect regime change"
    print("PASS\n")

    print("=== Test 4: irreducible variable (pure noise, no relationship) ===")
    rng2 = np.random.default_rng(7)
    noise = rng2.normal(0, 1, 30).tolist()
    trend = list(range(30))
    result4 = causal_scan_v2({"noise": noise, "trend": trend})
    print("Irreducible:", result4["irreducible_variables"])
    assert "noise" in result4["irreducible_variables"], "FAILED: should flag noise as irreducible"
    print("PASS\n")

    print("=== Test 5: backward compatibility (same-step correlation still works) ===")
    temp = [20, 21, 22, 23, 24, 25]
    humidity = [55, 53, 51, 49, 47, 45]
    result5 = causal_scan_v2({"temperature": temp, "humidity": humidity})
    print("Same-step correlations:", result5["same_step_correlations"])
    assert abs(result5["same_step_correlations"]["temperature<->humidity"]) > 0.9
    print("PASS\n")

    print("ALL TESTS PASSED")

    print("\n=== Test 6: constant variable (exact scenario from tonight's live run) ===")
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("error")  # promote any RuntimeWarning to an error
        result6 = causal_scan_v2({
            "temperature": [20, 21, 22, 23, 24, 25],
            "humidity": [55, 53, 51, 49, 47, 45],
            "pressure": [1013, 1013, 1013, 1013, 1013, 1013],
        })
    print("Held constant:", result6["held_constant"])
    print("Same-step correlations:", result6["same_step_correlations"])
    print("Summary:", result6["summary"])
    assert "pressure" in result6["held_constant"], "FAILED: pressure should be flagged as constant"
    assert "temperature<->humidity" in result6["same_step_correlations"], "FAILED: temp/humidity correlation lost"
    assert not any("pressure" in k for k in result6["same_step_correlations"]), "FAILED: pressure leaked into correlations"
    print("PASS -- no RuntimeWarning raised, constant variable correctly isolated\n")

    print("ALL 6 TESTS PASSED")
