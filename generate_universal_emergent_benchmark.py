"""
generate_universal_emergent_benchmark.py
OMEGA-CORE | ASSI Framework
Universal Emergent Systems Benchmark — 6 Domain Transition Datasets
Based on: Top 20 Strategic Research Areas + NSW Commercialisation Showcase Companies
Each dataset simulates a Phase Transition from Stable -> Adaptive -> Unstable
"""
import json
import numpy as np
import os
import sys
from datetime import datetime, timezone

def compute_entropy(values):
    """Shannon entropy of a normalized probability distribution."""
    probs = np.array(values)
    probs = probs / (probs.sum() + 1e-9)
    return float(-np.sum(probs * np.log(probs + 1e-9)))

def compute_coherence(values):
    """Coherence as mean pairwise synchronisation proxy."""
    return float(1.0 / (1.0 + np.std(values)))

def state_label(entropy, coherence):
    """Classify each timestep into a state label."""
    if coherence > 0.75 and entropy < 0.4:
        return "Stable"
    elif coherence > 0.45 and entropy < 0.7:
        return "Adaptive"
    elif coherence > 0.20 and entropy < 0.9:
        return "Unstable"
    else:
        return "Critical Transition"

def build_timeseries(sensor_trajectories, sensor_names, domain, company, category):
    """
    Given a dict of sensor_name -> list of values across timesteps,
    compute entropy, coherence, prediction error, and state for each timestep.
    """
    steps = list(sensor_trajectories.values())[0]
    n = len(steps)
    records = []
    prev_coherence = None

    for i in range(n):
        readings = [sensor_trajectories[s][i] for s in sensor_names]
        ent = compute_entropy(readings)
        coh = compute_coherence(readings)
        pred_err = abs(readings[-1] - readings[0]) if len(readings) > 1 else 0.0
        dC_dt = abs(coh - prev_coherence) if prev_coherence is not None else 0.0
        phase_event = dC_dt > 0.15  # Phase transition trigger threshold
        prev_coherence = coh

        record = {
            "timestep": f"t{i+1}",
            **{sensor_names[j]: round(readings[j], 4) for j in range(len(sensor_names))},
            "entropy": round(ent, 4),
            "coherence": round(coh, 4),
            "prediction_error": round(pred_err, 4),
            "dC_dt": round(dC_dt, 4),
            "phase_transition_event": phase_event,
            "state": state_label(ent, coh)
        }
        records.append(record)

    return {
        "domain": domain,
        "company_inspiration": company,
        "category": category,
        "sensor_names": sensor_names,
        "timeseries": records
    }


def generate_quantum_stability():
    """Q-CTRL inspired: Qubit noise, decoherence, environmental coupling."""
    t = np.linspace(0, 1, 12)
    sensor_trajectories = {
        "qubit_noise":          list(0.05 + 0.02*t + 0.3*t**3 + 0.1*np.random.randn(12)*t),
        "decoherence_rate":     list(0.03 + 0.01*t + 0.5*t**4),
        "env_coupling":         list(0.02 + 0.1*np.sin(t * np.pi) + 0.2*t**2),
        "gate_fidelity":        list(np.clip(0.99 - 0.8*t**2 - 0.1*np.random.randn(12)*t, 0, 1)),
    }
    return build_timeseries(
        sensor_trajectories,
        ["qubit_noise", "decoherence_rate", "env_coupling", "gate_fidelity"],
        "Quantum Computing Stability",
        "Q-CTRL",
        "Hybrid (Reducible -> Irreducible)"
    )

def generate_ocean_emergence():
    """Ocius inspired: Wave height, turbulence, salinity, weather coupling -> storm emergence."""
    t = np.linspace(0, 1, 12)
    sensor_trajectories = {
        "wave_height_m":        list(0.5 + 0.3*t + 2.5*t**3),
        "turbulence_index":     list(0.1 + 0.05*t + 0.8*t**4 + 0.1*np.random.randn(12)*t**2),
        "salinity_ppt":         list(35.0 - 0.5*t + 1.5*np.sin(t * 2 * np.pi)),
        "weather_coupling":     list(0.1 + 0.9*t**2),
        "current_velocity_ms":  list(0.3 + 0.2*t + 1.8*t**3),
    }
    return build_timeseries(
        sensor_trajectories,
        ["wave_height_m", "turbulence_index", "salinity_ppt", "weather_coupling", "current_velocity_ms"],
        "Ocean Systems Emergence",
        "Ocius",
        "Irreducible (Storm Emergence)"
    )

def generate_biological_transition():
    """Skin2Neuron + CREATE Medicines: Cellular state, metabolic patterns, protein activity."""
    t = np.linspace(0, 1, 12)
    sensor_trajectories = {
        "cellular_state":       list(0.1 + 0.05*t + 0.7*t**3 + 0.05*np.random.randn(12)),
        "metabolic_flux":       list(1.0 + 0.5*np.sin(t * np.pi * 2) + 0.3*t**2),
        "protein_activity":     list(0.2 + 0.1*t + 0.5*t**3),
        "differentiation_marker": list(np.clip(0.05 + 0.9*t**2 + 0.05*np.random.randn(12), 0, 1)),
        "apoptosis_signal":     list(np.clip(0.02 + 0.5*t**4, 0, 1)),
    }
    return build_timeseries(
        sensor_trajectories,
        ["cellular_state", "metabolic_flux", "protein_activity", "differentiation_marker", "apoptosis_signal"],
        "Biological State Transition",
        "Skin2Neuron / CREATE Medicines",
        "Emergent / Biological"
    )

def generate_climate_energy():
    """Thermal Dawn + HydGene: Thermal gradients, solar load, energy demand, atmospheric change."""
    t = np.linspace(0, 1, 12)
    sensor_trajectories = {
        "thermal_gradient_C":   list(5.0 + 2.0*t + 10.0*t**3),
        "solar_irradiance_W":   list(800 + 200*np.sin(t * np.pi) - 300*t**2),
        "energy_demand_kW":     list(50.0 + 20.0*t + 30.0*t**3 + 5*np.random.randn(12)),
        "atmospheric_CO2_ppm":  list(415 + 0.5*t * 100),
        "grid_stability":       list(np.clip(1.0 - 0.8*t**2 - 0.1*np.random.randn(12)*t, 0, 1)),
    }
    return build_timeseries(
        sensor_trajectories,
        ["thermal_gradient_C", "solar_irradiance_W", "energy_demand_kW", "atmospheric_CO2_ppm", "grid_stability"],
        "Climate-Energy Adaptive Systems",
        "Thermal Dawn / HydGene Renewables",
        "Hybrid (Reducible Physics -> Emergent Grid)"
    )

def generate_autonomous_vision():
    """Unleash Live + Carbonix: Scene instability, drone motion, anomaly detection."""
    t = np.linspace(0, 1, 12)
    sensor_trajectories = {
        "scene_instability":    list(0.1 + 0.05*t + 0.9*t**3 + 0.1*np.random.randn(12)*t),
        "object_motion_score":  list(0.2 + 0.1*t + 0.7*t**3),
        "occlusion_index":      list(0.05 + 0.6*t**2 + 0.1*np.random.randn(12)*t**2),
        "anomaly_score":        list(np.clip(0.01 + 0.99*t**3, 0, 1)),
        "lighting_variance":    list(0.1 + 0.5*np.abs(np.sin(t * np.pi * 3))),
    }
    return build_timeseries(
        sensor_trajectories,
        ["scene_instability", "object_motion_score", "occlusion_index", "anomaly_score", "lighting_variance"],
        "Autonomous Vision Systems",
        "Unleash Live / Carbonix",
        "Irreducible (Dynamic Scene)"
    )

def generate_semiconductor_nano():
    """SiNAB / Advanced Nano: Thermal noise, signal degradation, quantum effects."""
    t = np.linspace(0, 1, 12)
    sensor_trajectories = {
        "thermal_noise_nV":     list(2.0 + 0.5*t + 5.0*t**3 + 0.5*np.random.randn(12)),
        "signal_snr_dB":        list(np.clip(40.0 - 30.0*t**2 - 2*np.random.randn(12), 0, 40)),
        "quantum_tunneling_rate": list(0.001 + 0.1*t**3),
        "leakage_current_nA":   list(0.5 + 0.2*t + 2.0*t**3),
        "bit_error_rate":       list(np.clip(1e-9 + 0.05*t**4, 0, 1)),
    }
    return build_timeseries(
        sensor_trajectories,
        ["thermal_noise_nV", "signal_snr_dB", "quantum_tunneling_rate", "leakage_current_nA", "bit_error_rate"],
        "Semiconductor / Nano Engineering",
        "SiNAB / Advanced Semiconductor Systems",
        "Hybrid (Stable CMOS -> Quantum Instability)"
    )


def generate_universal_emergent_benchmark():
    print("=" * 60)
    print("  OMEGA-CORE | ASSI Universal Emergent Benchmark Generator")
    print("=" * 60)

    datasets = [
        generate_quantum_stability(),
        generate_ocean_emergence(),
        generate_biological_transition(),
        generate_climate_energy(),
        generate_autonomous_vision(),
        generate_semiconductor_nano(),
    ]

    output = {
        "metadata": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "framework": "OMEGA-CORE ASSI Engine",
            "version": "2.0",
            "description": "Universal Emergent Systems Benchmark — 6 Domain Phase Transition Datasets",
            "research_basis": "Top 20 Strategic Research Areas + NSW Commercialisation Showcase 2024/2025",
            "domains": len(datasets),
            "timesteps_per_domain": len(datasets[0]["timeseries"]),
            "phase_transition_threshold": "dC_dt > 0.15"
        },
        "domains": datasets
    }

    os.makedirs("data", exist_ok=True)
    out_path = "data/universal_emergent_benchmark.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4)

    print(f"\n{'Domain':<40} {'Total Steps':>12} {'Transitions Found':>18}")
    print("-" * 72)
    for d in datasets:
        transitions = sum(1 for r in d["timeseries"] if r["phase_transition_event"])
        print(f"{d['domain']:<40} {len(d['timeseries']):>12} {transitions:>18}")

    print(f"\n[OK] Benchmark saved -> {out_path}")
    print(f"     Total domains:   {len(datasets)}")
    print(f"     Total timesteps: {len(datasets) * len(datasets[0]['timeseries'])}")
    print("     Ready for ASSI Research Lab.")


if __name__ == "__main__":
    generate_universal_emergent_benchmark()
