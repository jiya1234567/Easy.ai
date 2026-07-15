import json
from omega_bridge_v2 import get_harness_v2
from intelligence.causal_discovery_engine import CausalDiscoveryEngine

def run_finance_test():
    data = {"interest_rate":[4.0,4.5,5.0,4.8,5.2,5.1,4.9,5.3,5.5,5.4],"gold":[1950,1920,1880,1900,1860,1875,1890,1855,1840,1848],"tech_return":[0.5,-0.5,-2.0,-1.2,-2.5,-1.8,-0.8,-2.8,-3.1,-2.9],"vix":[14,18,25,20,28,22,19,30,32,29]}
    query = "What is causing the tech selloff and is gold acting as a safe haven? Identify the regime change point."
    
    print("=========================================")
    print("1. AGENT COGNITIVE ANALYSIS (Mistral)")
    print("=========================================")
    h = get_harness_v2()
    agent = h["agents"]["finance"]
    
    # Fast models for testing
    agent.primary_model = "mistral"
    agent.challenger_model = "mistral"
    
    result = agent.run(query, data)
    print("PRIMARY REASONING:")
    print(result.primary_reasoning)
    print("\nFINAL ANSWER:")
    print(result.final_answer)
    
    print("\n=========================================")
    print("2. REAL CAUSAL DISCOVERY (Lag-Aware)")
    print("=========================================")
    causal_engine = CausalDiscoveryEngine()
    graph = causal_engine.discover("finance", observation=data, confidence_threshold=0.6)
    
    print("\nDiscovered Edges (Templates + Data):")
    for edge in graph.edges:
        print(f"  {edge.source} -> {edge.target} (conf: {edge.confidence:.2f}) | {edge.mechanism}")

if __name__ == "__main__":
    run_finance_test()
