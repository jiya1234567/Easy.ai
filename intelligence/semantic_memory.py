import json
import os
import math

class SemanticMemoryStore:
    """
    Addresses GAP 1: Semantic Exploit Memory
    Long-term exploit motif memory enabling transfer learning across repositories.
    """
    def __init__(self, data_path="data/exploit_motifs.json"):
        self.data_path = data_path
        self._ensure_data_dir()
        self.memory = self._load_memory()

    def _ensure_data_dir(self):
        os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
        if not os.path.exists(self.data_path):
            with open(self.data_path, 'w') as f:
                json.dump([], f)

    def _load_memory(self):
        try:
            with open(self.data_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_memory(self):
        with open(self.data_path, 'w') as f:
            json.dump(self.memory, f, indent=2)

    def store_motif(self, motif_name, causal_chain, exploitability_score):
        # Prevent duplicates
        for item in self.memory:
            if item.get("motif") == motif_name:
                item["historical_matches"].append("current_run")
                item["exploitability_score"] = exploitability_score
                self._save_memory()
                return

        new_motif = {
            "motif": motif_name,
            "causal_chain": causal_chain,
            "historical_matches": ["current_run"],
            "exploitability_score": exploitability_score
        }
        self.memory.append(new_motif)
        self._save_memory()

    def retrieve_similar(self, query, threshold=0.3):
        """
        Mock vector similarity based on keyword intersection.
        In a production system, this would use dense embeddings.
        """
        query_words = set(query.lower().split())
        results = []
        for item in self.memory:
            motif_words = set(item.get("motif", "").lower().replace("_", " ").split())
            causal_words = set(str(item.get("causal_chain", "")).lower().split())
            combined = motif_words.union(causal_words)
            
            if not combined:
                continue
                
            intersection = query_words.intersection(combined)
            score = len(intersection) / float(len(combined) + len(query_words) - len(intersection))
            
            if score >= threshold or len(intersection) > 0:
                results.append((score, item))
                
        results.sort(key=lambda x: x[0], reverse=True)
        return [res[1] for res in results]

if __name__ == "__main__":
    store = SemanticMemoryStore()
    store.store_motif("integer_overflow_to_heap_corruption", "math -> buffer -> override", 0.92)
    print("Stored successfully.")
    print("Retrieval test:", store.retrieve_similar("integer overflow error"))
