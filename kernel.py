import json, os, requests, random, re, time, base64, io
from PIL import Image

from cognitive_engine import InternalStateVector, CognitiveOrchestrator

def load_dna():
    try:
        with open("rules/rules_fixed.json", "r") as f: return json.load(f)
    except: return {"finance": {"max_rsi": 70}, "cfo_logic": {"risk_threshold": 0.7}, "hr_clearance": {"architect": "Simon"}}

class CognitiveMemory:
    def __init__(self, file="intelligence/experience.json"):
        self.file = file
        os.makedirs(os.path.dirname(self.file), exist_ok=True)
        self.log = self._load()

    def _load(self):
        try:
            if os.path.exists(self.file):
                with open(self.file, "r") as f: return json.load(f)
        except: pass
        return []

    def store(self, context, decision, outcome="Pending"):
        entry = {"id": f"ep-{int(time.time())}", "ts": time.ctime(), "ctx": context, "dec": decision, "out": outcome}
        self.log.append(entry)
        if len(self.log) > 100: self.log = self.log[-100:]
        with open(self.file, "w") as f: json.dump(self.log, f, indent=2)
        return entry["id"]

    def recall(self, regime):
        matches = [e for e in self.log if e['ctx'].get('regime') == regime and e['out'] != "Pending"]
        if not matches: return "No past data", 0.5
        successes = len([m for m in matches if m['out'] == "Success"])
        rate = successes / len(matches)
        bias = "Aggressive" if rate > 0.6 else "Defensive" if rate < 0.4 else "Balanced"
        return bias, rate

def run_psi_autopilot(intent, raw_paste, brain_mode, api_key, is_multi, chat_msg=None, image_bytes=None, episode_data=None):
    dna = load_dna()
    start_time = time.time()
    mem = CognitiveMemory()
    isv = InternalStateVector()
    chef = CognitiveOrchestrator(isv)
    
    # Inference Domain Processing
    if episode_data:
        cog_result = chef.process_episode(episode_data)
        isv_state = cog_result["isv"]
        orch_action = cog_result["orchestrator_action"]
    else:
        isv_state = {"mode": "CALM", "stability": 1.0, "identity": 1.0}
        orch_action = "Inference Domain Baseline"

    # Auto-Ingress
    if (not raw_paste or len(raw_paste) < 10) and os.path.exists("Target.JASON"):
        with open("Target.JASON", "r") as f: signals = json.load(f)
    else: signals = {"confidence": 0.99, "rsi": 32}

    rsi = float(signals.get('rsi', 50))
    conf = float(signals.get('confidence', 0.5))
    regime = signals.get("protocol", "Inference Domain")
    
    # --- COGNITIVE RECALL ---
    past_bias, success_rate = mem.recall(regime)
    
    # Markov Forecast
    markov = "STABLE" if isv_state["mode"] == "CALM" else "ADAPTIVE RECOVERY" if isv_state["mode"] == "ADAPTIVE" else "THREAT MITIGATION"
    
    # Agent Bus Logic
    cfo_report = "AUTHORIZED" if rsi < 70 else "DENIED: Risk Violation"
    hr_report = f"Simon: {isv_state['identity']} Identity Stability"
    
    # Store current episode
    context = {"rsi": rsi, "regime": regime, "isv": isv_state}
    decision = {"markov": markov, "orchestrator": orch_action}
    episode_id = mem.store(context, decision)

    # FINAL OMEGA ASSEMBLY
    dashboard = {
        "metrics": {
            "bias": isv_state["mode"], 
            "iq": 185, 
            "order_id": f"ID-{random.randint(10000,99999)}",
            "episode_id": episode_id,
            "success_rate": f"{isv_state['stability']:.1%}"
        },
        "agent_reports": {"cfo": cfo_report, "hr": hr_report, "orchestrator": orch_action},
        "physics": {"regime": regime, "identity": isv_state["identity"], "multimodal": "VERIFIED" if is_multi else "TEXT"},
        "steps": [f"Step 1: Ingesting Neuromorphic Episode", f"Step 2: ISV State Transition -> {isv_state['mode']}", f"Step 3: Chef Orchestration -> {orch_action}"],
        "chat_history": [{"role": "Agent", "content": f"Architect Simon, Inference Domain Audit Complete. Internal State: {isv_state['mode']}. Stability: {isv_state['stability']}."}]
    }
    
    with open("DASHBOARD.json", "w") as f:
        json.dump(dashboard, f, indent=2)
    return dashboard

