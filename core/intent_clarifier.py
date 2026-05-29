import os
import re
import json
import google.generativeai as genai
from google.generativeai import types
# Note: orchestrator_engine uses google.generativeai; we match that pattern here.

class IntentClarifier:
    """
    OMEGA-CORE | Intent Clarifier — Step 1 of the Robotics Pipeline.
    Parses ambiguous or structured user inputs and maps them to canonical
    OMEGA-CORE robotics intents. Uses Gemini for advanced disambiguation;
    falls back to rule-based matching when the API is unavailable.
    """

    ROBOTICS_INTENTS = [
        "optimize_trajectory",
        "avoid_collision",
        "calibrate_sensors",
        "reduce_energy",
        "improve_precision",
        "detect_anomalies",
        "multi_modal_sensing",
        "classify_environment",
    ]

    INTENT_TEMPLATES = {
        "optimize_trajectory":  "Optimize the robot trajectory to minimise {metric} while respecting {constraint}.",
        "avoid_collision":      "Plan a collision-free path for the robot from {start} to {goal}.",
        "calibrate_sensors":    "Calibrate the {sensor} sensor to reduce noise by {percentage}%.",
        "reduce_energy":        "Reduce robot energy consumption by {percentage}% without sacrificing {metric}.",
        "improve_precision":    "Improve robot precision for {task} by {percentage}%.",
        "detect_anomalies":     "Detect anomalies in the robot's {sensor} data stream.",
        "multi_modal_sensing":  "Classify the operating environment using vision, touch, and chemical sensors.",
        "classify_environment": "Classify the target environment using ASSI multi-modal entropy analysis.",
    }

    # Keyword → intent (rule-based fallback)
    _KEYWORD_MAP = {
        "trajectory":    "optimize_trajectory",
        "path":          "optimize_trajectory",
        "motion":        "optimize_trajectory",
        "collision":     "avoid_collision",
        "obstacle":      "avoid_collision",
        "calibrat":      "calibrate_sensors",
        "sensor":        "calibrate_sensors",
        "energy":        "reduce_energy",
        "power":         "reduce_energy",
        "precision":     "improve_precision",
        "accuracy":      "improve_precision",
        "anomal":        "detect_anomalies",
        "fault":         "detect_anomalies",
        "vision":        "multi_modal_sensing",
        "touch":         "multi_modal_sensing",
        "smell":         "multi_modal_sensing",
        "chemical":      "multi_modal_sensing",
        "classify":      "classify_environment",
        "environment":   "classify_environment",
        "entropy":       "classify_environment",
    }

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def clarify_intent(self, user_input: str) -> dict:
        """
        Primary entry point. Returns a dict with:
          status  : 'clear' | 'ambiguous'
          intent  : canonical intent string (when clear)
          confidence : float 0–1
          suggested_intents : list (when ambiguous)
          clarification_question : str (when ambiguous)
          template : the intent prompt template
        """
        if self.api_key:
            try:
                return self._clarify_with_gemini(user_input)
            except Exception as e:
                print(f"[IntentClarifier] Gemini unavailable ({e}). Using rule-based fallback.")

        return self._clarify_rule_based(user_input)

    def get_template(self, intent: str) -> str:
        """Return the prompt template for a given canonical intent."""
        return self.INTENT_TEMPLATES.get(intent, "Please describe your robotics task in more detail.")

    # ------------------------------------------------------------------
    # Gemini-powered clarification
    # ------------------------------------------------------------------

    def _clarify_with_gemini(self, user_input: str) -> dict:
        genai.configure(api_key=self.api_key)
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={"response_mime_type": "application/json"},
        )
        prompt = (
            "You are a robotics intent classifier for the OMEGA-CORE system.\n"
            f"Candidate intents: {json.dumps(self.ROBOTICS_INTENTS)}\n\n"
            f"User input: \"{user_input}\"\n\n"
            "Return EXACTLY valid JSON with keys: "
            "intent (string), confidence (float 0-1), status ('clear' or 'ambiguous'), "
            "suggested_intents (list of top 3 strings). No extra text."
        )
        response = model.generate_content(prompt)
        result = json.loads(response.text)
        result["template"] = self.get_template(result.get("intent", ""))
        if result.get("status") == "ambiguous":
            result["clarification_question"] = (
                f"Did you mean: {', '.join(result.get('suggested_intents', []))}?"
            )
        return result

    # ------------------------------------------------------------------
    # Rule-based fallback (no external dependencies)
    # ------------------------------------------------------------------

    def _clarify_rule_based(self, user_input: str) -> dict:
        lower = user_input.lower()
        scores = {}
        for keyword, intent in self._KEYWORD_MAP.items():
            if keyword in lower:
                scores[intent] = scores.get(intent, 0) + 1

        if not scores:
            return {
                "status": "ambiguous",
                "intent": None,
                "confidence": 0.0,
                "suggested_intents": self.ROBOTICS_INTENTS[:3],
                "clarification_question": (
                    "Could not determine your robotics intent. "
                    f"Did you mean: {', '.join(self.ROBOTICS_INTENTS[:3])}?"
                ),
                "template": "",
            }

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_intent, top_score = ranked[0]
        total = sum(s for _, s in ranked)
        confidence = round(top_score / total, 2) if total > 0 else 0.5

        # Tie-break: if top two intents share the same score, pick by canonical priority.
        if len(ranked) > 1 and ranked[0][1] == ranked[1][1]:
            tied = [i for i, s in ranked if s == top_score]
            for canonical in self.ROBOTICS_INTENTS:
                if canonical in tied:
                    top_intent = canonical
                    break
            confidence = round(min(0.99, confidence + 0.10), 2)

        if confidence >= 0.5:
            return {
                "status": "clear",
                "intent": top_intent,
                "confidence": confidence,
                "suggested_intents": [i for i, _ in ranked[:3]],
                "template": self.get_template(top_intent),
            }
        else:
            top3 = [i for i, _ in ranked[:3]]
            return {
                "status": "ambiguous",
                "intent": top_intent,
                "confidence": confidence,
                "suggested_intents": top3,
                "clarification_question": f"Did you mean: {', '.join(top3)}?",
                "template": self.get_template(top_intent),
            }


if __name__ == "__main__":
    ic = IntentClarifier()
    tests = [
        "optimise the robot arm trajectory to avoid hitting the wall",
        "I need to reduce energy usage",
        "run a full multi-modal sense sweep",
        "do something with the robot",
    ]
    for t in tests:
        r = ic.clarify_intent(t)
        print(f"Input : {t}")
        print(f"Result: {json.dumps(r, indent=2)}\n")
