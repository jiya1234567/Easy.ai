"""
provenance.py — Day 10
Every result traceable to: agent, run_id, data_hash, timestamp, models used.
Required for publication-grade science reproducibility.
"""
from __future__ import annotations
import json
import time
import hashlib
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ProvenanceRecord:
    record_id: str
    agent: str
    run_id: str
    timestamp: float
    primary_model: str
    challenger_model: str
    data_hash: str           # SHA256 of input data
    query_hash: str          # SHA256 of query text
    final_answer_hash: str   # SHA256 of output
    causal_scan_summary: list[str]
    prediction_ids: list[str]
    memory_entries_before: int
    memory_entries_after: int

    def to_dict(self) -> dict:
        return self.__dict__.copy()

    def citation(self) -> str:
        ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.timestamp))
        return (f"OMEGA-CORE [{self.agent}] run={self.run_id} "
                f"models={self.primary_model}x{self.challenger_model} "
                f"data={self.data_hash[:8]} ts={ts}")


class ProvenanceTracker:
    def __init__(self, path: str = "memory/provenance"):
        self.path = Path(path)
        self.path.mkdir(parents=True, exist_ok=True)
        self._records: dict[str, ProvenanceRecord] = {}
        self._load()

    def _file(self) -> Path:
        return self.path / "provenance.json"

    def _load(self):
        f = self._file()
        if f.exists():
            raw = json.loads(f.read_text(encoding='utf-8'))
            self._records = {k: ProvenanceRecord(**v) for k, v in raw.items()}

    def _save(self):
        self._file().write_text(
            json.dumps({k: v.to_dict() for k, v in self._records.items()}, indent=2),
            encoding='utf-8'
        )

    @staticmethod
    def _hash(obj: Any) -> str:
        return hashlib.sha256(
            json.dumps(obj, sort_keys=True, default=str).encode()
        ).hexdigest()[:16]

    def record(
        self,
        agent: str,
        run_id: str,
        primary_model: str,
        challenger_model: str,
        query: str,
        data: dict,
        final_answer: str,
        causal_scan_summary: list = None,
        prediction_ids: list = None,
        memory_before: int = 0,
        memory_after: int = 0,
    ) -> ProvenanceRecord:
        record = ProvenanceRecord(
            record_id=f"prov_{run_id}",
            agent=agent,
            run_id=run_id,
            timestamp=time.time(),
            primary_model=primary_model,
            challenger_model=challenger_model,
            data_hash=self._hash(data),
            query_hash=self._hash(query),
            final_answer_hash=self._hash(final_answer),
            causal_scan_summary=causal_scan_summary or [],
            prediction_ids=prediction_ids or [],
            memory_entries_before=memory_before,
            memory_entries_after=memory_after,
        )
        self._records[record.record_id] = record
        self._save()
        return record

    def get(self, run_id: str) -> ProvenanceRecord:
        return self._records.get(f"prov_{run_id}")

    def recent(self, n: int = 20) -> list[ProvenanceRecord]:
        return sorted(self._records.values(), key=lambda r: -r.timestamp)[:n]

    def summary(self) -> dict:
        return {
            "total_records": len(self._records),
            "agents": list({r.agent for r in self._records.values()}),
            "models_used": list({r.primary_model for r in self._records.values()}),
        }


if __name__ == "__main__":
    import tempfile
    print("=== Provenance Tracker Tests ===")

    with tempfile.TemporaryDirectory() as tmp:
        tracker = ProvenanceTracker(path=tmp)
        rec = tracker.record(
            agent="scientific_discovery",
            run_id="test_run_001",
            primary_model="mistral",
            challenger_model="phi3",
            query="What causes humidity to drop?",
            data={"temperature": [20,21,22], "humidity": [55,53,51]},
            final_answer="Temperature causes humidity to drop via evaporation.",
            causal_scan_summary=["temperature LEADS humidity by 1 step"],
            memory_before=10, memory_after=12,
        )
        print(f"[PASS] Recorded: {rec.record_id}")
        print(f"  Citation: {rec.citation()}")
        assert rec.data_hash != rec.query_hash
        assert len(tracker.recent()) == 1
        print(f"[PASS] Summary: {tracker.summary()}")

    print("ALL TESTS PASSED")
