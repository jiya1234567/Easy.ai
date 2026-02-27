import streamlit as st
import requests
import os
import json

st.set_page_config(page_title="Wellbeing Buddy", layout="wide")

st.title("🛡️ Wellbeing Buddy")
st.markdown("### *Powered by Phillips via FastAPI*")

# 1. CHECK BACKEND STATUS
try:
    backend_check = requests.get("http://localhost:8000/status").json()
    st.sidebar.success(f"Backend: {backend_check['status']}")
except:
    st.sidebar.error("Backend: OFFLINE (Check main.py)")

# 2. UI COLUMNS
col1, col2 = st.columns(2)

with col1:
    st.subheader("📸 Visual Ingress")
    camera_photo = st.camera_input("Take Selfie/Scan")
    if camera_photo:
        with open("./VARIABLE/input_image.jpg", "wb") as f:
            f.write(camera_photo.getbuffer())
        st.success("Senses Captured.")

with col2:
    st.subheader("⚙️ 90-Step Execution")
    if st.button("🚀 TRIGGER SOVEREIGN AUDIT"):
        with st.spinner("FastAPI is calculating Trajectory..."):
            # This calls the FastAPI server we built above
            response = requests.post("http://localhost:8000/execute")
            if response.status_code == 200:
                result = response.json()
                st.write(result['data'])
            else:
                st.error("Audit Failed. Check Kernel Environment Variables.")

# 3. SHOW DASHBOARD
if os.path.exists("DASHBOARD.md"):
    st.divider()
    with open("DASHBOARD.md", "r") as f:
        st.markdown(f.read())