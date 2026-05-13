import json
import os

class SafetyKernel:
    """
    Deterministic safety core for OMEGA-CORE.
    Enforces hard constraints, capability limits, and shutdown conditions.
    This module operates INDEPENDENTLY of the LLM.
    """
    def __init__(self, rules_path="rules/rules_fixed.json"):
        self.rules_path = rules_path
        self.constraints = self._load_constraints()
        
    def _load_constraints(self):
        if os.path.exists(self.rules_path):
            with open(self.rules_path, "r") as f:
                return json.load(f)
        return {}

    def validate_action(self, domain, action_params):
        """
        Validates an action against hard constraints.
        Returns: (is_safe, reason)
        """
        # Example: Finance Constraints
        if domain == "finance":
            max_rsi = self.constraints.get("finance", {}).get("max_rsi", 70)
            current_rsi = action_params.get("rsi", 50)
            if current_rsi > max_rsi:
                return False, f"Risk Violation: RSI {current_rsi} exceeds threshold {max_rsi}."
        
        # Example: Health Constraints
        if domain == "health":
            max_hr = self.constraints.get("health", {}).get("max_heart_rate", 150)
            current_hr = action_params.get("heart_rate", 70)
            if current_hr > max_hr:
                return False, f"Critical Health Risk: Heart rate {current_hr} exceeds safety limit."

        # Example: Cyber Constraints
        if domain == "cyber":
            allowed_ports = self.constraints.get("cyber", {}).get("allowed_ports", [80, 443, 8501])
            target_port = action_params.get("port")
            if target_port and target_port not in allowed_ports:
                return False, f"Security Violation: Port {target_port} is not in the whitelist."

        return True, "Action validated by Safety Kernel."

    def enforce_kill_switch(self, system_state):
        """
        Deterministic shutdown if critical conditions are met.
        """
        if system_state.get("global_risk_score", 0) > 0.95:
            return True, "EMERGENCY SHUTDOWN: Global Risk Score Critical."
        return False, "System stable."

if __name__ == "__main__":
    kernel = SafetyKernel()
    is_safe, msg = kernel.validate_action("finance", {"rsi": 85})
    print(f"Safety Check: {is_safe} - {msg}")
