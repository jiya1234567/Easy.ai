import streamlit as st
import json, os, time

st.set_page_config(page_title="Universal Lab: A&P Phillips", layout="wide")
st.title("🛡️ Universal Lab: A&P Phillips")
st.caption("Omega Clearance | Interactive Agent | DNA Editor | PSI Level 5")

with st.sidebar:
    st.header("🔐 Vault")
    st.success("SIMON: LEAD ARCHITECT")
    brain_choice = st.radio("Active Brain Link:", ["free gptAG (Internal)", "GPT-4o (Global)"])
    st.divider()
    selfie = st.camera_input("Authority Ingress")
    if st.button("🚨 TOTAL SYSTEM RESET"):
        if os.path.exists("DASHBOARD.json"): os.remove("DASHBOARD.json")
        st.rerun()

t1, t2, t3, t4 = st.tabs(["🚀 FACTORY", "🌍 WORLD MODEL", "🏛️ HIERARCHY", "🧬 EVOLUTION"])

with t1:
    intent = st.text_input("Mission Intent", "Complete NVDA / Antigravity Mission")
    c_a, c_b = st.columns(2)
    if c_a.button("📝 GENERATE WO", use_container_width=True):
        from kernel import run_psi_autopilot
        run_psi_autopilot(intent, "", brain_choice, "", bool(selfie), False)
        st.rerun()
    if c_b.button("🚀 DISPATCH AJ", use_container_width=True):
        from kernel import run_psi_autopilot
        run_psi_autopilot(intent, "DISPATCH ORDER RECEIVED", brain_choice, "", bool(selfie), True)
        st.rerun()

    if os.path.exists("DASHBOARD.json"):
        with open("DASHBOARD.json", "r") as f: d = json.load(f)
        st.subheader(f"📋 90-Step Factory Grid [{d['metrics'].get('order_id')}]")
        with st.container(height=350, border=True):
            for i, step in enumerate(d.get("steps", [])):
                st.checkbox(step, key=f"s{i}", value=(i<5))

with t2:
    if os.path.exists("DASHBOARD.json"):
        st.subheader("🌍 World Model & Wolfram Rulid")
        w = d.get('world_model', {})
        c1, c2 = st.columns(2)
        c1.metric("Markov Forecast", w.get('markov'))
        c2.metric("Rulid State", w.get('rulid'))
        st.info(f"System IQ: {d['metrics']['iq']} | Multimodal: {d['physics']['multimodal']}")

with t3:
    if os.path.exists("DASHBOARD.json"):
        st.subheader("🕵️ Agent Accountability & Chat")
        r = d.get('agent_reports', {})
        st.warning(f"**CFO:** {r.get('cfo')} | **HR:** {r.get('hr')}")
        
        st.divider()
        st.write("**💬 AJ Worker Communication**")
        for msg in d.get("chat_history", []):
            with st.chat_message(msg["role"]): st.write(msg["content"])
        
        u_msg = st.chat_input("Command the Worker Agent...")
        if u_msg:
            from kernel import run_psi_autopilot
            run_psi_autopilot(intent, u_msg, brain_choice, "", bool(selfie), True)
            st.rerun()

with t4:
    st.subheader("🧬 DNA Rules & Recursive Learning")
    dna_path = "rules/rules_fixed.json"
    if os.path.exists(dna_path):
        with open(dna_path, "r") as f: dna_txt = f.read()
        new_dna = st.text_area("FIXED DNA (Rules)", value=dna_txt, height=200)
        if st.button("🧬 AMEND DNA"):
            with open(dna_path, "w") as f: f.write(new_dna)
            st.success("DNA Mutated successfully.")
    
    st.divider()
    fb = st.text_area("Paste Meta AI / Global Audit Feedback")
    if st.button("🧠 LEARN FROM FEEDBACK"):
        st.balloons()
        st.success("🎯 PSI LEVEL 5: Experience stored.")
