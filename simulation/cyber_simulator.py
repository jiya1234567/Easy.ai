import numpy as np
import pandas as pd
import networkx as nx
from intelligence.bayesian_core import BayesianNetwork

class CyberSimulator:
    def __init__(self, data_path="reports/cyber_test_advanced.csv"):
        self.data_path = data_path
        self.data = None
        self.G = self._build_network()
        # Initialize Node States
        self.node_states = {
            node: {"status": "HEALTHY", "patch_level": 0.5, "protection": 0.5} 
            for node in self.G.nodes
        }
        self.bayesian_net = BayesianNetwork(self._get_adjacency_dict())

    def _build_network(self):
        G = nx.Graph()
        G.add_edges_from([
            ("N3", "N1"), ("N3", "N2"), ("N3", "N4"), ("N3", "N5"),
            ("N4", "N1"), ("N4", "N2")
        ])
        return G

    def _get_adjacency_dict(self):
        adj = {}
        for node in self.G.nodes:
            adj[node] = {neighbor: 0.7 for neighbor in self.G.neighbors(node)}
        return adj

    def simulate_attack(self, target_node, attack_type="DDoS", payload_intensity=1.0):
        if target_node not in self.G.nodes:
            return {"error": f"Node {target_node} not found in network."}

        # Check if node is already isolated
        if self.node_states[target_node]["status"] == "ISOLATED":
            return {target_node: {"status": "ISOLATED", "impact": 0.0, "msg": "Attack blocked by isolation."}}

        # Use Bayesian Propagation for Spread
        # Initial compromise probability depends on intensity and node protection
        node_prot = self.node_states[target_node]["protection"]
        compromise_prob = max(0.0, payload_intensity - (node_prot * 0.5))
        
        impact_map = self.bayesian_net.propagate({target_node: compromise_prob})
        
        results = {}
        for node, prob in impact_map.items():
            status = "HEALTHY"
            if prob > 0.8: status = "COMPROMISED"
            elif prob > 0.5: status = "INCIDENT"
            elif prob > 0.2: status = "WARNING"
            
            self.node_states[node]["status"] = status
            
            # GAP 2: Runtime Behavioral Reasoning (Causal Tracing)
            syscall_drift = "Normal"
            memory_mutation = "Stable"
            priv_escalation = "None"
            
            if status in ["COMPROMISED", "INCIDENT"]:
                syscall_drift = f"Anomaly_{np.random.randint(100, 999)}"
                memory_mutation = "Heap_Corruption_Detected" if prob > 0.7 else "Stack_Buffer_Warning"
                priv_escalation = "Root_Access_Obtained" if prob > 0.85 else "User_Level_Pivot"

            results[node] = {
                "type": attack_type if node == target_node else "Lateral Movement",
                "anomaly_prediction": prob,
                "status": status,
                "runtime_causality": {
                    "syscall_drift": syscall_drift,
                    "memory_mutation": memory_mutation,
                    "privilege_escalation": priv_escalation,
                    "propagation_risk": prob * 1.5
                }
            }

        return results

    def apply_mitigation(self, target_node, action="Block"):
        if target_node not in self.node_states:
            return {"error": "Node not found"}

        if action == "Block" or action == "Isolate":
            self.node_states[target_node]["status"] = "ISOLATED"
            self.node_states[target_node]["protection"] = 1.0
            return {"effectiveness": 0.99, "status": "ISOLATED"}
        elif action == "Patch":
            # GAP 4: Causal Patch Verification
            # Simulate applying the patch to check for regressions
            dependency_stability = np.random.uniform(0.0, 1.0)
            
            if dependency_stability < 0.2:
                # Patch breaks logic
                return {
                    "effectiveness": 0.0, 
                    "error": "Patch verification failed: Destabilizes downstream dependencies.",
                    "regression_risk": 1.0 - dependency_stability
                }
                
            self.node_states[target_node]["patch_level"] = min(1.0, self.node_states[target_node]["patch_level"] + 0.3)
            self.node_states[target_node]["protection"] = min(1.0, self.node_states[target_node]["protection"] + 0.2)
            return {
                "effectiveness": 0.70, 
                "new_patch_level": self.node_states[target_node]["patch_level"],
                "verification_status": "Passed",
                "regression_risk": 1.0 - dependency_stability
            }
        
        return {"effectiveness": 0.0}

if __name__ == "__main__":
    sim = CyberSimulator()
    print("Initial States:", sim.node_states)
    res = sim.simulate_attack("N3", "BruteForce", 0.9)
    print("Attack Results:", res)
    print("Post-Attack States:", sim.node_states)
    sim.apply_mitigation("N3", "Block")
    print("Post-Mitigation States:", sim.node_states)
