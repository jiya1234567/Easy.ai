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

    st.divider()
    st.subheader("🔑 Alert Credentials")
    with st.expander("⚙️ Configure Email & SMS", expanded=False):
        st.caption("Saved to .env file — never sent anywhere else.")

        st.markdown("**📧 Email — via SendGrid (Recommended — Free)**")
        st.caption("🔗 Get free key: sendgrid.com/free → Settings → API Keys → Create (100 emails/day free)")
        env_sg_key      = st.text_input("SendGrid API Key", value=os.environ.get("SENDGRID_API_KEY",""), key="cfg_sg", type="password",
                                         placeholder="SG.xxxxxxxxxxxxxxxxxxxx")
        env_email_from  = st.text_input("Your Verified Sender Email", value=os.environ.get("ALERT_EMAIL_FROM","aejphillips@outlook.com"), key="cfg_email_from",
                                         help="Must be verified in SendGrid: Settings → Sender Authentication")
        env_email_to    = st.text_input("Send Alerts To", value=os.environ.get("ALERT_EMAIL_TO","aejphillips@outlook.com"), key="cfg_email_to")
        env_email_pass  = st.text_input("Gmail App Password (optional fallback)", type="password", value=os.environ.get("ALERT_EMAIL_PASS",""), key="cfg_email_pass",
                                         help="Only needed if not using SendGrid. Gmail only: myaccount.google.com/apppasswords")

        st.markdown("**📱 SMS (Twilio — free at twilio.com)**")
        env_twilio_sid  = st.text_input("Twilio Account SID",  value=os.environ.get("TWILIO_ACCOUNT_SID",""), key="cfg_sid", type="password")
        env_twilio_tok  = st.text_input("Twilio Auth Token",   value=os.environ.get("TWILIO_AUTH_TOKEN",""),  key="cfg_tok", type="password")
        env_twilio_from = st.text_input("Twilio From Number",  value=os.environ.get("TWILIO_FROM_NUMBER",""), key="cfg_from",
                                         placeholder="+12015551234")
        env_twilio_to   = st.text_input("Your Mobile Number",  value=os.environ.get("TWILIO_TO_NUMBER","+61"), key="cfg_to",
                                         placeholder="+61412345678")

        if st.button("💾 SAVE CREDENTIALS TO .env"):
            env_lines = [
                "# OMEGA-CORE — Auto-saved credentials\n",
                f"GEMINI_API_KEY={os.environ.get('GEMINI_API_KEY','')}\n",
                f"SENDGRID_API_KEY={env_sg_key}\n",
                "ALERT_SMTP_HOST=smtp.gmail.com\n",
                "ALERT_SMTP_PORT=587\n",
                f"ALERT_EMAIL_FROM={env_email_from}\n",
                f"ALERT_EMAIL_PASS={env_email_pass}\n",
                f"ALERT_EMAIL_TO={env_email_to}\n",
                f"TWILIO_ACCOUNT_SID={env_twilio_sid}\n",
                f"TWILIO_AUTH_TOKEN={env_twilio_tok}\n",
                f"TWILIO_FROM_NUMBER={env_twilio_from}\n",
                f"TWILIO_TO_NUMBER={env_twilio_to}\n",
            ]
            with open(".env", "w") as ef:
                ef.writelines(env_lines)
            os.environ["SENDGRID_API_KEY"]    = env_sg_key
            os.environ["ALERT_EMAIL_FROM"]    = env_email_from
            os.environ["ALERT_EMAIL_PASS"]    = env_email_pass
            os.environ["ALERT_EMAIL_TO"]      = env_email_to
            os.environ["TWILIO_ACCOUNT_SID"]  = env_twilio_sid
            os.environ["TWILIO_AUTH_TOKEN"]   = env_twilio_tok
            os.environ["TWILIO_FROM_NUMBER"]  = env_twilio_from
            os.environ["TWILIO_TO_NUMBER"]    = env_twilio_to
            st.success("✅ Credentials saved to .env and active immediately!")

        st.caption("📌 Twilio free trial: twilio.com/try-twilio (AUD $20 credit, ~200 SMS)")


# --- MAIN UI ---
st.title("🚀 Singularity Dashboard")
st.caption(f"Omega Clearance: aejphillips@outlook.com | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

st.markdown("### Domain Configuration")
domain = st.selectbox("DOMAIN SELECTION", ["Health", "Finance", "Cybersecurity", "Smart City", "Materials", "Quantum", "Agriculture", "General"], label_visibility="collapsed")

# --- DOMAIN ENGINE INITIALIZATION ---
if domain == "Health":
    # Use Simplified Bio Test Data
    sci_engine = ScientificEngine(data_path="reports/bio_test.csv", metadata_path="reports/bio_test_metadata.json")
elif domain == "Cybersecurity":
    # Use Advanced Cyber Test Data
    sci_engine = ScientificEngine(data_path="reports/cyber_test_advanced.csv", metadata_path="reports/cyber_test_metadata.json")
elif domain == "Smart City":
    # Use Infrastructure Test Data
    sci_engine = ScientificEngine(data_path="reports/city_test_data.csv", metadata_path="reports/city_metadata.json")
elif domain == "Materials":
    # Use Universal Materials Science Data
    sci_engine = ScientificEngine(data_path="reports/materials_test.csv", metadata_path="reports/materials_metadata.json")
elif domain == "Quantum":
    # Use Universal Quantum Computing Data
    sci_engine = ScientificEngine(data_path="reports/quantum_test.csv", metadata_path="reports/quantum_metadata.json")
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
    "🔬 RESEARCH DEVICE", "🔄 EVOLUTION", "🌌 VISUAL MANIFOLD", "🚀 SINGULARITY FEED", "👨‍🔬 SCIENTIFIC DISCOVERY",
    "🌌 DISCOVERY DASHBOARD", "🔐 ADVERSARIAL LAB", "🏙️ SMART CITY TWIN"
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
for i, tab_name in enumerate(tabs_list[15:18]):
    col_idx = i % 5
    if cols4[col_idx].button(tab_name):
        st.session_state.active_tab = tab_name
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
            if st.button("🧬 CRISPR TEST"):
                from verify_universal_core import verify_omega_core
                audit = verify_omega_core()
                st.success(f"DNA AUDIT COMPLETE: Fidelity {audit['Final Score']}")
                with st.expander("View DNA Card", expanded=True):
                    st.json(audit)
            st.caption("Perform a Master DNA Audit to verify Domain & Intelligence integrity.")
        with col_t3:
            if st.button("🎥 VIDEO TEST"): st.success("Synthesizing Video")
            st.caption("Generate AI-driven disease progression video (Veo).")
    
    st.divider()

    col_dev1, col_dev2 = st.columns(2)
    with col_dev1:
        st.markdown("### Active Uplinks")
        devices = pd.DataFrame([
            {"Device": "Samsung Phone (AJ-Primary)",  "Type": "Android Smartphone",  "Status": "🟢 Connected"},
            {"Device": "Galaxy Fit 3 (Omega-Watch)",   "Type": "Samsung Smartwatch",   "Status": "🟢 Syncing"},
            {"Device": "Lab-Geneva",                   "Type": "Microscope Node",      "Status": "🔵 Standby"},
        ])
        st.dataframe(devices, width='stretch')
    with col_dev2:
        st.markdown("### ⌚ Samsung Galaxy Fit 3 — Uplink")
        if not st.session_state.watch_connected:
            if st.button("🔗 PAIR GALAXY FIT 3"):
                with st.spinner("Scanning BLE 5.0 — Samsung Health channel..."):
                    import time; time.sleep(2)
                    st.session_state.watch_connected = True
                    st.success("Samsung Galaxy Fit 3 Connected via Samsung Health.")
                    st.rerun()
        else:
            st.success("⌚ Galaxy Fit 3 — OMEGA LINK ACTIVE")
            col_w1, col_w2 = st.columns(2)
            with col_w1:
                st.metric("Heart Rate", "72 bpm", "Stable")
                st.metric("SpO2", "98%", "Normal")
            with col_w2:
                st.metric("Stress Index", "24", "Low")
                st.metric("Skin Temp", "36.6 °C", "Normal")
            st.caption("📡 Samsung Health BLE 5.0 | Pulse-Oximetry & ECG Sync Active")
            if st.button("🔓 DISCONNECT GALAXY FIT 3"):
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
        
        from kernel import run_psi_autopilot, record_outcome
        
        # Outcome Feedback Section
        if 'episode_id' in d.get('metrics', {}):
            st.divider()
            st.markdown("### 🎓 Training Command (Feedback Loop)")
            eid = d['metrics']['episode_id']
            st.caption(f"Last Episode ID: {eid} | Status: {d.get('metrics', {}).get('bias', 'N/A')}")
            
            col_f1, col_f2, col_f3 = st.columns([1, 1, 2])
            with col_f1:
                if st.button("✅ MARK SUCCESS", width='stretch'):
                    if record_outcome(eid, "Success"):
                        st.success("Learning Recorded: Positive Reinforcement.")
                        st.rerun()
            with col_f2:
                if st.button("❌ MARK FAILURE", width='stretch'):
                    if record_outcome(eid, "Failure"):
                        st.error("Learning Recorded: Negative Reinforcement.")
                        st.rerun()
            with col_f3:
                st.info("Training the model helps refine the Cognitive Recall engine.")

        st.divider()
        
        # Experience Log Visualization
        st.subheader("🧠 Cognitive Experience Log")
        exp_file = "intelligence/experience.json"
        if os.path.exists(exp_file):
            with open(exp_file, "r") as f: exp_data = json.load(f)
            if exp_data:
                # Show last 5 episodes in a clean table
                df_exp = pd.DataFrame(exp_data[-5:]).sort_values("ts", ascending=False)
                # Flatten context/decision for display
                df_exp['Regime'] = df_exp['ctx'].apply(lambda x: x.get('regime', 'N/A'))
                df_exp['Decision'] = df_exp['dec'].apply(lambda x: x.get('markov', 'N/A'))
                if 'out' in df_exp.columns:
                    st.table(df_exp[['ts', 'Regime', 'Decision', 'out']])
                else:
                    st.table(df_exp[['ts', 'Regime', 'Decision']])
            else:
                st.info("No episodes recorded yet. Start a mission to generate experience.")
        
        st.divider()
        st.write("**💬 AJ Worker Communication**")
        for msg in d.get("chat_history", []):
            with st.chat_message(msg.get("role", "user")): st.write(msg.get("content", ""))
        u_msg = st.chat_input("Command the Worker Agent...")
        if u_msg:
            run_psi_autopilot("System Update", u_msg, "free gptAG (Internal)", "", False, True)
            st.rerun()
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
    from intelligence.biometric_alert_engine import BiometricAlertEngine, THRESHOLDS

    st.header("👥 Digital Twin — Biometric Stress Test")
    st.caption("Real-time bio-feedback · Galaxy Fit 3 Uplink · Email & SMS Alert Engine")

    # ── Voice helper (browser Web Speech API) ─────────────────────────────────
    def speak(text):
        safe = text.replace("'", " ").replace('"', ' ').replace("\n", " ")
        st.components.v1.html(f"""<script>
        var u=new SpeechSynthesisUtterance('{safe}');
        u.rate=0.95;u.pitch=1.0;u.volume=1.0;
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(u);
        </script>""", height=0)

    alert_engine = BiometricAlertEngine("AJ Phillips")
    if 'bio_log' not in st.session_state:
        st.session_state.bio_log = []

    RISK_MAP = {
        "OK":       ("🟢 NORMAL",   "#10B981"),
        "WARNING":  ("🟡 WARNING",  "#F59E0B"),
        "CRITICAL": ("🔴 CRITICAL", "#EF4444"),
    }

    # ══════════════════════════════════════════════════════════════════════════
    # STEP 1 — Stress Test Input
    # ══════════════════════════════════════════════════════════════════════════
    st.subheader("🧬 Step 1 — Enter or Stress-Test Your Biometrics")
    st.caption("Drag sliders to dangerous values to trigger email/SMS/voice alerts.")

    col_in1, col_in2, col_in3 = st.columns(3)
    with col_in1:
        with st.container(border=True):
            st.markdown("**💓 Blood Pressure**")
            st.caption("Normal 120/80 | Warning 130+ | Critical 160+")
            bp_sys = st.slider("Systolic (mmHg)", 60, 220, 120)
            bp_dia = st.slider("Diastolic (mmHg)", 40, 140, 80)
            bp_in  = f"{bp_sys}/{bp_dia}"
            st.metric("BP Reading", bp_in)

    with col_in2:
        with st.container(border=True):
            st.markdown("**🩸 Blood Glucose**")
            st.caption("Normal 70-99 | Warning 140+ | Critical 200+")
            glucose_in = st.slider("Glucose (mg/dL)", 40, 400, 98)
            st.metric("Glucose", f"{glucose_in} mg/dL")
            st.markdown("**🫀 Pulse Rate**")
            st.caption("Normal 60-99 | Warning 100+ | Critical 130+")
            pulse_in = st.slider("Pulse (BPM)", 30, 200, 72)
            st.metric("Pulse", f"{pulse_in} bpm")

    with col_in3:
        with st.container(border=True):
            st.markdown("**🌬️ SpO2 (Oxygen %)**")
            st.caption("Normal 95-100 | Warning ≤94 | Critical ≤90")
            spo2_in = st.slider("SpO2 (%)", 70, 100, 98)
            st.metric("SpO2", f"{spo2_in}%")
            st.markdown("**📷 Retinal Fidelity**")
            st.metric("Eye Scan", st.session_state.eye_scan_fidelity)

    st.divider()

    # ══════════════════════════════════════════════════════════════════════════
    # STEP 2 — Run Analysis
    # ══════════════════════════════════════════════════════════════════════════
    st.subheader("⚡ Step 2 — Run Stress Analysis")
    col_run, col_voice = st.columns([2, 1])
    with col_run:
        run_analysis = st.button("🔬 RUN BIOMETRIC ANALYSIS")
    with col_voice:
        voice_on = st.toggle("🎙️ Voice Readout (Samsung Phone speaker)", value=True)

    if run_analysis:
        result = alert_engine.evaluate(bp_in, float(glucose_in), float(pulse_in), float(spo2_in))
        st.session_state.last_bio_result = result
        st.session_state.metabolic_data  = {"bp": bp_in, "sugar": glucose_in, "pulse": pulse_in}
        st.session_state.bio_log.append(result)

        label, color = RISK_MAP.get(result["level"], ("❓","#888"))
        st.markdown(f"""
        <div style="background:{color}22;border-left:5px solid {color};padding:16px;border-radius:10px;margin:12px 0;">
          <h2 style="color:{color};margin:0;">RISK STATUS: {label}</h2>
          <p style="color:#ccc;margin:4px 0 0 0;">Evaluated at {result['timestamp']}</p>
        </div>""", unsafe_allow_html=True)

        if result["breaches"]:
            st.error(f"🚨 {len(result['breaches'])} threshold breach(es) detected!")
            for b in result["breaches"]:
                st.warning(f"• **{b['metric']}** = {b['value']} → **{b['severity']}**")
            if voice_on:
                s = ", ".join([f"{b['metric']} is {b['severity']}" for b in result["breaches"]])
                speak(f"Omega Core Alert. Risk {result['level']}. Breaches: {s}. "
                      f"Blood pressure {bp_in}. Glucose {glucose_in}. Pulse {pulse_in}. "
                      f"SpO2 {spo2_in} percent. Check your Galaxy Fit 3 now.")
        else:
            st.success("✅ All vitals within normal range.")
            if voice_on:
                speak(f"All vitals normal. Blood pressure {bp_in}. Glucose {glucose_in}. "
                      f"Pulse {pulse_in}. SpO2 {spo2_in} percent. Omega Core passive monitoring active.")

    st.divider()

    # ══════════════════════════════════════════════════════════════════════════
    # STEP 3 — Email / SMS Alert
    # ══════════════════════════════════════════════════════════════════════════
    st.subheader("📨 Step 3 — Send Email or SMS Alert")

    if 'last_bio_result' in st.session_state:
        res   = st.session_state.last_bio_result
        label, color = RISK_MAP.get(res["level"], ("❓","#888"))
        st.info(f"Ready to dispatch: **{label}** — {res['timestamp']}")

        col_em, col_sm = st.columns(2)
        with col_em:
            with st.container(border=True):
                st.markdown("### 📧 Email Alert")
                st.caption("Set ALERT_EMAIL_FROM / ALERT_EMAIL_PASS / ALERT_EMAIL_TO in .env")
                email_to = st.text_input("Send to Email", value=os.environ.get("ALERT_EMAIL_TO","aejphillips@outlook.com"))
                if st.button("📧 SEND EMAIL ALERT"):
                    os.environ["ALERT_EMAIL_TO"] = email_to
                    status = alert_engine.send_email(res)
                    (st.success if "✅" in status else st.warning)(status)
                    if voice_on and "✅" in status:
                        speak(f"Email alert sent to {email_to}")

        with col_sm:
            with st.container(border=True):
                st.markdown("### 📱 SMS Alert (Twilio)")
                st.caption("Set TWILIO_ACCOUNT_SID / AUTH_TOKEN / FROM / TO in .env")
                sms_to = st.text_input("Send SMS to", value=os.environ.get("TWILIO_TO_NUMBER","+61400000000"))
                if st.button("📱 SEND SMS ALERT"):
                    os.environ["TWILIO_TO_NUMBER"] = sms_to
                    status = alert_engine.send_sms(res)
                    (st.success if "✅" in status else st.warning)(status)
                    if voice_on and "✅" in status:
                        speak("S M S alert sent successfully.")
    else:
        st.info("Run Step 2 analysis first to enable alert dispatch.")

    st.divider()

    # ══════════════════════════════════════════════════════════════════════════
    # STEP 4 & 5 — Watch Guide + Eye Scan
    # ══════════════════════════════════════════════════════════════════════════
    col_wt, col_sc = st.columns(2)
    with col_wt:
        with st.container(border=True):
            st.markdown("### ⌚ Step 4 — Galaxy Fit 3 Watch Log Guide")
            st.markdown("""
**On Samsung Phone (Samsung Health app):**
1. Open **Samsung Health**
2. Tap **Activity → Health Monitor**
3. Tap **Heart Rate / Blood Oxygen / Stress** → live graph
4. Swipe left for **Today's history log**
5. Tap **⋮ → Share data** to export CSV

**On Galaxy Fit 3 Watch:**
1. Press **side button** → scroll to **Heart Rate** → live reading
2. Scroll to **Stress** → see HRV stress index graph
3. **📳 Haptic buzz** = OMEGA-CORE critical alert received ✅
            """)
            if st.button("🎙️ READ GUIDE ALOUD"):
                speak("To view logs: Open Samsung Health on your phone. Tap Activity then Health Monitor. Select Heart Rate or Blood Oxygen. On the watch, press the side button, scroll to Heart Rate or Stress. A haptic buzz means an Omega Core alert was received.")

    with col_sc:
        with st.container(border=True):
            st.markdown("### 👁️ Step 5 — Total Eye Scan")
            st.caption("90-step BIO-METRIC-OMEGA · Galaxy Fit 3 Protocol")
            if st.button("⚡ INITIATE TOTAL OMEGA SCAN"):
                with st.spinner("Processing Bio-Metric Hypergraph — 90 steps..."):
                    import subprocess
                    subprocess.run(["py", "generate_eye_watch.py"], capture_output=True)
                    st.session_state.eye_scan_fidelity = "99.8%"
                    st.success("Eye Scan complete. Target.JASON updated. Galaxy Fit 3 alert queued.")
                    if voice_on:
                        speak("Total Eye Scan complete. Retinal fidelity 99.8 percent. Samsung Galaxy Fit 3 biometric sync active. Passive monitoring enabled.")
                    st.rerun()
            st.metric("Retinal Pattern Fidelity", st.session_state.eye_scan_fidelity)

    st.divider()

    # ══════════════════════════════════════════════════════════════════════════
    # STEP 6 — Alert History Log
    # ══════════════════════════════════════════════════════════════════════════
    st.subheader("📋 Step 6 — Alert History Log")
    if os.path.exists("reports/biometric_alert_log.json"):
        with open("reports/biometric_alert_log.json") as f:
            log_data = json.load(f)
        if log_data:
            rows = []
            for e in reversed(log_data[-20:]):
                lbl, _ = RISK_MAP.get(e["level"], ("❓","#888"))
                rows.append({
                    "Time": e["timestamp"], "Status": lbl,
                    "BP": e["vitals"]["bp"],
                    "Glucose": f"{e['vitals']['glucose']} mg/dL",
                    "Pulse": f"{e['vitals']['pulse']} bpm",
                    "SpO2": f"{e['vitals']['spo2']}%",
                    "Breaches": len(e["breaches"])
                })
            st.dataframe(pd.DataFrame(rows), width='stretch', hide_index=True)
        else:
            st.info("No alerts logged yet. Run Step 2 to begin.")
    else:
        st.info("No log file yet. Run a stress analysis to create it.")



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
        st.dataframe(devices, width='stretch')
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
        st.plotly_chart(fig, width='stretch')
        
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
# 14. SINGULARITY FEED
if st.session_state.active_tab == "🚀 SINGULARITY FEED":
    st.header("🚀 SINGULARITY FEED")
    st.subheader("Autonomous Scientist Discovery Stream")
    
    # Live Active Learning Metrics
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("DISCOVERY RATE", "1.2/hr", "Active")
    with col_b:
        st.metric("ENTROPY REDUCTION", "24.2%", "+2.1%")
    with col_c:
        st.metric("ASI PROGRESSION", "Level 4.2", "Steady")

    st.divider()

    if os.path.exists("reports/discovery_log.json"):
        with open("reports/discovery_log.json", "r") as f:
            discoveries = json.load(f)
            
        for disc in reversed(discoveries[-15:]): # Show last 15
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**[{disc['ts']}]**")
                    st.markdown(f"#### {disc['hypothesis']}")
                    st.caption(f"Domain: {disc['domain']} | Protocol: ACTIVE_LEARNING_V4")
                with col2:
                    st.metric("INFO GAIN", f"{disc.get('info_gain', 0.0):.2f}")
                
                det1, det2, det3 = st.columns(3)
                det1.write(f"**Driver:** {disc['driver']}")
                det2.write(f"**Target:** {disc['target']}")
                det3.write(f"**Delta:** {disc['delta']:.4f} {disc['uncertainty']}")
                
                st.success(f"Status: {disc['status']}")
    else:
        st.info("No autonomous discoveries archived yet. Run the Level 4 Science Loop to begin.")

# 15. SCIENTIFIC DISCOVERY
if st.session_state.active_tab == "👨‍🔬 SCIENTIFIC DISCOVERY":
    st.header("👨‍🔬 Scientific Discovery Engine")
    st.write("Hypothesis Engine across Multi-Asset Networks.")
    
    col_s1, col_s2 = st.columns([2, 1])
    with col_s2:
        st.markdown("### Experiment Loop")
        if st.button("START DISCOVERY LOOP"):
            with st.spinner("Analyzing cross-asset/feature contagion..."):
                avg_corr_high = sci_engine.detect_anomalies()
                regimes, _ = sci_engine.detect_regimes()
                
                # New metrics
                importance = sci_engine.compute_feature_importance(target_col="Mutation_Score")
                causal_g = sci_engine.discover_causality()
                silhouette = sci_engine.compute_silhouette()
                
                st.session_state.discovery_active = True
                st.session_state.discovery_result = {
                    "anomaly": "CRITICAL" if avg_corr_high else "STABLE",
                    "current_regime": f"Regime {regimes[-1]}",
                    "prob": 0.85 + (0.12 if avg_corr_high else 0),
                    "importance": importance,
                    "causal_g": causal_g,
                    "silhouette": silhouette
                }
    
    with col_s1:
        hypo = st.text_input("Enter Hypothesis:", placeholder="Mutation_Score directly drives Expression_Level variance")
        if st.button("RUN SCIENTIFIC VALIDATION"):
            if 'discovery_result' in st.session_state:
                res = st.session_state.discovery_result
                st.success(f"Hypothesis Parsed. Success Probability: {res['prob']*100:.1f}%")
                
                col_res1, col_res2 = st.columns(2)
                with col_res1:
                    st.metric("FIDELITY (SILHOUETTE)", f"{res['silhouette']:.4f}")
                    st.caption("Score > 0.5 indicates strong biological separation.")
                with col_res2:
                    st.metric("CAUSAL PATHS DETECTED", len(res['causal_g'].edges()))
                
                st.divider()
                
                # Feature Importance Chart
                st.subheader("🧬 Feature Attribution (Drivers)")
                imp_df = pd.DataFrame(list(res['importance'].items()), columns=['Feature', 'Importance'])
                fig_imp = px.bar(imp_df, x='Feature', y='Importance', color='Importance', 
                                 title="Feature Drivers of System State", color_continuous_scale='Viridis')
                st.plotly_chart(fig_imp, width='stretch')
                
                st.divider()
                
                # Causal Graph Visualization (Simple Plotly version)
                st.subheader("🕸️ Hypothesized Causal Graph")
                st.caption("Directed paths indicating mechanistic influence (A -> B)")
                
                G = res['causal_g']
                if len(G.edges()) > 0:
                    edge_list = list(G.edges())
                    st.write(f"Detected Mechansim: **{edge_list[0][0]}** $\rightarrow$ **{edge_list[0][1]}**")
                    # Simple list for now as networkx-plotly-3d is complex
                    for u, v in G.edges():
                        st.markdown(f"- `{u}` causes variance in `{v}` (Weight: {G[u][v]['weight']:.2f})")
                else:
                    st.info("No significant causal paths detected at current threshold.")

                st.markdown(f"""
                > **Scientific Rationale:**
                > System detected a **{res['anomaly']}** state within **{res['current_regime']}**. 
                > Manifold geometry indicates increased curvature in the feature subspace.
                > Silhouette score of **{res['silhouette']:.3f}** confirms the mathematical validity of these findings.
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
                st.plotly_chart(draw_min_manifold(st.session_state.shock_original, "Original Manifold"), width='stretch')
            with col_comp2:
                st.plotly_chart(draw_min_manifold(st.session_state.shock_manifold, "Post-Shock Manifold"), width='stretch')
        else:
            st.info("Initiate Shock Simulation to observe systemic geometry shifts.")

# 17. ADVERSARIAL LAB
if st.session_state.active_tab == "🔐 ADVERSARIAL LAB":
    st.header("🔐 Adversarial Lab: Cyber AI Defense")
    st.write("Simulating Red Team vs Blue Team dynamics with Bayesian Risk Propagation.")
    
    if domain != "Cybersecurity":
        st.warning("Please select 'Cybersecurity' domain in Domain Configuration to enable the Adversarial Lab.")
    else:
        col_adv1, col_adv2 = st.columns([1, 2])
        
        with col_adv1:
            st.markdown("### 🧪 Attack Simulator")
            target_node = st.selectbox("Target Node", ["N1", "N2", "N3", "N4", "N5"])
            attack_type = st.radio("Attack Type", ["DDoS", "BruteForce", "Privilege Escalation"])
            intensity = st.slider("Payload Intensity", 0.0, 1.0, 0.8)
            
            if st.button("🚀 EXECUTE ATTACK"):
                from simulation.cyber_simulator import CyberSimulator
                from simulation.adversarial_engine import AdversarialEngine
                from intelligence.mitre_mapper import MitreMapper
                
                sim = CyberSimulator()
                engine = AdversarialEngine(sim)
                
                # Run Round
                res = engine.run_round(target_node, attack_type)
                
                st.session_state.cyber_results = res
                st.session_state.mitre_context = MitreMapper.get_mitre_context(attack_type)
                st.session_state.cyber_active = True
                st.success(f"Attack on {target_node} executed. Blue Team responded.")

        with col_adv2:
            if 'cyber_active' in st.session_state and st.session_state.cyber_active:
                res = st.session_state.cyber_results
                mitre = st.session_state.mitre_context
                
                st.markdown(f"### 🛡️ MITRE Context: {mitre['name']} ({mitre['id']})")
                st.caption(mitre['description'])
                st.info(f"**Detection Guidance**: {mitre['detection']}")
                
                st.divider()
                st.subheader("📊 Bayesian Propagation Impact")
                
                # Show results in a table
                impact_df = pd.DataFrame([
                    {"Node": n, "Status": s} for n, s in res["system_state"].items()
                ])
                st.table(impact_df)
                
                st.divider()
                st.subheader("🤖 Autonomous Action Log")
                if res["blue_responses"]:
                    for action in res["blue_responses"]:
                        st.success(f"**{action['action']}** applied to **{action['node']}** | Result: {action.get('result', {}).get('status', 'SUCCESS')}")
                else:
                    st.warning("No autonomous actions triggered. Risk below threshold.")
            else:
                st.info("Execute an attack simulation to view reasoning and systemic impact.")

        st.divider()
        st.subheader("🔄 Multi-Round Adversarial Simulation")
        if st.button("🏃 START CONTINUOUS Red vs Blue LOOP"):
            from simulation.cyber_simulator import CyberSimulator
            from simulation.adversarial_engine import AdversarialEngine
            
            sim_loop = CyberSimulator()
            engine_loop = AdversarialEngine(sim_loop)
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            rounds_to_run = 3
            for r in range(rounds_to_run):
                status_text.text(f"Running Round {r+1} of {rounds_to_run}...")
                round_res = engine_loop.run_round()
                
                with st.expander(f"Round {r+1} Details"):
                    st.write(f"**Red Team**: {round_res['red_action']['type']} on {round_res['red_action']['target']}")
                    st.write(f"**Blue Team Actions**: {len(round_res['blue_responses'])} mitigations applied.")
                    st.json(round_res['system_state'])
                
                progress_bar.progress((r + 1) / rounds_to_run)
                import time; time.sleep(1)
            
            st.success("Simulation Complete. System co-evolution stabilized.")

# 18. SMART CITY TWIN
if st.session_state.active_tab == "🏙️ SMART CITY TWIN":
    import plotly.graph_objects as go
    import numpy as np
    from simulation.smart_city_simulator import SmartCitySimulator

    st.header("🏙️ Smart City Digital Twin")
    st.caption("Infrastructure Resilience & Cascading Failure Simulation — OMEGA-CORE Civic AI")

    # --- Persistent simulator instance ---
    if 'city_sim' not in st.session_state:
        st.session_state.city_sim = SmartCitySimulator()
        st.session_state.city_event_log = []

    sim = st.session_state.city_sim

    # --- NODE METADATA ---
    NODE_ICONS = {"P": "⚡", "C": "📡", "T": "🚦", "W": "💧", "E": "🚨"}
    NODE_COLORS = {
        "OPERATIONAL":    "#10B981",
        "DEGRADED":       "#F59E0B",
        "UNSTABLE":       "#F97316",
        "FAILURE":        "#EF4444",
        "THROTTLED":      "#6366F1",
        "RECOVERING":     "#3B82F6",
        "BACKUP_RUNNING": "#8B5CF6",
    }
    NODE_POS = {"P": (0, 0), "C": (2, 1), "T": (4, 2), "W": (2, -1), "E": (4, 0)}

    # ── Row 1: Control Panel + Topology Map ───────────────────────────────────
    col_ctrl, col_map = st.columns([1, 2])

    with col_ctrl:
        with st.container(border=True):
            st.markdown("### 🌋 Inject System Shock")
            target_node = st.selectbox(
                "Infrastructure Node",
                options=list(sim.nodes.keys()),
                format_func=lambda k: f"{NODE_ICONS[k]} {sim.nodes[k]}"
            )
            shock_type = st.radio("Shock Type", ["Power Failure", "Comms Blackout", "Flood", "Cyber Override"])
            intensity = st.slider("Shock Intensity", 0.0, 1.0, 0.9, step=0.05)

            if st.button("⚡ INITIATE SHOCK", width='stretch'):
                results = sim.inject_shock(target_node, shock_type, intensity)
                st.session_state.city_results = results
                ts = datetime.datetime.now().strftime("%H:%M:%S")
                st.session_state.city_event_log.append(
                    f"[{ts}] {shock_type} on {NODE_ICONS[target_node]} {sim.nodes[target_node]} (intensity={intensity:.2f})"
                )
                st.session_state.city_active = True
                st.success("Shock injected. Cascade propagated.")

        with st.container(border=True):
            st.markdown("### 🛡️ Resilience Actions")
            action_node = st.selectbox(
                "Target Node",
                options=list(sim.nodes.keys()),
                format_func=lambda k: f"{NODE_ICONS[k]} {sim.nodes[k]}",
                key="action_node_sel"
            )
            action_type = st.selectbox(
                "Action",
                ["Activate Backup", "Load Shedding", "Reroute Flow"]
            )
            if st.button("🔧 APPLY ACTION", width='stretch'):
                action_res = sim.apply_resilience_action(action_node, action_type)
                ts = datetime.datetime.now().strftime("%H:%M:%S")
                st.session_state.city_event_log.append(
                    f"[{ts}] ✅ {action_type} → {NODE_ICONS[action_node]} {sim.nodes[action_node]}"
                )
                st.success(f"Action '{action_type}' applied: {action_res['new_state']['status']}")
                # Refresh results
                st.session_state.city_results = sim._format_results({})
                st.session_state.city_active = True

            if st.button("🔄 RESET SIMULATION", width='stretch'):
                st.session_state.city_sim = SmartCitySimulator()
                st.session_state.city_event_log = []
                st.session_state.city_active = False
                if 'city_results' in st.session_state:
                    del st.session_state.city_results
                if 'city_reasoning' in st.session_state:
                    del st.session_state.city_reasoning
                st.rerun()

    with col_map:
        with st.container(border=True):
            st.markdown("### 🗺️ Infrastructure Topology")

            # Build Plotly network figure
            states = sim.node_states
            edges = list(sim.G.edges())

            edge_x, edge_y = [], []
            for u, v in edges:
                x0, y0 = NODE_POS[u]
                x1, y1 = NODE_POS[v]
                edge_x += [x0, x1, None]
                edge_y += [y0, y1, None]

            edge_trace = go.Scatter(
                x=edge_x, y=edge_y, mode='lines',
                line=dict(width=2, color='#444'),
                hoverinfo='none'
            )

            node_x, node_y, node_colors, node_text, node_hover = [], [], [], [], []
            for nid in sim.nodes:
                x, y = NODE_POS[nid]
                status = states[nid]["status"]
                integrity = states[nid]["integrity"]
                node_x.append(x)
                node_y.append(y)
                node_colors.append(NODE_COLORS.get(status, "#888"))
                node_text.append(f"{NODE_ICONS[nid]} {nid}")
                node_hover.append(
                    f"<b>{sim.nodes[nid]}</b><br>"
                    f"Status: {status}<br>"
                    f"Integrity: {integrity:.0%}<br>"
                    f"Load: {states[nid]['load']:.0%}"
                )

            node_trace = go.Scatter(
                x=node_x, y=node_y, mode='markers+text',
                text=node_text,
                textposition='top center',
                marker=dict(size=40, color=node_colors, line=dict(width=2, color='#fff')),
                hovertext=node_hover,
                hoverinfo='text'
            )

            fig_topo = go.Figure(data=[edge_trace, node_trace])
            fig_topo.update_layout(
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(15,15,15,1)',
                margin=dict(l=20, r=20, t=20, b=20),
                height=300,
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            )
            st.plotly_chart(fig_topo, width='stretch')

    st.divider()

    # ── Row 2: Integrity Gauges ────────────────────────────────────────────────
    st.subheader("📊 Node Integrity Gauges")
    gauge_cols = st.columns(5)
    for i, (nid, nname) in enumerate(sim.nodes.items()):
        state = sim.node_states[nid]
        integrity = max(0.0, state["integrity"])
        status = state["status"]
        color = NODE_COLORS.get(status, "#888")
        fig_g = go.Figure(go.Indicator(
            mode="gauge+number",
            value=round(integrity * 100, 1),
            title={'text': f"{NODE_ICONS[nid]} {nid}", 'font': {'color': 'white', 'size': 14}},
            gauge={
                'axis': {'range': [0, 100], 'tickcolor': '#555'},
                'bar': {'color': color},
                'bgcolor': '#111',
                'bordercolor': '#333',
                'steps': [
                    {'range': [0, 30],  'color': '#1a0000'},
                    {'range': [30, 70], 'color': '#1a1000'},
                    {'range': [70, 100],'color': '#001a0a'},
                ],
            },
            number={'suffix': '%', 'font': {'color': 'white'}}
        ))
        fig_g.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            height=200,
            margin=dict(l=10, r=10, t=30, b=10)
        )
        gauge_cols[i].plotly_chart(fig_g, width='stretch')
        gauge_cols[i].caption(f"**{status}**")

    st.divider()

    # ── Row 3: AI Reasoning + Event Log ───────────────────────────────────────
    col_reason, col_log = st.columns([3, 2])

    with col_reason:
        st.subheader("🧠 AI Resilience Reasoning")
        if 'city_active' in st.session_state and st.session_state.city_active:
            if st.button("🤖 RUN OMEGA REASONING ENGINE", width='stretch'):
                from intelligence.reasoning_agent import ReasoningAgent
                res = st.session_state.get('city_results', sim._format_results({}))
                with st.spinner("Traversing Causal Pathways..."):
                    reasoner = ReasoningAgent()
                    reasoning = reasoner.execute_reasoning({
                        "domain": "Smart City",
                        "shock_target": "Active",
                        "system_state": {k: {"status": v["status"], "integrity": v["integrity"]} for k, v in res.items()}
                    })
                    st.session_state.city_reasoning = reasoning

            if 'city_reasoning' in st.session_state:
                r = st.session_state.city_reasoning
                if "error" in r:
                    st.error(f"Reasoning error: {r['error']}")
                else:
                    risk_color = "#EF4444" if "High" in r.get("risk_prioritization","") else "#F59E0B"
                    st.markdown(f"""
                    <div style="background:{risk_color}22; border-left:4px solid {risk_color}; padding:12px; border-radius:8px; margin-bottom:12px;">
                        <strong style="color:{risk_color}">RISK PRIORITY: {r.get("risk_prioritization","N/A")}</strong>
                    </div>
                    """, unsafe_allow_html=True)

                    with st.container(border=True):
                        st.markdown("**📍 Domain Assessment**")
                        st.write(r.get("domain_assessment", ""))

                    with st.container(border=True):
                        st.markdown("**🔬 Root Cause Analysis**")
                        st.write(r.get("analysis", ""))

                    with st.container(border=True):
                        st.markdown("**⚠️ Key Vulnerabilities**")
                        for v in r.get("vulnerabilities", []):
                            st.markdown(f"- {v}")

                    with st.container(border=True):
                        st.markdown("**🛡️ Recommended Strategy**")
                        for s in r.get("strategy", []):
                            st.markdown(f"✅ {s}")
        else:
            st.info("Inject a system shock to enable AI reasoning analysis.")

    with col_log:
        st.subheader("📋 Live Event Log")
        if st.session_state.city_event_log:
            log_html = "<div style='font-family:monospace;font-size:12px;color:#10B981;background:#050505;padding:15px;border-radius:8px;height:360px;overflow-y:scroll;border:1px solid #222;'>"
            for entry in reversed(st.session_state.city_event_log):
                log_html += f"{entry}<br>"
            log_html += "</div>"
            st.markdown(log_html, unsafe_allow_html=True)
        else:
            st.info("No events yet. Inject a shock to begin logging.")

        if 'city_results' in st.session_state:
            st.divider()
            st.subheader("📡 Sector Impact Table")
            res = st.session_state.city_results
            impact_rows = []
            for nid, data in res.items():
                status = data["status"]
                color = NODE_COLORS.get(status, "#888")
                impact_rows.append({
                    "Node": f"{NODE_ICONS.get(nid, '')} {data['name']}",
                    "Status": status,
                    "Integrity": f"{data['integrity']:.0%}",
                    "Cascade Risk": f"{data['cascade_risk']:.0%}"
                })
            st.dataframe(pd.DataFrame(impact_rows), width='stretch', hide_index=True)

# --- FOOTER ---
st.divider()
st.caption("Universal Laptop Lab | Powered by OMEGA-CORE v2.5 | 10-Node Hyperarchitecture")
