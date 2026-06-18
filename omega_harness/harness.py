"""
harness.py — OMEGA-CORE Agent Harness
=======================================
Implements: AGENT = LLM + HARNESS

The Core Harness looping runtime:
    1. CONTEXT   — load memory + current state
    2. OBSERVE   — ingest sensor/tool data
    3. REASON    — call LLM (Mistral primary, Phi3 challenger)
    4. ACT       — execute tools, write memory, return result

Every tab in the OMEGA-CORE dashboard is one Agent instance
with its own PROMPT blueprint and TOOLS, sharing the same
MemoryLayer and LLM pool.

Usage:
    from harness import Agent, MemoryLayer, ToolRegistry

    mem   = MemoryLayer(path="C:/Universal_Lab_AP_Phillips/memory")
    tools = ToolRegistry()
    agent = Agent(name="finance", memory=mem, tools=tools)
    result = agent.run("What is driving the tech selloff?", context_data={...})
"""

from __future__ import annotations

import json
import time
import uuid
import hashlib
from pathlib import Path
from typing import Any, Callable, Optional
from dataclasses import dataclass, field

import ollama


# ─────────────────────────────────────────────────────────────────
# LLM Pool — Mistral (primary) + Phi3 (challenger)
# ─────────────────────────────────────────────────────────────────

PRIMARY_MODEL   = "mistral"
CHALLENGER_MODEL = "phi3"

_ollama_client = ollama.Client()


def _llm_call(model: str, system: str, user: str, temperature: float = 0.4) -> str:
    """Single LLM call, returns raw text."""
    response = _ollama_client.chat(
        model=model,
        messages=[
            {"role": "system",  "content": system},
            {"role": "user",    "content": user},
        ],
        options={"temperature": temperature},
    )
    return response["message"]["content"]


def _llm_json(model: str, system: str, user: str, temperature: float = 0.3) -> dict[str, Any]:
    """LLM call that enforces JSON output with retry."""
    import re
    messages = [
        {"role": "system", "content": system + "\n\nYou MUST respond with valid JSON only. No prose, no markdown fences."},
        {"role": "user",   "content": user},
    ]
    for attempt in range(3):
        response = _ollama_client.chat(model=model, messages=messages, options={"temperature": temperature})
        raw = response["message"]["content"].strip()
        raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw, flags=re.DOTALL).strip()
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            messages.append({"role": "assistant", "content": raw})
            messages.append({"role": "user", "content": "Invalid JSON. Reply with ONLY a valid JSON object."})
    raise ValueError(f"LLM ({model}) failed to return valid JSON after 3 attempts")


# ─────────────────────────────────────────────────────────────────
# Memory Layer — persistent JSON vector cache on disk
# ─────────────────────────────────────────────────────────────────

@dataclass
class MemoryEntry:
    id: str
    agent: str
    timestamp: float
    role: str            # "observation" | "hypothesis" | "action" | "result"
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id, "agent": self.agent,
            "timestamp": self.timestamp, "role": self.role,
            "content": self.content, "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "MemoryEntry":
        return cls(**d)


class MemoryLayer:
    """
    Persistent memory that survives restarts.
    Stores entries as a JSON file per agent namespace.
    Supports simple keyword recall (no vector DB required — 
    can be upgraded to ChromaDB later without changing the interface).
    """

    def __init__(self, path: str = "memory"):
        self.base_path = Path(path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self._cache: dict[str, list[MemoryEntry]] = {}

    def _agent_file(self, agent: str) -> Path:
        safe = agent.replace(" ", "_").lower()
        return self.base_path / f"{safe}_memory.json"

    def _load(self, agent: str) -> list[MemoryEntry]:
        if agent in self._cache:
            return self._cache[agent]
        f = self._agent_file(agent)
        if f.exists():
            raw = json.loads(f.read_text())
            entries = [MemoryEntry.from_dict(e) for e in raw]
        else:
            entries = []
        self._cache[agent] = entries
        return entries

    def _save(self, agent: str):
        entries = self._cache.get(agent, [])
        self._agent_file(agent).write_text(
            json.dumps([e.to_dict() for e in entries], indent=2)
        )

    def write(self, agent: str, role: str, content: str, metadata: dict | None = None) -> MemoryEntry:
        entries = self._load(agent)
        entry = MemoryEntry(
            id=uuid.uuid4().hex[:8],
            agent=agent,
            timestamp=time.time(),
            role=role,
            content=content,
            metadata=metadata or {},
        )
        entries.append(entry)
        self._save(agent)
        return entry

    def recall(self, agent: str, query: str, n: int = 5) -> list[MemoryEntry]:
        """
        Simple keyword-based recall.
        Returns the n most recent entries whose content contains
        any word from the query (case-insensitive).
        """
        entries = self._load(agent)
        keywords = set(query.lower().split())
        scored = []
        for e in entries:
            hits = sum(1 for kw in keywords if kw in e.content.lower())
            if hits > 0:
                scored.append((hits, e))
        scored.sort(key=lambda x: (-x[0], -x[1].timestamp))
        return [e for _, e in scored[:n]]

    def recent(self, agent: str, n: int = 10) -> list[MemoryEntry]:
        entries = self._load(agent)
        return sorted(entries, key=lambda e: -e.timestamp)[:n]

    def clear(self, agent: str):
        self._cache[agent] = []
        f = self._agent_file(agent)
        if f.exists():
            f.unlink()

    def all_agents(self) -> list[str]:
        return [f.stem.replace("_memory", "") for f in self.base_path.glob("*_memory.json")]

    def summary(self, agent: str) -> dict[str, Any]:
        entries = self._load(agent)
        by_role: dict[str, int] = {}
        for e in entries:
            by_role[e.role] = by_role.get(e.role, 0) + 1
        return {
            "agent": agent,
            "total_entries": len(entries),
            "by_role": by_role,
            "oldest": entries[0].timestamp if entries else None,
            "newest": entries[-1].timestamp if entries else None,
        }


# ─────────────────────────────────────────────────────────────────
# Tool Registry — pluggable function dispatch
# ─────────────────────────────────────────────────────────────────

class ToolRegistry:
    """
    Registry of callable tools available to agents.
    Each tool is a plain Python function registered with a name
    and description. The LLM sees the name + description when
    deciding whether to call a tool.
    """

    def __init__(self):
        self._tools: dict[str, dict[str, Any]] = {}

    def register(self, name: str, description: str, fn: Callable) -> None:
        self._tools[name] = {"name": name, "description": description, "fn": fn}

    def call(self, name: str, **kwargs) -> Any:
        if name not in self._tools:
            raise KeyError(f"Unknown tool: {name}. Available: {list(self._tools)}")
        return self._tools[name]["fn"](**kwargs)

    def catalog(self) -> list[dict[str, str]]:
        return [{"name": t["name"], "description": t["description"]}
                for t in self._tools.values()]

    def has(self, name: str) -> bool:
        return name in self._tools


# ─────────────────────────────────────────────────────────────────
# Agent — the core harness loop
# ─────────────────────────────────────────────────────────────────

@dataclass
class AgentResult:
    agent: str
    run_id: str
    timestamp: float
    query: str
    context_summary: str
    observation: str
    primary_reasoning: str
    challenger_reasoning: str
    arbiter_decision: str
    final_answer: str
    actions_taken: list[str]
    memory_entries_written: int
    duration_seconds: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "agent": self.agent,
            "run_id": self.run_id,
            "timestamp": self.timestamp,
            "query": self.query,
            "context_summary": self.context_summary,
            "observation": self.observation,
            "primary_reasoning": self.primary_reasoning,
            "challenger_reasoning": self.challenger_reasoning,
            "arbiter_decision": self.arbiter_decision,
            "final_answer": self.final_answer,
            "actions_taken": self.actions_taken,
            "memory_entries_written": self.memory_entries_written,
            "duration_seconds": self.duration_seconds,
        }


class Agent:
    """
    OMEGA-CORE Agent: implements AGENT = LLM + HARNESS

    Loop:
        1. CONTEXT  — assemble memory + state into a context string
        2. OBSERVE  — run observation tools, ingest context_data
        3. REASON   — Mistral proposes, Phi3 challenges, arbiter picks
        4. ACT      — write memory, optionally call action tools

    One Agent instance per OMEGA tab. All share the same
    MemoryLayer and ToolRegistry passed at construction.
    """

    def __init__(
        self,
        name: str,
        prompt_blueprint: str,
        memory: MemoryLayer,
        tools: ToolRegistry,
        observe_tool: Optional[str] = None,   # tool name for observation step
        action_tool: Optional[str] = None,    # tool name for action step
        use_debate: bool = True,              # enable Mistral vs Phi3 debate
        memory_recall_n: int = 5,
    ):
        self.name = name
        self.prompt_blueprint = prompt_blueprint
        self.memory = memory
        self.tools = tools
        self.observe_tool = observe_tool
        self.action_tool = action_tool
        self.use_debate = use_debate
        self.memory_recall_n = memory_recall_n

    # ── 1. CONTEXT ────────────────────────────────────────────────
    def _build_context(self, query: str) -> str:
        recent = self.memory.recent(self.name, n=self.memory_recall_n)
        recalled = self.memory.recall(self.name, query, n=3)

        all_entries = {e.id: e for e in recent + recalled}
        sorted_entries = sorted(all_entries.values(), key=lambda e: e.timestamp)

        if not sorted_entries:
            return "No prior memory for this agent."

        lines = [f"[{e.role.upper()} @ {time.strftime('%H:%M:%S', time.localtime(e.timestamp))}] {e.content[:300]}"
                 for e in sorted_entries[-8:]]
        return "\n".join(lines)

    # ── 2. OBSERVE ────────────────────────────────────────────────
    def _observe(self, context_data: dict[str, Any]) -> str:
        parts = []
        if context_data:
            parts.append("Input data summary:")
            for k, v in context_data.items():
                if isinstance(v, list):
                    parts.append(f"  {k}: {len(v)} values, range [{min(v):.2f}, {max(v):.2f}]")
                elif isinstance(v, dict):
                    parts.append(f"  {k}: {list(v.keys())}")
                else:
                    parts.append(f"  {k}: {str(v)[:100]}")

        if self.observe_tool and self.tools.has(self.observe_tool):
            try:
                tool_output = self.tools.call(self.observe_tool, data=context_data)
                parts.append(f"Tool [{self.observe_tool}] output: {json.dumps(tool_output)[:500]}")
            except Exception as e:
                parts.append(f"Tool [{self.observe_tool}] error: {e}")

        return "\n".join(parts) if parts else "No structured observations."

    # ── 3. REASON (dual-pathway debate) ───────────────────────────
    def _reason(self, query: str, context: str, observation: str) -> tuple[str, str, str]:
        """
        Returns (primary_reasoning, challenger_reasoning, arbiter_decision)
        """
        tools_info = json.dumps(self.tools.catalog(), indent=2) if self.tools.catalog() else "None"

        system_base = f"""{self.prompt_blueprint}

MEMORY CONTEXT:
{context}

OBSERVATION:
{observation}

AVAILABLE TOOLS:
{tools_info}

Respond with a clear, structured answer to the query. Be specific and grounded."""

        # Primary: Mistral proposes
        primary = _llm_call(
            PRIMARY_MODEL,
            system_base,
            f"Query: {query}\n\nProvide your analysis and recommendation.",
        )

        if not self.use_debate:
            return primary, "", primary

        # Challenger: Phi3 challenges or extends
        challenger = _llm_call(
            CHALLENGER_MODEL,
            system_base + f"\n\nPrimary analysis to challenge:\n{primary[:800]}",
            f"Query: {query}\n\nChallenge, extend, or refine the primary analysis. "
            "Point out any missed factors, logical gaps, or alternative explanations.",
        )

        # Arbiter: Mistral picks the stronger path
        arbiter_system = """You are an arbiter. Given two analyses of the same query,
pick the stronger elements from each and synthesize a final decision.
Be concise. State which reasoning was stronger and why, then give the final answer."""

        arbiter = _llm_call(
            PRIMARY_MODEL,
            arbiter_system,
            f"Query: {query}\n\nAnalysis A (Primary):\n{primary[:600]}\n\n"
            f"Analysis B (Challenger):\n{challenger[:600]}\n\n"
            "Synthesize the best final answer.",
            temperature=0.2,
        )

        return primary, challenger, arbiter

    # ── 4. ACT ────────────────────────────────────────────────────
    def _act(self, final_answer: str, context_data: dict[str, Any]) -> list[str]:
        actions = []

        # Always write the final answer to memory
        self.memory.write(
            self.name, "result", final_answer[:1000],
            metadata={"timestamp": time.time()}
        )
        actions.append("wrote result to memory")

        # Optionally call an action tool
        if self.action_tool and self.tools.has(self.action_tool):
            try:
                self.tools.call(self.action_tool, answer=final_answer, data=context_data)
                actions.append(f"called action tool: {self.action_tool}")
            except Exception as e:
                actions.append(f"action tool failed: {e}")

        return actions

    # ── PUBLIC: run one full loop ──────────────────────────────────
    def run(self, query: str, context_data: dict[str, Any] | None = None) -> AgentResult:
        t0 = time.time()
        run_id = uuid.uuid4().hex[:8]
        context_data = context_data or {}

        # Log the incoming query
        self.memory.write(self.name, "observation", f"Query: {query}", {"run_id": run_id})

        # 1. CONTEXT
        context = self._build_context(query)

        # 2. OBSERVE
        observation = self._observe(context_data)
        self.memory.write(self.name, "observation", observation[:500], {"run_id": run_id})

        # 3. REASON
        primary, challenger, arbiter = self._reason(query, context, observation)
        self.memory.write(self.name, "hypothesis", primary[:500], {"run_id": run_id, "model": PRIMARY_MODEL})
        if challenger:
            self.memory.write(self.name, "hypothesis", f"[CHALLENGE] {challenger[:400]}", {"run_id": run_id, "model": CHALLENGER_MODEL})

        final_answer = arbiter if arbiter else primary

        # 4. ACT
        actions = self._act(final_answer, context_data)

        return AgentResult(
            agent=self.name,
            run_id=run_id,
            timestamp=time.time(),
            query=query,
            context_summary=context[:300],
            observation=observation[:300],
            primary_reasoning=primary,
            challenger_reasoning=challenger,
            arbiter_decision=arbiter,
            final_answer=final_answer,
            actions_taken=actions,
            memory_entries_written=len(actions),
            duration_seconds=round(time.time() - t0, 2),
        )
