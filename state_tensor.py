"""
state_tensor.py — 5D State Tensor Engine
Maps any domain's sensor data into: H, K, E, B, R coordinates.
"""
from __future__ import annotations
import numpy as np
from dataclasses import dataclass
from typing import Any


@dataclass
class StateTensor:
    entropy_H: float
    coherence_K: float
    emergence_E: float
    bifurcation_B: float
    reducibility_R: float
    domain: str = ""
    n_variables: int = 0
    n_observations: int = 0
    dominant_driver: str = ""
    interpretation: str = ""

    def to_dict(self) -> dict:
        return {k: round(v, 3) if isinstance(v, float) else v
                for k, v in self.__dict__.items()}

    def summary(self) -> str:
        lines = [f"State Tensor [{self.domain}]",
            f"  H (Entropy):      {self.entropy_H:.2f}",
            f"  K (Coherence):    {self.coherence_K:.2f}",
            f"  E (Emergence):    {self.emergence_E:.2f}",
            f"  B (Bifurcation):  {self.bifurcation_B:.2f}  {'NEAR TIPPING POINT' if self.bifurcation_B > 0.7 else ''}",
            f"  R (Reducibility): {self.reducibility_R:.2f}",
            f"  Driver: {self.dominant_driver}",
            f"  {self.interpretation}"]
        return "\n".join(lines)


def _safe_r(a, b):
    if np.std(a) == 0 or np.std(b) == 0:
        return 0.0
    return float(np.corrcoef(a, b)[0, 1])


def compute_state_tensor(data: dict, domain: str = "") -> StateTensor:
    variables = [k for k, v in data.items()
                 if isinstance(v, (list, tuple)) and len(v) >= 4]
    if not variables:
        return StateTensor(0.5, 0.5, 0.5, 0.5, 0.5,
                          domain=domain, interpretation="Insufficient data")

    arrays = {v: np.array(data[v], dtype=float) for v in variables}
    n = min(len(a) for a in arrays.values())
    arrays = {v: a[:n] for v, a in arrays.items()}
    nv = len(variables)

    # H: Entropy — coefficient of variation per variable
    entropies = []
    for v, a in arrays.items():
        mean = abs(np.mean(a)) or 1e-9
        cv = np.std(a) / mean
        trend = np.polyval(np.polyfit(np.arange(n), a, 1), np.arange(n))
        residual = np.std(a - trend) / (np.std(a) + 1e-9)
        entropies.append(min(1.0, cv * 0.6 + residual * 0.4))
    entropy_H = float(np.clip(np.mean(entropies), 0, 1))

    # K: Coherence — avg absolute pairwise correlation
    var_list = list(variables)
    if nv < 2:
        coherence_K = 0.5
    else:
        corrs = [abs(_safe_r(arrays[var_list[i]], arrays[var_list[j]]))
                 for i in range(nv) for j in range(i+1, nv)]
        coherence_K = float(np.clip(np.mean(corrs), 0, 1))

    # E: Emergence — joint vs individual variance
    if nv < 2:
        emergence_E = 0.0
    else:
        stacked = np.stack([arrays[v] for v in variables])
        joint_var = float(np.var(np.mean(stacked, axis=0)))
        mean_indiv = float(np.mean([np.var(arrays[v]) for v in variables]))
        emergence_E = float(np.clip(joint_var / (mean_indiv + joint_var + 1e-9), 0, 1))

    # B: Bifurcation — variance acceleration + correlation sign flip
    mid = n // 2
    bif_signals = []
    if mid >= 3:
        for v, a in arrays.items():
            v1, v2 = np.var(a[:mid]), np.var(a[mid:])
            if v1 > 0:
                bif_signals.append(min(1.0, (v2 / (v1 + 1e-9) - 1.0) / 3.0))
        if nv >= 2:
            for i in range(min(nv, 3)):
                for j in range(i+1, min(nv, 4)):
                    r1 = _safe_r(arrays[var_list[i]][:mid], arrays[var_list[j]][:mid])
                    r2 = _safe_r(arrays[var_list[i]][mid:], arrays[var_list[j]][mid:])
                    if r1 * r2 < 0:  # sign flip -- strong bifurcation signal
                        bif_signals.append(0.9)
                        bif_signals.append(0.9)  # double-weight sign flips
                    elif abs(r1 - r2) > 0.4:
                        bif_signals.append(0.5)
    bifurcation_B = float(np.clip(np.mean(bif_signals) if bif_signals else 0.1, 0, 1))

    # R: Reducibility — how much variance is explained by linear trend
    r_scores = []
    for v, a in arrays.items():
        if np.std(a) == 0:
            r_scores.append(1.0)
            continue
        trend = np.polyval(np.polyfit(np.arange(n), a, 1), np.arange(n))
        r_scores.append(float(np.clip(1.0 - np.var(a - trend) / (np.var(a) + 1e-9), 0, 1)))
    reducibility_R = float(np.clip(np.mean(r_scores), 0, 1))

    # Dominant driver
    contributions = {v: abs(np.polyfit(np.arange(n), arrays[v], 1)[0]) *
                    (np.std(arrays[v]) / (abs(np.mean(arrays[v])) + 1e-9))
                    for v in variables}
    dominant = max(contributions, key=contributions.get)

    interp = _interpret(entropy_H, coherence_K, emergence_E, bifurcation_B, reducibility_R)

    return StateTensor(entropy_H, coherence_K, emergence_E, bifurcation_B, reducibility_R,
                      domain=domain, n_variables=nv, n_observations=n,
                      dominant_driver=dominant, interpretation=interp)


def _interpret(H, K, E, B, R):
    if B > 0.75: return "CRITICAL: Tipping point approaching — regime change imminent"
    if H > 0.75 and K < 0.3: return "HIGH DISORDER: Variables decoupled and chaotic"
    if K > 0.8 and H < 0.3: return "LOCKED STATE: Stable attractor — high coherence"
    if E > 0.7 and K < 0.4: return "EMERGENT: New collective patterns forming"
    if R > 0.8: return "REDUCIBLE: Simple trends explain the system well"
    if R < 0.2: return "IRREDUCIBLE: Complex nonlinear dynamics"
    if H > 0.5 and B > 0.5: return "TRANSITIONAL: Increasing disorder near regime change"
    return "MODERATE: No critical signals detected"


if __name__ == "__main__":
    print("=== State Tensor Tests ===")

    t1 = compute_state_tensor({"temp":[20,21,22,23,24,25,26,27,28,29],
        "hum":[55,53,51,49,47,45,43,41,39,37]}, domain="weather")
    assert t1.coherence_K > 0.7 and t1.reducibility_R > 0.7
    print(f"[PASS] Clean linear: K={t1.coherence_K:.2f} R={t1.reducibility_R:.2f}")

    t2 = compute_state_tensor({"a":[2,45,3,88,5,120,8,200,4,95],
        "b":[35,90,38,95,40,98,37,99,36,92]}, domain="adversarial")
    assert t2.entropy_H > 0.3
    print(f"[PASS] Volatile: H={t2.entropy_H:.2f} B={t2.bifurcation_B:.2f}")

    # Regime change: relationship flips sign mid-series
    t3 = compute_state_tensor({"x":[1,2,3,4,5,6,7,8,9,10],
        "y":[1,2,3,4,5,4,3,2,1,0]}, domain="test")
    assert t3.bifurcation_B > 0.3, f"Got B={t3.bifurcation_B}"
    print(f"[PASS] Regime change: B={t3.bifurcation_B:.2f}")

    t4 = compute_state_tensor({"x":[1,2]}, domain="edge")
    assert "Insufficient" in t4.interpretation
    print(f"[PASS] Edge case: {t4.interpretation}")

    print("ALL TESTS PASSED")
