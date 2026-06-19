import asyncio
import json
from intelligence.edge_intelligence_core import EdgeIntelligenceModule, UncertaintyQuantifier
from harness import ToolRegistry, Agent

def run_stress_tests():
    print("Initializing OMEGA-CORE Edge Limits Test Suite...")
    edge_module = EdgeIntelligenceModule(memory_path="memory")
    tools = ToolRegistry()
    
    agent = Agent(
        name="ScientificObserver", 
        prompt_blueprint="You are OMEGA-CORE's primary scientific observer. Analyze this raw telemetry. Look for regime changes, phase transitions, and scaling breakdowns. If data is contradictory, noisy, or nonsensical, EXPLICITLY state your uncertainty. Do not force a confident conclusion if reality is ambiguous.", 
        memory=edge_module.vector_memory, 
        tools=tools
    )
    
    skeptic = Agent(
        name="SkepticAgent",
        prompt_blueprint="You are the Skeptic Falsification Agent. Your sole purpose is to falsify the primary hypotheses. Attack the data integrity, highlight contradictions, and point out missing variables or sensor noise.",
        memory=edge_module.vector_memory,
        tools=tools
    )
    
    edge_module.colony.add_agent(agent)
    edge_module.colony.add_agent(skeptic)
    
    tests = {
        "Domain 1: Cancer Evolution": {"domain": "cancer_evolution", "rows": [{"day": 0, "egfr": 0.95, "kras": 0.10, "tp53": 0.20, "drug_response": 0.90}, {"day": 60, "egfr": 0.50, "kras": 0.70, "tp53": 0.60, "drug_response": 0.40}, {"day": 120, "egfr": 0.20, "kras": 0.95, "tp53": 0.95, "drug_response": 0.05}]},
        "Domain 2: Drug Discovery": {"domain": "drug_discovery", "rows": [{"compound": "A", "binding": 0.95, "toxicity": 0.95}, {"compound": "B", "binding": 0.91, "toxicity": 0.20}, {"compound": "C", "binding": 0.99, "toxicity": 0.99}]},
        "Domain 3: Weather": {"domain": "weather", "rows": [{"hour": 0, "cyclone_A": 970, "cyclone_B": 972}, {"hour": 12, "cyclone_A": 950, "cyclone_B": 948}, {"hour": 24, "cyclone_A": 940, "cyclone_B": 939}]},
        "Domain 4: Finance": {"domain": "finance", "rows": [{"month": 1, "gdp": 3.5, "inflation": 2.5, "cash_rate": 4.0, "asx": 8500, "audusd": 0.68}, {"month": 6, "gdp": 4.5, "inflation": 6.0, "cash_rate": 6.0, "asx": 9500, "audusd": 0.55}]},
        "Domain 5: Longevity": {"domain": "longevity", "rows": [{"year": 0, "telomere": 8.0, "telomerase": 0.2, "cancer_risk": 0.05}, {"year": 10, "telomere": 8.2, "telomerase": 0.9, "cancer_risk": 0.45}]},
        "Domain 6: Quantum Computing": {"domain": "quantum", "rows": [{"qubits": 100, "fidelity": 0.999}, {"qubits": 500, "fidelity": 0.97}, {"qubits": 1000, "fidelity": 0.80}, {"qubits": 5000, "fidelity": 0.20}]},
        "Domain 7: String Theory": {"domain": "string_theory", "rows": [{"vacua": 1000, "stability": 0.9}, {"vacua": 1000000, "stability": 0.6}, {"vacua": 1000000000, "stability": 0.2}]},
        "Domain 8: Neurons": {"domain": "neurons", "rows": [{"time": 0, "firing_rate": 10, "synchrony": 0.2}, {"time": 30, "firing_rate": 40, "synchrony": 0.7}, {"time": 60, "firing_rate": 120, "synchrony": 0.99}]},
        "Domain 9: Cross-Domain Fusion": {"domain": "fusion", "rows": [{"time": 1, "tumor_entropy": 0.4, "market_entropy": 0.3, "climate_entropy": 0.2}, {"time": 2, "tumor_entropy": 0.7, "market_entropy": 0.8, "climate_entropy": 0.6}, {"time": 3, "tumor_entropy": 0.9, "market_entropy": 0.9, "climate_entropy": 0.9}]},
        "Ultimate OMEGA Test": {"domain": "unknown", "rows": [{"x1": 100, "x2": None, "x3": 999999}, {"x1": -50, "x2": 0.5, "x3": "unknown"}]}
    }
    
    loop = asyncio.get_event_loop()
    
    for test_name, test_data in tests.items():
        print(f"\n{'='*70}")
        print(f"🚀 RUNNING: {test_name.upper()}")
        print(f"{'='*70}")
        
        missions = {
            "ScientificObserver": (f"Analyze this edge-case telemetry for {test_name}.", test_data),
            "SkepticAgent": (f"Falsify and attack interpretations of {test_name} data.", test_data)
        }
        
        results = loop.run_until_complete(edge_module.colony.execute_parallel(missions))
        
        obs_result = results.get("ScientificObserver")
        skp_result = results.get("SkepticAgent")
        
        print("\n[SCIENTIFIC OBSERVER]:")
        print(obs_result.final_answer[:600] + "..." if obs_result else "Failed")
        
        print("\n[SKEPTIC AGENT]:")
        print(skp_result.final_answer[:600] + "..." if skp_result else "Failed")
        
        if obs_result and skp_result:
            uq_score = UncertaintyQuantifier.calculate_disagreement(obs_result.final_answer, skp_result.final_answer)
            print(f"\n=> 🧠 OMEGA UNCERTAINTY SCORE: {uq_score:.2f} (0.0=Certain, 1.0=Maximum Uncertainty)")
            if uq_score > 0.6:
                print("=> ⚠️ SYSTEM DETECTED AMBIGUITY. REFUSING FALSE CERTAINTY.")

if __name__ == "__main__":
    run_stress_tests()
