import json
import random
import os
from datetime import datetime

def generate_cognitive_episodes(output_file="data/neuromorphic_episodes.json"):
    """
    Generates temporal 'Cognitive Episode' telemetry for the Inference Domain.
    Models the 'Cat' (Internal State) and 'Chef' (Orchestrator) dynamics.
    """
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    episodes = [
        {
            "episode_id": "EP-NORMAL-001",
            "type": "baseline",
            "timestamp": datetime.now().isoformat(),
            "telemetry": {
                "visual_entropy": 0.21,
                "audio_salience": 0.15,
                "biometric_stress": 0.12,
                "attention_focus": "environmental_scan",
                "workspace_activation": 0.31,
                "prediction_confidence": 0.95,
                "prediction_error": 0.05,
                "identity_stability": 0.98,
                "energy_consumption": 0.15,
                "recovery_rate": 1.0,
                "power_draw_watts": 0.8,
                "active_nodes": 45
            }
        },
        {
            "episode_id": "EP-SURPRISE-002",
            "type": "prediction_error",
            "timestamp": datetime.now().isoformat(),
            "telemetry": {
                "visual_entropy": 0.71,
                "audio_salience": 0.43,
                "biometric_stress": 0.82,
                "attention_focus": "threat_region",
                "workspace_activation": 0.91,
                "prediction_confidence": 0.62,
                "prediction_error": 0.38,
                "identity_stability": 0.84,
                "energy_consumption": 0.27,
                "recovery_rate": 0.44,
                "power_draw_watts": 4.2,
                "active_nodes": 892
            }
        },
        {
            "episode_id": "EP-ADVERSARIAL-003",
            "type": "false_memory_injection",
            "timestamp": datetime.now().isoformat(),
            "telemetry": {
                "scenario": "false_memory_injection",
                "memory_conflict_score": 0.88,
                "identity_alignment": 0.57,
                "narrative_coherence": 0.49,
                "grounding_recovery_cycles": 7,
                "watchdog_triggered": True,
                "final_state_stability": 0.79,
                "prediction_error": 0.65,
                "energy_consumption": 0.85,
                "power_draw_watts": 6.8,
                "active_nodes": 1420
            }
        },
        {
            "episode_id": "EP-SPARSE-004",
            "type": "neuromorphic_efficiency",
            "timestamp": datetime.now().isoformat(),
            "telemetry": {
                "compute_mode": "event_driven",
                "active_nodes": 182,
                "inactive_nodes": 18211,
                "power_draw_watts": 2.1,
                "prediction_accuracy": 0.91,
                "latency_ms": 14,
                "manifold_coherence": 0.93,
                "energy_consumption": 0.08
            }
        }

    ]

    with open(output_file, "w") as f:
        json.dump(episodes, f, indent=2)
    
    print(f"Neuromorphic episodes generated at: {output_file}")
    return output_file

if __name__ == "__main__":
    generate_cognitive_episodes()
