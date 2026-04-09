import streamlit as st
import os
import json
import pandas as pd
import plotly.express as px
from google import genai
from google.genai import types
import datetime

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Buddy's Toolset by A&P Phillips | OMEGA-CORE",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load API Key
API_KEY = os.environ.get("GEMINI_API_KEY")

# --- STYLING ---
st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #1A1A1A;
        color: white;
        border: 1px solid #333;
    }
    .stButton>button:hover {
        background-color: #000;
        border: 1px solid #555;
    }
    .metric-card {
        background-color: #1A1A1A;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #333;
    }
    .neural-log {
        font-family: 'Courier New', Courier, monospace;
        font-size: 12px;
        color: #00FF00;
        background-color: #000;
        padding: 10px;
        border-radius: 5px;
        height: 200px;
        overflow-y: scroll;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("🔬 OMEGA-CORE")
    st.subheader("Buddy's Toolset by A&P Phillips")
    
    domain = st.selectbox("DOMAIN SELECTION", ["Health", "Finance", "Agriculture", "General"])
    
    st.divider()
    
    st.info("AGENTIC AUTONOMY ACTIVE")
    st.caption("Uplink: Node-04 (Geneva)")
    
    if st.button("REBOOT NEURAL ENGINE"):
        st.rerun()

# --- MAIN UI ---
st.title("🚀 Singularity Dashboard")
st.caption(f"Omega Clearance: aejphillips@outlook.com | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("HYPERGRAPH SYNC", "98.2%", "+1.2%")
with col2:
    st.metric("EVOLUTION RATE", "4.2x", "+0.5x")
with col3:
    st.metric("RULIAD DEPTH", "14.2k", "Nodes")
with col4:
    st.metric("SYSTEM HEALTH", "OPTIMAL", "Stable")

# --- TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["FACTORY (CHAT)", "WORLD MODEL", "RESEARCH DEVICE", "EVOLUTION"])

with tab1:
    st.header("Mission Intent Factory")
    
    intent = st.text_area("ENTER MISSION INTENT", placeholder="e.g., Analyze IL-6 hypergraph nodes for flare prediction...")
    
    col_a, col_b = st.columns([3, 1])
    with col_b:
        ticker = st.text_input("TICKER INGRESS", placeholder="TSLA")
    
    if st.button("EXECUTE MISSION"):
        if not intent and not ticker:
            st.warning("Please enter mission intent or ticker.")
        else:
            with st.spinner("Traversing Hypergraph..."):
                # Call Gemini
                client = genai.Client(api_key=API_KEY)
                
                system_instruction = f"You are the MULTI-AGENT ORCHESTRATOR. Domain: {domain}. Intent: {intent}. Ticker: {ticker}."
                
                try:
                    response = client.models.generate_content(
                        model="gemini-3-flash-preview",
                        contents=f"Execute: {intent} {ticker}",
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction,
                            response_mime_type="application/json"
                        )
                    )
                    result = json.loads(response.text)
                    
                    st.success("Mission Executed Successfully")
                    
                    st.subheader("Computational Prediction")
                    st.code(result.get("prediction", "No prediction generated."))
                    
                    st.subheader("Agent Reports")
                    rep_col1, rep_col2, rep_col3 = st.columns(3)
                    reports = result.get("agentReports", {})
                    with rep_col1:
                        st.markdown("**SCIENTIST**")
                        st.caption(reports.get("scientist", "N/A"))
                    with rep_col2:
                        st.markdown("**RISK MANAGER**")
                        st.caption(reports.get("riskManager", "N/A"))
                    with rep_col3:
                        st.markdown("**STRATEGIST**")
                        st.caption(reports.get("strategist", "N/A"))
                        
                except Exception as e:
                    st.error(f"Uplink Error: {e}")

with tab2:
    st.header("World Model Router")
    st.write("Extracting non-obvious rules from the computational universe.")
    
    if st.button("SEARCH RULIAD"):
        st.info("Traversing Ruliad Hypergraph...")
        # Mocking Ruliad Search for Streamlit Demo
        rules = [
            {"rule": "Causal invariance across metabolic nodes.", "dimension": "Causal", "prob": 0.98},
            {"rule": "Multiway branching of stock volatility vectors.", "dimension": "Multiway", "prob": 0.85},
            {"rule": "Branchial entanglement of immune response.", "dimension": "Branchial", "prob": 0.92}
        ]
        df = pd.DataFrame(rules)
        st.table(df)
        
        fig = px.bar(df, x='dimension', y='prob', title="Rule Confidence by Dimension", color='dimension')
        st.plotly_chart(fig, width='stretch')

with tab3:
    st.header("Research Device Uplink")
    st.write("Live spectral analysis and device management.")
    
    col_dev1, col_dev2 = st.columns(2)
    with col_dev1:
        st.markdown("### Active Uplinks")
        devices = pd.DataFrame([
            {"Device": "Mobile-Alpha", "Type": "Smartphone", "Status": "Connected"},
            {"Device": "Robot-Unit-01", "Type": "Bot", "Status": "Standby"},
            {"Device": "Lab-Geneva", "Type": "Microscope", "Status": "Syncing"}
        ])
        st.dataframe(devices, width='stretch')
    
    with col_dev2:
        st.markdown("### Spectral Analysis (Node-04)")
        # Simulate a spectral chart
        chart_data = pd.DataFrame(
            [10, 20, 15, 40, 30, 50, 45, 60, 55, 70],
            columns=['Intensity']
        )
        st.line_chart(chart_data)

with tab4:
    st.header("Evolutionary Engine")
    st.write("Recursive profile optimization and mutation logs.")
    
    st.progress(85, text="Singularity Alignment: 85%")
    
    st.subheader("Neural Log (Live)")
    st.markdown("""
        <div class="neural-log">
            [01:57:52] SCIENTIST: Analyzing IL-6 hypergraph nodes...<br>
            [01:57:55] RISK MANAGER: Recalculating flare probability thresholds...<br>
            [01:58:02] STRATEGIST: Optimizing circadian metabolic alignment...<br>
            [01:58:10] EVOLUTION ENGINE: Synthesizing Ruliad-v2 insights...<br>
            [01:58:15] SYSTEM: Verifying budget constraints for TSLA ingress...<br>
        </div>
    """, unsafe_allow_html=True)

# --- FOOTER ---
st.divider()
st.caption("Universal Laptop Lab | Powered by OMEGA-CORE v2.5")
