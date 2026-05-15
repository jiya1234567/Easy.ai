import networkx as nx
import pandas as pd
import numpy as np

class InterpretabilityEngine:
    """
    Provides mechanistic explanations for the ASI framework.
    Translates causal graph dynamics into human-interpretable attribution maps.
    """
    def __init__(self, causal_graph=None):
        self.graph = causal_graph

    def update_graph(self, causal_graph):
        self.graph = causal_graph

    def get_attention_anchors(self, top_n=3):
        """
        Identifies 'Attention Anchors' - nodes with the highest causal influence.
        Uses PageRank as a proxy for signal dominance in the manifold.
        """
        if self.graph is None or len(self.graph.nodes) == 0:
            return []
        
        try:
            # Use PageRank to find influential nodes
            pagerank = nx.pagerank(self.graph, weight='weight')
            sorted_nodes = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)
            return sorted_nodes[:top_n]
        except:
            # Fallback to degree centrality if PageRank fails (e.g. disconnected graph)
            centrality = nx.degree_centrality(self.graph)
            sorted_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
            return sorted_nodes[:top_n]

    def trace_causal_flow(self, target_node, depth=2):
        """
        Explains WHY a specific node moved by tracing its strongest causal ancestors.
        """
        if self.graph is None or target_node not in self.graph.nodes:
            return f"Node {target_node} not found in causal manifold."

        # Get predecessors (drivers of this node)
        predecessors = list(self.graph.predecessors(target_node))
        if not predecessors:
            return f"Node {target_node} is a primary driver (root node)."

        # Sort by weight
        flows = []
        for p in predecessors:
            weight = self.graph[p][target_node].get('weight', 0)
            flows.append({"driver": p, "impact": weight})
        
        flows = sorted(flows, key=lambda x: abs(x['impact']), reverse=True)
        
        explanation = f"Mechanistic Trace for {target_node}: "
        contributions = [f"{f['driver']} ({f['impact']:.2f})" for f in flows[:depth]]
        explanation += " + ".join(contributions)
        return explanation

    def get_system_attribution_map(self):
        """
        Generates a full attribution report for the current system state.
        """
        anchors = self.get_attention_anchors()
        report = {
            "anchors": [{"node": n, "influence": round(v, 4)} for n, v in anchors],
            "top_flows": []
        }
        
        # Trace flows for top anchors if they are properties/effects
        for node, influence in anchors:
            trace = self.trace_causal_flow(node)
            report["top_flows"].append({"target": node, "trace": trace})
            
        return report

if __name__ == "__main__":
    # Test
    G = nx.DiGraph()
    G.add_edge("Interest_Rate", "Price", weight=0.8)
    G.add_edge("Market_Sentiment", "Price", weight=0.4)
    G.add_edge("Price", "Volatility", weight=0.6)
    
    engine = InterpretabilityEngine(G)
    print("Attention Anchors:", engine.get_attention_anchors())
    print("Causal Flow:", engine.trace_causal_flow("Price"))
    print("Attribution Map:", engine.get_system_attribution_map())
