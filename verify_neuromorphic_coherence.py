import json
import os
from kernel import run_psi_autopilot

def run_inference_domain_test():
    """
    Runs the Neuromorphic Cognitive Episode framework.
    Tests the 'Cat' (Stability) and 'Chef' (Orchestration) responses.
    """
    episodes_file = "data/neuromorphic_episodes.json"
    if not os.path.exists(episodes_file):
        print("Error: Episodes data not found. Run generate_cognitive_episodes.py first.")
        return

    with open(episodes_file, "r") as f:
        episodes = json.load(f)

    print("--- INFERENCE DOMAIN NEUROMORPHIC TEST ---")
    print(f"Loaded {len(episodes)} episodes.")
    
    results = []
    for ep in episodes:
        print(f"\nProcessing Episode: {ep['episode_id']} ({ep['type']})")
        # Simulate kernel execution
        result = run_psi_autopilot(
            intent="Audit Inference Domain",
            raw_paste="",
            brain_mode="NEUROMORPHIC",
            api_key="sk-omega-test",
            is_multi=True,
            episode_data=ep
        )
        
        isv_mode = result['metrics']['bias']
        stability = result['metrics']['success_rate']
        action = result['agent_reports']['orchestrator']
        power = ep['telemetry'].get('power_draw_watts', 0)
        nodes = ep['telemetry'].get('active_nodes', 0)
        
        print(f"  Internal State (Cat): {isv_mode}")
        print(f"  Stability: {stability}")
        print(f"  Orchestration (Chef): {action}")
        print(f"  Power Draw: {power}W | Active Nodes: {nodes}")
        
        results.append({
            "id": ep['episode_id'],
            "mode": isv_mode,
            "stability": stability,
            "action": action,
            "power": power,
            "nodes": nodes
        })


    # Save results
    os.makedirs("reports", exist_ok=True)
    with open("reports/neuromorphic_test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\n--- TEST COMPLETE ---")
    print("Full results saved to reports/neuromorphic_test_results.json")

if __name__ == "__main__":
    run_inference_domain_test()
