"""
omega_bridge.py — OMEGA-CORE Streamlit Bridge
==============================================
Connects the harness (local Ollama LLMs) to the Streamlit UI.

Environment variables (optional, set in .env):
    USE_LOCAL_LLM=true   — already the default; Ollama runs locally, no API key needed.

Usage in streamlit_app.py (2 lines only):
    from omega_bridge import run_agent_panel, memory_dashboard
    run_agent_panel('scientific_discovery')   # at bottom of any tab block
"""
import streamlit as st
from harness import Agent, MemoryLayer, ToolRegistry
from blueprints import get_blueprint
import json, time

# Shared infrastructure - initialised once per session
MEMORY_PATH = "C:/Universal_Lab_AP_Phillips/memory"

@st.cache_resource
def get_harness():
    mem = MemoryLayer(path=MEMORY_PATH)
    tools = ToolRegistry()
    agents = {t: Agent(name=t, prompt_blueprint=get_blueprint(t), memory=mem, tools=tools, use_debate=True)
              for t in ["scientific_discovery","finance","weather_manifold","health_protocol",
                        "adversarial_lab","world_model","asi_core","digital_twin",
                        "smart_city_twin","agriculture_asi","global_monitoring","clinical_stress_test"]}
    return mem, agents

def run_agent_panel(tab_name: str, query: str = None, context_data: dict = None):
    mem, agents = get_harness()
    agent = agents.get(tab_name)
    if not agent:
        st.warning(f"No agent configured for {tab_name}")
        return

    st.markdown("---")
    st.markdown("####  OMEGA Harness  Mistral  Phi3 Debate")

    if query is None:
        query = st.text_area("Mission Intent (Hypothesis/Goal)", placeholder="What should this agent analyze?", key=f"hq_{tab_name}")
        
    context_json_str = st.text_area("Context Data (Paste JSON here)", placeholder='{"sensor_x": 912, "sensor_y": 0.03, ...}', key=f"ctx_{tab_name}")
    
    if st.button(" Run Agent Harness", key=f"hbtn_{tab_name}"):
        with st.spinner("Mistral reasoning... Phi3 challenging... Arbiter deciding..."):
            
            # Parse the JSON if the user pasted any
            parsed_context = context_data or {}
            if context_json_str.strip():
                try:
                    parsed_context = json.loads(context_json_str)
                except json.JSONDecodeError:
                    st.error("Invalid JSON format in Context Data. Proceeding with raw text.")
                    query += f"\n\nRaw Data:\n{context_json_str}"
            try:
                result = agent.run(query, parsed_context)
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Primary  Mistral**")
                    st.text_area("Primary Reasoning", result.primary_reasoning, height=200, key=f"pr_{tab_name}_{result.run_id}")
                with col2:
                    st.markdown("**Challenger  Phi3 + Arbiter**")
                    chall = result.challenger_reasoning + chr(10)*2 + "ARBITER:" + chr(10) + result.arbiter_decision
                    st.text_area("Challenger + Arbiter", chall, height=200, key=f"ch_{tab_name}_{result.run_id}")
                st.success(result.final_answer)
                st.caption(f"Run {result.run_id}  {result.duration_seconds}s  Memory: {mem.summary(tab_name)['total_entries']} entries")
            except Exception as e:
                st.error(f"Agent error: {e}")

def memory_dashboard():
    mem, agents = get_harness()
    st.markdown("####  Cross-Agent Memory")
    for a in mem.all_agents():
        s = mem.summary(a)
        st.markdown(f"**{a}**  {s['total_entries']} entries  {s['by_role']}")
        recent = mem.recent(a, n=3)
        for e in recent:
            st.caption(f"[{e.role}] {e.content[:120]}")

