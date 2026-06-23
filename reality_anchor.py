"""
reality_anchor.py
==================
Gap 4 fix: Reality Anchor — closes the prediction→reality feedback loop.

When an agent makes a prediction, it's stored here.
When new sensor data arrives, actual outcomes are compared to predictions.
Theory confidence is automatically adjusted based on accuracy.

This is what separates a hypothesis generator from a scientific platform.
"""

from __future__ import annotations
import json
import time
import uuid
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class Prediction:
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    agent: str = ""
    theory_id: str = ""
    prediction_text: str = ""
    predicted_variables: dict[str, float] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    horizon_seconds: float = 3600.0   # how long before we check reality
    actual_values: dict[str, float] = field(default_factory=dict)
    accuracy_score: Optional[float] = None
    validated: bool = False
    notes: str = ""

    def to_dict(self) -> dict:
        return self.__dict__.copy()

    @classmethod
    def from_dict(cls, d: dict) -> "Prediction":
        return cls(**d)


class RealityAnchor:
    """
    Stores predictions, receives real measurements, computes accuracy,
    and feeds confidence adjustments back to the TheoryEngine or MemoryLayer.

    Usage:
        anchor = RealityAnchor("C:/Universal_Lab_AP_Phillips/memory/reality")

        # When agent makes a prediction:
        pred_id = anchor.record_prediction(
            agent="finance",
            theory_id="abc123",
            prediction_text="Gold will rise if VIX exceeds 25",
            predicted_variables={"gold": 1920.0, "vix_threshold": 25.0}
        )

        # When real data arrives:
        accuracy = anchor.validate(pred_id, actual={"gold": 1935.0, "vix": 27.0})
    """

    def __init__(self, path: str = "memory/reality"):
        self.path = Path(path)
        self.path.mkdir(parents=True, exist_ok=True)
        self._predictions: dict[str, Prediction] = {}
        self._load()

    def _file(self) -> Path:
        return self.path / "predictions.json"

    def _load(self):
        f = self._file()
        if f.exists():
            raw = json.loads(f.read_text())
            self._predictions = {k: Prediction.from_dict(v) for k, v in raw.items()}

    def _save(self):
        self._file().write_text(
            json.dumps({k: v.to_dict() for k, v in self._predictions.items()}, indent=2)
        )

    def record_prediction(
        self,
        agent: str,
        prediction_text: str,
        predicted_variables: dict[str, float],
        theory_id: str = "",
        horizon_seconds: float = 3600.0,
    ) -> str:
        pred = Prediction(
            agent=agent,
            theory_id=theory_id,
            prediction_text=prediction_text,
            predicted_variables=predicted_variables,
            horizon_seconds=horizon_seconds,
        )
        self._predictions[pred.id] = pred
        self._save()
        return pred.id

    def validate(self, pred_id: str, actual: dict[str, float]) -> float:
        """
        Compare predicted values to actual measurements.
        Returns accuracy score 0-1 (1 = perfect prediction).
        Uses mean absolute percentage error across all predicted variables.
        """
        if pred_id not in self._predictions:
            raise KeyError(f"Unknown prediction: {pred_id}")

        pred = self._predictions[pred_id]
        pred.actual_values = actual
        pred.validated = True

        errors = []
        for var, predicted_val in pred.predicted_variables.items():
            if var in actual and predicted_val != 0:
                actual_val = actual[var]
                pct_error = abs(predicted_val - actual_val) / abs(predicted_val)
                errors.append(min(pct_error, 1.0))

        accuracy = 1.0 - (sum(errors) / len(errors)) if errors else 0.5
        pred.accuracy_score = round(accuracy, 3)
        self._save()
        return pred.accuracy_score

    def pending_validations(self) -> list[Prediction]:
        """Return predictions past their horizon that haven't been validated."""
        now = time.time()
        return [
            p for p in self._predictions.values()
            if not p.validated and (now - p.created_at) > p.horizon_seconds
        ]

    def accuracy_by_agent(self) -> dict[str, float]:
        """Average accuracy per agent across all validated predictions."""
        by_agent: dict[str, list[float]] = {}
        for p in self._predictions.values():
            if p.validated and p.accuracy_score is not None:
                by_agent.setdefault(p.agent, []).append(p.accuracy_score)
        return {a: round(sum(s)/len(s), 3) for a, s in by_agent.items()}

    def recent(self, n: int = 10) -> list[Prediction]:
        return sorted(self._predictions.values(), key=lambda p: -p.created_at)[:n]

    def summary(self) -> dict[str, Any]:
        total = len(self._predictions)
        validated = sum(1 for p in self._predictions.values() if p.validated)
        pending = len(self.pending_validations())
        return {
            "total_predictions": total,
            "validated": validated,
            "pending": pending,
            "accuracy_by_agent": self.accuracy_by_agent(),
        }
