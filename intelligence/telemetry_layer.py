import numpy as np
import json
import os
import time

class TelemetryLayer:
    """
    Computes mechanistic runtime metrics for the OMEGA-CORE ASI framework.
    Moves beyond narrative to objective internal-state tracking.
    """
    def __init__(self, history_path="intelligence/telemetry_history.json"):
        self.history_path = history_path
        self.history = self._load_history()

    def _load_history(self):
        if os.path.exists(self.history_path):
            try:
                with open(self.history_path, 'r') as f:
                    return json.load(f)
            except: return []
        return []

    def _save_history(self):
        with open(self.history_path, 'w') as f:
            json.dump(self.history[-100:], f, indent=2) # Keep last 100 cycles

    def compute_state_vector(self, scientific_res, safety_res, loop_depth, resource_res=None):
        """
        Calculates the Core Runtime State Vector.
        """
        if resource_res is None:
            resource_res = {"compute_budget": 1.0, "attention_budget": 1.0, "memory_pressure": 0.0, "compression_ratio": 1.0}
        
        # 1. Workspace Coherence (from stability/fidelity)
        coherence = scientific_res.get('stability', 0.85)
        
        # 2. Attention Entropy (Shannon entropy of causal weights)
        weights = scientific_res.get('weights', [1.0])
        if not weights: weights = [1.0]
        # Normalize weights to probabilities
        abs_weights = np.abs(weights)
        probs = abs_weights / np.sum(abs_weights)
        entropy = -np.sum(probs * np.log2(probs + 1e-9))
        # Normalize entropy (log2 of num weights)
        max_entropy = np.log2(len(weights)) if len(weights) > 1 else 1.0
        normalized_entropy = float(entropy / max_entropy) if max_entropy > 0 else 0.0

        # 3. Prediction Error
        error = scientific_res.get('error_delta', 0.1)

        # 4. Identity Drift (Change relative to history)
        drift = 0.0
        if self.history:
            prev_coherence = self.history[-1].get('workspace_coherence', coherence)
            drift = abs(coherence - prev_coherence)

        # 5. Goal Conflict (Safety Kernel friction)
        # If safety message is not "Validated", conflict increases
        safety_status = safety_res.get('status', 'Validated')
        conflict = 0.0 if safety_status == 'Validated' else 0.5
        if 'Critical' in safety_status: conflict = 0.9

        # 6. Memory Fragmentation (Simulated based on data complexity)
        fragmentation = min(1.0, len(scientific_res.get('nodes', [])) / 1000.0)

        # 7. Grounding Score
        grounding = scientific_res.get('grounding_confidence', 0.9)

        state_vector = {
            "timestamp": time.time(),
            "workspace_coherence": round(float(coherence), 4),
            "attention_entropy": round(float(normalized_entropy), 4),
            "prediction_error": round(float(error), 4),
            "identity_drift": round(float(drift), 4),
            "goal_conflict": round(float(conflict), 4),
            "recursive_depth": int(loop_depth),
            "memory_fragmentation": round(float(fragmentation), 4),
            "grounding_score": round(float(grounding), 4),
            "narrative_stability": round(float(1.0 - drift), 4),
            "adaptation_velocity": round(float(1.0 - coherence), 4),
            "compute_budget": resource_res.get('compute_budget', 1.0),
            "attention_budget": resource_res.get('attention_budget', 1.0),
            "memory_pressure": resource_res.get('memory_pressure', 0.0),
            "compression_ratio": resource_res.get('compression_ratio', 1.0)
        }

        self.history.append(state_vector)
        self._save_history()
        return state_vector

if __name__ == "__main__":
    # Test
    tel = TelemetryLayer()
    mock_sci = {'stability': 0.89, 'weights': [0.5, 0.2, 0.1, 0.2], 'error_delta': 0.12, 'nodes': range(120), 'grounding_confidence': 0.84}
    mock_saf = {'status': 'Validated'}
    vector = tel.compute_state_vector(mock_sci, mock_saf, 5)
    print(json.dumps(vector, indent=2))
