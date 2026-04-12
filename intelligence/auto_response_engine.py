from simulation.cyber_simulator import CyberSimulator
from intelligence.reasoning_agent import ReasoningAgent

class AutoResponseEngine:
    """
    Closes the 'Detect -> Decide -> Act' loop by automatically executing mitigations.
    """
    def __init__(self, simulator: CyberSimulator):
        self.sim = simulator
        self.reasoner = ReasoningAgent()
        self.action_log = []

    def process_threats(self, detected_anomalies):
        """
        Receives a dictionary of {node: impact_data} and decides on actions.
        """
        if not detected_anomalies:
            return []

        # 1. Filter high-risk threats
        high_risk = {n: d for n, d in detected_anomalies.items() if d.get("anomaly_prediction", 0) > 0.7}
        
        if not high_risk:
            return []

        # 2. Get AI Strategy
        context = {
            "threats": high_risk,
            "system_state": {n: self.sim.node_states.get(n, {}).get("status") for n in self.sim.G.nodes}
        }
        decision = self.reasoner.execute_reasoning(context)
        
        # 3. Execute Actions
        executed_actions = []
        strategy = decision.get("strategy", [])
        
        for step in strategy:
            # Parse the strategy into simulator actions
            # Example strategies: "Isolate N3", "Patch N1", "Block high risk nodes"
            if "Isolate" in step or "Block" in step:
                # Find the node in the step text or use the threat list
                target_nodes = [n for n in high_risk.keys() if n in step]
                if not target_nodes: target_nodes = list(high_risk.keys())
                
                for node in target_nodes:
                    res = self.sim.apply_mitigation(node, "Block")
                    action_entry = {"node": node, "action": "BLOCK", "result": res, "rationale": step}
                    executed_actions.append(action_entry)
                    self.action_log.append(action_entry)
            
            elif "Patch" in step:
                target_nodes = [n for n in self.sim.node_states if n in step]
                if not target_nodes: target_nodes = list(high_risk.keys())
                
                for node in target_nodes:
                    res = self.sim.apply_mitigation(node, "Patch")
                    action_entry = {"node": node, "action": "PATCH", "result": res, "rationale": step}
                    executed_actions.append(action_entry)
                    self.action_log.append(action_entry)

        return executed_actions

if __name__ == "__main__":
    sim = CyberSimulator()
    engine = AutoResponseEngine(sim)
    
    # Simulate a threat
    threats = {
        "N3": {"anomaly_prediction": 0.9, "status": "COMPROMISED"}
    }
    actions = engine.process_threats(threats)
    print("Executed Actions:", actions)
