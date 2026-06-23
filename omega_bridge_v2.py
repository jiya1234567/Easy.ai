"""
omega_bridge_v2.py
====================
Unified bridge wiring all 6 gap fixes into the existing Streamlit
harness panel. Drop-in upgrade for omega_bridge.py — same function
names (run_agent_panel, memory_dashboard) so existing tab injections
keep working without further edits to streamlit_app.py.

Gaps closed:
  1. Live/Manual toggle      -> sensor_loop.SensorLoop
  2. Semantic memory          -> vector_memory.VectorMemoryLayer
  3. Uncertainty quantification -> uncertainty.compute_uncertainty
  4. Reality anchor feedback  -> reality_anchor.RealityAnchor
  5. Parallel agent colony    -> agent_colony.AgentColony
  6. Self-improvement         -> self_improve.SelfImprovementEngine
"""

import streamlit as st
import json
import time

from harness import Agent, ToolRegistry
from blueprints import get_blueprint

from vector_memory import VectorMemoryLayer
from reality_anchor import RealityAnchor
from uncertainty import compute_uncertainty
from sensor_loop import SensorLoop
from agent_colony import AgentColony
from self_improve import SelfImprovementEngine
from discovery_planner import DiscoveryPlanner
from auto_chain import AutoChain, DEFAULT_MAX_CYCLES, MAX_ALLOWED_CYCLES

MEMORY_PATH = "C:/Universal_Lab_AP_Phillips/memory"
REALITY_PATH = "C:/Universal_Lab_AP_Phillips/memory/reality"
CALIBRATION_PATH = "C:/Universal_Lab_AP_Phillips/memory/calibration"

ALL_AGENT_NAMES = [
    "scientific_discovery", "finance", "weather_manifold", "health_protocol",
    "adversarial_lab", "world_model", "asi_core", "digital_twin",
    "smart_city_twin", "agriculture_asi", "global_monitoring", "clinical_stress_test",
]


@st.cache_resource
def get_harness_v2():
    """Initialise all gap-fix subsystems once per Streamlit session."""
    mem = VectorMemoryLayer(path=MEMORY_PATH)
    tools = ToolRegistry()
    reality = RealityAnchor(path=REALITY_PATH)
    calibration = SelfImprovementEngine(path=CALIBRATION_PATH)

    agents = {}
    for name in ALL_AGENT_NAMES:
        base_blueprint = get_blueprint(name)
        # Apply any approved self-improvement calibrations on top of base prompt
        calibrated_blueprint = calibration.apply_approved(name, base_blueprint)
        agents[name] = Agent(
            name=name,
            prompt_blueprint=calibrated_blueprint,
            memory=mem,
            tools=tools,
            use_debate=True,
        )

    colony = AgentColony(agents)
    planner = DiscoveryPlanner()

    return {
        "memory": mem,
        "tools": tools,
        "agents": agents,
        "reality": reality,
        "calibration": calibration,
        "colony": colony,
        "planner": planner,
    }


def _sensor_loop_for(tab_name: str, data_source_fn, query: str) -> SensorLoop:
    """One SensorLoop instance per tab, cached in session_state."""
    key = f"sensorloop_{tab_name}"
    if key not in st.session_state:
        h = get_harness_v2()
        st.session_state[key] = SensorLoop(
            agent=h["agents"][tab_name],
            data_source_fn=data_source_fn,
            query=query,
            interval_seconds=60.0,
            log_path=f"{MEMORY_PATH}/sensor_logs/{tab_name}.json",
        )
    return st.session_state[key]


def run_agent_panel(tab_name: str, query: str = None, context_data: dict = None):
    """
    Main harness panel. Drop-in replacement for the original
    run_agent_panel — adds Live/Manual toggle, uncertainty display,
    and reality-anchor prediction tracking.
    """
    h = get_harness_v2()
    agent = h["agents"].get(tab_name)
    if not agent:
        st.warning(f"No agent configured for {tab_name}")
        return

    st.markdown("---")
    st.markdown("#### 🧠 OMEGA Harness v2 — Mistral × Phi3 Debate + Reality Loop")

    # ── Inference stack selector ────────────────────────────────────
    # Pulled from your installed Ollama models (mistral, phi3, llava per
    # earlier `ollama list`). Add more here as you pull additional models.
    AVAILABLE_PRIMARY = ["mistral", "mistral-large", "llava"]
    AVAILABLE_CHALLENGER = ["phi3", "phi3:mini", "mistral", "llava"]

    with st.expander("⚙️ Inference Stack", expanded=False):
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            chosen_primary = st.selectbox(
                "Primary model", AVAILABLE_PRIMARY,
                index=AVAILABLE_PRIMARY.index(agent.primary_model) if agent.primary_model in AVAILABLE_PRIMARY else 0,
                key=f"primary_model_{tab_name}",
            )
        with col_m2:
            chosen_challenger = st.selectbox(
                "Challenger model", AVAILABLE_CHALLENGER,
                index=AVAILABLE_CHALLENGER.index(agent.challenger_model) if agent.challenger_model in AVAILABLE_CHALLENGER else 0,
                key=f"challenger_model_{tab_name}",
            )
        st.caption(
            "Changes apply to this agent's next run. Smaller models (e.g. "
            "phi3:mini) trade reasoning depth for speed — useful for testing "
            "the loop quickly before committing to longer auto-chain runs."
        )
        # Apply selection to the cached agent instance (safe: these are
        # plain string attributes read fresh inside _reason() each call,
        # not baked into the harness at construction time).
        agent.primary_model = chosen_primary
        agent.challenger_model = chosen_challenger

    # ── Live / Manual toggle ──────────────────────────────────────
    mode = st.radio(
        "Mode", ["Manual", "Live (auto-poll)"],
        horizontal=True, key=f"mode_{tab_name}",
        help="Manual: you trigger each run. Live: automatically re-runs on an interval using the last data provided.",
    )

    if query is None:
        # Discovery Planner suggestion (scoped to Scientific Discovery tab for v1)
        if tab_name == "scientific_discovery":
            with st.expander("💡 Discovery Planner suggests a next experiment", expanded=False):
                if st.button("Generate suggestion", key=f"plan_gen_{tab_name}"):
                    with st.spinner("Reviewing history and accuracy record..."):
                        try:
                            suggestion = h["planner"].suggest_next(
                                agent_name=tab_name,
                                memory=h["memory"],
                                reality_anchor=h["reality"],
                            )
                            st.session_state[f"plan_suggestion_{tab_name}"] = suggestion
                        except Exception as e:
                            st.error(f"Planner error: {e}")

                cached = st.session_state.get(f"plan_suggestion_{tab_name}")
                if cached:
                    st.markdown(f"**Proposed:** {cached.proposed_query}")
                    st.caption(f"Reasoning: {cached.reasoning}")
                    st.caption(f"Type: {cached.question_type} · Variables: {', '.join(cached.target_variables) or 'none specified'}")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.button("✅ Use this suggestion", key=f"plan_use_{tab_name}"):
                            st.session_state[f"hq_{tab_name}"] = cached.proposed_query
                            st.rerun()
                    with col_b:
                        if st.button("✖ Dismiss", key=f"plan_dismiss_{tab_name}"):
                            del st.session_state[f"plan_suggestion_{tab_name}"]
                            st.rerun()

            with st.expander("🔄 Auto-Chain Discovery Loop (autonomous, capped, stoppable)", expanded=False):
                st.caption(
                    "Runs Suggest → Run cycles automatically up to a hard cap. "
                    "Does NOT auto-validate predictions against reality — that "
                    "always requires your review in the Reality Anchor panel."
                )
                max_cycles = st.slider(
                    "Max cycles this run", 1, MAX_ALLOWED_CYCLES, DEFAULT_MAX_CYCLES,
                    key=f"chain_max_{tab_name}",
                )

                chain_key = f"autochain_{tab_name}"
                if chain_key not in st.session_state:
                    def _read_current_data(tn=tab_name):
                        raw = st.session_state.get(f"hd_{tn}", "")
                        if raw and raw.strip():
                            try:
                                return json.loads(raw)
                            except Exception:
                                return {}
                        return {}

                    st.session_state[chain_key] = AutoChain(
                        agent=agent,
                        memory=h["memory"],
                        reality_anchor=h["reality"],
                        context_data_fn=_read_current_data,
                        planner=DiscoveryPlanner(),
                    )
                chain = st.session_state[chain_key]

                col_x, col_y = st.columns(2)
                with col_x:
                    start_chain = st.button("▶ Start Auto-Chain", key=f"chain_start_{tab_name}")
                with col_y:
                    stop_chain = st.button("⏹ Stop", key=f"chain_stop_{tab_name}")

                if stop_chain:
                    chain.stop()
                    st.warning("Stop requested — will halt after the current step.")

                if start_chain:
                    chain.start(max_cycles=max_cycles)
                    progress_area = st.empty()
                    cycle_log = []

                    def _log_cycle(c):
                        cycle_log.append(
                            f"**Cycle {c.cycle_number}** ({c.question_type}): {c.suggestion_query}\n\n"
                            f"  Reasoning: {c.suggestion_reasoning}\n\n"
                            f"  Result: {c.agent_result.final_answer[:200]}\n\n  ---"
                        )
                        progress_area.markdown("\n\n".join(cycle_log))

                    chain.on_cycle_complete = _log_cycle

                    with st.spinner(f"Running auto-chain (max {max_cycles} cycles)..."):
                        results = chain.run_all()

                    if chain.state.last_error:
                        st.error(f"Chain stopped due to error: {chain.state.last_error}")
                    else:
                        st.success(f"Auto-chain completed {len(results)} cycle(s).")

                status = chain.status()
                if status["cycle_count"] > 0:
                    st.caption(
                        f"Last run: {status['cycle_count']}/{status['max_cycles']} cycles · "
                        f"{'still running' if status['running'] else 'stopped'}"
                    )

        query = st.text_area("Mission Intent", placeholder="What should this agent analyze?", key=f"hq_{tab_name}")

    data_str = st.text_area(
        "Context Data (JSON, optional)",
        placeholder='{"var1":[1,2,3],"var2":[4,5,6]}',
        key=f"hd_{tab_name}",
    )
    parsed_data = context_data or {}
    if data_str and data_str.strip():
        try:
            parsed_data = json.loads(data_str)
        except Exception:
            st.caption("⚠️ Could not parse JSON — running without context data.")

    if mode == "Live (auto-poll)":
        interval = st.slider("Poll interval (seconds)", 10, 300, 60, key=f"interval_{tab_name}")
        loop = _sensor_loop_for(tab_name, lambda: parsed_data, query or "Monitor for changes")
        loop.state.interval_seconds = interval
        loop.query = query or loop.query
        loop.data_source_fn = lambda: parsed_data

        col1, col2 = st.columns(2)
        with col1:
            if not loop.state.running:
                if st.button("▶ Start Live Polling", key=f"live_start_{tab_name}"):
                    loop.start_live()
                    st.rerun()
            else:
                if st.button("⏸ Stop Live Polling", key=f"live_stop_{tab_name}"):
                    loop.stop_live()
                    st.rerun()
        with col2:
            status = loop.status()
            st.caption(
                f"Status: {'🟢 Running' if status['running'] else '⚪ Stopped'} · "
                f"Polls: {status['poll_count']} · Errors: {status['error_count']}"
            )
        if loop.state.last_result_summary:
            st.info(f"Last result: {loop.state.last_result_summary}")
        return  # live mode doesn't use the manual run button below

    # ── Manual mode ───────────────────────────────────────────────
    if st.button("▶ Run Agent Harness", key=f"hbtn_{tab_name}"):
        with st.spinner("Mistral reasoning... Phi3 challenging... Arbiter deciding..."):
            try:
                result = agent.run(query, parsed_data)

                # Uncertainty quantification (Gap 3)
                unc = compute_uncertainty(result.primary_reasoning, result.challenger_reasoning)

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Primary — {agent.primary_model}**")
                    st.text_area("Primary Reasoning", result.primary_reasoning, height=200,
                                key=f"pr_{tab_name}_{result.run_id}")
                with col2:
                    st.markdown(f"**Challenger — {agent.challenger_model} + Arbiter**")
                    chall = (result.challenger_reasoning + "\n\nARBITER:\n" + result.arbiter_decision)
                    st.text_area("Challenger + Arbiter", chall, height=200,
                                key=f"ch_{tab_name}_{result.run_id}")

                st.success(result.final_answer)

                # Uncertainty badge
                label_color = {"high": "🟢", "moderate": "🟡", "low": "🔴", "unknown": "⚪"}
                st.markdown(
                    f"{label_color.get(unc.confidence_label,'⚪')} **Calibrated confidence: "
                    f"{unc.confidence_label}** (agreement: {unc.agreement_score:.0%}, "
                    f"epistemic uncertainty: {unc.epistemic_uncertainty:.0%})"
                )
                if unc.disagreement_points:
                    with st.expander("Specific points of disagreement"):
                        for p in unc.disagreement_points:
                            st.caption(f"• {p}")

                st.caption(
                    f"Run {result.run_id} · {result.duration_seconds}s · "
                    f"Memory: {h['memory'].summary(tab_name)['total_entries']} entries"
                )

                # Reality Anchor — offer to record this as a trackable prediction
                with st.expander("📌 Track this as a prediction (Reality Anchor)"):
                    st.caption(
                        "If this answer makes a specific, checkable prediction about a "
                        "variable's future value, record it here. When real data arrives "
                        "later, validate it to build an accuracy track record."
                    )
                    pred_var = st.text_input("Variable name", key=f"predvar_{tab_name}_{result.run_id}")
                    pred_val = st.number_input("Predicted value", key=f"predval_{tab_name}_{result.run_id}", value=0.0)
                    if st.button("Record prediction", key=f"recpred_{tab_name}_{result.run_id}"):
                        if pred_var:
                            pid = h["reality"].record_prediction(
                                agent=tab_name,
                                prediction_text=result.final_answer[:200],
                                predicted_variables={pred_var: pred_val},
                            )
                            st.success(f"Recorded prediction {pid} for tracking.")

            except Exception as e:
                st.error(f"Agent error: {e}")


def reality_validation_panel():
    """
    UI for validating pending predictions against actual outcomes,
    and viewing accuracy track records per agent. Call this from a
    dedicated tab or the Memory Inspector.
    """
    h = get_harness_v2()
    reality = h["reality"]
    calibration = h["calibration"]

    st.markdown("#### 📌 Reality Anchor — Prediction Validation")

    summary = reality.summary()
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Predictions", summary["total_predictions"])
    col2.metric("Validated", summary["validated"])
    col3.metric("Pending", summary["pending"])

    if summary["accuracy_by_agent"]:
        st.markdown("**Accuracy by agent:**")
        for agent, acc in summary["accuracy_by_agent"].items():
            st.caption(f"  {agent}: {acc:.0%}")

    st.markdown("---")
    st.markdown("**Validate a pending prediction**")
    pending = reality.recent(n=20)
    unvalidated = [p for p in pending if not p.validated]

    if not unvalidated:
        st.caption("No pending predictions to validate.")
    else:
        options = {f"{p.id} — {p.prediction_text[:60]}": p.id for p in unvalidated}
        choice = st.selectbox("Select prediction", list(options.keys()))
        if choice:
            pred_id = options[choice]
            pred = reality._predictions[pred_id]
            st.json(pred.predicted_variables)
            actual_inputs = {}
            for var in pred.predicted_variables:
                actual_inputs[var] = st.number_input(f"Actual value for '{var}'", key=f"actual_{var}_{pred_id}")
            if st.button("Validate", key=f"validate_{pred_id}"):
                acc = reality.validate(pred_id, actual_inputs)
                st.success(f"Validated — accuracy: {acc:.0%}")

                # Trigger self-improvement check (Gap 6)
                notes = calibration.propose_calibrations(reality, pred.agent)
                if notes:
                    st.info(f"📈 {len(notes)} new calibration note(s) proposed for '{pred.agent}' agent — review in Memory Inspector.")

    # Self-improvement pending review
    st.markdown("---")
    st.markdown("**🧬 Pending Calibration Notes (Self-Improvement)**")
    pending_notes = calibration.pending_review()
    if not pending_notes:
        st.caption("No pending calibration notes.")
    for note in pending_notes:
        with st.expander(f"{note.agent}: {note.evidence_summary}"):
            st.write(note.proposed_addition)
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Approve", key=f"approve_{note.id}"):
                    calibration.approve(note.id)
                    st.rerun()
            with col2:
                if st.button("❌ Reject", key=f"reject_{note.id}"):
                    calibration.reject(note.id)
                    st.rerun()


def colony_panel():
    """
    UI for running multiple agents in parallel and viewing the
    inter-agent message bus (Gap 5).
    """
    h = get_harness_v2()
    colony = h["colony"]

    st.markdown("#### 🐝 Agent Colony — Parallel Execution")

    selected = st.multiselect("Select agents to run in parallel", ALL_AGENT_NAMES,
                              default=["scientific_discovery", "finance"])

    queries = {}
    for name in selected:
        queries[name] = st.text_input(f"Query for {name}", key=f"colony_q_{name}")

    if st.button("▶ Run Colony (parallel)"):
        jobs = {name: (q, {}) for name, q in queries.items() if q.strip()}
        if jobs:
            with st.spinner(f"Running {len(jobs)} agents in parallel..."):
                t0 = time.time()
                results = colony.run_parallel(jobs)
                elapsed = time.time() - t0

            st.success(f"Completed {len(results)} agents in {elapsed:.1f}s (parallel)")
            for name, result in results.items():
                with st.expander(f"{name}: {result.final_answer[:80]}"):
                    st.write(result.final_answer)

    st.markdown("---")
    st.markdown("**📨 Inter-Agent Message Bus**")
    messages = colony.bus.all_messages(n=20)
    if not messages:
        st.caption("No messages yet.")
    for m in messages:
        st.caption(f"[{m.from_agent} → {m.to_agent}] {m.content[:150]}")


def memory_dashboard():
    """Cross-agent memory view — now semantic-search-aware (Gap 2)."""
    h = get_harness_v2()
    mem = h["memory"]

    st.markdown("#### 💾 Cross-Agent Memory")
    st.caption(f"Semantic search: {'🟢 enabled (ChromaDB)' if mem.semantic_enabled else '⚪ keyword fallback (install chromadb for semantic search)'}")

    for a in mem.all_agents():
        s = mem.summary(a)
        st.markdown(f"**{a}** — {s['total_entries']} entries — {s['by_role']}")
        recent = mem.recent(a, n=3)
        for e in recent:
            st.caption(f"[{e['role']}] {e['content'][:120]}")
