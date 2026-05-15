import json
import os
import time
import hashlib

class MemoryController:
    """
    Tiered Memory System for OMEGA-CORE.
    Implements Episodic (events), Semantic (facts), and Identity (persistence).
    """
    def __init__(self, base_path="intelligence/memory"):
        self.base_path = base_path
        self.episodic_path = os.path.join(base_path, "episodic.json")
        self.semantic_path = os.path.join(base_path, "semantic.json")
        self.identity_path = os.path.join(base_path, "identity_anchor.json")
        
        if not os.path.exists(base_path):
            os.makedirs(base_path)
            
        self.episodic = self._load_file(self.episodic_path, [])
        self.semantic = self._load_file(self.semantic_path, {})
        self.identity = self._load_file(self.identity_path, {"anchor_hash": "", "last_sync": 0})

    def _load_file(self, path, default):
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    return json.load(f)
            except: return default
        return default

    def _save_file(self, path, data):
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)

    def record_episode(self, domain, state_vector, result):
        """
        Stores a specific event/cycle (Episodic Memory).
        """
        episode = {
            "ts": time.time(),
            "domain": domain,
            "state_vector": state_vector,
            "outcome": result.get("execute", {}).get("action", "No action")
        }
        self.episodic.append(episode)
        # Keep last 500 episodes
        self._save_file(self.episodic_path, self.episodic[-500:])
        return episode

    def update_semantic_knowledge(self, domain, attribution_report):
        """
        Distills 'Facts' from attribution reports (Semantic Memory).
        """
        if domain not in self.semantic:
            self.semantic[domain] = {"known_anchors": {}, "causal_laws": []}
            
        # Update influence history of anchors
        for anchor in attribution_report.get('anchors', []):
            node = anchor['node']
            inf = anchor['influence']
            if node not in self.semantic[domain]["known_anchors"]:
                self.semantic[domain]["known_anchors"][node] = {"count": 0, "avg_influence": 0}
            
            entry = self.semantic[domain]["known_anchors"][node]
            entry["avg_influence"] = (entry["avg_influence"] * entry["count"] + inf) / (entry["count"] + 1)
            entry["count"] += 1

        self._save_file(self.semantic_path, self.semantic)

    def generate_identity_anchor(self, current_state):
        """
        Creates a 'Self-Fingerprint' to detect Identity Drift.
        """
        # Hash core config and current stability
        core_str = f"OMEGA-CORE-V2.5-{current_state.get('workspace_coherence', 1.0)}"
        new_hash = hashlib.sha256(core_str.encode()).hexdigest()
        
        drift_detected = False
        if self.identity["anchor_hash"] and self.identity["anchor_hash"] != new_hash:
            drift_detected = True
            
        self.identity = {
            "anchor_hash": new_hash,
            "last_sync": time.time(),
            "drift_detected": drift_detected
        }
        self._save_file(self.identity_path, self.identity)
        return self.identity

    def get_recall(self, domain, limit=3):
        """
        Retrieves relevant past episodes for a given domain.
        """
        relevant = [e for e in self.episodic if e['domain'] == domain]
        return relevant[-limit:]

if __name__ == "__main__":
    mc = MemoryController()
    mc.record_episode("Health", {"workspace_coherence": 0.9}, {"execute": {"action": "Optimized dose"}})
    print("Semantic Memory updated.")
