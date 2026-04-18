import networkx as nx
import random
from intelligence.bayesian_core import BayesianNetwork

class SmartCitySimulator:
    """
    Simulates cascading failures across Smart City infrastructure.
    Nodes: Power (P), Comms (C), Transport (T), Water (W), Emergency (E).
    """
    def __init__(self):
        self.G = nx.DiGraph()
        self.nodes = {
            "P": "Power Grid Substation",
            "C": "Communications Backbone",
            "T": "Traffic & Transit Control",
            "W": "Water Treatment & Pumps",
            "E": "Emergency Response Center"
        }
        self.G.add_nodes_from(self.nodes.keys())
        
        # Physical & Cyber Dependencies (Edges)
        # Power is the primary driver
        self.G.add_edge("P", "C")
        self.G.add_edge("P", "W")
        self.G.add_edge("C", "T")
        self.G.add_edge("C", "E")
        self.G.add_edge("T", "E") # Transport affects emergency speed
        
        # State tracking
        self.node_states = {n: {
            "status": "OPERATIONAL",
            "integrity": 1.0, # 0.0 to 1.0
            "backups_active": False,
            "load": random.uniform(0.3, 0.6)
        } for n in self.nodes}
        
        self.bayesian_net = BayesianNetwork()
        for u, v in self.G.edges():
            # Higher weight means stronger dependency
            weight = 0.8 if u == "P" else 0.6
            self.bayesian_net.add_dependency(u, v, weight)

    def inject_shock(self, target_node, shock_type="Failure", intensity=0.8):
        """
        Injects a system shock and propagates cascades.
        """
        print(f"[SIMULATOR] Injecting {shock_type} shock on {target_node} ({intensity})")
        
        # Update target node
        self.node_states[target_node]["integrity"] -= intensity
        if self.node_states[target_node]["integrity"] < 0.3:
            self.node_states[target_node]["status"] = "FAILURE"
        elif self.node_states[target_node]["integrity"] < 0.7:
            self.node_states[target_node]["status"] = "UNSTABLE"

        # Propagate using Bayesian logic
        risk_map = {target_node: 1.0 - self.node_states[target_node]["integrity"]}
        cascade_results = self.bayesian_net.propagate(risk_map)
        
        # Update system states based on cascade
        for node, prob in cascade_results.items():
            if node != target_node:
                # Probability of failure impacts integrity
                impact = prob * 0.5 # Cascade is slightly dampended unless cumulative
                self.node_states[node]["integrity"] -= impact
                if self.node_states[node]["integrity"] < 0.4:
                    self.node_states[node]["status"] = "FAILURE"
                elif self.node_states[node]["integrity"] < 0.75:
                    self.node_states[node]["status"] = "DEGRADED"

        return self._format_results(cascade_results)

    def apply_resilience_action(self, node, action):
        """
        Applies a resilience/mitigation action (e.g., Load Shedding, Backup).
        """
        if action == "Activate Backup":
            self.node_states[node]["backups_active"] = True
            self.node_states[node]["integrity"] = min(1.0, self.node_states[node]["integrity"] + 0.4)
            self.node_states[node]["status"] = "BACKUP_RUNNING"
        elif action == "Load Shedding":
            self.node_states[node]["load"] *= 0.5
            self.node_states[node]["integrity"] = min(1.0, self.node_states[node]["integrity"] + 0.2)
            self.node_states[node]["status"] = "THROTTLED"
        elif action == "Reroute Flow":
            self.node_states[node]["integrity"] = min(1.0, self.node_states[node]["integrity"] + 0.3)
            self.node_states[node]["status"] = "RECOVERING"

        return {"status": "SUCCESS", "new_state": self.node_states[node]}

    def _format_results(self, cascade_results):
        formatted = {}
        for node in self.nodes:
            formatted[node] = {
                "name": self.nodes[node],
                "status": self.node_states[node]["status"],
                "integrity": round(self.node_states[node]["integrity"], 2),
                "cascade_risk": round(cascade_results.get(node, 0.0), 2),
                "anomaly_prediction": 1.0 - self.node_states[node]["integrity"]
            }
        return formatted

if __name__ == "__main__":
    sim = SmartCitySimulator()
    print("Initial State:", sim.node_states)
    results = sim.inject_shock("P", intensity=0.9)
    print("\nState after Power Failure:")
    for n, r in results.items():
        print(f"{n}: {r['status']} | Cascade Risk: {r['cascade_risk']}")
