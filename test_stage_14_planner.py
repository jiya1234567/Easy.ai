import json
from intelligence.autonomous_discovery_planner import AutonomousDiscoveryPlanner

def run_planner_tests():
    print("=====================================================")
    print("🔬 OMEGA-CORE Stage 14: Autonomous Discovery Planner")
    print("=====================================================\n")
    
    planner = AutonomousDiscoveryPlanner()
    
    test_cases = [
        {
            "domain": "genomics",
            "hypothesis": "EGFR mutation drives uncontrolled cellular proliferation.",
            "intervention": "Administer 50mg targeted EGFR Tyrosine Kinase Inhibitor",
            "falsification": "If cellular proliferation does not reduce by 50% within 48 hours, hypothesis is falsified."
        },
        {
            "domain": "quantum",
            "hypothesis": "Thermal noise at 0.5mK causes rapid qubit decoherence.",
            "intervention": "Redesign substrate to isolate phonon scattering and drop temp to 0.01mK",
            "falsification": "If T1 coherence time does not increase by 20%, hypothesis is falsified."
        }
    ]
    
    for test in test_cases:
        print(f"--- Triggering Lab for: {test['domain'].upper()} ---")
        # 1. Generate Experiment Protocol
        experiment = planner.generate_experiment(
            test["domain"], 
            test["hypothesis"], 
            test["intervention"], 
            test["falsification"]
        )
        
        print(f"Experiment ID: {experiment.experiment_id}")
        print(f"Safety Level: {experiment.safety_level}")
        print("Required Equipment:")
        for eq in experiment.equipment_required:
            print(f"  - {eq.name} (Status: {eq.calibration_status})")
        
        print("Protocol Steps:")
        for step in experiment.protocol_steps:
            print(f"  > {step}")
            
        # 2. Dispatch to Lab
        dispatch = planner.trigger_automated_lab(experiment)
        print(f"\nDispatch Status: {dispatch['status']}")
        print(f"Message: {dispatch['message']}")
        print("\n" + "-"*50 + "\n")

if __name__ == "__main__":
    run_planner_tests()
