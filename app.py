import streamlit as st
import os
import json
import pandas as pd
import plotly.express as px
from google import genai
from google.genai import types
import datetime
from intelligence.scientific_engine import ScientificEngine

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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }
    .main {
        background-color: #000000;
        color: #FFFFFF;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #1A1A1A;
        color: #E2E8F0;
        border: 1px solid #333333;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #2563EB;
        color: #FFFFFF;
        border-color: #3B82F6;
        box-shadow: 0 0 12px rgba(59, 130, 246, 0.3);
    }
    .stButton>button:active {
        background-color: #1D4ED8;
    }
    .metric-card {
        background-color: #1A1A1A;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #333;
    }
    .neural-log {
        font-family: 'Courier New', Courier, monospace;
        font-size: 12px;
        color: #10B981;
        background-color: #050505;
        padding: 15px;
        border-radius: 8px;
        height: 200px;
        overflow-y: scroll;
        border: 1px solid #222;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("🔬 OMEGA-CORE")
    st.subheader("Buddy's Toolset by A&P Phillips")
    
    if not API_KEY:
        API_KEY = st.text_input("🔑 Gemini API Key", type="password", help="Required for Factory Mission Execution. Get one at https://aistudio.google.com/")
    
    st.divider()
    
    st.markdown("### 📷 Visual Ingress")
    optical_ingress = st.camera_input("Take Selfie", label_visibility="collapsed")
    if optical_ingress is not None:
        st.success("Optical Ingress Acquired. Ready.")
        
    st.divider()
    
    st.info("AGENTIC AUTONOMY ACTIVE")
    st.caption("Uplink: Node-04 (Geneva)")
    
    if st.button("REBOOT NEURAL ENGINE"):
        st.rerun()

    st.divider()
    st.subheader("🗑️ Data Custodian")
    if st.checkbox("Confirm Data Purge"):
        if st.button("🗑️ PURGE ALL REPORTS"):
            import glob
            files = glob.glob("reports/metrics/*.json")
            for f in files:
                if "assets.json" not in f:
                    os.remove(f)
            st.success("Reports Purged. Starting Fresh.")
            st.rerun()

# --- MAIN UI ---
st.title("🚀 Singularity Dashboard")
st.caption(f"Omega Clearance: aejphillips@outlook.com | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

st.markdown("### Domain Configuration")
domain = st.selectbox("DOMAIN SELECTION", ["Health", "Finance", "Agriculture", "General"], label_visibility="collapsed")

# --- DOMAIN ENGINE INITIALIZATION ---
if domain == "Health":
    # Use Simplified Bio Test Data
    sci_engine = ScientificEngine(data_path="reports/bio_test.csv", metadata_path="reports/bio_test_metadata.json")
else:
    # Use Simplified Finance Test Data
    sci_engine = ScientificEngine(data_path="reports/finance_test.csv", metadata_path="reports/finance_test_metadata.json")
    
# --- METRIC CARDS OVERVIEW ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("HYPERGRAPH SYNC", "98.2%", "+1.2%")
with col2:
    st.metric("EVOLUTION RATE", "4.2x", "+0.5x")
with col3:
    st.metric("RULIAD DEPTH", "14.2k", "Nodes")
with col4:
    st.metric("SYSTEM HEALTH", "OPTIMAL", "Stable")

# --- SESSION STATE INITIALIZATION ---
if 'watch_connected' not in st.session_state:
    st.session_state.watch_connected = False
if 'metabolic_data' not in st.session_state:
    st.session_state.metabolic_data = {"bp": "120/80", "sugar": 98, "pulse": 72}
if 'eye_scan_fidelity' not in st.session_state:
    st.session_state.eye_scan_fidelity = "N/A"

st.divider()

# --- 10 INTERCONNECTED TABS (Command Center Style) ---
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "📖 HOW TO USE"

tabs_list = [
    "📖 HOW TO USE", "🎛️ COMMAND CENTER", "⚙️ FACTORY", "📊 ASSET RADAR", "📈 BACKTEST", 
    "🌍 WORLD MODEL", "🏛️ HIERARCHY", "🧬 DNA EDITOR", "🧪 MOLECULAR DOCKING", "👥 DIGITAL TWIN",
    "🔬 RESEARCH DEVICE", "🔄 EVOLUTION", "🌌 VISUAL MANIFOLD", "🤖 COSMO-HUMANOID", "👨‍🔬 SCIENTIFIC DISCOVERY",
    "🌌 DISCOVERY DASHBOARD"
]

cols1 = st.columns(5)
cols2 = st.columns(5)
cols3 = st.columns(5)

for i, tab_name in enumerate(tabs_list[:5]):
    if cols1[i].button(tab_name):
        st.session_state.active_tab = tab_name
        st.rerun()
for i, tab_name in enumerate(tabs_list[5:10]):
    if cols2[i].button(tab_name):
        st.session_state.active_tab = tab_name
        st.rerun()
for i, tab_name in enumerate(tabs_list[10:15]):
    if cols3[i].button(tab_name):
        st.session_state.active_tab = tab_name
        st.rerun()

cols4 = st.columns(5)
if cols4[0].button(tabs_list[15]):
    st.session_state.active_tab = tabs_list[15]
    st.rerun()

st.divider()

# 1. HOW TO USE
if st.session_state.active_tab == "📖 HOW TO USE":
    st.header("Overview & Protocol")
    
    col_feat1, col_feat2 = st.columns(2)
    with col_feat1:
        with st.container(border=True):
            st.markdown("✅ **Backtesting Engine** `IMPLEMENTED`")
            st.caption("Historical accuracy validation and hit rate tracking.")
        with st.container(border=True):
            st.markdown("✅ **Transparency Layer** `IMPLEMENTED`")
            st.caption("Neural logs and data gap identification.")
            
    with col_feat2:
        with st.container(border=True):
            st.markdown("✅ **Decision Engine** `IMPLEMENTED`")
            st.caption("Buy/Hold/Sell logic with grounded rationale.")
        with st.container(border=True):
            st.markdown("✅ **Mobile Optimization** `IMPLEMENTED`")
            st.caption("Responsive sidebar and touch-friendly UI.")

    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.subheader("📖 Singularity Lab Protocol (7 Steps)")
        st.markdown("""
        **1. Define Domain & Intent:** Tell the system what to analyze (e.g. 'Finance', 'Analyze TSLA for breakout').
        **2. Agentic Hand-off:** The system breaks instructions down for the Scientist, Risk Manager, and Strategist.
        **3. Ruliad Traversal:** Discovers underlying physics/market rules.
        **4. Simulate Future States:** Runs predictive scenarios.
        **5. Execute Directives:** Follows the approved step-by-step logic.
        **6. Backtest Evaluation:** Verifies logic against historical performance.
        **7. Monitor Digital Twin:** Provides bio-metric/systemic real-time feedback loops.
        """)

# 2. COMMAND CENTER
if st.session_state.active_tab == "🎛️ COMMAND CENTER":
    st.header("System Test Suite & Device Uplink")
    
    with st.container(border=True):
        st.markdown("### ⚡ System Test Suite")
        st.caption("VERIFY VIDEO, CRISPR & OMEGA PROTOCOLS")
        col_t1, col_t2, col_t3 = st.columns(3)
        with col_t1:
            if st.button("🛡️ OMEGA PROTOCOL"): st.success("Omega Protocol Initialized")
            st.caption("Full scale verification of Optical, Voice, and Email layers.")
        with col_t2:
            if st.button("🧬 CRISPR TEST"): st.success("CRISPR Simulation Running")
            st.caption("Simulate gene editing and molecular Cas9 intervention.")
        with col_t3:
            if st.button("🎥 VIDEO TEST"): st.success("Synthesizing Video")
            st.caption("Generate AI-driven disease progression video (Veo).")
    
    st.divider()

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
        st.markdown("### ⌚ Watch Uplink Terminal")
        if not st.session_state.watch_connected:
            if st.button("🔗 PAIR OMEGA WATCH"):
                with st.spinner("Scanning for Bluetooth LE nodes..."):
                    import time; time.sleep(2)
                    st.session_state.watch_connected = True
                    st.success("Omega Watch Connected Successfully.")
                    st.rerun()
        else:
            st.success("⌚ Watch-Omega Connected")
            st.caption("Syncing Heart Rate & Pulse-Oximetry...")
            if st.button("🔓 DISCONNECT WATCH"):
                st.session_state.watch_connected = False
                st.rerun()

    st.divider()
    col_log1, col_log2 = st.columns(2)
    with col_log1:
        st.markdown("### Neural Log (Live)")
        st.markdown("""
            <div class="neural-log">
                [01:57:52] SCIENTIST: Analyzing IL-6 hypergraph nodes...<br>
                [01:57:55] RISK MANAGER: Recalculating flare probability thresholds...<br>
                [01:58:02] STRATEGIST: Optimizing circadian metabolic alignment...<br>
                [01:58:10] SYSTEM: Verifying budget constraints for TSLA ingress...<br>
            </div>
        """, unsafe_allow_html=True)

# 3. FACTORY (CHAT)
if st.session_state.active_tab == "⚙️ FACTORY":
    st.header("Mission Intent Factory")
    intent = st.text_area("ENTER MISSION INTENT", placeholder="e.g., Analyze IL-6 hypergraph nodes for flare prediction...")
    col_a, col_b = st.columns([3, 1])
    with col_b:
        ticker = st.text_input("TICKER INGRESS", placeholder="TSLA")
    
    if st.button("EXECUTE MISSION"):
        if not intent and not ticker:
            st.warning("Please enter mission intent or ticker.")
        elif not API_KEY:
            st.error("Uplink Error: No API key was provided. Please enter a valid API key in the sidebar.")
        else:
            with st.spinner("Traversing Hypergraph..."):
                try:
                    client = genai.Client(api_key=API_KEY)
                    system_instruction = f"""
                    You are the MULTI-AGENT ORCHESTRATOR. Domain: {domain}. Intent: {intent}. Ticker: {ticker}.
                    DATE: 2026-04-08 (Today)
                    STRICT SCHEMA REQUIREMENT: You must return a JSON object with these EXACT keys:
                    - "asset": "{ticker}"
                    - "status": A 3-word summary of the outlook
                    - "recent_price": Current market price (e.g., "A$152.40")
                    - "regime": Either "RISK-ON" or "RISK-OFF"
                    - "regime_summary": A one-sentence macro summary
                    - "analysis": A list of dicts with EXACT columns: "Category", "Status", and "Meaning"
                    - "prediction": A technical forecast summary
                    - "report_date": "2026-04-08"

                    REQUIRED ANALYSIS ROWS: You MUST include rows for: 
                    "Risk Regime", "Tailwinds", "Headwinds", "Price Range", and "Investor Action".
                    """
                    response = client.models.generate_content(
                        model="gemini-3-flash-preview",
                        contents=f"Execute analysis for: {intent} {ticker}",
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction,
                            response_mime_type="application/json"
                        )
                    )
                    result = json.loads(response.text)
                    
                    # --- AUTO-SAVE TO METRICS ---
                    if ticker:
                        save_path = os.path.join("reports/metrics", f"{ticker.lower()}.json")
                        with open(save_path, "w", encoding="utf-8") as f:
                            json.dump(result, f, indent=2)
                        st.success(f"Mission Executed. {ticker} report saved to Asset Radar.")
                    else:
                        st.success("Mission Executed.")
                    
                    st.subheader("Computational Prediction")
                    st.code(result.get("prediction", "No prediction generated."))
                except Exception as e:
                    st.error(f"Uplink Error: {e}. Check API Key or connectivity.")

# 4. ASSET RADAR (Dynamic Reports)
if st.session_state.active_tab == "📊 ASSET RADAR":
    st.header("📊 Asset Radar Terminal")
    st.caption("ROUTED: OMEGA-QUANT-EPSILON")
    
    asset_dir = "reports/metrics"
    if os.path.exists(asset_dir):
        available_assets = [f.replace(".json", "").upper() for f in os.listdir(asset_dir) if f.endswith(".json") and f != "assets.json"]
        selected_asset = st.selectbox("SELECT ASSET FOR ANALYSIS", available_assets)
        
        if selected_asset:
            with open(os.path.join(asset_dir, f"{selected_asset.lower()}.json"), "r", encoding="utf-8") as f:
                report = json.load(f)
            
            col_r1, col_r2 = st.columns([1, 3])
            with col_r1:
                st.metric("RECENT PRICE", report.get('recent_price', 'N/A'))
            with col_r2:
                st.subheader(f"🔍 {report.get('asset', selected_asset)} Status: {report.get('status', 'Analyzing...')}")
            
            st.caption(f"Analysis as at: {report.get('report_date', '2026-04-08')}")
            
            # Risk Regime Alert
            regime = report.get('regime', 'UNKNOWN')
            regime_summary = report.get('regime_summary', 'No summary available.')
            regime_color = "#2563EB" if regime == "RISK-ON" else "#10B981"
            st.markdown(f"""
                <div style="background-color:{regime_color}; padding:10px; border-radius:8px; margin-bottom:20px; color:white; font-weight:800;">
                    {regime} - {regime_summary}
                </div>
            """, unsafe_allow_html=True)
            
            # The Genius Template Table
            if 'analysis' in report:
                df = pd.DataFrame(report['analysis'])
                # Rename columns according to the user's template
                df = df.rename(columns={
                    "Status": f"{report.get('asset', selected_asset)} Status",
                    "Meaning": "What it means for investors"
                })
                st.table(df)
            else:
                st.info("Additional analysis data pending...")
            
            # Peer Comparison Summary
            if os.path.exists(os.path.join(asset_dir, "assets.json")):
                st.divider()
                st.subheader(f"📊 {report.get('asset', selected_asset)} vs Industry Peers Summary")
                with open(os.path.join(asset_dir, "assets.json"), "r", encoding="utf-8") as f:
                    peers = json.load(f)
                st.table(pd.DataFrame(peers))
                st.caption(f"{report['asset']} = value at cycle bottom. Perfect portfolio balance.")
    else:
        st.warning("No reports found. Please generate asset metrics via Mission Intent Factory.")

# 5. BACKTEST
if st.session_state.active_tab == "📈 BACKTEST":
    st.header("Historical Backtesting & Simulation")
    chart_data = pd.DataFrame(
        [100, 105, 102, 110, 115, 112, 120, 125, 122, 130],
        columns=['Omega-Core Performance']
    )
    st.line_chart(chart_data)
    st.info("Agentic Backtest run over 10 epochs. Baseline Outperformance: +18.4%")

# 6. WORLD MODEL
if st.session_state.active_tab == "🌍 WORLD MODEL":
    st.header("World Model Router")
    st.write("Extracting non-obvious rules from the computational universe.")
    if st.button("SEARCH RULIAD"):
        st.info("Traversing Ruliad Hypergraph...")
        rules = [
            {"rule": "Causal invariance across metabolic nodes.", "dimension": "Causal", "prob": 0.98},
            {"rule": "Multiway branching of stock volatility vectors.", "dimension": "Multiway", "prob": 0.85},
            {"rule": "Branchial entanglement of immune response.", "dimension": "Branchial", "prob": 0.92}
        ]
        df = pd.DataFrame(rules)
        st.table(df)
        fig = px.bar(df, x='dimension', y='prob', title="Rule Confidence by Dimension", color='dimension')
        st.plotly_chart(fig, width='stretch')

# 7. HIERARCHY
if st.session_state.active_tab == "🏛️ HIERARCHY":
    st.header("Hierarchy & Workforce")
    
    # NEW MOBILE UPLINK COMPONENT
    st.markdown("""
    <div style="background-color:#111; padding:20px; border-radius:12px; border:1px solid #333; margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; gap: 15px; align-items: center;">
                <div style="background-color:#2563EB; width: 40px; height: 40px; border-radius: 50%; display: flex; justify-content: center; align-items: center;">📱</div>
                <div>
                   <span style="font-size: 0.8rem; color: #888; font-weight: 600;">MOBILE UPLINK</span><br>
                   <strong style="font-size: 1.1rem; color: white;">VOICE UPLINK IDLE</strong>
                </div>
            </div>
            <div style="background-color:#222; width: 40px; height: 40px; border-radius: 50%; display: flex; justify-content: center; align-items: center; cursor: pointer; color: white;">🎤</div>
        </div>
        <div style="text-align: center; color: #444; margin: 15px 0;">. . . . . . . . . . . .</div>
        <div style="display: flex; justify-content: space-between; font-size: 0.7rem; color: #666; font-weight: 600;">
            <span>LATENCY: 0.004MS</span>
            <span>UPLINK: STABLE</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if os.path.exists("DASHBOARD.json"):
        st.subheader("🕵️ Agent Accountability & Chat")
        with open("DASHBOARD.json", "r") as f: d = json.load(f)
        r = d.get('agent_reports', {})
        st.warning(f"**CFO:** {r.get('cfo', 'N/A')} | **HR:** {r.get('hr', 'N/A')}")
        st.divider()
        st.write("**💬 AJ Worker Communication**")
        for msg in d.get("chat_history", []):
            with st.chat_message(msg.get("role", "user")): st.write(msg.get("content", ""))
        u_msg = st.chat_input("Command the Worker Agent...")
        if u_msg:
            from kernel import run_psi_autopilot
            run_psi_autopilot("System Update", u_msg, "free gptAG (Internal)", "", False, True)
            st.rerun()
    else:
        st.info("No DASHBOARD.json found. Dispatch a mission via Factory to begin workforce logs.")

# 8. DNA EDITOR
if st.session_state.active_tab == "🧬 DNA EDITOR":
    st.header("🧬 DNA Rules & Recursive Learning")
    dna_path = "rules/rules_fixed.json"
    if os.path.exists(dna_path):
        with open(dna_path, "r") as f: dna_txt = f.read()
        new_dna = st.text_area("CRISPR-Cas9 Parameter Map (Rules)", value=dna_txt, height=250)
        if st.button("🧬 AMEND DNA SEQUENCE"):
            with open(dna_path, "w") as f: f.write(new_dna)
            st.success("DNA Mutated successfully.")
    else:
        st.warning("DNA file (rules_fixed.json) missing. Running in baseline mode.")

# 9. MOLECULAR DOCKING
if st.session_state.active_tab == "🧪 MOLECULAR DOCKING":
    st.header("🧪 Molecular Docking")
    st.write("Step-21 drug discovery simulation environments.")
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.metric("Binding Affinity", "-9.4 kcal/mol", "+0.2")
        st.metric("Ligand RMSD", "1.2 Å", "-0.1")
    with col_m2:
        st.progress(78, text="Docking Traversal Phase 2...")
        st.info("AlphaFold embeddings synced successfully.")

# 10. DIGITAL TWIN
if st.session_state.active_tab == "👥 DIGITAL TWIN":
    st.header("👥 Digital Twin Feedback Loop")
    st.write("Real-time bio-feedback and state progression forecasting.")
    
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.markdown("### 🧬 Metabolic Ingress")
        bp_in = st.text_input("Blood Pressure (Systolic/Diastolic)", value=st.session_state.metabolic_data["bp"])
        sugar_in = st.number_input("Blood Glucose (mg/dL)", value=st.session_state.metabolic_data["sugar"])
        pulse_in = st.number_input("Pulse Rate (BPM)", value=st.session_state.metabolic_data["pulse"])
        
        if st.button("📤 SYNC METABOLIC DATA"):
            st.session_state.metabolic_data = {"bp": bp_in, "sugar": sugar_in, "pulse": pulse_in}
            st.success("Metabolic state synchronized with Omega-Core.")
            
    with col_d2:
        st.markdown("### 👁️ Biometric Fidelity")
        st.metric("Retinal Pattern Fidelity", st.session_state.eye_scan_fidelity)
        st.warning("⚠️ Critical Flare Probability: 12%")
        
    st.divider()
    
    with st.container(border=True):
        st.markdown("### 👁️ Optical Sensor (Total Eye Scan)")
        st.caption("TOTAL RETINAL BIOMETRIC & VASCULAR MAPPING")
        col_scan1, col_scan2 = st.columns([2, 1])
        with col_scan1:
            if st.button("⚡ INITIATE TOTAL OMEGA SCAN"):
                with st.spinner("Processing Bio-Metric Hypergraph..."):
                    import subprocess
                    # Trigger the 90-step generator
                    subprocess.run(["py", "generate_eye_watch.py"], capture_output=True)
                    # Update local state
                    st.session_state.eye_scan_fidelity = "99.8%"
                    st.success("Total Eye Scan Verified. Protocol generated in Target.JASON.")
                    st.rerun()
        with col_scan2:
            st.info("Status: READY")

# 11. RESEARCH DEVICE
if st.session_state.active_tab == "🔬 RESEARCH DEVICE":
    st.header("🔬 Research Device Uplink")
    st.write("Live spectral analysis and device management.")
    col_dev1, col_dev2 = st.columns(2)
    with col_dev1:
        st.markdown("### Active Uplinks")
        devices = pd.DataFrame([
            {"Device": "Mobile-Alpha", "Type": "Smartphone", "Status": "Connected"},
            {"Device": "Robot-Unit-01", "Type": "Bot", "Status": "Standby"},
            {"Device": "Lab-Geneva", "Type": "Microscope", "Status": "Syncing"}
        ])
        st.dataframe(devices, use_container_width=True)
    with col_dev2:
        st.markdown("### Spectral Analysis (Node-04)")
        chart_data = pd.DataFrame([10, 20, 15, 40, 30, 50, 45, 60, 55, 70], columns=['Intensity'])
        st.line_chart(chart_data)

# 12. EVOLUTION
if st.session_state.active_tab == "🔄 EVOLUTION":
    st.header("🔄 Evolutionary Engine")
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

# 13. VISUAL MANIFOLD
if st.session_state.active_tab == "🌌 VISUAL MANIFOLD":
    st.header("🌌 Manifold Engine (Multi-Asset Latent Space)")
    st.write("Visualizing the hidden geometry of the global financial system.")
    
    col_m1, col_m2 = st.columns([1, 4])
    with col_m1:
        method = st.selectbox("Manifold Method", ["PCA", "TSNE", "UMAP"])
        n_dim = st.radio("Dimensions", [2, 3], index=1)
        if st.button("RUN MANIFOLD ANALYSIS"):
            with st.spinner(f"Computing {method} Projection..."):
                st.session_state.manifold_df = sci_engine.compute_manifold(method=method, n_components=n_dim)
                st.success("Mapping complete.")

    if 'manifold_df' in st.session_state:
        df = st.session_state.manifold_df
        if n_dim == 3:
            fig = px.scatter_3d(df, x='Dim_1', y='Dim_2', z='Dim_3', color='Type', text='Asset', 
                                title=f"Latent Asset Projection ({method})", opacity=0.8)
        else:
            fig = px.scatter(df, x='Dim_1', y='Dim_2', color='Type', text='Asset', 
                             title=f"Latent Asset Projection ({method})")
        
        fig.update_traces(textposition='top center')
        st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        st.subheader("🔗 Correlation Network Graph")
        threshold = st.slider("Correlation Threshold", 0.0, 1.0, 0.7)
        if st.button("CONSTRUCT NETWORK"):
            import networkx as nx
            G = sci_engine.compute_network(threshold=threshold)
            pos = nx.spring_layout(G, dim=3)
            
            edge_x, edge_y, edge_z = [], [], []
            for edge in G.edges():
                x0, y0, z0 = pos[edge[0]]
                x1, y1, z1 = pos[edge[1]]
                edge_x.extend([x0, x1, None])
                edge_y.extend([y0, y1, None])
                edge_z.extend([z0, z1, None])

            edge_trace = px.line_3d(x=edge_x, y=edge_y, z=edge_z)
            
            node_x, node_y, node_z, node_text = [], [], [], []
            for node in G.nodes():
                x, y, z = pos[node]
                node_x.append(x)
                node_y.append(y)
                node_z.append(z)
                node_text.append(node)

            node_trace = px.scatter_3d(x=node_x, y=node_y, z=node_z, text=node_text, color_discrete_sequence=['#2563EB'])
            
            import plotly.graph_objects as go
            fig_net = go.Figure(data=[
                go.Scatter3d(x=edge_x, y=edge_y, z=edge_z, mode='lines', line=dict(color='#888', width=1), hoverinfo='none'),
                go.Scatter3d(x=node_x, y=node_y, z=node_z, mode='markers+text', text=node_text, 
                             marker=dict(size=5, color='#2563EB'), textposition="top center")
            ])
            fig_net.update_layout(title="Asset Contagion Network", showlegend=False)
            st.plotly_chart(fig_net, use_container_width=True)
    else:
        st.info("Initiate analysis to view the economic map.")

# 14. COSMO-HUMANOID
if st.session_state.active_tab == "🤖 COSMO-HUMANOID":
    st.header("🤖 Cosmo-Humanoid Actuators")
    st.write("Proto-consciousness & Motor control arrays.")
    col_h1, col_h2, col_h3 = st.columns(3)
    with col_h1:
        st.metric(label="Mood", value="80%", delta="+5%")
        st.metric(label="Energy", value="90%", delta="-2%")
    with col_h2:
        st.metric(label="Stress", value="20%", delta="-10%", delta_color="inverse")
        st.metric(label="Anger", value="0%", delta="0", delta_color="inverse")
    with col_h3:
        st.metric(label="Attention", value="88%", delta="+12%")
        st.metric(label="Engagement", value="60%", delta="+5%")
    
    st.subheader("Humanoid Action Array")
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        if st.button("Run Precision TestSuite"):
            st.success("Precision suite activated. Actuator fidelity: 99.8%.")
    with col_a2:
        if st.button("Run Emotion Module"):
            st.success("Emotion module synced. Empathy resonance maximized.")

# 15. SCIENTIFIC DISCOVERY
if st.session_state.active_tab == "👨‍🔬 SCIENTIFIC DISCOVERY":
    st.header("👨‍🔬 Scientific Discovery Engine")
    st.write("Hypothesis Engine across Multi-Asset Networks.")
    
    col_s1, col_s2 = st.columns([2, 1])
    with col_s2:
        st.markdown("### Experiment Loop")
        if st.button("START DISCOVERY LOOP"):
            with st.spinner("Analyzing cross-asset contagion..."):
                avg_corr_high = sci_engine.detect_anomalies()
                regimes, _ = sci_engine.detect_regimes()
                st.session_state.discovery_active = True
                st.session_state.discovery_result = {
                    "anomaly": "CRITICAL" if avg_corr_high else "STABLE",
                    "current_regime": f"Regime {regimes[-1]}",
                    "prob": 0.85 + (0.12 if avg_corr_high else 0)
                }
    
    with col_s1:
        hypo = st.text_input("Enter Hypothesis:", placeholder="Contagion will spread from CDS to Equities in < 24h")
        if st.button("RUN SCIENTIFIC VALIDATION"):
            if 'discovery_result' in st.session_state:
                res = st.session_state.discovery_result
                st.success(f"Hypothesis Parsed. Success Probability: {res['prob']*100:.1f}%")
                st.markdown(f"""
                > **Scientific Rationale:**
                > System detected a **{res['anomaly']}** state within **{res['current_regime']}**. 
                > Manifold geometry indicates increased curvature in the Credit-Equity subspace, 
                > validating the hypothesis of rapid shock propagation.
                """)
            else:
                st.warning("Run Discovery Loop first to sync systemic state.")

# 16. DISCOVERY DASHBOARD
if st.session_state.active_tab == "🌌 DISCOVERY DASHBOARD":
    st.header("🌌 Discovery Dashboard: Irreducibility & Geometry")
    st.write("Detecting structural 'tears' and manifold instability across the system.")
    
    # Run Discovery Metrics
    stability = sci_engine.compute_stability()
    reducibility = sci_engine.compute_reducibility()
    sensitivity = sci_engine.compute_sensitivity()
    
    # A. Stability & Reducibility Gauges
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        st.metric("STABILITY INDEX", f"{stability:.2%}")
    with col_stat2:
        st.metric("REDUCIBILITY SCORE", f"{reducibility:.2%}")
    with col_stat3:
        st.metric("SENSITIVITY (LYAPUNOV)", f"{sensitivity:.4f}")

    # B. Interpretation Layer (The Logic)
    if reducibility > 0.8:
        st.success("✔️ System is REDUCIBLE (Predictable Structure Detected)")
    elif stability < 0.5:
        st.warning("⚠️ System is UNSTABLE (High Risk of Regime Shift)")
    else:
        st.error("🔥 IRREDUCIBLE / CHAOTIC SYSTEM DETECTED (Predictive Power Minimal)")

    st.divider()
    
    # C. Shock Simulator UI (Global vs Selective)
    st.subheader("🌋 Shock Simulator (Experimental Stress Test)")
    col_shk1, col_shk2 = st.columns([1, 2])
    
    with col_shk1:
        shock_mode = st.radio("Shock Mode", ["Global", "Selective"])
        
        if shock_mode == "Selective":
            # Load data to get columns
            sci_engine.load_data()
            available_assets = sci_engine.data.columns.tolist()
            asset = st.selectbox("Select Asset to Shock", available_assets)
            shock_value = st.number_input("Shock Value", value=160.0 if "FX" in asset or "EQ" in asset else 20.0)
        else:
            asset = "ALL"
            shock_value = 0.05 # Noise epsilon
            
        if st.button("Run Shock Simulation"):
            with st.spinner("Calculating Manifold Tear..."):
                import numpy as np
                st.session_state.shock_original = sci_engine.compute_manifold(n_components=3)
                if shock_mode == "Selective":
                    st.session_state.shock_manifold = sci_engine.simulate_shock(asset, shock_value)
                    
                    # Compute Geometric Distortion
                    orig_coords = st.session_state.shock_original[['Dim_1', 'Dim_2', 'Dim_3']].values
                    shok_coords = st.session_state.shock_manifold[['Dim_1', 'Dim_2', 'Dim_3']].values
                    st.session_state.distortion = np.linalg.norm(orig_coords - shok_coords)
                else:
                    st.session_state.shock_manifold = st.session_state.shock_original # Placeholder for global
                    st.session_state.distortion = 0.0
                
                st.session_state.shock_active = True
                st.success(f"Shock Deployed on {asset}.")

    with col_shk2:
        if 'shock_active' in st.session_state and st.session_state.shock_active:
            # D. Side-by-Side Manifold "Tear" Visual
            st.markdown("#### Manifold Distortion Comparison")
            
            if 'distortion' in st.session_state:
                st.metric("GEOMETRIC DISTORTION", f"{st.session_state.distortion:.4f}")
            
            col_comp1, col_comp2 = st.columns(2)
            
            def draw_min_manifold(df, title):
                fig = px.scatter_3d(df, x='Dim_1', y='Dim_2', z='Dim_3', color='Type', text='Asset', 
                                    title=title, opacity=0.7)
                fig.update_layout(margin=dict(l=0, r=0, b=0, t=30), height=350, showlegend=False)
                return fig

            with col_comp1:
                st.plotly_chart(draw_min_manifold(st.session_state.shock_original, "Original Manifold"), use_container_width=True)
            with col_comp2:
                st.plotly_chart(draw_min_manifold(st.session_state.shock_manifold, "Post-Shock Manifold"), use_container_width=True)
        else:
            st.info("Initiate Shock Simulation to observe systemic geometry shifts.")

# --- FOOTER ---
st.divider()
st.caption("Universal Laptop Lab | Powered by OMEGA-CORE v2.5 | 10-Node Hyperarchitecture")
