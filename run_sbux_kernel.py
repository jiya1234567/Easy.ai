from kernel import run_psi_autopilot
import json

# Process the Target.JASON we just created
print("Processing SBUX through ASI Kernel...")
dashboard = run_psi_autopilot(
    intent="Analyze SBUX for Institutional Entry", 
    raw_paste="", 
    brain_mode="Omega-Core (Internal)", 
    api_key="", 
    is_multi=True
)

print(f"SBUX Prediction: {dashboard['agent_reports']['sim']}")
print(f"Episode ID: {dashboard['metrics']['episode_id']}")
print("DASHBOARD.json updated.")
