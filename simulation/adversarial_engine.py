import random
import time
from intelligence.reasoning_agent import ReasoningAgent
from simulation.cyber_simulator import CyberSimulator

class AdversarialEngine:
    """
    Manages the 'Red Team vs Blue Team' co-evolution loop.
    """
    def __init__(self, simulator: CyberSimulator):
        self.sim = simulator
        self.reasoner = ReasoningAgent()
        
        # GAP 3: Independent Watchdog Cognition / Multi-agent
        self.defensive_auditor = ReasoningAgent()
        self.narrative_verifier = ReasoningAgent()
        
        self.history = []
        self.round = 0

    def run_round(self, red_target=None, attack_type="BruteForce"):
        self.round += 1
        print(f"\n--- Round {self.round} Start ---")
        
        # 1. Red Team Action
        if not red_target:
            # Simple strategy: Choose a node that isn't isolated/blocked
            active_nodes = [n for n in self.sim.G.nodes if self.sim.node_states.get(n, {}).get("status") != "ISOLATED"]
            red_target = random.choice(active_nodes) if active_nodes else "N3"
        
        intensity = random.uniform(0.6, 0.95)
        print(f"[RED TEAM] Attacking {red_target} with {attack_type} (Intensity: {intensity:.2f})")
        
        attack_results = self.sim.simulate_attack(red_target, attack_type, intensity)
        
        # 2. Blue Team Detection & Reasoning
        # Extract high risk nodes for reasoning
        high_risk_nodes = [node for node, data in attack_results.items() if data.get("anomaly_prediction", 0) > 0.6]
        
        mitigation_actions = []
        if high_risk_nodes:
            print(f"[BLUE TEAM] High risk detected on {high_risk_nodes}. Reasoning...")
            context = {
                "detected_nodes": high_risk_nodes,
                "attack_type": attack_type,
                "impact_data": attack_results,
                "round": self.round
            }
            # LLM Suggests Strategy
            decision = self.reasoner.execute_reasoning(context)
            strategy = decision.get("strategy", ["Block source node"])
            
            # 3. Defensive Auditor checks the mitigation actions
            print(f"[DEFENSIVE AUDITOR] Auditing {len(strategy)} proposed actions...")
            audit_context = {"proposed_strategy": strategy, "current_state": self.sim.node_states}
            audit_result = self.defensive_auditor.execute_reasoning(audit_context)
            
            # 4. Narrative Verifier ensures continuity (Identity Drift detection)
            verifier_context = {"history_length": len(self.history), "recent_actions": strategy}
            self.narrative_verifier.execute_reasoning(verifier_context)
            
            # 5. Blue Team Action (Autonomous Response) if approved by auditor
            if audit_result.get("watchdog_status", "PASS") == "PASS":
                for step in strategy:
                    # Map broad strategy to specific simulator actions
                    if "Block" in step or "Isolate" in step:
                        for node in high_risk_nodes:
                            action_res = self.sim.apply_mitigation(node, "Block")
                            mitigation_actions.append({"node": node, "action": "Block", "result": action_res})
                    elif "Patch" in step:
                        for node in high_risk_nodes:
                            action_res = self.sim.apply_mitigation(node, "Patch")
                            mitigation_actions.append({"node": node, "action": "Patch", "result": action_res})
            else:
                print(f"[BLUE TEAM] Strategy quarantined by auditor: {audit_result.get('error')}")

        # Record History
        round_data = {
            "round": self.round,
            "red_action": {"target": red_target, "type": attack_type, "intensity": intensity},
            "blue_responses": mitigation_actions,
            "system_state": {n: self.sim.node_states.get(n, {}).get("status") for n in self.sim.G.nodes}
        }
        self.history.append(round_data)
        
        return round_data

if __name__ == "__main__":
    sim = CyberSimulator()
    engine = AdversarialEngine(sim)
    
    # Run 3 rounds of simulation
    for i in range(3):
        res = engine.run_round()
        print(f"Round {i+1} Result: {res['blue_responses']}")
