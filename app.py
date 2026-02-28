import streamlit as st
import requests
import os
import json
import time

st.set_page_config(page_title="🛡️ Wellbeing Buddy", layout="wide")

st.title("🛡️ Wellbeing Buddy")
st.markdown("### *Powered by A&P Phillips via FastAPI*")

# 1. THE INSTITUTIONAL GATEWAY
BACKEND_URL = "https://animated-disco-7vqxw9vxr4j6fpw67-8000.app.github.dev"

# 2. INGRESS LAYER (Senses + Intent)
col1, col2 = st.columns(2)

with col1:
    st.subheader("📸 Visual Ingress")
    camera_photo = st.camera_input("Scan Product / Take Selfie")
    if camera_photo:
        with open("./VARIABLE/input_image.jpg", "wb") as f:
            f.write(camera_photo.getbuffer())
        st.success("Senses Logged.")

with col2:
    st.subheader("🎙️ Intent Ingress (The Mission)")
    user_intent = st.text_area("What is your question Simon?", 
                                placeholder="e.g. 'Sell my stock and book a doctor checkup.'")

    if st.button("🚀 TRIGGER 90-STEP AUDIT"):
        # Save Intent to Variable Text
        with open("./VARIABLE/placeholder.txt", "w") as f:
            f.write(user_intent)
            
        with st.spinner("Phillips Reasoning Engine..."):
            response = requests.post(f"{BACKEND_URL}/execute")
            if response.status_code == 200:
                st.info("### 👁️ ASI INSIGHT")
                st.write(response.json()['data'])
                
                # --- AGENT FULFILLMENT DISPLAY ---
                if os.path.exists("TASK_LIST.json"):
                    st.divider()
                    st.subheader("🤖 Agent Fulfillment (The Hands)")
                    with open("TASK_LIST.json", "r") as f:
                        plan = json.load(f)
                    
                    for task in plan['tasks']:
                        with st.status(f"Executing: {task['agent']}...", expanded=True):
                            st.write(f"Action: {task['action']} {task['target']}")
                            time.sleep(1.5) # Simulating API Fulfillment
                            st.success(f"SUCCESS: {task['agent']} completed mission.")

# 3. THE AUDIT TRAIL
if os.path.exists("DASHBOARD.md"):
    st.divider()
    st.subheader("📊 Sovereign Artifact: DASHBOARD.md")
    with open("DASHBOARD.md", "r") as f:
        st.markdown(f.read())