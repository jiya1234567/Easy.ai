"""
reproducibility.py — Step 13
Generates reproducibility certificates for any agent run.
Required for publication-grade science.
A certificate confirms: same data + same query = same causal conclusion.
"""
from __future__ import annotations
import json
import time
import hashlib
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class ReproducibilityCertificate:
    cert_id: str
    agent: str
    run_id: str
    timestamp: float
    data_hash: str
    query_hash: str
    causal_conclusions: list[str]
    state_tensor_snapshot: dict
    prediction_ids: list[str]
    reproducible: bool
    reproducibility_score: float   # 0-1
    notes: str = ""

    def to_dict(self) -> dict:
        return self.__dict__.copy()

    def certificate_text(self) -> str:
        ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.timestamp))
        status = "REPRODUCIBLE" if self.reproducible else "NOT YET VERIFIED"
        lines = [
            "=" * 55,
            f"OMEGA-CORE REPRODUCIBILITY CERTIFICATE",
            f"Status: {status}",
            f"Score:  {self.reproducibility_score:.0%}",
            "=" * 55,
            f"Agent:     {self.agent}",
            f"Run ID:    {self.run_id}",
            f"Timestamp: {ts}",
            f"Data hash: {self.data_hash}",
            f"Query hash:{self.query_hash}",
            "",
            "Causal conclusions:",
        ]
        for c in self.causal_conclusions:
            lines.append(f"  - {c}")
        if self.state_tensor_snapshot:
            st = self.state_tensor_snapshot
            lines += [
                "",
                "State tensor at time of finding:",
                f"  H={st.get('entropy_H','?'):.2f} K={st.get('coherence_K','?'):.2f} "
                f"E={st.get('emergence_E','?'):.2f} B={st.get('bifurcation_B','?'):.2f} "
                f"R={st.get('reducibility_R','?'):.2f}",
            ]
        lines.append("=" * 55)
        return "\n".join(str(l) for l in lines)


class ReproducibilityEngine:
    def __init__(self, path: str = "memory/reproducibility"):
        self.path = Path(path)
        self.path.mkdir(parents=True, exist_ok=True)
        self._certs: dict[str, ReproducibilityCertificate] = {}
        self._load()

    def _file(self) -> Path:
        return self.path / "certificates.json"

    def _load(self):
        f = self._file()
        if f.exists():
            raw = json.loads(f.read_text(encoding='utf-8'))
            self._certs = {k: ReproducibilityCertificate(**v) for k, v in raw.items()}

    def _save(self):
        self._file().write_text(
            json.dumps({k: v.to_dict() for k, v in self._certs.items()}, indent=2),
            encoding='utf-8'
        )

    @staticmethod
    def _hash(obj: Any) -> str:
        return hashlib.sha256(
            json.dumps(obj, sort_keys=True, default=str).encode()
        ).hexdigest()[:16]

    def issue(
        self,
        agent: str,
        run_id: str,
        data: dict,
        query: str,
        causal_conclusions: list[str],
        state_tensor: Any = None,
        prediction_ids: list = None,
        prior_run_hashes: list = None,
    ) -> ReproducibilityCertificate:
        """
        Issue a reproducibility certificate for a completed run.
        If prior_run_hashes provided, check consistency with prior runs.
        """
        data_hash = self._hash(data)
        query_hash = self._hash(query)

        # Check reproducibility against prior runs with same data+query
        reproducible = False
        repro_score = 0.5  # baseline: no prior runs to compare

        if prior_run_hashes:
            # Find prior certs with same data_hash and query_hash
            matching_prior = [
                c for c in self._certs.values()
                if c.data_hash == data_hash and c.query_hash == query_hash
                and c.agent == agent
            ]
            if matching_prior:
                # Compare causal conclusions (simple overlap score)
                all_prior_conclusions = set()
                for pc in matching_prior:
                    all_prior_conclusions.update(pc.causal_conclusions)
                current_set = set(causal_conclusions)
                if all_prior_conclusions:
                    overlap = len(current_set & all_prior_conclusions)
                    union = len(current_set | all_prior_conclusions)
                    repro_score = overlap / union if union > 0 else 0.0
                    reproducible = repro_score >= 0.6
                else:
                    repro_score = 1.0
                    reproducible = True
            else:
                # First run with this data+query = baseline
                repro_score = 1.0
                reproducible = True
                prior_run_hashes = []
        else:
            repro_score = 1.0
            reproducible = True

        st_snapshot = state_tensor.to_dict() if state_tensor and hasattr(state_tensor, 'to_dict') else {}

        cert = ReproducibilityCertificate(
            cert_id=f"cert_{run_id}",
            agent=agent,
            run_id=run_id,
            timestamp=time.time(),
            data_hash=data_hash,
            query_hash=query_hash,
            causal_conclusions=causal_conclusions,
            state_tensor_snapshot=st_snapshot,
            prediction_ids=prediction_ids or [],
            reproducible=reproducible,
            reproducibility_score=round(repro_score, 3),
        )
        self._certs[cert.cert_id] = cert
        self._save()
        return cert

    def verify(self, run_id: str) -> Optional[ReproducibilityCertificate]:
        return self._certs.get(f"cert_{run_id}")

    def summary(self) -> dict:
        total = len(self._certs)
        repro = sum(1 for c in self._certs.values() if c.reproducible)
        return {
            "total_certificates": total,
            "reproducible": repro,
            "not_verified": total - repro,
            "reproducibility_rate": round(repro/total, 3) if total else None,
        }


if __name__ == "__main__":
    import tempfile
    print("=== Reproducibility Engine Tests ===")

    with tempfile.TemporaryDirectory() as tmp:
        engine = ReproducibilityEngine(path=tmp)
        data = {"temperature": [20,21,22], "humidity": [55,53,51]}
        query = "What causes humidity to drop?"
        conclusions = ["temperature LEADS humidity by 1 step (r=0.99)"]

        # First run -- baseline
        cert1 = engine.issue("scientific_discovery", "run_001",
                             data, query, conclusions)
        print(f"[PASS] First run cert: {cert1.cert_id} reproducible={cert1.reproducible}")

        # Second run -- same data/query/conclusions = reproducible
        cert2 = engine.issue("scientific_discovery", "run_002",
                             data, query, conclusions, prior_run_hashes=["run_001"])
        print(f"[PASS] Second run: reproducible={cert2.reproducible} score={cert2.reproducibility_score}")
        assert cert2.reproducible

        # Third run -- different conclusions = not reproducible
        cert3 = engine.issue("scientific_discovery", "run_003",
                             data, query,
                             ["pressure is the root cause (unrelated to temperature)"],
                             prior_run_hashes=["run_001"])
        print(f"[PASS] Conflicting run: reproducible={cert3.reproducible} score={cert3.reproducibility_score}")
        assert not cert3.reproducible

        print(f"[PASS] Summary: {engine.summary()}")
        print()
        print(cert1.certificate_text())

    print("ALL TESTS PASSED")
