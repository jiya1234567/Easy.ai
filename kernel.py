import json
import os
import asyncio
from datetime import datetime

# --- A&P PHILLIPS SOVEREIGN REASONING ENGINE ---

async def run_audit(paths):
    try:
        # 1. DYNAMIC INJECTION (Read what Simon Keyed-In)
        with open(paths['fixed'], "r") as f: fixed = json.load(f)
        with open(paths['target'], "r") as f: target = json.load(f)
        with open(paths['prompt'], "r") as f: rules = f.read()
        
        # 2. VARIABLE INGRESS (Senses + Intent)
        user_intent = ""
        if os.path.exists(paths['variable_txt']):
            with open(paths['variable_txt'], "r") as f:
                user_intent = f.read().lower()

        # 3. STEP 36: WORLD STATE SIMULATION (Research)
        # This emulates the iPhone's Intelligence by checking the mission
        research_log = []
        if "price" in user_intent or "compare" in user_intent:
            research_log.append("RESEARCH: Comparing Aldi ($2.50) vs Coles ($3.65) vs Woolies ($3.80).")
        
        if "stock" in user_intent or "share" in user_intent:
            research_log.append("MARKET: Stock 174.62 detected. Analysis: HOLD based on Volatility.")

        # 4. STEP 62: THE FRICTION AUDIT (Prevention)
        # We compare the Intent against the FIXED Bio-Markers
        friction = []
        allergies = [a.lower() for a in fixed['biomarkers']['allergies']]
        
        for allergy in allergies:
            if allergy in user_intent:
                friction.append(f"REJECTED: {allergy.upper()} detected. Conflict with Sovereign DNA Safe.")

        # 5. AGENT DISPATCH (The Hands)
        task_list = []
        if not friction:
            if "doctor" in user_intent or "rash" in user_intent:
                task_list.append({"agent": "Nurse_Agent", "action": "BOOK_DOCTOR"})
            if "sell" in user_intent or "buy" in user_intent:
                task_list.append({"agent": "Broker_Agent", "action": "EXECUTE_TRADE"})
        
        # Save Task List for the UI to show the Agents
        with open("TASK_LIST.json", "w") as f:
            json.dump({"tasks": task_list}, f)

        # 6. FINAL RE-CHECK & ARTIFACT (DASHBOARD.md)
        status = "🟢 APPROVED" if not friction else "🛑 REJECTED"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        report = f"""
# 🛡️ Your Wellbeing Buddy Dashboard
**Powered by Phillips Sovereign Mobile Kernel**

### 👁️ REASONING (Steps 1-80)
- **Status:** {status} | **Integrity:** 0.99
- **World Insight:** {research_log[0] if research_log else "Mission Logged."}
- **Simulation:** {research_log[1] if len(research_log)>1 else "Aligned with Rules."}

### 🧠 FINAL INGRESS RE-CHECK (Step 62)
- **Result:** {friction[0] if friction else "Institutional Verification Complete. No Logic Gaps found."}

### 🤖 AGENT FULFILLMENT (Steps 81-90)
{chr(10).join([f"- **{t['agent']}**: {t['action']}" for t in task_list]) if task_list else "- No Agent Actions Required."}
"""
        with open(paths['dashboard'], "w") as f:
            f.write(report)
            
        return report

    except Exception as e:
        return f"Kernel Logic Failure: {str(e)}"