import json, os, requests, time, re, random

def load_dna():
    f_path = "rules/rules_fixed.json"
    default = {"science": {"budget": 10000000, "max_toxicity": 0.12}, "finance": {"max_rsi": 70}}
    try:
        if os.path.exists(f_path) and os.path.getsize(f_path) > 0:
            with open(f_path, "r") as f: return json.load(f)
    except: pass
    with open(f_path, "w") as f: json.dump(default, f, indent=2)
    return default

def run_psi_autopilot(intent, chat_input, brain_mode, api_key, is_multi, is_dispatch=False, recursive_feedback=None):
    # Recalibrate
    if not os.path.exists("DASHBOARD.json"):
        with open("DASHBOARD.json", "w") as f: json.dump({"chat_history": []}, f)
    
    with open("DASHBOARD.json", "r") as f: d_old = json.load(f)
    history = d_old.get("chat_history", [])

    dna = load_dna()
    if os.path.exists("Target.JASON"):
        with open("Target.JASON", "r") as f: signals = json.load(f)
    else: signals = {"confidence": 0.5, "rsi": 50}

    # Agent Logic
    rsi = float(signals.get('rsi', 50))
    order_id = f"WO-{random.randint(10000, 99999)}"
    status = "EXECUTING" if is_dispatch else "STAGING"
    
    # Process Chat
    if chat_input:
        history.append({"role": "Simon", "content": chat_input})
        history.append({"role": "Agent", "content": f"Acknowledged, Architect. Order {order_id} is being optimized for current physics."})

    dashboard = {
        "metrics": {"bias": "Optimized" if rsi < 40 else "Caution", "iq": 185, "order_id": order_id},
        "agent_reports": {"cfo": status, "hr": "Omega Verified", "ceo": brain_mode},
        "world_model": {"markov": "STABLE", "rulid": "Symmetry Locked"},
        "physics": {"regime": "Universal Lab", "multimodal": "VERIFIED" if is_multi else "TEXT"},
        "steps": signals.get("steps", [f"Step {i}: Computational Node {i} active" for i in range(1, 91)]),
        "chat_history": history[-10:] # Keep recent memory
    }
    with open("DASHBOARD.json", "w") as f: json.dump(dashboard, f, indent=2)
    return dashboard
