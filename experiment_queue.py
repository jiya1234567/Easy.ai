"""
experiment_queue.py
====================
Autonomous Experiment Queue driven by uncertainty reduction.

Answers: "What should I test next to learn the most?"

Selects experiments that maximally reduce uncertainty by:
  1. Targeting unresolved hypotheses first
  2. Testing variable combinations not yet explored
  3. Applying confirmed findings to untested boundary conditions
  4. Propagating reusable discoveries to new domains
  5. Filling gaps identified by the causal scan

Integrates with ResearchDirector (what's been tried) and
DiscoveryPlanner (what Mistral suggests) to form a complete
autonomous research loop.
"""

from __future__ import annotations
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class QueuedExperiment:
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    domain: str = ""
    query: str = ""
    target_variables: list[str] = field(default_factory=list)
    expected_uncertainty_reduction: float = 0.0
    priority: int = 0          # lower = higher priority
    reason: str = ""           # why this experiment was queued
    queued_at: float = field(default_factory=time.time)
    status: str = "queued"     # queued | running | complete | skipped
    experiment_id: str = ""    # filled when completed

    def to_dict(self) -> dict:
        return self.__dict__.copy()


class ExperimentQueue:
    """
    Priority queue of experiments to run, ordered by expected
    uncertainty reduction.

    The queue is rebuilt each time from the ResearchDirector's
    current agenda -- it's not persisted separately since
    ResearchDirector is the source of truth.
    """

    def __init__(self, research_director):
        self.director = research_director
        self._queue: list[QueuedExperiment] = []
        self._completed: list[str] = []  # experiment IDs

    def rebuild(
        self,
        domain: str,
        available_variables: list[str],
        causal_scan_result: dict = None,
        planner_suggestion: str = None,
    ) -> list[QueuedExperiment]:
        """
        Rebuild the priority queue from scratch based on current
        research state. Call this at the start of each Auto-Chain cycle.

        Priority order:
          1. Unresolved questions (highest value -- already identified gap)
          2. Planner suggestion (Mistral's view of what's next)
          3. Variable combinations not yet tested
          4. Boundary conditions of confirmed findings
          5. Cross-domain reusable discovery application
        """
        self._queue = []
        agenda = self.director.current_agenda(domain)
        tested_queries = set(q.lower() for q in self.director.what_has_been_tested(domain))
        tested_vars = self.director.what_variables_tested(domain)
        untested_vars = [v for v in available_variables if v not in tested_vars]

        priority = 0

        # Priority 1: Unresolved questions
        for q in agenda.unresolved_questions[:3]:
            if q.lower() not in tested_queries or True:  # always re-queue unresolved
                exp_reduction = 0.4  # unresolved -> resolving = ~40% uncertainty drop
                self._queue.append(QueuedExperiment(
                    domain=domain,
                    query=f"Re-examine with focused data: {q}",
                    target_variables=available_variables[:3],
                    expected_uncertainty_reduction=exp_reduction,
                    priority=priority,
                    reason=f"Unresolved question -- highest information value",
                ))
                priority += 1

        # Priority 2: Planner suggestion (if provided and not already tested)
        if planner_suggestion:
            planner_lower = planner_suggestion.lower()
            if not any(planner_lower in t for t in tested_queries):
                self._queue.append(QueuedExperiment(
                    domain=domain,
                    query=planner_suggestion,
                    target_variables=available_variables,
                    expected_uncertainty_reduction=0.35,
                    priority=priority,
                    reason="Discovery Planner recommendation",
                ))
                priority += 1

        # Priority 3: Untested variable combinations
        if len(untested_vars) >= 1 and len(available_variables) >= 2:
            for uv in untested_vars[:2]:
                tested_partner = next(
                    (v for v in available_variables if v != uv and v in tested_vars),
                    available_variables[0]
                )
                query = (
                    f"Test causal relationship between {uv} and {tested_partner} "
                    f"-- {uv} has not been tested in isolation yet"
                )
                self._queue.append(QueuedExperiment(
                    domain=domain,
                    query=query,
                    target_variables=[uv, tested_partner],
                    expected_uncertainty_reduction=0.30,
                    priority=priority,
                    reason=f"Variable '{uv}' not yet tested in this domain",
                ))
                priority += 1

        # Priority 4: Lag/regime gaps from causal scan
        if causal_scan_result:
            regime_changes = causal_scan_result.get("regime_changes", [])
            for rc in regime_changes[:2]:
                query = (
                    f"Investigate regime change: {rc} -- "
                    f"what triggered this relationship shift?"
                )
                self._queue.append(QueuedExperiment(
                    domain=domain,
                    query=query,
                    target_variables=available_variables,
                    expected_uncertainty_reduction=0.35,
                    priority=priority,
                    reason=f"Regime change detected -- unexplained by current hypotheses",
                ))
                priority += 1

            hyperedges = causal_scan_result.get("hyperedges", [])
            for he in hyperedges[:1]:
                drivers = he.get("drivers", [])
                target = he.get("target", "")
                if drivers and target:
                    query = (
                        f"Verify hyperedge: does ({' AND '.join(drivers)}) "
                        f"jointly cause {target} more than either alone?"
                    )
                    self._queue.append(QueuedExperiment(
                        domain=domain,
                        query=query,
                        target_variables=drivers + [target],
                        expected_uncertainty_reduction=0.40,
                        priority=priority,
                        reason="Hyperedge detected -- joint causation needs verification",
                    ))
                    priority += 1

        # Priority 5: Boundary conditions of confirmed findings
        for finding in agenda.confirmed_findings[:2]:
            query = (
                f"Test boundary: does '{finding}' still hold "
                f"under extreme values or inverted conditions?"
            )
            self._queue.append(QueuedExperiment(
                domain=domain,
                query=query,
                target_variables=available_variables,
                expected_uncertainty_reduction=0.20,
                priority=priority,
                reason=f"Boundary test of confirmed finding",
            ))
            priority += 1

        # Priority 6: Cross-domain reusable discovery application
        for disc in self.director._reusable_discoveries[:2]:
            if domain not in disc["domains"]:
                query = (
                    f"Test cross-domain discovery in {domain}: "
                    f"'{disc['finding']}' -- confirmed in {disc['domains']}"
                )
                self._queue.append(QueuedExperiment(
                    domain=domain,
                    query=query,
                    target_variables=available_variables[:3],
                    expected_uncertainty_reduction=0.25,
                    priority=priority,
                    reason=f"Reusable discovery from {disc['domains']} not yet tested here",
                ))
                priority += 1

        self._queue.sort(key=lambda e: (e.priority, -e.expected_uncertainty_reduction))
        return self._queue

    def next(self) -> Optional[QueuedExperiment]:
        """Return the highest-priority queued experiment."""
        for exp in self._queue:
            if exp.status == "queued":
                return exp
        return None

    def mark_running(self, exp_id: str):
        for exp in self._queue:
            if exp.id == exp_id:
                exp.status = "running"

    def mark_complete(self, exp_id: str, experiment_id: str):
        for exp in self._queue:
            if exp.id == exp_id:
                exp.status = "complete"
                exp.experiment_id = experiment_id
                self._completed.append(experiment_id)

    def mark_skipped(self, exp_id: str, reason: str = ""):
        for exp in self._queue:
            if exp.id == exp_id:
                exp.status = "skipped"

    def pending(self) -> list[QueuedExperiment]:
        return [e for e in self._queue if e.status == "queued"]

    def status_summary(self) -> dict:
        counts = {}
        for e in self._queue:
            counts[e.status] = counts.get(e.status, 0) + 1
        return {
            "total_queued": len(self._queue),
            "pending": counts.get("queued", 0),
            "running": counts.get("running", 0),
            "complete": counts.get("complete", 0),
            "skipped": counts.get("skipped", 0),
            "next_experiment": self.next().query[:80] if self.next() else None,
        }


if __name__ == "__main__":
    import sys
    import tempfile
    sys.path.insert(0, "/home/claude/research_director")

    from research_director import ResearchDirector, HypothesisStatus

    print("=" * 55)
    print("Experiment Queue Self-Tests")
    print("=" * 55)

    with tempfile.TemporaryDirectory() as tmp:
        director = ResearchDirector(path=tmp)

        # Seed with some history
        director.record_experiment(
            domain="scientific_discovery",
            query="Does temperature cause humidity to drop?",
            variables_tested=["temperature", "humidity"],
            final_answer="Confirmed",
            causal_findings=["temperature leads humidity by 1 step"],
            hypothesis_status=HypothesisStatus.CONFIRMED,
            uncertainty_before=0.8, uncertainty_after=0.2,
        )
        director.record_experiment(
            domain="scientific_discovery",
            query="Is there a lag-2 relationship?",
            variables_tested=["temperature", "pressure"],
            final_answer="Ambiguous",
            hypothesis_status=HypothesisStatus.UNRESOLVED,
            uncertainty_before=0.6, uncertainty_after=0.5,
        )

        queue = ExperimentQueue(director)
        available_vars = ["temperature", "humidity", "pressure", "wind_speed"]

        mock_causal = {
            "regime_changes": ["temperature<->pressure: r flips +0.8 -> -0.6 at step 5"],
            "hyperedges": [{"drivers": ["temperature", "wind_speed"], "target": "humidity"}],
        }

        experiments = queue.rebuild(
            domain="scientific_discovery",
            available_variables=available_vars,
            causal_scan_result=mock_causal,
            planner_suggestion="What is the effect of wind_speed on humidity at low pressure?",
        )

        print(f"\n[PASS] Queue built: {len(experiments)} experiments")
        print(f"\nPriority order:")
        for i, exp in enumerate(experiments):
            print(f"  #{i+1} [P{exp.priority}] [{exp.expected_uncertainty_reduction:.0%} reduction]")
            print(f"       {exp.query[:70]}")
            print(f"       Reason: {exp.reason}")

        # Test next()
        nxt = queue.next()
        assert nxt is not None
        print(f"\n[PASS] Next experiment: {nxt.query[:60]}")

        # Test mark_complete
        queue.mark_running(nxt.id)
        queue.mark_complete(nxt.id, "exp_001")
        next2 = queue.next()
        assert next2 is not None and next2.id != nxt.id
        print(f"[PASS] After completing first, next is: {next2.query[:60]}")

        # Test status summary
        s = queue.status_summary()
        print(f"\n[PASS] Status: {s}")
        assert s["complete"] == 1
        assert s["pending"] >= 1

    print("\nALL TESTS PASSED")
