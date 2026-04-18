import os
import json
from google import genai
from google.genai import types

class ReasoningAgent:
    def __init__(self, provider="Gemini"):
        self.provider = "Gemini" # Standardized on Gemini
        self.gemini_key = os.environ.get("GEMINI_API_KEY")

    def execute_reasoning(self, context_data):
        """
        Uses Gemini to reason about the system state.
        """
        prompt = f"""
        You are the OMEGA-CORE REASONING ENGINE (Universal Resilience Module).
        
        System Context & State:
        {json.dumps(context_data, indent=2)}
        
        Task:
        1. Contextualize the threat/shock based on the domain (Cyber, Finance, Smart City, or Health).
        2. Identify the core vulnerability or structural weakness in the causal chain.
        3. Suggest a multi-layer mitigation or resilience strategy (e.g., technical blocks for cyber, resource allocation for city).
        4. Highlight systemic risks, cascading blind spots, or uncertainty in the propagation path.
        
        STRICT SCHEMA REQUIREMENT: Return a JSON object with:
        - "domain_assessment": "How this affects the specific domain",
        - "analysis": "Detailed explanation of the threat/shock",
        - "vulnerabilities": ["v1", "v2"],
        - "strategy": ["step1", "step2"],
        - "risk_prioritization": "High/Medium/Low with reason"
        """

        return self._gemini_reasoning(prompt)

    def _gemini_reasoning(self, prompt):
        if not self.gemini_key:
            return {"error": "No Gemini API Key found."}
        
        try:
            client = genai.Client(api_key=self.gemini_key)
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            return json.loads(response.text)
        except Exception as e:
            return {"error": f"Gemini Reasoning failed: {e}"}

if __name__ == "__main__":
    # Test
    agent = ReasoningAgent()
    sample_data = {
        "node": "N3",
        "risk_score": 0.85,
        "causal_path": "Low Patch Level -> High Privilege -> Attack",
        "spread_risk": "High"
    }
    result = agent.execute_reasoning(sample_data)
    print(json.dumps(result, indent=2))
