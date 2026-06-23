"""
agent_colony.py
================
Gap 5 fix: Multi-agent parallelism with inter-agent messaging.

Instead of one agent running at a time, multiple agents can run
concurrently and pass findings to each other via a simple message bus.

Example use case: Finance agent detects a regime change -> posts a
message -> World Model agent picks it up on its next run and
incorporates it into cross-domain reasoning.
"""

from __future__ import annotations
import time
import uuid
import threading
import concurrent.futures
from dataclasses import dataclass, field
from typing import Any, Optional, Callable


@dataclass
class ColonyMessage:
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    from_agent: str = ""
    to_agent: str = ""             # "" or "*" means broadcast to all
    content: str = ""
    metadata: dict = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    consumed_by: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return self.__dict__.copy()


class MessageBus:
    """
    Thread-safe in-memory message bus. Agents post findings here;
    other agents can read messages addressed to them (or broadcasts)
    since their last check.
    """

    def __init__(self):
        self._messages: list[ColonyMessage] = []
        self._lock = threading.Lock()

    def post(self, from_agent: str, content: str, to_agent: str = "*", metadata: dict | None = None) -> str:
        msg = ColonyMessage(from_agent=from_agent, to_agent=to_agent,
                            content=content, metadata=metadata or {})
        with self._lock:
            self._messages.append(msg)
        return msg.id

    def read_for(self, agent_name: str, mark_consumed: bool = True, limit: int = 10) -> list[ColonyMessage]:
        """Get messages addressed to this agent (or broadcasts) not yet consumed by it."""
        with self._lock:
            relevant = [
                m for m in self._messages
                if (m.to_agent == agent_name or m.to_agent == "*")
                and m.from_agent != agent_name
                and agent_name not in m.consumed_by
            ]
            relevant.sort(key=lambda m: -m.timestamp)
            result = relevant[:limit]
            if mark_consumed:
                for m in result:
                    m.consumed_by.append(agent_name)
            return result

    def all_messages(self, n: int = 50) -> list[ColonyMessage]:
        with self._lock:
            return sorted(self._messages, key=lambda m: -m.timestamp)[:n]

    def clear(self):
        with self._lock:
            self._messages = []


class AgentColony:
    """
    Coordinates parallel execution of multiple agents, with a shared
    MessageBus so findings can propagate between them.

    Usage:
        colony = AgentColony(agents={"finance": finance_agent, "world_model": wm_agent})

        # Run several agents in parallel, each on its own query/data:
        results = colony.run_parallel({
            "finance": ("Analyze rate hike impact", {"rate": [4,4.5,5]}),
            "world_model": ("Extract systemic rules", {"x": [1,2,3]}),
        })

        # An agent can post a finding for others to pick up:
        colony.bus.post(from_agent="finance", content="Detected regime change: hiking cycle began")

        # Next time world_model runs, it can check colony.bus.read_for("world_model")
        # and fold that into its context.
    """

    def __init__(self, agents: dict[str, Any]):
        self.agents = agents
        self.bus = MessageBus()
        self._last_results: dict[str, Any] = {}

    def run_parallel(
        self,
        jobs: dict[str, tuple[str, dict]],
        max_workers: int = 4,
        inject_messages: bool = True,
    ) -> dict[str, Any]:
        """
        Run multiple agents concurrently.
        jobs: {agent_name: (query, context_data)}
        Returns: {agent_name: AgentResult}
        """
        def _run_one(name: str, query: str, data: dict):
            agent = self.agents[name]

            if inject_messages:
                pending = self.bus.read_for(name)
                if pending:
                    inbox_note = "\n".join(f"[from {m.from_agent}] {m.content}" for m in pending)
                    query = f"{query}\n\nMessages from other agents:\n{inbox_note}"

            result = agent.run(query, data)
            return name, result

        results: dict[str, Any] = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(_run_one, name, q, d): name
                for name, (q, d) in jobs.items()
                if name in self.agents
            }
            for future in concurrent.futures.as_completed(futures):
                name, result = future.result()
                results[name] = result

        self._last_results.update(results)
        return results

    def run_sequential_with_handoff(
        self,
        chain: list[tuple[str, str, dict]],
    ) -> list[tuple[str, Any]]:
        """
        Run agents one after another, where each agent's final_answer
        is automatically posted to the bus for the next agent to see.

        chain: [(agent_name, query, data), ...]
        Returns: [(agent_name, AgentResult), ...]
        """
        results = []
        for name, query, data in chain:
            agent = self.agents.get(name)
            if not agent:
                continue

            pending = self.bus.read_for(name)
            if pending:
                inbox_note = "\n".join(f"[from {m.from_agent}] {m.content}" for m in pending)
                query = f"{query}\n\nContext from prior agents:\n{inbox_note}"

            result = agent.run(query, data)
            results.append((name, result))

            self.bus.post(
                from_agent=name,
                content=result.final_answer[:300],
                to_agent="*",
            )

        return results

    def colony_status(self) -> dict[str, Any]:
        return {
            "agents": list(self.agents.keys()),
            "total_messages": len(self.bus.all_messages(n=10**6)),
            "last_run_agents": list(self._last_results.keys()),
        }


# ── Self-test ─────────────────────────────────────────────────────
if __name__ == "__main__":
    class FakeResult:
        def __init__(self, name, q):
            self.run_id = f"r_{name}"
            self.final_answer = f"{name} concluded: analysis of '{q[:30]}...' complete"

    class FakeAgent:
        def __init__(self, name):
            self.name = name
        def run(self, query, data):
            time.sleep(0.2)
            return FakeResult(self.name, query)

    agents = {n: FakeAgent(n) for n in ["finance", "world_model", "weather"]}
    colony = AgentColony(agents)

    print("=== Parallel run ===")
    t0 = time.time()
    results = colony.run_parallel({
        "finance": ("Analyze rates", {}),
        "world_model": ("Extract rules", {}),
        "weather": ("Check pressure", {}),
    })
    print(f"Completed in {time.time()-t0:.2f}s (should be ~0.2s, not 0.6s, due to parallelism)")
    for name, r in results.items():
        print(f"  {name}: {r.final_answer}")

    print("\n=== Sequential with handoff ===")
    colony.bus.clear()
    chain_results = colony.run_sequential_with_handoff([
        ("finance", "Detect regime change", {}),
        ("world_model", "Incorporate finance findings", {}),
    ])
    for name, r in chain_results:
        print(f"  {name}: {r.final_answer}")

    print("\n=== Message bus contents ===")
    for m in colony.bus.all_messages():
        print(f"  [{m.from_agent} -> {m.to_agent}] {m.content}")
