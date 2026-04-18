import time
import json
import os
import random
import numpy as np
from intelligence.scientific_engine import ScientificEngine
from kernel import CognitiveMemory, record_outcome

class AutonomousResearcher:
    """
    [LEVEL 4: AUTONOMOUS SCIENTIST]
    Upgraded Science Loop with Active Learning & Information Gain prioritization.
    """
    def __init__(self, domain="Materials", data_path="reports/materials_test.csv"):
        self.domain = domain
        self.engine = ScientificEngine(data_path=data_path)
        self.engine.load_data()
        self.log_file = "reports/discovery_log.json"
        self.memory = CognitiveMemory()
        os.makedirs("reports", exist_ok=True)
        self.discoveries = self._load_logs()

    def _load_logs(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, "r") as f: return json.load(f)
        return []

    def _save_logs(self):
        with open(self.log_file, "w") as f: json.dump(self.discoveries, f, indent=2)

    def prioritize_hypothesis(self, graph):
        """
        [ACTIVE LEARNING] 
        Prioritizes links with High Weight + High Uncertainty (Surprise Factor).
        """
        scored_edges = []
        for u, v, attr in graph.edges(data=True):
            weight = abs(attr['weight'])
            uncertainty = attr.get('uncertainty', 0.1)
            # Curiosity Score = weight * (1 + uncertainty)
            # This favors strong links we aren't sure about yet.
            curiosity_score = weight * (1 + uncertainty)
            scored_edges.append((u, v, curiosity_score, attr))
            
        scored_edges = sorted(scored_edges, key=lambda x: x[2], reverse=True)
        return scored_edges[0] if scored_edges else (None, None, 0, None)

    def run_cycle(self):
        """
        Executes an Autonomous Science Cycle.
        """
        print(f"--- [LEVEL 4 RESEARCHER] Cycle Start | Domain: {self.domain} ---")
        
        # 1. Hypothesize via Active Learning
        graph = self.engine.discover_causality()
        u, v, score, attr = self.prioritize_hypothesis(graph)
        
        if not u:
            print("Entropy low. No high-surprise hypothesis found.")
            return

        hypothesis = f"Surprise Target: {u} -> {v} (Active Learning Score: {score:.2f})"
        print(f"SELECTION: {hypothesis}")
        
        # 2. Consult Cognitive Memory for Bias
        bias, success_rate = self.memory.recall(self.domain)
        print(f"COGNITIVE BIAS: {bias} (Past Success: {success_rate:.1%})")
        
        # Adjust intervention based on bias
        perturbation = 1.3 if bias == "Aggressive" else 1.1 if bias == "Defensive" else 1.2
        baseline_val = self.engine.data[u].iloc[-1]
        intervention_val = baseline_val * perturbation
        
        # 3. Experiment
        print(f"EXPERIMENT: Perturbing {u} (Policy: {bias})")
        results, msg = self.engine.simulate_intervention(u, intervention_val, graph=graph)
        
        # 4. Evaluate & Learn
        if v in results["projections"]:
            proj = results["projections"][v]
            discovery = {
                "ts": time.ctime(),
                "domain": self.domain,
                "hypothesis": hypothesis,
                "driver": u, "target": v,
                "delta": proj["delta"],
                "uncertainty": proj["uncertainty_level"],
                "info_gain": score,
                "status": "Verified"
            }
            self.discoveries.append(discovery)
            self._save_logs()
            
            # Record outcome in Cognitive Core
            ctx = {"domain": self.domain, "driver": u, "target": v}
            dec = {"perturbation": perturbation, "score": score}
            eid = self.memory.store(ctx, dec, outcome="Success")
            
            print(f"DISCOVERY: {v} shifted by {proj['delta']:.4f} {proj['uncertainty_level']}")
            print(f"MEMORY: Session archived as {eid}.")
        else:
            print("EXPERIMENT FAILED: Propagation failed.")

        print("-" * 50)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run Autonomous Research Cycle")
    parser.add_argument("--domain", type=str, default="Materials", help="Scientific Domain")
    parser.add_argument("--data", type=str, default="reports/materials_test.csv", help="Dataset Path")
    args = parser.parse_args()

    researcher = AutonomousResearcher(domain=args.domain, data_path=args.data)
    for i in range(3):
        researcher.run_cycle()
        time.sleep(1)
