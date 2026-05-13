import os
import json
import datetime
from google import genai
from google.genai import types
from core.safety_kernel import SafetyKernel
from core.grounding_engine import GroundingEngine
from intelligence.scientific_engine import ScientificEngine

class OrchestratorEngine:
    def __init__(self, api_key=None, engine="Gemini"):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "")
        self.engine = engine
        self.safety = SafetyKernel()
        self.grounding = GroundingEngine()
        self.scientific = ScientificEngine()
        
        self.domains = [
            "Personalized Cancer Digital Twin",
            "CRISPR Off-Target Prediction System",
            "Satellite Climate-Agriculture Twin",
            "Autonomous Drug Discovery Loop",
            "Driverless Medical Logistics Network",
            "Immunotherapy Response Prediction",
            "Aging & Longevity Digital Twin",
            "Quantum Materials Discovery",
            "Pandemic Propagation Manifold",
            "Recursive Cyber Defense Twin",
            "Brain-Computer Interface Stability Research",
            "Autonomous Wet-Lab Robotics",
            "Fusion Reactor Stability Prediction",
            "Human-AI Internal State Research",
            "Global Household Optimization Twin",
            "Global Macro Stress Test (SOP-31)"
        ]

    def run_recursive_loop(self, domain, ingress_data=None):
        """
        Executes a grounded 9-step scientific orchestration loop.
        Separates deterministic validation from LLM interpretation.
        """
        # --- MAPPING DOMAIN TO CORE LOGIC ---
        short_domain = domain.split(" ")[0].lower()
        if "cancer" in domain.lower(): short_domain = "health"
        if "finance" in domain.lower() or "macro" in domain.lower(): short_domain = "finance"
        if "cyber" in domain.lower(): short_domain = "cyber"

        # --- LAYER 1: OBSERVE (Deterministic Grounding) ---
        ingress_validation = self.grounding.validate_sensor_ingress(domain, ingress_data)
        
        # --- LAYER 2: COMPRESS (Manifold Embedding) ---
        self.scientific.load_data(domain=short_domain)
        manifold_df = self.scientific.compute_manifold(n_components=2)
        latent_desc = f"Manifold established with {len(manifold_df)} nodes. Variance Explained: {self.scientific.compute_reducibility():.2%}"

        # --- LAYER 3: PREDICT (Causal Discovery) ---
        causal_g = self.scientific.discover_causality()
        prediction_paths = len(causal_g.edges())

        # --- LAYER 4: SIMULATION (Digital Twin Run) ---
        # Simulate a 10% shock to the primary driver
        target_node = list(causal_g.nodes())[0] if causal_g.nodes() else "Price"
        sim_results, sim_msg = self.scientific.simulate_intervention(target_node, 1.1)
        risk_score = self.scientific.compute_sensitivity()

        # --- LAYER 5: OPTIMIZATION & ARBITRATION (Safety Kernel) ---
        is_safe, safety_msg = self.safety.validate_action(short_domain, ingress_data or {})

        # --- LAYER 6: EXECUTION (Agent Bus) ---
        from kernel import run_psi_autopilot
        execution_report = run_psi_autopilot(f"Orchestration for {domain}", json.dumps(ingress_data), "OMEGA-CORE", self.api_key, True)

        # --- LAYER 7: VERIFICATION (Ground Truth Delta) ---
        # If we have ground truth in the sim, calculate fidelity
        fidelity = self.scientific.compute_stability()

        # --- LAYER 8: LEARNING (Bayesian Update) ---
        learn_success, learn_msg = self.scientific.learn_from_ground_truth()

        # --- LAYER 9: DNA REBUILD (Mutation Suggestion) ---
        mutation_suggested = "Proposed: Tighten RSI threshold by 5%" if risk_score > 0.5 else "None"

        # --- LLM NARRATION PHASE ---
        if "Gemini" in self.engine and self.api_key:
            try:
                client = genai.Client(api_key=self.api_key)
                prompt = f"""
                You are the OMEGA-CORE Unified Recursive Scientific Orchestrator.
                You are executing a GROUNDED stress-test simulation on the domain: {domain}.
                
                DETERMINISTIC OUTPUTS FROM CORE ENGINES:
                1. Observe: {json.dumps(ingress_validation)}
                2. Compress: {latent_desc}
                3. Predict: {prediction_paths} causal paths identified.
                4. Simulate: {json.dumps(sim_results)}
                5. Optimize: Safety Status: {safety_msg}
                6. Execute: Order ID: {execution_report['metrics']['order_id']}
                7. Measure: System Stability: {fidelity:.4f}
                8. Learn: {json.dumps(learn_msg)}
                9. Rebuild: {mutation_suggested}
                
                Provide the final 9-step narration. Return EXACTLY valid JSON matching this schema:
                {{
                    "observe": {{"action": "...", "metric": "...", "uncertainty": {ingress_validation['confidence']}}},
                    "compress": {{"action": "...", "latent_space_desc": "{latent_desc}"}},
                    "predict": {{"action": "...", "forecast": "Causal density: {prediction_paths} edges"}},
                    "simulate": {{"action": "...", "scenario": "Shock to {target_node}", "risk_score": {risk_score}}},
                    "optimize": {{"action": "...", "tradeoff_resolved": "...", "safety_status": "{safety_msg}"}},
                    "execute": {{"action": "...", "agent_dispatched": "Mitigation Node {execution_report['metrics']['order_id']}"}},
                    "measure": {{"action": "...", "ground_truth_delta": {1.0 - fidelity}}},
                    "learn": {{"action": "...", "causal_update": "Bayesian weights adjusted"}},
                    "rebuild_world_model": {{"action": "...", "new_paradigm": "{mutation_suggested}"}}
                }}
                """
                
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json"
                    )
                )
                
                result = json.loads(response.text)
                self.grounding.log_reality_anchor(domain, result.get("observe", {}).get("action", "No state"))
                return result
                
            except Exception as e:
                print(f"API Error: {str(e)}. Falling back to mock.")
                return self._mock_fallback(domain, safety_msg)
        else:
            return self._mock_fallback(domain, safety_msg)

    def _mock_fallback(self, domain, safety_msg="Validated"):
        """Fallback simulation if API is unavailable."""
        return {
            "observe": {"action": f"Observed validated telemetry for {domain}", "metric": "Noise: Nominal", "uncertainty": 0.02},
            "compress": {"action": "Mapped to lower dimensional latent space", "latent_space_desc": "Semantic manifold established"},
            "predict": {"action": "Extrapolated vector trajectory", "forecast": "System stability within ±0.05"},
            "simulate": {"action": "Ran Digital Twin scenario", "scenario": "Nominal equilibrium", "risk_score": 0.15},
            "optimize": {"action": "TCA Resolved: Resource allocation", "tradeoff_resolved": "Performance vs Stability", "safety_status": safety_msg},
            "execute": {"action": "Dispatched worker agents", "agent_dispatched": "Node-Alpha"},
            "measure": {"action": "Recorded post-intervention state", "ground_truth_delta": 0.01},
            "learn": {"action": "Updated Bayesian priors", "causal_update": "System fidelity improved"},
            "rebuild_world_model": {"action": "Confirmed world model stability", "new_paradigm": "Resilient state maintained"}
        }

if __name__ == "__main__":
    import sys
    target_domain = sys.argv[1] if len(sys.argv) > 1 else "Personalized Cancer Digital Twin"
    orchestrator = OrchestratorEngine()
    result = orchestrator.run_recursive_loop(target_domain, {"heart_rate": 72, "rsi": 35})
    print(json.dumps(result, indent=2))
