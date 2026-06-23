"""
vector_memory.py
=================
Gap 2 fix: Semantic vector memory, upgrading from keyword-only recall.

If ChromaDB is installed, uses real embedding-based similarity search.
If not, gracefully falls back to the original keyword matching —
the system never crashes due to a missing dependency.

Install for full functionality:
    pip install chromadb
"""

from __future__ import annotations
import json
import time
import uuid
from pathlib import Path
from typing import Any, Optional

try:
    import chromadb
    _CHROMA_AVAILABLE = True
except ImportError:
    _CHROMA_AVAILABLE = False


class _MemEntryView:
    """
    Lightweight attribute-access wrapper around a memory entry dict,
    so VectorMemoryLayer is a true drop-in replacement for
    harness.MemoryLayer (whose entries are MemoryEntry objects with
    .id, .content, .timestamp, etc. — not dict keys).
    """
    __slots__ = ("_d",)

    def __init__(self, d: dict):
        object.__setattr__(self, "_d", d)

    def __getattr__(self, name):
        try:
            return self._d[name]
        except KeyError:
            raise AttributeError(name)

    def __getitem__(self, key):
        return self._d[key]

    def get(self, key, default=None):
        return self._d.get(key, default)

    def to_dict(self) -> dict:
        return dict(self._d)

    def __repr__(self):
        return f"_MemEntryView({self._d!r})"


class VectorMemoryLayer:
    """
    Drop-in upgrade for MemoryLayer (harness.py) that adds semantic
    similarity search on top of the existing JSON-backed storage.

    Interface-compatible with MemoryLayer — same method signatures —
    so it can replace it in harness.py without changing Agent code.
    """

    def __init__(self, path: str = "memory"):
        self.base_path = Path(path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self._cache: dict[str, list] = {}

        self.semantic_enabled = _CHROMA_AVAILABLE
        if self.semantic_enabled:
            self._chroma_client = chromadb.PersistentClient(
                path=str(self.base_path / "_vector_store")
            )
        else:
            self._chroma_client = None

    # ── Same data model as MemoryLayer ───────────────────────────
    def _agent_file(self, agent: str) -> Path:
        safe = agent.replace(" ", "_").lower()
        return self.base_path / f"{safe}_memory.json"

    def _agent_collection(self, agent: str):
        if not self.semantic_enabled:
            return None
        safe = agent.replace(" ", "_").lower()
        return self._chroma_client.get_or_create_collection(name=f"mem_{safe}")

    def _load(self, agent: str) -> list[dict]:
        if agent in self._cache:
            return self._cache[agent]
        f = self._agent_file(agent)
        entries = json.loads(f.read_text()) if f.exists() else []
        self._cache[agent] = entries
        return entries

    def _save(self, agent: str):
        entries = self._cache.get(agent, [])
        self._agent_file(agent).write_text(json.dumps(entries, indent=2))

    def write(self, agent: str, role: str, content: str, metadata: dict | None = None) -> "_MemEntryView":
        entries = self._load(agent)
        entry = {
            "id": uuid.uuid4().hex[:8],
            "agent": agent,
            "timestamp": time.time(),
            "role": role,
            "content": content,
            "metadata": metadata or {},
        }
        entries.append(entry)
        self._save(agent)

        if self.semantic_enabled:
            try:
                coll = self._agent_collection(agent)
                coll.add(
                    documents=[content],
                    ids=[entry["id"]],
                    metadatas=[{"role": role, "timestamp": entry["timestamp"]}],
                )
            except Exception:
                pass  # semantic indexing is best-effort; JSON storage is source of truth

        return _MemEntryView(entry)

    def recall(self, agent: str, query: str, n: int = 5) -> list["_MemEntryView"]:
        """
        Semantic recall if ChromaDB available, else falls back to keyword match.
        """
        if self.semantic_enabled:
            try:
                coll = self._agent_collection(agent)
                results = coll.query(query_texts=[query], n_results=min(n, max(coll.count(), 1)))
                if results and results.get("ids") and results["ids"][0]:
                    ids = set(results["ids"][0])
                    entries = self._load(agent)
                    return [_MemEntryView(e) for e in entries if e["id"] in ids]
            except Exception:
                pass  # fall through to keyword search

        # Keyword fallback (same logic as original MemoryLayer)
        entries = self._load(agent)
        keywords = set(query.lower().split())
        scored = []
        for e in entries:
            hits = sum(1 for kw in keywords if kw in e["content"].lower())
            if hits > 0:
                scored.append((hits, e))
        scored.sort(key=lambda x: (-x[0], -x[1]["timestamp"]))
        return [_MemEntryView(e) for _, e in scored[:n]]

    def recent(self, agent: str, n: int = 10) -> list["_MemEntryView"]:
        entries = self._load(agent)
        sorted_entries = sorted(entries, key=lambda e: -e["timestamp"])[:n]
        return [_MemEntryView(e) for e in sorted_entries]

    def clear(self, agent: str):
        self._cache[agent] = []
        f = self._agent_file(agent)
        if f.exists():
            f.unlink()
        if self.semantic_enabled:
            try:
                safe = agent.replace(" ", "_").lower()
                self._chroma_client.delete_collection(name=f"mem_{safe}")
            except Exception:
                pass

    def all_agents(self) -> list[str]:
        return [f.stem.replace("_memory", "") for f in self.base_path.glob("*_memory.json")]

    def summary(self, agent: str) -> dict[str, Any]:
        entries = self._load(agent)
        by_role: dict[str, int] = {}
        for e in entries:
            by_role[e["role"]] = by_role.get(e["role"], 0) + 1
        return {
            "agent": agent,
            "total_entries": len(entries),
            "by_role": by_role,
            "oldest": entries[0]["timestamp"] if entries else None,
            "newest": entries[-1]["timestamp"] if entries else None,
            "semantic_search": self.semantic_enabled,
        }


# ── Self-test ─────────────────────────────────────────────────────
if __name__ == "__main__":
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        mem = VectorMemoryLayer(path=tmp)
        print(f"Semantic search enabled: {mem.semantic_enabled}")

        mem.write("test_agent", "hypothesis", "Rising temperature causes increased pressure in sealed systems")
        mem.write("test_agent", "hypothesis", "Stock prices fall when interest rates rise sharply")
        mem.write("test_agent", "result", "Confirmed thermal expansion drives the pressure increase")

        results = mem.recall("test_agent", "thermal effects on gas pressure", n=2)
        print(f"\nRecall results for 'thermal effects on gas pressure':")
        for r in results:
            print(f"  [{r['role']}] {r['content']}")

        print(f"\nSummary: {mem.summary('test_agent')}")
