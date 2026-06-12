"""
OMEGA-CORE Stage 13 — Reality Feedback Engine
==============================================
Closes the scientific loop: Prediction → Actual → Error → Correction.

Without this: Simulation
With this:    Science

Architecture:
    Prediction (from Chef / Agents)
        ↓
    Reality Anchor (actual outcome logged)
        ↓
    Error Calculation
        ↓
    Model Weight Correction
        ↓
    Updated World Model
"""

import json
import math
import random
import datetime
from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass
class PredictionRecord:
    id: str
    domain: str
    variable: str
    predicted_value: float
    actual_value: float | None
    error: float | None
    relative_error_pct: float | None
    correction_factor: float | None
    status: str          # "PENDING" | "VERIFIED" | "REVISED"
    prediction_time: str
    verification_time: str | None
    notes: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ModelCalibration:
    domain: str
    variable: str
    bias: float            # systematic over/under-prediction
    rmse: float            # root mean squared error
    mae: float             # mean absolute error
    r_squared: float       # prediction accuracy
    records_count: int
    calibration_status: str  # "WELL_CALIBRATED" | "OVER_PREDICTING" | "UNDER_PREDICTING" | "NOISY"
    recommendation: str
    computed_at: str

    def to_dict(self) -> dict:
        return asdict(self)


class RealityFeedbackEngine:
    """
    Stage 13 — Reality Feedback Engine (Reality Anchor).

    Stores predictions, accepts actual measurements, calculates errors,
    and derives correction factors to continuously improve model calibration.

    Usage:
        engine = RealityFeedbackEngine()
        rec_id = engine.predict("oncology", "tumor_cells", 46000)
        engine.anchor(rec_id, actual_value=38000)
        cal = engine.calibrate("oncology", "tumor_cells")
    """

    def __init__(self, ledger_path: str = "reports/reality_feedback_ledger.json"):
        self.ledger_path = ledger_path
        self._ledger: list[PredictionRecord] = []
        self._load_ledger()

    # ── Persistence ───────────────────────────────────────────────────────────

    def _load_ledger(self):
        import os
        if os.path.exists(self.ledger_path):
            try:
                with open(self.ledger_path, "r") as f:
                    raw = json.load(f)
                self._ledger = [PredictionRecord(**r) for r in raw]
            except Exception:
                self._ledger = []

    def _save_ledger(self):
        import os
        os.makedirs(os.path.dirname(self.ledger_path), exist_ok=True)
        with open(self.ledger_path, "w") as f:
            json.dump([r.to_dict() for r in self._ledger], f, indent=2)

    # ── Core API ──────────────────────────────────────────────────────────────

    def predict(self, domain: str, variable: str, predicted_value: float,
                notes: str = "") -> str:
        """
        Log a new prediction before the outcome is known.

        Returns:
            record_id (str) to be used when anchoring actual value
        """
        rec_id = f"RF-{domain[:3].upper()}-{datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d%H%M%S%f')[:18]}"
        record = PredictionRecord(
            id=rec_id,
            domain=domain,
            variable=variable,
            predicted_value=predicted_value,
            actual_value=None,
            error=None,
            relative_error_pct=None,
            correction_factor=None,
            status="PENDING",
            prediction_time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            verification_time=None,
            notes=notes,
        )
        self._ledger.append(record)
        self._save_ledger()
        return rec_id

    def anchor(self, record_id: str, actual_value: float) -> PredictionRecord:
        """
        Provide the actual observed value for a prediction.
        Calculates error and correction factor.
        """
        record = next((r for r in self._ledger if r.id == record_id), None)
        if record is None:
            raise ValueError(f"Record '{record_id}' not found in ledger.")

        pred = record.predicted_value
        actual = actual_value
        error = round(actual - pred, 6)
        rel_error = round((error / pred) * 100, 3) if pred != 0 else None

        # Correction factor: multiply future predictions by this
        correction = round(actual / pred, 6) if pred != 0 else 1.0

        record.actual_value = actual
        record.error = error
        record.relative_error_pct = rel_error
        record.correction_factor = correction
        record.status = "VERIFIED"
        record.verification_time = datetime.datetime.now(datetime.timezone.utc).isoformat()
        self._save_ledger()
        return record

    def simulate_anchors(self, domain: str, n_records: int = 10):
        """
        Simulate a batch of predictions + actual values for demonstration.
        Used when real sensor data is not yet available.
        """
        demo_variables = {
            "oncology":         [("tumor_cells", 40000, 15000), ("ki67", 0.70, 0.30)],
            "weather":          [("pressure", 990, 40), ("wind", 120, 60)],
            "macroeconomics":   [("inflation", 3.5, 1.5), ("gdp", 2.1, 0.8)],
            "longevity":        [("telomere_length", 6000, 2000), ("senescent_cells", 0.30, 0.20)],
            "graphene_quantum": [("coherence_time_us", 12, 8), ("defect_density", 0.005, 0.004)],
            "finance":          [("price", 150, 50), ("volatility", 0.25, 0.15)],
        }
        vars_for_domain = demo_variables.get(domain.lower(),
            [("metric_a", 100, 30), ("metric_b", 50, 20)])

        ids = []
        for var, base, spread in vars_for_domain:
            for _ in range(max(1, n_records // len(vars_for_domain))):
                predicted = round(base + random.uniform(-spread * 0.5, spread * 0.5), 4)
                actual    = round(predicted * random.uniform(0.75, 1.25), 4)
                rec_id = self.predict(domain, var, predicted,
                                      notes=f"Simulated batch record — {domain}")
                self.anchor(rec_id, actual)
                ids.append(rec_id)
        return ids

    # ── Calibration ───────────────────────────────────────────────────────────

    def calibrate(self, domain: str = None, variable: str = None) -> list[ModelCalibration]:
        """
        Compute calibration statistics for domain/variable combinations.
        Returns list of ModelCalibration objects.
        """
        verified = [r for r in self._ledger
                    if r.status == "VERIFIED"
                    and (domain is None or r.domain == domain)
                    and (variable is None or r.variable == variable)
                    and r.error is not None]

        # Group by (domain, variable)
        groups: dict[tuple, list] = {}
        for r in verified:
            key = (r.domain, r.variable)
            groups.setdefault(key, []).append(r)

        calibrations = []
        for (dom, var), records in groups.items():
            errors = [r.error for r in records]
            preds  = [r.predicted_value for r in records]
            acts   = [r.actual_value for r in records]

            n = len(errors)
            bias = round(sum(errors) / n, 6)
            mae  = round(sum(abs(e) for e in errors) / n, 6)
            rmse = round(math.sqrt(sum(e**2 for e in errors) / n), 6)

            mean_act = sum(acts) / n
            ss_res = sum((a - p)**2 for a, p in zip(acts, preds))
            ss_tot = sum((a - mean_act)**2 for a in acts)
            r2 = round(1 - ss_res / ss_tot, 4) if ss_tot != 0 else 0.0

            if abs(bias) < mae * 0.1:
                cal_status = "WELL_CALIBRATED"
                rec = "Model is well-calibrated. Continue monitoring."
            elif bias > 0:
                cal_status = "UNDER_PREDICTING"
                rec = f"Model consistently under-predicts by {bias:+.2f}. Apply correction factor +{abs(bias / (sum(preds)/n) * 100):.1f}%."
            else:
                cal_status = "OVER_PREDICTING"
                rec = f"Model consistently over-predicts by {abs(bias):.2f}. Scale predictions down by {abs(bias / (sum(preds)/n) * 100):.1f}%."

            if rmse > mae * 1.5:
                cal_status = "NOISY"
                rec = "High variance in prediction errors. Increase observation frequency."

            calibrations.append(ModelCalibration(
                domain=dom,
                variable=var,
                bias=bias,
                rmse=rmse,
                mae=mae,
                r_squared=max(-1.0, min(1.0, r2)),
                records_count=n,
                calibration_status=cal_status,
                recommendation=rec,
                computed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            ))

        return calibrations

    def get_pending(self) -> list[dict]:
        return [r.to_dict() for r in self._ledger if r.status == "PENDING"]

    def get_verified(self, domain: str = None) -> list[dict]:
        return [r.to_dict() for r in self._ledger
                if r.status == "VERIFIED"
                and (domain is None or r.domain == domain)]

    def get_summary(self) -> dict:
        total    = len(self._ledger)
        verified = len([r for r in self._ledger if r.status == "VERIFIED"])
        pending  = len([r for r in self._ledger if r.status == "PENDING"])
        domains  = list({r.domain for r in self._ledger})

        verified_records = [r for r in self._ledger if r.error is not None]
        avg_abs_error = (
            round(sum(abs(r.error) for r in verified_records) / len(verified_records), 4)
            if verified_records else 0.0
        )
        avg_rel_error = (
            round(sum(abs(r.relative_error_pct or 0) for r in verified_records) / len(verified_records), 2)
            if verified_records else 0.0
        )

        return {
            "total_predictions": total,
            "verified": verified,
            "pending": pending,
            "domains_tracked": domains,
            "avg_absolute_error": avg_abs_error,
            "avg_relative_error_pct": avg_rel_error,
            "ledger_path": self.ledger_path,
            "summary_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }


if __name__ == "__main__":
    engine = RealityFeedbackEngine("reports/reality_feedback_ledger.json")
    print("Simulating 10 anchored records for oncology...")
    engine.simulate_anchors("oncology", 10)
    print("Summary:", json.dumps(engine.get_summary(), indent=2))
    calibrations = engine.calibrate("oncology")
    for cal in calibrations:
        print(json.dumps(cal.to_dict(), indent=2))
