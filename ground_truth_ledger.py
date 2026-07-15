"""
ground_truth_ledger.py — Day 12
Tracks prediction vs actual outcome over time.
Builds an auditable scientific ledger required for publication-grade results.
"""
from __future__ import annotations
import json
import time
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class LedgerEntry:
    entry_id: str
    agent: str
    prediction_id: str
    variable: str
    predicted_value: float
    actual_value: float
    absolute_error: float
    percentage_error: float
    accuracy: float          # 1 - min(pct_error, 1)
    timestamp_predicted: float
    timestamp_validated: float
    lag_seconds: float       # how long between prediction and validation
    domain: str = ""
    notes: str = ""

    def to_dict(self) -> dict:
        return self.__dict__.copy()


class GroundTruthLedger:
    """
    Immutable append-only scientific ledger.
    Records every prediction->actual comparison permanently.
    """

    def __init__(self, path: str = "memory/ledger"):
        self.path = Path(path)
        self.path.mkdir(parents=True, exist_ok=True)
        self._entries: list[LedgerEntry] = []
        self._load()

    def _file(self) -> Path:
        return self.path / "ground_truth_ledger.json"

    def _load(self):
        f = self._file()
        if f.exists():
            raw = json.loads(f.read_text(encoding='utf-8'))
            self._entries = [LedgerEntry(**e) for e in raw]

    def _save(self):
        self._file().write_text(
            json.dumps([e.to_dict() for e in self._entries], indent=2),
            encoding='utf-8'
        )

    def record(
        self,
        agent: str,
        prediction_id: str,
        variable: str,
        predicted: float,
        actual: float,
        timestamp_predicted: float,
        domain: str = "",
        notes: str = "",
    ) -> LedgerEntry:
        now = time.time()
        abs_err = abs(predicted - actual)
        pct_err = abs_err / abs(predicted) if predicted != 0 else abs_err
        accuracy = max(0.0, 1.0 - min(pct_err, 1.0))

        entry = LedgerEntry(
            entry_id=f"led_{len(self._entries):06d}",
            agent=agent,
            prediction_id=prediction_id,
            variable=variable,
            predicted_value=round(predicted, 4),
            actual_value=round(actual, 4),
            absolute_error=round(abs_err, 4),
            percentage_error=round(pct_err, 4),
            accuracy=round(accuracy, 4),
            timestamp_predicted=timestamp_predicted,
            timestamp_validated=now,
            lag_seconds=round(now - timestamp_predicted, 1),
            domain=domain,
            notes=notes,
        )
        self._entries.append(entry)
        self._save()
        return entry

    def accuracy_by_agent(self) -> dict[str, float]:
        by_agent: dict[str, list] = {}
        for e in self._entries:
            by_agent.setdefault(e.agent, []).append(e.accuracy)
        return {a: round(sum(v)/len(v), 3) for a, v in by_agent.items()}

    def accuracy_by_variable(self) -> dict[str, float]:
        by_var: dict[str, list] = {}
        for e in self._entries:
            by_var.setdefault(e.variable, []).append(e.accuracy)
        return {v: round(sum(vals)/len(vals), 3) for v, vals in by_var.items()}

    def recent(self, n: int = 20) -> list[LedgerEntry]:
        return sorted(self._entries, key=lambda e: -e.timestamp_validated)[:n]

    def summary(self) -> dict:
        if not self._entries:
            return {"total_entries": 0, "overall_accuracy": None}
        overall = sum(e.accuracy for e in self._entries) / len(self._entries)
        return {
            "total_entries": len(self._entries),
            "overall_accuracy": round(overall, 3),
            "accuracy_by_agent": self.accuracy_by_agent(),
            "accuracy_by_variable": self.accuracy_by_variable(),
        }


if __name__ == "__main__":
    import tempfile
    print("=== Ground Truth Ledger Tests ===")

    with tempfile.TemporaryDirectory() as tmp:
        ledger = GroundTruthLedger(path=tmp)

        e1 = ledger.record("finance", "pred_001", "gold", 1920.0, 1935.0,
                           time.time()-3600, domain="finance")
        e2 = ledger.record("finance", "pred_002", "vix", 25.0, 28.0,
                           time.time()-7200, domain="finance")
        e3 = ledger.record("weather_manifold", "pred_003", "temperature",
                           28.5, 27.8, time.time()-1800, domain="weather")

        s = ledger.summary()
        print(f"[PASS] Total entries: {s['total_entries']}")
        print(f"[PASS] Overall accuracy: {s['overall_accuracy']}")
        print(f"[PASS] By agent: {s['accuracy_by_agent']}")
        print(f"[PASS] By variable: {s['accuracy_by_variable']}")

        assert s["total_entries"] == 3
        assert s["accuracy_by_agent"]["finance"] > 0.8  # gold 1920 vs 1935 = 99.2% acc
        assert e1.lag_seconds > 0

        # Test persistence
        ledger2 = GroundTruthLedger(path=tmp)
        assert len(ledger2._entries) == 3
        print("[PASS] Persistence confirmed")

    print("ALL TESTS PASSED")
