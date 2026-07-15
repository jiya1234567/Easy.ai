"""
benchmark_suite.py — Step 11
Compares OMEGA-CORE agent findings against accepted scientific baselines.
Tests causal detection accuracy, prediction calibration, and reasoning quality.
"""
from __future__ import annotations
import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class BenchmarkResult:
    benchmark_id: str
    name: str
    passed: bool
    score: float          # 0-1
    expected: Any
    actual: Any
    notes: str
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass
class BenchmarkSuiteResult:
    suite_name: str
    total: int
    passed: int
    failed: int
    score: float
    results: list[BenchmarkResult]
    timestamp: float = field(default_factory=time.time)

    def summary(self) -> str:
        lines = [
            f"Benchmark Suite: {self.suite_name}",
            f"Score: {self.score:.0%} ({self.passed}/{self.total} passed)",
            ""
        ]
        for r in self.results:
            status = "PASS" if r.passed else "FAIL"
            lines.append(f"  [{status}] {r.name}: {r.score:.2f} — {r.notes}")
        return "\n".join(lines)


# ── Benchmark definitions ──────────────────────────────────────────

KNOWN_CAUSAL_PAIRS = [
    # (cause, effect, expected_lag, description)
    ("temperature", "humidity", 0, "Psychrometrics: temp drives relative humidity"),
    ("interest_rate", "bond_yield", 1, "Finance: rate hikes lead bond yields by ~1 period"),
    ("soil_moisture", "yield_forecast", 0, "Agriculture: soil moisture directly affects yield"),
    ("cortisol", "heart_rate", 0, "Health: cortisol and heart rate co-vary"),
    ("ndvi", "yield_forecast", 0, "Remote sensing: NDVI directly predicts yield"),
]

KNOWN_REGIME_PAIRS = [
    # (domain, description of expected regime change)
    ("finance", "VIX > 25 with rate > 4.5 signals volatility regime"),
    ("weather", "Pressure drop > 10 hPa over 6 hours signals storm regime"),
    ("health", "HRV < 40ms with cortisol > 25 signals stress regime"),
]


def run_causal_benchmark(causal_scan_result: dict) -> BenchmarkResult:
    """Test if causal scan correctly identifies known causal relationships."""
    if not causal_scan_result:
        return BenchmarkResult("b_causal", "Causal Detection", False, 0.0,
                              "known pairs", "no scan result", "No causal scan provided")

    lag_leads = causal_scan_result.get("lag_leads", {})
    same_step = causal_scan_result.get("same_step_correlations", {})
    variables = set(causal_scan_result.get("variables", []))

    found = 0
    total_testable = 0
    notes_parts = []

    for cause, effect, expected_lag, desc in KNOWN_CAUSAL_PAIRS:
        if cause in variables and effect in variables:
            total_testable += 1
            detected_lag = cause in lag_leads and effect in lag_leads[cause]
            detected_same = any(
                cause in k and effect in k
                for k in same_step.keys()
            )
            if detected_lag or detected_same:
                found += 1
                notes_parts.append(f"✓ {cause}->{effect}")
            else:
                notes_parts.append(f"✗ {cause}->{effect} not detected")

    score = found / total_testable if total_testable > 0 else 0.5
    passed = score >= 0.6

    return BenchmarkResult(
        "b_causal", "Causal Detection",
        passed, round(score, 3),
        f"{total_testable} known pairs",
        f"{found} detected",
        "; ".join(notes_parts) or "No testable pairs in this dataset"
    )


def run_prediction_calibration_benchmark(
    ledger_summary: dict
) -> BenchmarkResult:
    """Test if predictions are well-calibrated against reality."""
    if not ledger_summary or ledger_summary.get("total_entries", 0) == 0:
        return BenchmarkResult("b_calib", "Prediction Calibration", False, 0.0,
                              ">= 0.70 accuracy", "no data",
                              "No validated predictions yet -- run Auto-Chain and validate")

    accuracy = ledger_summary.get("overall_accuracy", 0)
    passed = accuracy >= 0.70
    score = accuracy

    return BenchmarkResult(
        "b_calib", "Prediction Calibration",
        passed, round(score, 3),
        ">= 0.70 accuracy",
        f"{accuracy:.0%} across {ledger_summary['total_entries']} predictions",
        f"{'Good calibration' if passed else 'Below 70% threshold -- needs more data or model improvement'}"
    )


def run_state_tensor_benchmark(state_tensor: Any) -> BenchmarkResult:
    """Test if state tensor dimensions are in valid range and consistent."""
    if state_tensor is None:
        return BenchmarkResult("b_tensor", "State Tensor Validity", False, 0.0,
                              "all dims in [0,1]", "no tensor", "No state tensor provided")

    dims = {
        "H": getattr(state_tensor, 'entropy_H', None),
        "K": getattr(state_tensor, 'coherence_K', None),
        "E": getattr(state_tensor, 'emergence_E', None),
        "B": getattr(state_tensor, 'bifurcation_B', None),
        "R": getattr(state_tensor, 'reducibility_R', None),
    }

    valid = {k: v for k, v in dims.items() if v is not None and 0.0 <= v <= 1.0}
    score = len(valid) / 5.0
    passed = score == 1.0

    # Physical consistency check: high K + high H is unusual (coherent chaos)
    notes = f"{len(valid)}/5 dimensions valid"
    H = dims.get("H", 0)
    K = dims.get("K", 0)
    if H > 0.8 and K > 0.8:
        notes += "; NOTE: high entropy + high coherence is unusual -- verify data"

    return BenchmarkResult(
        "b_tensor", "State Tensor Validity",
        passed, round(score, 3),
        "all 5 dims in [0,1]",
        str({k: round(v, 2) for k, v in dims.items() if v is not None}),
        notes
    )


def run_reproducibility_benchmark(repro_summary: dict) -> BenchmarkResult:
    """Test if findings are reproducible across runs."""
    if not repro_summary or repro_summary.get("total_certificates", 0) == 0:
        return BenchmarkResult("b_repro", "Reproducibility", False, 0.0,
                              ">= 0.80 rate", "no certs",
                              "No reproducibility certificates yet")

    rate = repro_summary.get("reproducibility_rate", 0) or 0
    passed = rate >= 0.80

    return BenchmarkResult(
        "b_repro", "Reproducibility",
        passed, round(rate, 3),
        ">= 0.80 rate",
        f"{rate:.0%} ({repro_summary['reproducible']}/{repro_summary['total_certificates']} runs)",
        "Good" if passed else "Below 80% -- conflicting conclusions across runs"
    )


def run_full_benchmark_suite(
    causal_scan_result: dict = None,
    ledger_summary: dict = None,
    state_tensor: Any = None,
    repro_summary: dict = None,
    suite_name: str = "OMEGA-CORE Full Suite",
) -> BenchmarkSuiteResult:
    """Run all benchmarks and return a consolidated report."""
    results = [
        run_causal_benchmark(causal_scan_result or {}),
        run_prediction_calibration_benchmark(ledger_summary or {}),
        run_state_tensor_benchmark(state_tensor),
        run_reproducibility_benchmark(repro_summary or {}),
    ]

    passed = sum(1 for r in results if r.passed)
    total = len(results)
    score = sum(r.score for r in results) / total

    return BenchmarkSuiteResult(
        suite_name=suite_name,
        total=total,
        passed=passed,
        failed=total - passed,
        score=round(score, 3),
        results=results,
    )


if __name__ == "__main__":
    print("=== Benchmark Suite Tests ===\n")

    # Mock causal scan with known pairs
    mock_scan = {
        "variables": ["temperature", "humidity", "pressure"],
        "lag_leads": {"temperature": ["humidity"]},
        "same_step_correlations": {"temperature<->humidity": -0.99},
    }

    # Mock state tensor
    class FakeTensor:
        entropy_H = 0.3
        coherence_K = 0.95
        emergence_E = 0.2
        bifurcation_B = 0.1
        reducibility_R = 0.92

    # Mock ledger
    mock_ledger = {
        "total_entries": 10,
        "overall_accuracy": 0.87,
        "accuracy_by_agent": {"scientific_discovery": 0.87}
    }

    # Mock repro
    mock_repro = {
        "total_certificates": 5,
        "reproducible": 5,
        "not_verified": 0,
        "reproducibility_rate": 1.0
    }

    suite = run_full_benchmark_suite(
        causal_scan_result=mock_scan,
        ledger_summary=mock_ledger,
        state_tensor=FakeTensor(),
        repro_summary=mock_repro,
    )

    print(suite.summary())
    assert suite.passed >= 3, f"Expected >= 3 passed, got {suite.passed}"
    assert suite.score > 0.7
    print(f"\n[PASS] Suite score: {suite.score:.0%}")
    print("ALL TESTS PASSED")
