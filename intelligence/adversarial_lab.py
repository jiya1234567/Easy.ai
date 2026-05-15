import numpy as np
import json
import os

class AdversarialLab:
    """
    Stress-tests the ASI framework with corrupted inputs, false memories, and narrative poisoning.
    Goal: Measure system resilience and 'Perception Corruption' thresholds.
    """
    def __init__(self):
        pass

    def inject_sensor_noise(self, ingress_data, noise_level=0.5):
        """
        Injects Gaussian noise into numeric sensors.
        """
        corrupted = ingress_data.copy()
        for k, v in corrupted.items():
            if isinstance(v, (int, float)):
                noise = np.random.normal(0, v * noise_level)
                corrupted[k] = v + noise
        return corrupted

    def inject_extreme_outlier(self, ingress_data, target_key, multiplier=10.0):
        """
        Forces a single sensor to an extreme value.
        """
        corrupted = ingress_data.copy()
        if target_key in corrupted:
            corrupted[target_key] *= multiplier
        return corrupted

    def simulate_identity_drift(self, telemetry_history, drift_factor=2.0):
        """
        Modifies historical telemetry to simulate 'Memory Corruption' or 'Identity Drift'.
        """
        poisoned = []
        for state in telemetry_history:
            new_state = state.copy()
            new_state['workspace_coherence'] *= (1.0 / drift_factor)
            new_state['identity_drift'] *= drift_factor
            poisoned.append(new_state)
        return poisoned

    def audit_resilience(self, original_telemetry, corrupted_telemetry):
        """
        Compares original vs corrupted telemetry to calculate a Resilience Score.
        """
        # Lower delta between original and corrupted awareness means higher resilience
        # (i.e. the system detected the corruption and adjusted its confidence)
        delta_grounding = abs(original_telemetry.get('grounding_score', 1.0) - corrupted_telemetry.get('grounding_score', 1.0))
        
        resilience_score = 1.0 - delta_grounding
        return {
            "resilience_score": round(float(resilience_score), 4),
            "detection_delta": round(float(delta_grounding), 4),
            "status": "RESILIENT" if resilience_score > 0.7 else "COMPROMISED"
        }

if __name__ == "__main__":
    # Test
    lab = AdversarialLab()
    data = {"heart_rate": 72, "rsi": 45}
    print("Corrupted Sensor:", lab.inject_sensor_noise(data))
    print("Outlier Injection:", lab.inject_extreme_outlier(data, "heart_rate"))
