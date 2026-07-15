import traceback
from omega_bridge_v2 import get_harness_v2

def main():
    print("=" * 80)
    print("🚀 OMEGA-CORE WHOLESOME DOMAINS TEST SUITE")
    print("=" * 80 + "\n")
    
    h = get_harness_v2()
    agents = h["agents"]
    
    test_results = []
    
    domains_to_test = [
        "scientific_discovery", "finance", "weather_manifold", "health_protocol",
        "adversarial_lab", "world_model", "asi_core", "digital_twin",
        "smart_city_twin", "agriculture_asi", "global_monitoring", "clinical_stress_test",
        "reducibility_sandbox", "inference_domain"
    ]
    
    for domain in domains_to_test:
        print(f"Testing Domain: {domain}")
        try:
            agent = agents.get(domain)
            if not agent:
                print(f"  ❌ FAILED: No agent found for {domain}")
                test_results.append({"domain": domain, "passed": False, "error": "Agent not found"})
                continue
                
            query = f"Provide a brief 1-sentence hypothesis for {domain} anomalies."
            context_data = {"test_variable": [1.0, 1.1, 1.2]}
            
            # Use a fast model if possible to avoid hanging for minutes
            agent.primary_model = "mistral"
            agent.challenger_model = "mistral" 
            
            result = agent.run(query, context_data)
            print(f"  ✅ SUCCESS: {result.final_answer[:100]}...")
            test_results.append({"domain": domain, "passed": True})
        except Exception as e:
            print(f"  ❌ FAILED: {e}")
            test_results.append({"domain": domain, "passed": False, "error": str(e)})
            
    passed = sum(1 for r in test_results if r["passed"])
    print(f"\n✅ Domain Tests Completed: {passed}/{len(domains_to_test)} Passed.")

if __name__ == "__main__":
    main()
