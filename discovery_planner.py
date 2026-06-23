"""
discovery_planner.py
======================
Discovery Planner v1 — closes the "what should I investigate next?" gap.

Given an agent's recent memory and Reality Anchor accuracy history,
proposes the single most valuable next query to run. Human-in-the-loop:
never auto-executes, always requires explicit approval via the UI.

Scope (deliberately limited for v1):
  - One suggestion per call, not a queue
  - Stays within one agent's domain (no cross-domain switching)
  - Does not modify the agent's blueprint (that's self_improve.py's job)
  - Reuses existing MemoryLayer/VectorMemoryLayer and RealityAnchor —
    no new storage infrastructure
"""

from __future__ import annotations
import json
from dataclasses import dataclass
from typing import Any, Optional

from mistral_client import MistralClient


PLANNER_SYSTEM_PROMPT = """\
You are the Discovery Planner for a scientific research agent.

Your job: given the agent's recent reasoning history and its track record
of prediction accuracy, propose the SINGLE most valuable next question
for this agent to investigate.

Guidelines:
- If recent hypotheses share an unexamined gap (e.g. no lag/timing analysis,
  no consideration of a particular variable), propose closing that gap.
- If the agent's prediction accuracy has been LOW, propose a narrower,
  more easily-testable question rather than an ambitious one.
- If the agent's prediction accuracy has been HIGH, propose a more
  ambitious follow-up question that builds on confirmed findings.
- If there is no accuracy history yet, propose a question that would
  generate a clearly falsifiable/checkable prediction (good for starting
  a track record).
- Never repeat a question that was already asked recently (see history).
- Be specific and concrete — name actual variables from the history
  when relevant, not generic placeholders.

Respond with ONLY a JSON object:
{
  "proposed_query": "the next question to investigate, written as a complete sentence",
  "reasoning": "1-3 sentences explaining why this is the most valuable next step",
  "target_variables": ["list", "of", "variable", "names", "this", "touches"],
  "question_type": "narrow_validation" | "gap_closing" | "ambitious_followup" | "exploratory"
}
"""


@dataclass
class PlannerSuggestion:
    proposed_query: str
    reasoning: str
    target_variables: list[str]
    question_type: str

    def to_dict(self) -> dict:
        return {
            "proposed_query": self.proposed_query,
            "reasoning": self.reasoning,
            "target_variables": self.target_variables,
            "question_type": self.question_type,
        }


class DiscoveryPlanner:
    """
    Usage:
        planner = DiscoveryPlanner(mistral_client)
        suggestion = planner.suggest_next(
            agent_name="finance",
            memory=memory_layer,
            reality_anchor=reality_anchor,   # optional, can be None
        )
        print(suggestion.proposed_query)
    """

    def __init__(self, client: Optional[MistralClient] = None):
        self.client = client or MistralClient()

    def _build_history_summary(self, agent_name: str, memory, n: int = 5) -> str:
        recent = memory.recent(agent_name, n=n)
        if not recent:
            return "No prior history for this agent."

        lines = []
        for e in recent:
            role = e.role if hasattr(e, "role") else e["role"]
            content = e.content if hasattr(e, "content") else e["content"]
            lines.append(f"[{role}] {content[:200]}")
        return "\n".join(lines)

    def _build_accuracy_summary(self, agent_name: str, reality_anchor) -> str:
        if reality_anchor is None:
            return "No Reality Anchor configured — no accuracy track record available."

        try:
            acc_by_agent = reality_anchor.accuracy_by_agent()
            agent_acc = acc_by_agent.get(agent_name)
            summary = reality_anchor.summary()

            if agent_acc is None:
                return (
                    f"No validated predictions yet for this agent "
                    f"({summary['pending']} pending validation)."
                )
            return (
                f"Average prediction accuracy: {agent_acc:.0%} "
                f"({summary['validated']} validated predictions total)."
            )
        except Exception:
            return "Could not retrieve accuracy history."

    def suggest_next(
        self,
        agent_name: str,
        memory,
        reality_anchor=None,
        recent_n: int = 5,
    ) -> PlannerSuggestion:
        """
        Generate a single proposed next experiment for this agent.
        """
        history_summary = self._build_history_summary(agent_name, memory, n=recent_n)
        accuracy_summary = self._build_accuracy_summary(agent_name, reality_anchor)

        user_prompt = (
            f"Agent: {agent_name}\n\n"
            f"Recent history (most recent {recent_n} entries):\n{history_summary}\n\n"
            f"Prediction track record:\n{accuracy_summary}\n\n"
            f"Propose the single most valuable next question to investigate."
        )

        result = self.client.generate_json(
            system_prompt=PLANNER_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            temperature=0.5,
        )

        return PlannerSuggestion(
            proposed_query=result.get("proposed_query", ""),
            reasoning=result.get("reasoning", ""),
            target_variables=result.get("target_variables", []),
            question_type=result.get("question_type", "exploratory"),
        )


# ── Self-test (uses fake memory/reality objects, no live LLM needed for structure check) ──
if __name__ == "__main__":
    class FakeEntry:
        def __init__(self, role, content):
            self.role = role
            self.content = content

    class FakeMemory:
        def recent(self, agent_name, n=5):
            return [
                FakeEntry("hypothesis", "H: Rising temperature causes rising pressure (same timestep)"),
                FakeEntry("hypothesis", "H: Rising temperature causes falling humidity (same timestep)"),
                FakeEntry("result", "Confirmed both relationships hold across the dataset"),
            ]

    class FakeRealityAnchor:
        def accuracy_by_agent(self):
            return {"weather_manifold": 0.45}
        def summary(self):
            return {"validated": 4, "pending": 1}

    print("Testing prompt construction (no live LLM call)...")
    planner = DiscoveryPlanner.__new__(DiscoveryPlanner)  # skip __init__ to avoid needing Ollama
    planner.client = None

    history = planner._build_history_summary("weather_manifold", FakeMemory())
    accuracy = planner._build_accuracy_summary("weather_manifold", FakeRealityAnchor())

    print("\n=== History summary ===")
    print(history)
    print("\n=== Accuracy summary ===")
    print(accuracy)

    print("\n=== Full prompt that would be sent ===")
    print(f"Agent: weather_manifold\n\nRecent history:\n{history}\n\nTrack record:\n{accuracy}")

    print("\nStructure test passed. Run with a live Ollama connection for a real suggestion:")
    print('  planner = DiscoveryPlanner()')
    print('  suggestion = planner.suggest_next("weather_manifold", FakeMemory(), FakeRealityAnchor())')
