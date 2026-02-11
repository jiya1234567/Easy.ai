import streamlit as st
import json
import time
import numpy as np
from PIL import Image

st.set_page_config(page_title="Tier-Ω ASI Dashboard", layout="wide", page_icon="🧠")

class UnifiedBioASI:
    def execute_25_step_loop(self, domain, script, is_synthetic):
        status = st.status("🧠 Running Cognitive Loop...", expanded=True)

        dish = script.get("dish_data", {}).get("macros", {})
        user = script.get("user_profile", {}).get("vitals", {})

        sodium = dish.get("sodium_mg", 0)
        bp = user.get("blood_pressure_systolic", 120)

        if is_synthetic:
            sodium += 500
            status.write("🧬 Synthetic stress applied")

        risk = int(((sodium / 2000) * 50) + ((bp / 135) * 50))

        if risk > 75:
            action = "MANDATORY_HYDRATION_TAKE"
            narrative = f"High metabolic risk detected. Sodium={sodium}mg."
        else:
            action = "NOMINAL_TRANSIT"
            narrative = f"System stable. Protein={dish.get('protein_g',0)}g."

        time.sleep(0.3)
        status.update(label="✅ Cognitive Loop Complete", state="complete")

        return {"risk": min(100, risk), "action": action, "narrative": narrative}

if "brain" not in st.session_state:
    st.session_state.brain = UnifiedBioASI()

with st.sidebar:
    active_domain = st.selectbox("Domain", ["Heart","Brain","Finance","Autoimmune","General"])
    use_synth = st.toggle("Stress Dream", True)

    default_json = {
        "dish_data":{"macros":{"protein_g":9.5,"sodium_mg":990}},
        "user_profile":{"vitals":{"blood_pressure_systolic":135}}
    }

    input_json = st.text_area("JSON Input", json.dumps(default_json,indent=2), height=250)

st.title("🧠 Tier-Ω ASI Dashboard")

image = st.camera_input("Capture")

if st.button("RUN"):
    pocket = json.loads(input_json)
    result = st.session_state.brain.execute_25_step_loop(active_domain,pocket,use_synth)
    st.metric("Risk",result["risk"])
    st.write(result["action"])
    st.write(result["narrative"])
    if image:
        st.image(image)
