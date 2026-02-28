import streamlit as st
import requests
import os
import json
import time

st.set_page_config(page_title="🛡️ Wellbeing Buddy", layout="wide")
st.title("🛡️ Wellbeing Buddy")
st.markdown("### *Powered by A&P Phillips*")

BACKEND_URL = "https://animated-disco-7vqxw9vxr4j6fpw67-8000.app.github.dev"

col1, col2 = st.columns(2)

with col1:
    st.subheader("📸 Senses (Visual Ingress)")
    # FIXED: Added both Camera and File Upload support
    img_ingress = st.camera_input("Take Photo")
    file_ingress = st.file_uploader("Or Upload File (Video/Txt/Img)", type=['jpg','png','mp4','txt'])
    
    ingress_data = img_ingress or file_ingress
    if ingress_data:
        # Determine file type and save
        ext = "txt" if "text" in ingress_data.type else "jpg"
        with open(f"./VARIABLE/input_image.{ext}", "wb") as f:
            f.write(ingress_data.getbuffer())
        st.success(f"Ingress Captured: {ingress_data.name if hasattr(ingress_data, 'name') else 'Camera'}")

with col2:
    st.subheader("🎙️ Intent Ingress (The Mission)")
    user_intent = st.text_area("What is your question Simon?", key="intent_box")

    if st.button("🚀 TRIGGER 90-STEP AUDIT"):
        # Save prompt immediately to Variable Text
        with open("./VARIABLE/placeholder.txt", "w") as f:
            f.write(user_intent)
            
        with st.spinner("Phillips Reasoning Engine..."):
            response = requests.post(f"{BACKEND_URL}/execute")
            
        if response.status_code == 200:
            # --- SHOW DYNAMIC AGENT FULFILLMENT ---
            if os.path.exists("TASK_LIST.json"):
                st.divider()
                st.subheader("🤖 Agent Fulfillment (The Hands)")
                with open("TASK_LIST.json", "r") as f:
                    plan = json.load(f)
                
                if not plan['tasks']:
                    st.warning("No Agents Dispatched. Check Invariants.")
                
                for task in plan['tasks']:
                    # This is the "Dynamic Hands" loop
                    with st.status(f"Agent {task['agent']} active...", expanded=True):
                        st.write(f"Executing: {task['action']} for {task['target']}")
                        time.sleep(1.5) # Simulating Agency
                        st.success(f"COMPLETE: {task['target']} processed.")

# 3. FINAL ARTIFACT DISPLAY
if os.path.exists("DASHBOARD.md"):
    st.divider()
    st.subheader("📊 Latest Sovereign Artifact")
    with open("DASHBOARD.md", "r") as f:
        st.markdown(f.read())