import json
import time
import numpy as np
import networkx as nx
from typing import Dict, List, Any, Optional


class CausalAgent:
    """
    OMEGA-CORE | CausalAgent — Step 7 of the Robotics Pipeline.

    Builds a causal graph (networkx DiGraph) from agent output,
    performs causal path queries, computes edge strengths from
    empirical anomaly co-occurrence, and returns a serialisable
    causal graph dict for ExplainabilityEngine consumption.

    Uses networkx (already in requirements.txt).
    Production upgrade: persist graph to Neo4j via py2neo.
    """

    # Default causal schema for robotics domain
    _DEFAULT_EDGES = [
        ("joint_position",     "collision_risk",     0.90),
        ("joint_velocity",     "collision_risk",     0.80),
        ("joint_position",     "energy_consumption", 0.70),
        ("joint_velocity",     "energy_consumption", 0.80),
        ("joint_acceleration", "energy_consumption", 0.60),
        ("collision_risk",     "trajectory_error",   0.95),
        ("energy_consumption", "trajectory_error",   0.50),
        ("lidar",              "collision_risk",     0.85),
        ("force",              "joint_position",     0.65),
    ]

    def __init__(self):
        self.graph = nx.DiGraph()
        self._build_default_graph()
        self._anomaly_co_occurrence: Dict[str, int] = {}

    # ------------------------------------------------------------------
    # Primary entrypoint
    # ------------------------------------------------------------------

    def process(self, agent_output: dict) -> dict:
        """
        Args:
          agent_output: result dict from RoboticsAgent.process()

        Returns:
          causal_graph    : {nodes, edges} serialisable dict
          top_drivers     : sorted list of nodes by out-degree centrality
          anomaly_paths   : causal traces for each detected anomaly
          intervention_candidates : nodes whose removal would break most paths
        """
        anomalies  = agent_output.get("anomalies", [])
        trajectory = agent_output.get("trajectory", {})
        dynamics   = agent_output.get("dynamics", {})

        # --- Update edge weights from anomaly co-occurrence ---
        self._update_weights_from_anomalies(anomalies)

        # --- Annotate nodes with live values ---
        self._annotate_nodes(agent_output)

        # --- Causal path queries for each anomaly ---
        anomaly_paths = []
        for a in anomalies:
            root = a.get("metric_key", "").split(".")[0]
            paths = self._get_all_causal_paths(root, "trajectory_error")
            anomaly_paths.append({
                "anomaly":       a.get("metric_key"),
                "severity":      a.get("severity"),
                "causal_paths":  paths,
            })

        # --- Centrality analysis ---
        centrality = nx.out_degree_centrality(self.graph)
        top_drivers = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:5]

        # --- Intervention candidates (highest betweenness centrality) ---
        between = nx.betweenness_centrality(self.graph, normalized=True)
        intervention_candidates = sorted(between.items(), key=lambda x: x[1], reverse=True)[:3]

        return {
            "agent":                    "CausalAgent",
            "causal_graph":             self._export_graph(),
            "top_drivers":              [{"node": n, "centrality": round(c, 4)} for n, c in top_drivers],
            "intervention_candidates":  [{"node": n, "betweenness": round(b, 4)} for n, b in intervention_candidates],
            "anomaly_paths":            anomaly_paths,
            "anomaly_count":            len(anomalies),
            "timestamp":                time.time(),
        }

    # ------------------------------------------------------------------
    # Graph construction
    # ------------------------------------------------------------------

    def _build_default_graph(self):
        for src, tgt, weight in self._DEFAULT_EDGES:
            self.graph.add_edge(src, tgt, weight=weight, type="CAUSES")

    def add_edge(self, source: str, target: str, weight: float = 0.5):
        """Extend the causal graph dynamically."""
        self.graph.add_edge(source, target, weight=weight, type="CAUSES")

    def _update_weights_from_anomalies(self, anomalies: List[dict]):
        """Increment edge weights when anomalous nodes co-occur."""
        roots = [a.get("metric_key", "").split(".")[0] for a in anomalies]
        for r in roots:
            self._anomaly_co_occurrence[r] = self._anomaly_co_occurrence.get(r, 0) + 1
            for _, tgt, data in self.graph.out_edges(r, data=True):
                count = self._anomaly_co_occurrence[r]
                # Bayesian-style weight update: nudge toward 1.0
                data["weight"] = min(1.0, data["weight"] + 0.01 * count)

    def _annotate_nodes(self, agent_output: dict):
        """Tag graph nodes with live values from agent output."""
        energy = agent_output.get("energy", {}).get("total", 0.0)
        assi   = agent_output.get("assi", {})
        cost   = agent_output.get("trajectory_cost", 0.0)

        annotations = {
            "energy_consumption": energy,
            "trajectory_error":   cost,
            "collision_risk":     0.0 if agent_output.get("collision_free") else 1.0,
            "joint_position":     assi.get("global_entropy", 0.5),
        }
        for node, value in annotations.items():
            if node in self.graph.nodes:
                self.graph.nodes[node]["live_value"] = round(float(value), 4)

    # ------------------------------------------------------------------
    # Graph queries
    # ------------------------------------------------------------------

    def _get_all_causal_paths(self, source: str, target: str) -> List[List[str]]:
        if source not in self.graph or target not in self.graph:
            return []
        try:
            return list(nx.all_simple_paths(self.graph, source, target, cutoff=5))
        except nx.NetworkXNoPath:
            return []

    def get_shortest_path(self, source: str, target: str) -> List[str]:
        try:
            return nx.shortest_path(self.graph, source, target, weight="weight")
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return []

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def _export_graph(self) -> dict:
        nodes = []
        for node, data in self.graph.nodes(data=True):
            nodes.append({"name": node, **data})

        edges = []
        for src, tgt, data in self.graph.edges(data=True):
            edges.append({
                "source": src,
                "target": tgt,
                "weight": round(data.get("weight", 0.5), 4),
                "type":   data.get("type", "CAUSES"),
            })

        return {"nodes": nodes, "edges": edges}


if __name__ == "__main__":
    from agents.robotics_agent import RoboticsAgent
    agent  = RoboticsAgent()
    a_out  = agent.process(
        {
            "start": {"shoulder": 0.0, "elbow": 0.0, "wrist": 0.0},
            "goal":  {"shoulder": 1.2, "elbow": -0.8, "wrist": 0.5},
            "sensor_data": {"vision_entropy": 0.4, "touch_entropy": 0.6, "smell_entropy": 0.3},
        },
        {"anomalies": [{"metric_key": "joint_velocity.shoulder", "severity": "HIGH"}]},
    )
    ca     = CausalAgent()
    result = ca.process(a_out)
    print(json.dumps({k: v for k, v in result.items() if k != "causal_graph"}, indent=2))
    print(f"Graph nodes: {len(result['causal_graph']['nodes'])} | edges: {len(result['causal_graph']['edges'])}")
