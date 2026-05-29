"""
OMEGA-CORE | Robotics Pipeline Orchestrator
============================================
Wires all 12 pipeline steps into a single callable:

  Step 1  IntentClarifier      → parse user intent
  Step 2  RoboticsValidator    → schema + physics + sensor validation
  Step 3  TensorScope          → update global state tensor
  Step 4  AnomalyPropagator    → detect threshold / spike anomalies
  Step 5  RoboticsModel        → trajectory optimisation
  Step 6  RoboticsAgent        → domain knowledge + ASSI classification
  Step 7  CausalAgent          → causal graph + intervention candidates
  Step 8  RecursiveASI         → iterative RL refinement
  Step 9  FeedbackLoop         → KPI validation + reality anchor
  Step 10 ExplainabilityEngine → feature importance + causal narration
  Step 11 ActionabilityEngine  → prioritised action plan
  Step 12 Result packaging     → structured dict ready for Streamlit / API

Usage
-----
  from robotics_pipeline import RoboticsPipeline
  pipeline = RoboticsPipeline()
  result = pipeline.run(intent="optimise robot arm trajectory", payload={...})
"""

import json
import time
from typing import Optional

from core.intent_clarifier      import IntentClarifier
from core.data_validator        import RoboticsValidator
from core.tensor_scope          import TensorScope
from core.anomaly_propagator    import AnomalyPropagator
from models.robotics_model      import RoboticsModel
from agents.robotics_agent      import RoboticsAgent
from agents.causal_agent        import CausalAgent
from models.recursive_asi       import RecursiveASI
from core.feedback_loop         import FeedbackLoop
from core.explainability_engine import ExplainabilityEngine
from core.actionability_engine  import ActionabilityEngine


class RoboticsPipeline:
    """
    OMEGA-CORE | End-to-End Robotics Pipeline (12 Steps).
    All components share state through the TensorScope singleton.
    """

    def __init__(self, api_key: Optional[str] = None):
        # Instantiate all components
        self.intent_clarifier      = IntentClarifier(api_key)
        self.data_validator        = RoboticsValidator()
        self.tensor_scope          = TensorScope()
        self.anomaly_propagator    = AnomalyPropagator()
        self.robotics_agent        = RoboticsAgent()
        self.causal_agent          = CausalAgent()
        self.recursive_asi         = RecursiveASI(max_steps=15)
        self.feedback_loop         = FeedbackLoop()
        self.explainability_engine = ExplainabilityEngine()
        self.actionability_engine  = ActionabilityEngine()

    # ------------------------------------------------------------------
    # Primary run method
    # ------------------------------------------------------------------

    def run(self, intent: str, payload: dict, ground_truth: Optional[dict] = None) -> dict:
        """
        Execute the full 12-step robotics pipeline.

        Args:
          intent       : Free-text user request (e.g. "optimise robot arm trajectory")
          payload      : Raw robotics data dict (joint_states, sensor_data, start, goal, …)
          ground_truth : Optional dict of measured KPI values for feedback validation

        Returns:
          Full result dict with step-by-step outputs + final action plan.
        """
        t0 = time.time()
        pipeline_log = []

        # ── Step 1: Intent Clarification ─────────────────────────────
        intent_result = self.intent_clarifier.clarify_intent(intent)
        pipeline_log.append({"step": 1, "name": "IntentClarifier", "status": intent_result["status"]})

        if intent_result["status"] == "ambiguous":
            return {
                "status": "AMBIGUOUS_INTENT",
                "clarification_question": intent_result.get("clarification_question"),
                "suggested_intents": intent_result.get("suggested_intents"),
                "pipeline_log": pipeline_log,
            }

        # ── Step 2: Data Validation ───────────────────────────────────
        validation = self.data_validator.validate(payload)
        pipeline_log.append({"step": 2, "name": "RoboticsValidator",
                              "status": validation["status"],
                              "errors": validation.get("errors", []),
                              "warnings": validation.get("warnings", [])})

        if validation["status"] == "invalid":
            return {
                "status": "VALIDATION_FAILED",
                "errors": validation["errors"],
                "warnings": validation.get("warnings", []),
                "pipeline_log": pipeline_log,
            }

        validated_payload = validation["payload"]

        # ── Step 3: TensorScope (State Tensor Update) ─────────────────
        self.tensor_scope.update_robotics_data(validated_payload)
        assi_vector = self.tensor_scope.get_assi_vector()
        pipeline_log.append({"step": 3, "name": "TensorScope",
                              "coherence": assi_vector["coherence"],
                              "entropy": assi_vector["entropy"]})

        # ── Step 4: Anomaly Detection ─────────────────────────────────
        robotics_state  = self.tensor_scope.get_robotics_state()
        anomaly_report  = self.anomaly_propagator.check_robotics_anomalies(robotics_state)
        pipeline_log.append({"step": 4, "name": "AnomalyPropagator",
                              "severity": anomaly_report["severity_summary"],
                              "count": anomaly_report["anomaly_count"]})

        # Build input dict for RoboticsAgent (from validated payload)
        agent_input = {
            "start":       payload.get("start", {}),
            "goal":        payload.get("goal", {}),
            "obstacles":   payload.get("obstacles", []),
            "sensor_data": dict(validated_payload.sensor_data),
            "steps":       payload.get("steps", 20),
        }

        # ── Steps 5 & 6: RoboticsModel + RoboticsAgent ───────────────
        agent_output = self.robotics_agent.process(agent_input, anomaly_report)
        pipeline_log.append({"step": "5+6", "name": "RoboticsAgent",
                              "assi": agent_output["assi"]["classification"],
                              "collision_free": agent_output["collision_free"],
                              "energy_status": agent_output["energy"]["status"]})

        # ── Step 7: CausalAgent ───────────────────────────────────────
        causal_output = self.causal_agent.process(agent_output)
        # Attach causal graph to agent output for downstream steps
        agent_output["causal_graph"] = causal_output["causal_graph"]
        pipeline_log.append({"step": 7, "name": "CausalAgent",
                              "top_driver": causal_output["top_drivers"][0]["node"]
                              if causal_output["top_drivers"] else "N/A"})

        # ── Step 8: RecursiveASI ──────────────────────────────────────
        refined = self.recursive_asi.refine(agent_output)
        pipeline_log.append({"step": 8, "name": "RecursiveASI",
                              "validation_score": refined["validation_score"],
                              "convergence_steps": refined["convergence_steps"],
                              "fallback_used": refined["fallback_used"]})

        # ── Step 9: FeedbackLoop ──────────────────────────────────────
        feedback = self.feedback_loop.close_loop(refined, ground_truth)
        pipeline_log.append({"step": 9, "name": "FeedbackLoop",
                              "overall_status": feedback["overall_status"],
                              "weighted_score": feedback["weighted_score"]})

        # ── Step 10: ExplainabilityEngine ────────────────────────────
        explanation = self.explainability_engine.explain_trajectory(
            trajectory   = agent_output.get("trajectory", {}),
            anomalies    = refined.get("anomalies", []),
            causal_graph = causal_output.get("causal_graph"),
            dynamics     = agent_output.get("dynamics"),
        )
        pipeline_log.append({"step": 10, "name": "ExplainabilityEngine",
                              "top_feature": explanation["feature_importance"][0]["joint"]
                              if explanation["feature_importance"] else "N/A"})

        # ── Step 11: ActionabilityEngine ─────────────────────────────
        # Merge causal graph into refined for action triggers
        refined["causal_graph"] = causal_output.get("causal_graph")
        action_plan = self.actionability_engine.get_action_plan(refined)
        pipeline_log.append({"step": 11, "name": "ActionabilityEngine",
                              "primary_action": action_plan["primary_action"],
                              "halt_required": action_plan["halt_required"]})

        # ── Step 12: Package Result ───────────────────────────────────
        elapsed = round(time.time() - t0, 3)
        pipeline_log.append({"step": 12, "name": "ResultPackaging",
                              "elapsed_s": elapsed})

        return {
            "status":             "SUCCESS",
            "elapsed_s":          elapsed,
            # Step outputs
            "intent":             intent_result,
            "validation":         {"status": validation["status"], "warnings": validation.get("warnings", [])},
            "state_tensor":       assi_vector,
            "anomaly_report":     anomaly_report,
            "agent_output":       {k: v for k, v in agent_output.items() if k not in ("trajectory", "dynamics")},
            "causal_output":      causal_output,
            "refined_state":      {k: v for k, v in refined.items() if k not in ("trajectory", "rl_trace")},
            "rl_trace":           refined.get("rl_trace", []),
            "feedback":           feedback,
            "explanation":        explanation,
            "action_plan":        action_plan,
            "pipeline_log":       pipeline_log,
        }


# ---------------------------------------------------------------------------
# CLI / quick test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import os

    pipeline = RoboticsPipeline(api_key=os.getenv("GEMINI_API_KEY"))

    test_payload = {
        "robot_id": "UR5-LAB-01",
        "joint_states": [
            {"joint_id": "shoulder", "position": 0.0,  "velocity": 0.3,  "acceleration": 1.0},
            {"joint_id": "elbow",    "position": 0.0,  "velocity": 0.2,  "acceleration": 0.8},
            {"joint_id": "wrist",    "position": 0.0,  "velocity": 0.1,  "acceleration": 0.5},
        ],
        "sensor_data": {
            "lidar": [1.5, 2.0, 0.8],
            "force": [5.0, 3.2],
        },
        "start":  {"shoulder": 0.0, "elbow": 0.0,  "wrist": 0.0},
        "goal":   {"shoulder": 1.2, "elbow": -0.8, "wrist": 0.5},
        "obstacles": [{"position": [0.6, -0.4, 0.2], "radius": 0.15}],
        "steps": 20,
    }

    result = pipeline.run(
        intent  = "optimise robot arm trajectory to avoid collision",
        payload = test_payload,
    )

    # Pretty-print summary
    print("\n" + "=" * 60)
    print("  OMEGA-CORE ROBOTICS PIPELINE — RESULT SUMMARY")
    print("=" * 60)
    print(f"Status         : {result['status']}")

    if result["status"] != "SUCCESS":
        print(f"Reason         : {result.get('clarification_question') or result.get('errors')}")
        print(f"Pipeline Steps : {result.get('pipeline_log', [])}")
    else:
        print(f"Elapsed        : {result['elapsed_s']}s")
        print(f"Intent         : {result['intent']['intent']} ({result['intent']['confidence']})")
        print(f"ASSI           : {result['agent_output']['assi']['classification']}")
        print(f"Anomalies      : {result['anomaly_report']['anomaly_count']} ({result['anomaly_report']['severity_summary']})")
        print(f"Validation     : {result['feedback']['overall_status']} (score={result['feedback']['weighted_score']})")
        print(f"Primary Action : {result['action_plan']['primary_action']}")
        print(f"Halt Required  : {result['action_plan']['halt_required']}")
        print("\nPipeline Steps:")
        for step in result["pipeline_log"]:
            print(f"  Step {str(step['step']):4s} | {step['name']:25s} | "
                  f"{json.dumps({k:v for k,v in step.items() if k not in ('step','name')})}")
