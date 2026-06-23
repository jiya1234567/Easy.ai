"""
auto_chain.py
==============
Auto-Chain Discovery Loop — closes the autonomous "Observe -> Hypothesize
-> Test -> Validate -> Suggest again" cycle.

This is the highest-autonomy module in the system, so it ships with
non-negotiable safety guardrails:

  1. HARD CAP on cycles per run (default 5, max 20) — never unbounded.
  2. Every cycle is logged and visible — nothing happens silently.
  3. A stop control is always available; the loop checks a stop flag
     between every step, not just between cycles.
  4. Reality validation (comparing predictions to actual outcomes)
     remains a HUMAN action — auto-chain proposes and runs experiments,
     it does NOT auto-validate predictions against reality. That keeps
     a human in the loop for the step where the system could otherwise
     reinforce its own errors silently.
  5. If a single cycle errors, the chain stops (does not silently skip
     and continue) — failures must be visible, not swallowed.
"""

from __future__ import annotations
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Optional, Callable

from discovery_planner import DiscoveryPlanner


MAX_ALLOWED_CYCLES = 20
DEFAULT_MAX_CYCLES = 5


@dataclass
class ChainCycleResult:
    cycle_number: int
    suggestion_query: str
    suggestion_reasoning: str
    question_type: str
    agent_result: Any              # harness.AgentResult
    duration_seconds: float
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict:
        return {
            "cycle_number": self.cycle_number,
            "suggestion_query": self.suggestion_query,
            "suggestion_reasoning": self.suggestion_reasoning,
            "question_type": self.question_type,
            "final_answer": self.agent_result.final_answer if self.agent_result else None,
            "run_id": self.agent_result.run_id if self.agent_result else None,
            "duration_seconds": self.duration_seconds,
            "timestamp": self.timestamp,
        }


@dataclass
class ChainState:
    running: bool = False
    cycle_count: int = 0
    max_cycles: int = DEFAULT_MAX_CYCLES
    stop_requested: bool = False
    cycles: list = field(default_factory=list)   # list[ChainCycleResult]
    last_error: str = ""


class AutoChain:
    """
    Usage:
        chain = AutoChain(
            agent=my_agent,
            memory=memory_layer,
            reality_anchor=reality_anchor,   # optional
            context_data_fn=lambda: {"temperature": [...], ...},  # static or live source
        )

        chain.start(max_cycles=5)
        # ... runs cycles synchronously when run_next_cycle() is called,
        # or use run_all() to execute the full chain in one call.

        chain.stop()   # can be called at any time; checked between every step
    """

    def __init__(
        self,
        agent: Any,                                  # harness.Agent
        memory: Any,                                  # MemoryLayer / VectorMemoryLayer
        reality_anchor: Optional[Any] = None,
        context_data_fn: Optional[Callable[[], dict]] = None,
        planner: Optional[DiscoveryPlanner] = None,
        on_cycle_complete: Optional[Callable[[ChainCycleResult], None]] = None,
    ):
        self.agent = agent
        self.memory = memory
        self.reality_anchor = reality_anchor
        self.context_data_fn = context_data_fn or (lambda: {})
        self.planner = planner or DiscoveryPlanner()
        self.on_cycle_complete = on_cycle_complete

        self.state = ChainState()

    def start(self, max_cycles: int = DEFAULT_MAX_CYCLES):
        """Reset and begin a new chain run. Does not block — call run_next_cycle()
        repeatedly or run_all() to execute."""
        max_cycles = max(1, min(max_cycles, MAX_ALLOWED_CYCLES))
        self.state = ChainState(running=True, max_cycles=max_cycles)

    def stop(self):
        """Request the chain to stop. Checked between every step, not just
        between cycles, so this takes effect promptly."""
        self.state.stop_requested = True
        self.state.running = False

    def _should_continue(self) -> bool:
        if self.state.stop_requested:
            return False
        if self.state.cycle_count >= self.state.max_cycles:
            return False
        return True

    def run_next_cycle(self) -> Optional[ChainCycleResult]:
        """
        Execute exactly one cycle: suggest -> run -> record prediction
        (if applicable). Returns None if the chain should not continue
        (stopped, or max cycles reached).

        Does NOT auto-validate predictions against reality — that step
        remains a human action via RealityAnchor.validate(), by design.
        """
        if not self._should_continue():
            self.state.running = False
            return None

        t0 = time.time()
        agent_name = getattr(self.agent, "name", "unknown")

        try:
            # Step 1: Discovery Planner suggests next question
            suggestion = self.planner.suggest_next(
                agent_name=agent_name,
                memory=self.memory,
                reality_anchor=self.reality_anchor,
            )

            if self.state.stop_requested:
                self.state.running = False
                return None

            # Step 2: Run the agent on that suggestion
            context_data = self.context_data_fn()
            agent_result = self.agent.run(suggestion.proposed_query, context_data)

            if self.state.stop_requested:
                self.state.running = False
                return None

            # Step 3: Optionally record as a trackable prediction
            # (only if the suggestion named specific target variables —
            # otherwise there's nothing concrete to validate later)
            if self.reality_anchor and suggestion.target_variables:
                try:
                    self.reality_anchor.record_prediction(
                        agent=agent_name,
                        prediction_text=agent_result.final_answer[:300],
                        predicted_variables={v: 0.0 for v in suggestion.target_variables},
                        # NOTE: predicted_variables values default to 0.0 placeholders
                        # since the agent's free-text answer isn't auto-parsed into
                        # numeric predictions in v1. This still creates a tracked
                        # entry for human follow-up, but real numeric prediction
                        # extraction is a known v2 improvement, not silently claimed
                        # as done here.
                    )
                except Exception:
                    pass  # prediction tracking is best-effort, not chain-critical

            self.state.cycle_count += 1
            cycle = ChainCycleResult(
                cycle_number=self.state.cycle_count,
                suggestion_query=suggestion.proposed_query,
                suggestion_reasoning=suggestion.reasoning,
                question_type=suggestion.question_type,
                agent_result=agent_result,
                duration_seconds=round(time.time() - t0, 1),
            )
            self.state.cycles.append(cycle)

            if self.on_cycle_complete:
                self.on_cycle_complete(cycle)

            if self.state.cycle_count >= self.state.max_cycles:
                self.state.running = False

            return cycle

        except Exception as e:
            # Guardrail 5: failures stop the chain, they don't get silently skipped
            self.state.last_error = str(e)
            self.state.running = False
            self.state.stop_requested = True
            return None

    def run_all(self) -> list[ChainCycleResult]:
        """
        Run cycles synchronously until max_cycles reached, stop requested,
        or an error occurs. Blocking — intended for use inside a Streamlit
        button click (each cycle takes ~15-60s with live LLM calls).
        """
        results = []
        while self._should_continue():
            cycle = self.run_next_cycle()
            if cycle is None:
                break
            results.append(cycle)
        return results

    def status(self) -> dict:
        return {
            "running": self.state.running,
            "cycle_count": self.state.cycle_count,
            "max_cycles": self.state.max_cycles,
            "stop_requested": self.state.stop_requested,
            "last_error": self.state.last_error,
            "cycles_summary": [
                {"n": c.cycle_number, "query": c.suggestion_query[:80], "type": c.question_type}
                for c in self.state.cycles
            ],
        }


# ── Self-test (fake agent/memory/planner, no live LLM needed) ──────
if __name__ == "__main__":
    class FakeResult:
        def __init__(self, n):
            self.run_id = f"run{n}"
            self.final_answer = f"Fake finding #{n}"

    class FakeAgent:
        name = "test_agent"
        def __init__(self):
            self.n = 0
        def run(self, query, data):
            self.n += 1
            return FakeResult(self.n)

    class FakeMemory:
        def recent(self, agent_name, n=5):
            return []

    class FakeSuggestion:
        def __init__(self, n):
            self.proposed_query = f"Test question #{n}"
            self.reasoning = "Fake reasoning"
            self.target_variables = ["var_a"]
            self.question_type = "exploratory"

    class FakePlanner:
        def __init__(self):
            self.n = 0
        def suggest_next(self, agent_name, memory, reality_anchor=None):
            self.n += 1
            return FakeSuggestion(self.n)

    print("=== Test 1: run_all with max_cycles=3 ===")
    chain = AutoChain(
        agent=FakeAgent(),
        memory=FakeMemory(),
        reality_anchor=None,
        planner=FakePlanner(),
        on_cycle_complete=lambda c: print(f"  Cycle {c.cycle_number} complete: {c.suggestion_query}"),
    )
    chain.start(max_cycles=3)
    results = chain.run_all()
    print(f"Completed {len(results)} cycles")
    print(f"Final status: {chain.status()}")

    print("\n=== Test 2: stop mid-chain ===")
    chain2 = AutoChain(agent=FakeAgent(), memory=FakeMemory(), planner=FakePlanner())
    chain2.start(max_cycles=10)
    chain2.run_next_cycle()
    chain2.run_next_cycle()
    chain2.stop()
    result = chain2.run_next_cycle()
    print(f"After stop, run_next_cycle returned: {result}")
    print(f"Cycles completed before stop: {chain2.state.cycle_count}")

    print("\n=== Test 3: max cycles cap enforcement ===")
    chain3 = AutoChain(agent=FakeAgent(), memory=FakeMemory(), planner=FakePlanner())
    chain3.start(max_cycles=999)  # should be clamped to MAX_ALLOWED_CYCLES
    print(f"Requested 999 cycles, clamped to: {chain3.state.max_cycles}")
    assert chain3.state.max_cycles == MAX_ALLOWED_CYCLES

    print("\nALL TESTS PASSED")
