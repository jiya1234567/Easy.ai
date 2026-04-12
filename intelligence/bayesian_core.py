import json
import numpy as np

class BayesianGuard:
    def update_belief(self, prior, likelihood):
        """Bayesian Inference: P(H|E) = (P(E|H) * P(H)) / P(E)"""
        epsilon = 1e-9
        numerator = likelihood * prior
        denominator = numerator + (1 - likelihood) * (1 - prior) + epsilon
        return round(min(0.9999, numerator / denominator), 4)

class BayesianNetwork:
    """
    Manages probabilistic risk propagation across a network of nodes.
    Supports weighted dependencies.
    """
    def __init__(self, adjacency_matrix=None, initial_priors=None):
        self.adj = adjacency_matrix if adjacency_matrix else {} # {node: {neighbor: weight}}
        self.nodes = list(self.adj.keys())
        self.priors = initial_priors if initial_priors else {}

    def add_dependency(self, u, v, weight=0.7):
        if u not in self.adj:
            self.adj[u] = {}
        self.adj[u][v] = weight
        if u not in self.nodes: self.nodes.append(u)
        if v not in self.nodes: self.nodes.append(v)

    def propagate(self, incident_map):
        """
        Calculates the probability of spread starting from an incident map.
        incident_map: {node: severity_prob}
        """
        results = incident_map.copy()
        queue = list(incident_map.items())
        visited = set(incident_map.keys())

        while queue:
            curr, prob = queue.pop(0)
            neighbors = self.adj.get(curr, {})
            
            for neighbor, weight in neighbors.items():
                # Spread probability is Current_Prob * Dependency_Weight
                spread_prob = prob * weight
                
                # If neighbor already has a probability, take the max (or combine)
                if neighbor in results:
                    results[neighbor] = max(results[neighbor], round(spread_prob, 4))
                else:
                    results[neighbor] = round(spread_prob, 4)
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, spread_prob))
        
        return results

if __name__ == "__main__":
    bn = BayesianNetwork()
    bn.add_dependency("P", "C", 0.9)
    bn.add_dependency("C", "T", 0.8)
    impact = bn.propagate({"P": 1.0})
    print(f"Cascading Risk from Power Failure: {impact}")
