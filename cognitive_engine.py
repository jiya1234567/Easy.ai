import json
import time

class InternalStateVector:
    """The 'Cat': Tracks internal organism stability and stress."""
    def __init__(self):
        self.stability = 1.0
        self.stress = 0.0
        self.energy = 1.0
        self.mode = "CALM"
        self.identity_anchor = 1.0

    def update(self, telemetry):
        # State Transition Logic
        error = telemetry.get("prediction_error", 0)
        stress = telemetry.get("biometric_stress", 0)
        
        # Surprise drives stress up, stability down
        self.stress = 0.7 * self.stress + 0.3 * (error + stress)
        self.stability = 1.0 - self.stress
        
        # Energy consumption impacts mode
        energy_draw = telemetry.get("energy_consumption", 0.1)
        self.energy -= energy_draw
        
        if self.stress > 0.6:
            self.mode = "ALERT"
        elif self.stress > 0.3:
            self.mode = "ADAPTIVE"
        else:
            self.mode = "CALM"
            
        # Recovery dynamics
        if self.stability < 0.5:
            self.identity_anchor *= 0.95 # Drift
        else:
            self.identity_anchor = min(1.0, self.identity_anchor + 0.01)
            
        return {
            "stability": round(self.stability, 2),
            "stress": round(self.stress, 2),
            "mode": self.mode,
            "identity": round(self.identity_anchor, 2)
        }

class CognitiveOrchestrator:
    """The 'Chef': Manages multi-agent coordination and recursive auditing."""
    def __init__(self, isv):
        self.isv = isv
        self.workspace_active = False

    def process_episode(self, episode):
        telemetry = episode.get("telemetry", {})
        isv_state = self.isv.update(telemetry)
        
        # Workspace Ignition Logic
        activation = telemetry.get("workspace_activation", 0)
        if activation > 0.8 or isv_state["mode"] == "ALERT":
            self.workspace_active = True
            action = "GLOBAL_BROADCAST: All agents active for threat mitigation."
        else:
            self.workspace_active = False
            action = "SPARSE_ACTIVATION: Routing only salience nodes."
            
        # Recursive Audit (Self-Correction)
        audit = {
            "meta_reflection": "Confidence aligned" if isv_state["stability"] > 0.7 else "Initiating self-correction loop",
            "recursive_update": True if isv_state["mode"] == "ALERT" else False
        }
        
        return {
            "isv": isv_state,
            "orchestrator_action": action,
            "audit": audit
        }
