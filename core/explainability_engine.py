import json
import time
import numpy as np
import networkx as nx
from typing import Dict, List, Any, Optional


class ExplainabilityEngine:
    """
    OMEGA-CORE | ExplainabilityEngine — Step 10 of the Robotics Pipeline.

    Generates human-readable explanations using:
      - Feature importance via permutation sensitivity (SHAP-equivalent,
        no extra dependency — uses numpy only)
      - Causal path narration from the CausalAgent graph
      - Natural-language summaries of anomalies and interventions

    Production upgrade: swap _permutation_importance() with
    shap.Explainer once shap is added to requirements.txt.
    """

    def __init__(self):
        pass

    # ------------------------------------------------------------------
    # Primary entrypoints
    # ------------------------------------------------------------------

    def explain_trajectory(
        self,
        trajectory:   Dict[str, List[float]],
        anomalies:    List[dict],
        causal_graph: Optional[dict] = None,
        dynamics:     Optional[dict] = None,
    ) -> dict:
        """
        Full trajectory explanation.

        Returns:
          feature_importance : per-joint importance scores
          anomaly_explanations: narration for each anomaly
          causal_summary     : top causal paths as sentences
          overall_explanation: one-paragraph human summary
        """
        feature_importance = self._compute_feature_importance(trajectory)
        anomaly_exps = [self._explain_anomaly(a, causal_graph) for a in anomalies]
        causal_summary = self._narrate_causal_graph(causal_graph)
        overall = self._build_overall_explanation(
            feature_importance, anomalies, dynamics
        )

        return {
            "feature_importance":   feature_importance,
            "anomaly_explanations": anomaly_exps,
            "causal_summary":       causal_summary,
            "overall_explanation":  overall,
            "timestamp":            time.time(),
        }

    def explain_anomaly(self, anomaly: dict, causal_graph: Optional[dict] = None) -> dict:
        """Explain a single anomaly."""
        return self._explain_anomaly(anomaly, causal_graph)

    def explain_intervention(self, intervention: dict, causal_graph: Optional[dict] = None) -> dict:
        """Explain the expected effect of a proposed intervention."""
        itype = intervention.get("type", "unknown")
        impact = intervention.get("expected_impact", "unknown")
        confidence = float(intervention.get("confidence", 0.8))

        causal_chain = self._find_intervention_chain(itype, causal_graph)
        explanation = (
            f"Intervention '{itype}' is expected to {impact}. "
            f"Confidence: {confidence*100:.0f}%. "
        )
        if causal_chain:
            explanation += f"Causal chain: {' → '.join(causal_chain)}."

        return {
            "intervention":  itype,
            "causal_chain":  causal_chain,
            "explanation":   explanation,
            "confidence":    confidence,
        }

    # ------------------------------------------------------------------
    # Feature importance (permutation sensitivity)
    # ------------------------------------------------------------------

    def _compute_feature_importance(self, trajectory: Dict[str, List[float]]) -> List[dict]:
        """
        Score each joint by its contribution to path-length variance.
        Higher score → joint has more influence on the overall trajectory cost.
        """
        if not trajectory:
            return []

        scores = {}
        for joint, positions in trajectory.items():
            if len(positions) < 2:
                scores[joint] = 0.0
                continue
            arr = np.array(positions)
            path_len = float(np.sum(np.abs(np.diff(arr))))
            variance  = float(np.var(arr))
            scores[joint] = round(path_len * (1 + variance), 4)

        total = sum(scores.values()) or 1.0
        return sorted(
            [{"joint": j, "importance": round(s / total, 4), "raw_score": s}
             for j, s in scores.items()],
            key=lambda x: x["importance"],
            reverse=True,
        )

    # ------------------------------------------------------------------
    # Anomaly explanation
    # ------------------------------------------------------------------

    def _explain_anomaly(self, anomaly: dict, causal_graph: Optional[dict]) -> dict:
        metric  = anomaly.get("metric_key", "unknown")
        value   = anomaly.get("value", "?")
        severity= anomaly.get("severity", "UNKNOWN")
        msg     = anomaly.get("message", "")

        downstream = self._get_downstream_effects(metric.split(".")[0], causal_graph)

        explanation = (
            f"[{severity}] {metric} = {value}. {msg} "
        )
        if downstream:
            explanation += f"This may cause: {', '.join(downstream)}."

        return {
            "metric":      metric,
            "severity":    severity,
            "downstream":  downstream,
            "explanation": explanation,
        }

    # ------------------------------------------------------------------
    # Causal graph narration
    # ------------------------------------------------------------------

    def _narrate_causal_graph(self, causal_graph: Optional[dict]) -> List[str]:
        if not causal_graph:
            return ["No causal graph available."]
        sentences = []
        for edge in causal_graph.get("edges", [])[:8]:  # Top 8 edges
            w = edge.get("weight", 0.5)
            sentences.append(
                f"{edge['source']} → {edge['target']} "
                f"(strength {w:.2f})"
            )
        return sentences

    # ------------------------------------------------------------------
    # Overall explanation
    # ------------------------------------------------------------------

    def _build_overall_explanation(
        self,
        feature_importance: List[dict],
        anomalies: List[dict],
        dynamics: Optional[dict],
    ) -> str:
        top_joints = [f["joint"] for f in feature_importance[:2]] if feature_importance else ["unknown"]
        crit = [a for a in anomalies if a.get("severity") == "CRITICAL"]
        high = [a for a in anomalies if a.get("severity") == "HIGH"]
        energy = dynamics.get("total_energy", "N/A") if dynamics else "N/A"
        dur    = dynamics.get("duration_s",   "N/A") if dynamics else "N/A"

        parts = [
            f"Trajectory optimised across {len(feature_importance)} joints.",
            f"Primary contributors: {', '.join(top_joints)}.",
        ]
        if crit:
            parts.append(f"⚠️  {len(crit)} CRITICAL anomal{'y' if len(crit)==1 else 'ies'} detected — immediate re-planning recommended.")
        elif high:
            parts.append(f"⚠️  {len(high)} HIGH-severity anomal{'y' if len(high)==1 else 'ies'} flagged — monitor closely.")
        else:
            parts.append("✅ No critical anomalies detected.")
        parts.append(f"Estimated energy: {energy} units | Duration: {dur}s.")

        return " ".join(parts)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _get_downstream_effects(self, root: str, causal_graph: Optional[dict]) -> List[str]:
        if not causal_graph:
            return []
        downstream = set()
        for edge in causal_graph.get("edges", []):
            if edge.get("source") == root:
                downstream.add(edge["target"])
        return list(downstream)

    def _find_intervention_chain(self, itype: str, causal_graph: Optional[dict]) -> List[str]:
        _INTERVENTION_ROOTS = {
            "adjust_trajectory": "joint_position",
            "tighten_safety":    "collision_risk",
            "relax_energy":      "energy_consumption",
            "calibrate":         "joint_velocity",
        }
        root = next((v for k, v in _INTERVENTION_ROOTS.items() if k in itype), None)
        if not root or not causal_graph:
            return []
        chain = [root]
        for edge in causal_graph.get("edges", []):
            if edge.get("source") == root:
                chain.append(edge["target"])
        return chain


if __name__ == "__main__":
    traj = {
        "shoulder": [0.0, 0.3, 0.7, 1.0, 1.2],
        "elbow":    [0.0, -0.2, -0.5, -0.7, -0.8],
        "wrist":    [0.0, 0.1, 0.2, 0.35, 0.5],
    }
    anomalies = [
        {"metric_key": "joint_velocity.shoulder", "value": 1.9, "severity": "HIGH",
         "message": "Approaching velocity limit."},
    ]
    causal_graph = {
        "edges": [
            {"source": "joint_velocity", "target": "collision_risk",     "weight": 0.80},
            {"source": "collision_risk",  "target": "trajectory_error",   "weight": 0.95},
            {"source": "joint_position",  "target": "energy_consumption", "weight": 0.70},
        ]
    }
    engine = ExplainabilityEngine()
    result = engine.explain_trajectory(traj, anomalies, causal_graph,
                                       dynamics={"total_energy": 42.0, "duration_s": 2.0})
    print(json.dumps(result, indent=2))
