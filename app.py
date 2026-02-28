import streamlit as st
import requests
import os
import json

st.set_page_config(page_title="🛡️ Wellbeing Buddy", layout="wide")

st.title("🛡️ Wellbeing Buddy")
st.markdown("### *Powered by Phillips via FastAPI*")

# 1. BACKEND HANDSHAKE
BACKEND_URL = "http://localhost:8000"
try:
    status_check = requests.get(f"{BACKEND_URL}/status").json()
    st.sidebar.success(f"🛡️ {status_check['status']}")
except:
    st.sidebar.error("⚠️ Backend: OFFLINE (Run main.py)")

# 2. VISUAL INGRESS (Senses)
col1, col2 = st.columns(2)

with col1:
    st.subheader("📸 Visual Ingress")
    camera_photo = st.camera_input("Scan Product / Take Selfie")
    if camera_photo:
        # Save to the exact VARIABLE path
        with open("./VARIABLE/input_image.jpg", "wb") as f:
            f.write(camera_photo.getbuffer())
        st.success("Senses Captured in VARIABLE folder.")

with col2:
    st.subheader("⚙️ 90-Step Execution")
    if st.button("🚀 TRIGGER SOVEREIGN AUDIT"):
        with st.spinner("Phillips is calculating Trajectory..."):
            try:
                # Call the FastAPI Brain
                response = requests.post(f"{BACKEND_URL}/execute")
                if response.status_code == 200:
                    result = response.json()
                    # SAFE CHECK for 'data' key to prevent KeyError
                    if 'data' in result:
                        st.info("### 👁️ ASI INSIGHT")
                        st.write(result['data'])
                    else:
                        st.warning(f"Response received but 'data' missing: {result}")
                else:
                    st.error(f"Server Error: {response.status_code}")
            except Exception as e:
                st.error(f"Connection Error: {e}")

# 3. THE ARTIFACT (Dashboard)
if os.path.exists("DASHBOARD.md"):
    st.divider()
    st.subheader("📊 Latest Sovereign Artifact")
    with open("DASHBOARD.md", "r") as f:
        st.markdown(f.read())