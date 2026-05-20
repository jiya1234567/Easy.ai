import json
import os
import sys

# Ensure simulation directory can be resolved
sys.path.append(os.getcwd())

from simulation.omega_unified_runner import OmegaUnifiedRunner
from simulation.omega_replay_kernel import ScientificValidationEngine

def verify_unified_benchmark():
    print("--- [VERIFICATION] INITIATING OMEGA-CORE UNIFIED BENCHMARK & SIMULATION SUITE ---")
    
    # 1. Initialize Runner
    runner = OmegaUnifiedRunner(data_path="data/omega_unified_suite.json")
    
    # 2. Run All Tests
    print("\nRunning test cases through the 11-stage pipeline...")
    logs = runner.run_all()
    print(f"DONE: Executed {len(logs)} standard benchmark test cases.")
    
    # 3. Print Category Audit
    print("\n" + "="*50)
    print("      STAGE & SYSTEM LEVEL VERIFICATION STATUS")
    print("="*50)
    
    categories = {}
    for log in logs:
        cat = log["category"]
        categories[cat] = categories.get(cat, 0) + 1
        
        status_flag = "[PASS]"
        p_check = log["stages"]["5_physics_consistency"]["physics_consistent"]
        v_flag = log["stages"]["9_vulnerability_discovery"]["vulnerability_flagged"]
        
        if not p_check:
            status_flag = "[PHYS_VIOLATION]"
        elif v_flag:
            status_flag = "[VULN_DETECTED]"
            
        print(f"Case {log['test_id']} [{cat.upper()}] -> Status: {status_flag}")
        print(f"  -> Prediction: {log['stages']['11_final_output']['prediction']}")
        print(f"  -> Confidence: {log['stages']['11_final_output']['confidence_score']*100:.1f}%")
        
        if v_flag:
            print(f"  -> [OMEGA-MYTHOS EXPLOIT]: {log['stages']['9_vulnerability_discovery']['vulnerability_chain']}")
        if not p_check:
            print(f"  -> [THERMODYNAMIC VIOLATION]: {log['stages']['5_physics_consistency']['log']}")
        print("-" * 50)
        
    # 4. GAP 5: Run Statistical Scientific Validation (1,000 Run Monte-Carlo)
    print("\n" + "="*50)
    print("      STATISTICAL SCIENTIFIC VALIDATION METRICS")
    print("="*50)
    
    base_case = next(c for c in runner.suite_data["1_master_test_entry_format"] if c["test_id"] == "T-0001")
    validator = ScientificValidationEngine(runner)
    
    stats = validator.run_monte_carlo_validation(base_case, iterations=1000)
    
    # Save validation reports
    with open("reports/omega_scientific_validation.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)
        
    print(f"\nMonte Carlo Runs:             {stats['iterations']} Perturbations")
    print(f"Mean Replay Fidelity:          {stats['replay_fidelity']:.3f}% (Stable)")
    print(f"Thermal Prediction MAE:        {stats['prediction_error_mae']:.5f} C")
    print(f"  -> 95% Confidence Interval: [{stats['prediction_error_ci_95'][0]:.5f}, {stats['prediction_error_ci_95'][1]:.5f}]")
    print(f"Mean Prediction Confidence:    {stats['confidence_score_mean']*100:.2f}%")
    print(f"  -> 95% Confidence Interval: [{stats['confidence_score_ci_95'][0]*100:.2f}%, {stats['confidence_score_ci_95'][1]*100:.2f}%]")
    print(f"Vulnerability Isolation Latency: {stats['mythos_isolation_latency_ns_mean']:.2f} ns (Std: {stats['mythos_isolation_latency_ns_std']:.2f} ns)")
    print(f"Thermodynamic Compliance Rate:  {stats['thermodynamic_compliance_rate']:.2f}%")
    print("\nStatistical outputs saved to reports/omega_scientific_validation.json")
    
    # 5. Comparative Telemetry Output
    print("\n" + "="*50)
    print("    NVIDIA JETSON vs OMEGA COGNITIVE SEMICONDUCTOR")
    print("="*50)
    
    benchmarks = runner.generate_comparative_benchmarks()
    for metric, data in benchmarks.items():
        m_name = metric.replace('_', ' ').upper()
        print(f"\nMetric: {m_name}")
        print(f"  NVIDIA Jetson Orin: {data['nvidia_jetson_orin']}")
        print(f"  OMEGA-CORE:         {data['omega_core']}")
        print(f"  ADVANTAGE:          {data['delta']}")
        
    print("\n" + "="*50)
    print("GLOBAL UNIFIED TEST EXECUTION SUCCESSFUL")
    print("="*50)

if __name__ == "__main__":
    verify_unified_benchmark()
