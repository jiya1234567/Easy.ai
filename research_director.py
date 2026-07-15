"""
research_director.py
=====================
The Research Director is the orchestrating "scientist brain" of OMEGA-CORE.

It maintains a complete scientist memory:
  - What experiments were run (and when)
  - What hypotheses were confirmed, rejected, or unresolved
  - What variables have been tested together
  - What discoveries are reusable across domains
  - What should be tested next (drives the experiment queue)

This closes the gap between:
  "AI assistant that answers questions"
  and
  "Autonomous research laboratory that learns from its own history"

Usage:
    director = ResearchDirector(path="memory/research_director")
    director.record_experiment(experiment)
    next_exp = director.propose_next(domain="scientific_discovery")
    agenda = director.current_agenda(domain="scientific_discovery")
"""

from __future__ import annotations
import json
import time
import uuid
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any, Optional
from enum import Enum


class HypothesisStatus(str, Enum):
    PENDING    = "pending"      # not yet tested
    CONFIRMED  = "confirmed"    # tested, supported by evidence
    REJECTED   = "rejected"     # tested, refuted by evidence
    UNRESOLVED = "unresolved"   # tested, ambiguous result
    REUSABLE   = "reusable"     # confirmed AND applicable across domains


@dataclass
class Experiment:
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    domain: str = ""
    query: str = ""
    variables_tested: list[str] = field(default_factory=list)
    data_hash: str = ""
    timestamp: float = field(default_factory=time.time)
    primary_reasoning: str = ""
    final_answer: str = ""
    causal_findings: list[str] = field(default_factory=list)
    hypothesis_status: str = HypothesisStatus.PENDING
    uncertainty_before: float = 0.5
    uncertainty_after: float = 0.5
    uncertainty_reduction: float = 0.0
    run_id: str = ""
    notes: str = ""

    def to_dict(self) -> dict:
        return self.__dict__.copy()

    @classmethod
    def from_dict(cls, d: dict) -> "Experiment":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class ResearchAgenda:
    domain: str
    confirmed_findings: list[str]
    rejected_hypotheses: list[str]
    unresolved_questions: list[str]
    reusable_discoveries: list[str]
    variables_not_yet_tested: list[str]
    suggested_next_experiments: list[str]
    total_experiments: int
    overall_uncertainty: float

    def summary(self) -> str:
        lines = [
            f"Research Agenda [{self.domain}]",
            f"Total experiments: {self.total_experiments}",
            f"Overall uncertainty: {self.overall_uncertainty:.0%}",
            "",
            f"Confirmed ({len(self.confirmed_findings)}):",
        ]
        for f in self.confirmed_findings[:5]:
            lines.append(f"  ✓ {f}")
        lines.append(f"\nRejected ({len(self.rejected_hypotheses)}):")
        for r in self.rejected_hypotheses[:3]:
            lines.append(f"  ✗ {r}")
        lines.append(f"\nUnresolved ({len(self.unresolved_questions)}):")
        for u in self.unresolved_questions[:3]:
            lines.append(f"  ? {u}")
        if self.reusable_discoveries:
            lines.append(f"\nReusable discoveries ({len(self.reusable_discoveries)}):")
            for d in self.reusable_discoveries[:3]:
                lines.append(f"  ★ {d}")
        lines.append(f"\nSuggested next ({len(self.suggested_next_experiments)}):")
        for s in self.suggested_next_experiments[:3]:
            lines.append(f"  → {s}")
        return "\n".join(lines)


class ResearchDirector:
    """
    The orchestrating scientist memory for OMEGA-CORE.

    Tracks all experiments, their outcomes, and what should come next.
    Drives the autonomous research loop by maintaining a complete
    history of what's been tried, confirmed, rejected, and discovered.
    """

    def __init__(self, path: str = "memory/research_director"):
        self.path = Path(path)
        self.path.mkdir(parents=True, exist_ok=True)
        self._experiments: dict[str, Experiment] = {}
        self._reusable_discoveries: list[dict] = []
        self._load()

    def _exp_file(self) -> Path:
        return self.path / "experiments.json"

    def _disc_file(self) -> Path:
        return self.path / "reusable_discoveries.json"

    def _load(self):
        f = self._exp_file()
        if f.exists():
            raw = json.loads(f.read_text(encoding="utf-8"))
            self._experiments = {
                k: Experiment.from_dict(v) for k, v in raw.items()
            }
        d = self._disc_file()
        if d.exists():
            self._reusable_discoveries = json.loads(d.read_text(encoding="utf-8"))

    def _save(self):
        self._exp_file().write_text(
            json.dumps({k: v.to_dict() for k, v in self._experiments.items()},
                      indent=2),
            encoding="utf-8"
        )
        self._disc_file().write_text(
            json.dumps(self._reusable_discoveries, indent=2),
            encoding="utf-8"
        )

    def record_experiment(
        self,
        domain: str,
        query: str,
        variables_tested: list[str],
        final_answer: str,
        causal_findings: list[str] = None,
        hypothesis_status: str = HypothesisStatus.UNRESOLVED,
        uncertainty_before: float = 0.5,
        uncertainty_after: float = 0.5,
        primary_reasoning: str = "",
        run_id: str = "",
        data_hash: str = "",
        notes: str = "",
    ) -> Experiment:
        """Record a completed experiment into the research memory."""
        exp = Experiment(
            domain=domain,
            query=query,
            variables_tested=variables_tested,
            final_answer=final_answer,
            causal_findings=causal_findings or [],
            hypothesis_status=hypothesis_status,
            uncertainty_before=uncertainty_before,
            uncertainty_after=uncertainty_after,
            uncertainty_reduction=max(0, uncertainty_before - uncertainty_after),
            primary_reasoning=primary_reasoning,
            run_id=run_id,
            data_hash=data_hash,
            notes=notes,
        )
        self._experiments[exp.id] = exp

        # Auto-promote confirmed findings to reusable if they appear
        # across multiple domains
        if hypothesis_status == HypothesisStatus.CONFIRMED:
            for finding in (causal_findings or []):
                self._check_promote_to_reusable(finding, domain)

        self._save()
        return exp

    def _check_promote_to_reusable(self, finding: str, domain: str):
        """
        If the same causal finding appears in multiple domains,
        promote it to a reusable discovery.
        """
        matching_domains = set()
        for exp in self._experiments.values():
            if (exp.hypothesis_status == HypothesisStatus.CONFIRMED and
                    finding.lower() in " ".join(exp.causal_findings).lower()):
                matching_domains.add(exp.domain)

        if len(matching_domains) >= 2:
            already = any(
                d["finding"] == finding
                for d in self._reusable_discoveries
            )
            if not already:
                self._reusable_discoveries.append({
                    "finding": finding,
                    "domains": list(matching_domains),
                    "promoted_at": time.time(),
                })

    def update_status(
        self,
        experiment_id: str,
        status: str,
        notes: str = "",
    ):
        """Update hypothesis status after human review or auto-validation."""
        if experiment_id in self._experiments:
            self._experiments[experiment_id].hypothesis_status = status
            if notes:
                self._experiments[experiment_id].notes += f"\n{notes}"
            self._save()

    def what_has_been_tested(self, domain: str = None) -> list[str]:
        """Return list of queries already tested (to avoid repetition)."""
        exps = self._experiments.values()
        if domain:
            exps = [e for e in exps if e.domain == domain]
        return [e.query for e in exps]

    def what_variables_tested(self, domain: str = None) -> set[str]:
        """Return all variable names that have been observed so far."""
        exps = self._experiments.values()
        if domain:
            exps = [e for e in exps if e.domain == domain]
        all_vars = set()
        for e in exps:
            all_vars.update(e.variables_tested)
        return all_vars

    def confirmed_findings(self, domain: str = None) -> list[str]:
        exps = self._experiments.values()
        if domain:
            exps = [e for e in exps if e.domain == domain]
        findings = []
        for e in [x for x in exps if x.hypothesis_status == HypothesisStatus.CONFIRMED]:
            findings.extend(e.causal_findings)
        return list(dict.fromkeys(findings))  # deduplicate, preserve order

    def rejected_hypotheses(self, domain: str = None) -> list[str]:
        exps = self._experiments.values()
        if domain:
            exps = [e for e in exps if e.domain == domain]
        return [e.query for e in exps
                if e.hypothesis_status == HypothesisStatus.REJECTED]

    def unresolved_questions(self, domain: str = None) -> list[str]:
        exps = self._experiments.values()
        if domain:
            exps = [e for e in exps if e.domain == domain]
        return [e.query for e in exps
                if e.hypothesis_status == HypothesisStatus.UNRESOLVED]

    def current_agenda(self, domain: str = None) -> ResearchAgenda:
        """
        Generate the current research agenda — the complete picture
        of what's known, unknown, and what should be tried next.
        """
        confirmed = self.confirmed_findings(domain)
        rejected = self.rejected_hypotheses(domain)
        unresolved = self.unresolved_questions(domain)
        tested_vars = self.what_variables_tested(domain)
        reusable = [d["finding"] for d in self._reusable_discoveries]

        # Overall uncertainty: proportion of experiments that are unresolved
        total = len([e for e in self._experiments.values()
                    if not domain or e.domain == domain])
        unresolved_count = len(unresolved)
        uncertainty = unresolved_count / total if total > 0 else 0.8

        # Suggest next experiments based on gaps
        suggestions = self._suggest_next(domain, confirmed, rejected,
                                         unresolved, tested_vars)

        return ResearchAgenda(
            domain=domain or "all",
            confirmed_findings=confirmed,
            rejected_hypotheses=rejected,
            unresolved_questions=unresolved,
            reusable_discoveries=reusable,
            variables_not_yet_tested=[],  # filled by experiment_queue
            suggested_next_experiments=suggestions,
            total_experiments=total,
            overall_uncertainty=round(uncertainty, 3),
        )

    def _suggest_next(
        self,
        domain: str,
        confirmed: list,
        rejected: list,
        unresolved: list,
        tested_vars: set,
    ) -> list[str]:
        suggestions = []

        # 1. Re-test unresolved questions with different data
        for q in unresolved[:2]:
            suggestions.append(
                f"Re-test with varied data: '{q[:80]}' "
                f"(currently unresolved)"
            )

        # 2. Extend confirmed findings
        for finding in confirmed[:2]:
            suggestions.append(
                f"Extend confirmed finding to boundary conditions: '{finding[:80]}'"
            )

        # 3. Test combinations of confirmed variables
        confirmed_vars = list(tested_vars)[:4]
        if len(confirmed_vars) >= 2:
            suggestions.append(
                f"Test joint effect of {confirmed_vars[0]} AND "
                f"{confirmed_vars[1]} on {confirmed_vars[-1]}"
            )

        # 4. Apply reusable discoveries to this domain
        for disc in self._reusable_discoveries[:1]:
            if domain and domain not in disc["domains"]:
                suggestions.append(
                    f"Apply cross-domain discovery to {domain}: "
                    f"'{disc['finding'][:80]}'"
                )

        return suggestions[:5]

    def propose_next_query(self, domain: str, available_variables: list[str]) -> str:
        """
        Propose the single best next experiment query based on
        what's been tried, what failed, and what's unresolved.
        Returns a specific, actionable query string.
        """
        agenda = self.current_agenda(domain)

        if agenda.unresolved_questions:
            # Narrow down the most ambiguous question
            return (
                f"Clarify with controlled variables: "
                f"{agenda.unresolved_questions[0]}"
            )

        if agenda.confirmed_findings:
            # Push confirmed finding to boundary
            return (
                f"Test boundary condition of confirmed finding: "
                f"{agenda.confirmed_findings[0]} -- "
                f"does it hold when {available_variables[-1] if available_variables else 'other variables'} "
                f"is held constant?"
            )

        # Default: explore least-tested relationship
        if len(available_variables) >= 2:
            return (
                f"Explore causal relationship between "
                f"{available_variables[0]} and {available_variables[-1]} "
                f"using lag analysis and regime detection"
            )

        return "What is the dominant causal driver in this dataset?"

    def summary(self, domain: str = None) -> dict:
        exps = list(self._experiments.values())
        if domain:
            exps = [e for e in exps if e.domain == domain]

        status_counts = {}
        for e in exps:
            status_counts[e.hypothesis_status] = \
                status_counts.get(e.hypothesis_status, 0) + 1

        avg_uncertainty_reduction = (
            sum(e.uncertainty_reduction for e in exps) / len(exps)
            if exps else 0
        )

        return {
            "total_experiments": len(exps),
            "status_breakdown": status_counts,
            "reusable_discoveries": len(self._reusable_discoveries),
            "avg_uncertainty_reduction": round(avg_uncertainty_reduction, 3),
            "domains_active": list({e.domain for e in exps}),
        }


if __name__ == "__main__":
    import tempfile
    print("=" * 55)
    print("Research Director Self-Tests")
    print("=" * 55)

    with tempfile.TemporaryDirectory() as tmp:
        director = ResearchDirector(path=tmp)

        # Test 1: Record experiments
        e1 = director.record_experiment(
            domain="scientific_discovery",
            query="Does temperature cause humidity to drop?",
            variables_tested=["temperature", "humidity", "pressure"],
            final_answer="Yes -- temperature LEADS humidity by 1 step (r=0.99)",
            causal_findings=["temperature leads humidity by 1 step"],
            hypothesis_status=HypothesisStatus.CONFIRMED,
            uncertainty_before=0.8,
            uncertainty_after=0.2,
        )
        print(f"\n[PASS] Recorded experiment: {e1.id}")
        print(f"  Uncertainty reduction: {e1.uncertainty_reduction:.2f}")

        # Test 2: Record a rejected hypothesis
        e2 = director.record_experiment(
            domain="scientific_discovery",
            query="Does pressure directly cause humidity changes?",
            variables_tested=["pressure", "humidity"],
            final_answer="No significant direct relationship found",
            causal_findings=[],
            hypothesis_status=HypothesisStatus.REJECTED,
            uncertainty_before=0.6,
            uncertainty_after=0.3,
        )
        print(f"[PASS] Recorded rejected: {e2.id}")

        # Test 3: Record unresolved
        e3 = director.record_experiment(
            domain="scientific_discovery",
            query="Is there a lag-2 relationship between temperature and pressure?",
            variables_tested=["temperature", "pressure"],
            final_answer="Ambiguous -- some evidence but not conclusive",
            hypothesis_status=HypothesisStatus.UNRESOLVED,
        )
        print(f"[PASS] Recorded unresolved: {e3.id}")

        # Test 4: Cross-domain reusable discovery
        director.record_experiment(
            domain="weather_manifold",
            query="Does temperature lead humidity in weather data?",
            variables_tested=["temperature", "humidity"],
            final_answer="Confirmed -- same lag relationship as scientific_discovery",
            causal_findings=["temperature leads humidity by 1 step"],
            hypothesis_status=HypothesisStatus.CONFIRMED,
        )
        assert len(director._reusable_discoveries) == 1
        print(f"[PASS] Reusable discovery auto-promoted across domains")
        print(f"  Discovery: {director._reusable_discoveries[0]}")

        # Test 5: Generate agenda
        agenda = director.current_agenda("scientific_discovery")
        print(f"\n[PASS] Agenda generated:")
        print(agenda.summary())
        assert len(agenda.confirmed_findings) >= 1
        assert len(agenda.rejected_hypotheses) >= 1
        assert len(agenda.suggested_next_experiments) >= 1

        # Test 6: Propose next query
        next_q = director.propose_next_query(
            "scientific_discovery",
            ["temperature", "humidity", "pressure", "wind_speed"]
        )
        print(f"\n[PASS] Next query proposed: {next_q}")
        assert len(next_q) > 10

        # Test 7: Persistence
        director2 = ResearchDirector(path=tmp)
        assert len(director2._experiments) == 4
        print(f"[PASS] Persistence confirmed: {len(director2._experiments)} experiments")

        # Test 8: Summary
        s = director.summary()
        print(f"[PASS] Summary: {s}")
        assert s["total_experiments"] >= 4

    print("\nALL TESTS PASSED")
