import streamlit as st
import requests
import os
import json
import time

st.set_page_config(page_title="🛡️ Wellbeing Buddy", layout="wide")
st.title("🛡️ Your Wellbeing Buddy")
st.markdown("### *Powered by A&P Phillips*")

BACKEND_URL = "https://animated-disco-7vqxw9vxr4j6fpw67-8000.app.github.dev"

# 1. DYNAMIC INJECTION (The "Key-In" Area)
with st.expander("⚙️ Mission Control (Key in your Rules here)"):
    # Load current files to the boxes
    t_val = open("Target.JASON").read() if os.path.exists("Target.JASON") else "{}"
    p_val = open("PROMPT").read() if os.path.exists("PROMPT") else ""
    
    new_t = st.text_area("Target.JASON", value=t_val, height=100)
    new_p = st.text_area("PROMPT Rules", value=p_val, height=100)
    
    if st.button("💾 SAVE RULES"):
        with open("Target.JASON", "w") as f: f.write(new_t)
        with open("PROMPT", "w") as f: f.write(new_p)
        st.success("Sovereign Files Updated.")

# 2. INGRESS
col1, col2 = st.columns(2)
with col1:
    st.subheader("📸 Senses")
    cam = st.camera_input("Scan")
with col2:
    st.subheader("🎙️ Intent")
    intent = st.text_area("What is the mission Simon?")
    
    if st.button("🚀 TRIGGER 90-STEP AUDIT"):
        with open("./VARIABLE/placeholder.txt", "w") as f: f.write(intent)
        with st.status("🧠 Phillips is Reasoning...", expanded=True):
            response = requests.post(f"{BACKEND_URL}/execute")
            time.sleep(1) # Institutional delay
        st.info(response.json()['data'])

# 3. AGENT STATUS
if os.path.exists("TASK_LIST.json"):
    with open("TASK_LIST.json", "r") as f:
        tasks = json.load(f)['tasks']
    if tasks:
        st.divider()
        st.subheader("🤖 Agent Fulfillment")
        for t in tasks:
            st.success(f"Agent {t['agent']} is performing {t['action']}...")

# 4. ARTIFACT
if os.path.exists("DASHBOARD.md"):
    st.divider()
    with open("DASHBOARD.md", "r") as f: st.markdown(f.read())