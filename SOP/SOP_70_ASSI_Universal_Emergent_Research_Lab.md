# 🤖 SOP 70: ASSI Universal Emergent Systems Research Lab
**AP Phillips Universal Laboratory | OMEGA-CORE ASI Framework v3.0**

---

## 📋 Overview

This SOP documents the full operational procedure for using the **ASSI Research Lab** tab in the OMEGA-CORE Singularity Dashboard to:

1. Load and classify research domains
2. Generate emergent benchmark datasets
3. Run phase transition analysis
4. Interpret results scientifically

**Scientific Basis:** Adaptive System State Intelligence (ASSI) — detecting when a system transitions from **Reducible** (predictable, governed by compact equations) to **Irreducible** (chaotic, nonlinear, emergent).

**Research Domains:** Based on the NSW Commercialisation Showcase 2024/2025 and the Top 20 Strategic Research Areas for the Next 25 Years.

---

## 🔬 Core Concepts

| Metric | Formula | Meaning |
|--------|---------|---------|
| **Entropy (S)** | S = −Σ pᵢ log pᵢ | Disorder/unpredictability of sensor readings |
| **Coherence (C)** | C = 1 / (1 + σ) | Synchronisation across sensor streams |
| **dC/dt** | \|Cₜ − Cₜ₋₁\| | Rate of coherence change — the phase transition trigger |
| **Prediction Error** | \|Observed − Predicted\| | Surprise level from the environment |

### State Classification

| State | Entropy | Coherence | Meaning |
|-------|---------|-----------|---------|
| **Stable** | < 0.4 | > 0.75 | System predictable, reducible physics dominant |
| **Adaptive** | 0.4–0.7 | 0.45–0.75 | Hybrid — stable core with emergent fluctuations |
| **Unstable** | 0.7–0.9 | 0.20–0.45 | Nonlinear dynamics taking over |
| **Critical Transition** | > 0.9 | < 0.20 | System fully irreducible, phase boundary crossed |

### ASSI Ontological Categories

| Category | Predictability | Example |
|----------|---------------|---------|
| **Reducible** | High | Thermal diffusion, crystal sorting |
| **Hybrid** | Transitioning | Quantum control vs noise |
| **Emergent / Biological** | Structured but hidden | Cellular differentiation |
| **Irreducible** | Chaotic | Storm emergence, turbulence |

---

## 🚀 Step-by-Step: How to Run an Experiment

### Step 1 — Open the ASSI Research Lab
1. Launch the dashboard: `py -m streamlit run streamlit_app.py`
2. In the tab grid, scroll to the last row and click **🤖 ASSI RESEARCH LAB**

### Step 2 — Build the Classification Dataset
1. Click **BUILD CLASSIFICATION DATA**
2. The engine processes 19 total cases:
   - 11 standard domains (NSW Showcase companies)
   - 8 robotic multi-modal domains (Vision + Touch + Smell)
3. Output saved to: `data/assi_research_data.json`
4. View results in the **Standard Domains** and **Robotic Fused Domains** sub-tabs
5. The bar chart shows distribution across ASSI categories

### Step 3 — Build the Emergent Benchmark Dataset
1. Click **BUILD EMERGENT BENCHMARK**
2. Generates 6 domain × 12 timestep transition datasets (72 total records)
3. Output saved to: `data/universal_emergent_benchmark.json`
4. Domains generated:

| Domain | Company Inspiration | Category |
|--------|--------------------|----|
| Quantum Computing Stability | Q-CTRL | Hybrid → Irreducible |
| Ocean Systems Emergence | Ocius | Irreducible (Storm) |
| Biological State Transition | Skin2Neuron / CREATE Medicines | Emergent |
| Climate-Energy Adaptive Systems | Thermal Dawn / HydGene | Hybrid → Emergent Grid |
| Autonomous Vision Systems | Unleash Live / Carbonix | Irreducible |
| Semiconductor / Nano Engineering | SiNAB | Hybrid → Quantum Instability |

### Step 4 — Inspect a Domain
1. Use **SELECT DOMAIN TO INSPECT** dropdown to choose a domain
2. Review:
   - **Entropy & Coherence chart** — tracks the evolution of S and C over 12 timesteps
   - **dC/dt line** — spikes above 0.15 threshold indicate phase transition events
   - **State Labels chart** — visual evolution from Stable → Adaptive → Unstable → Critical Transition
   - **Phase Transition Analysis** — automated verdict

### Step 5 — Run Full Transition Analysis
1. Click **ANALYSE TRANSITIONS**
2. The engine runs `detect_phase_transition()` across all 6 domains
3. The all-domain comparison bar chart shows Final Entropy — higher entropy means more emergent/irreducible

---

## 📊 How to Interpret the Results

### Section A: Classification Results (19 Cases)

**What to look for:**
- If most NSW Showcase companies fall into **Hybrid (Transitioning)** → the market is at a technology inflection point
- **Reducible** companies (Advanced Navigation, Extel) represent mature, stable-physics domains
- **Emergent** companies (Skin2Neuron, CREATE Medicines) represent the frontier where ASSI becomes most valuable

### Section B: Emergent Benchmark — Reading the Charts

#### Entropy & Coherence Chart
- **Red line (Entropy)** rising = system becoming harder to predict
- **Green line (Coherence)** falling = sensors diverging, system destabilising
- **Yellow line (dC/dt)** spiking above 0.15 dashed line = **phase transition event detected**

#### State Labels Chart
- Follow the dot pattern left to right
- Ideal reducible trajectory: all dots at **Stable**
- Hybrid trajectory: Stable → Adaptive
- Irreducible trajectory: Stable → Adaptive → Unstable → Critical Transition

### Reading the Phase Transition Verdict

| Verdict | Meaning | Action |
|---------|---------|--------|
| **STABLE — No phase transitions detected** | System remained in one state throughout | Confirm initial state classification |
| **TRANSITIONING — 1 boundary crossing** | Single phase boundary crossed | Log the timestep; begin adaptive protocol |
| **CRITICAL — N transitions detected** | Highly dynamic, multiple boundary crossings | Engage full irreducible sensing mode |

### Interpreting the Ocean Systems Emergence (Ocius) Result

**Observed:**
- Initial State: **Critical Transition**
- Final State: **Critical Transition**
- Final Entropy: **0.69**
- Final Coherence: **0.071**
- Verdict: **STABLE — No phase transitions detected**

**Scientific Interpretation:**

This is a correct and meaningful result. The ocean system entered a **Critical Transition** state at timestep 1 and remained there throughout. This means:

> The ocean system did **not** transition — it was already in its irreducible chaotic regime from the first measurement.

This is analogous to measuring a fully-formed storm. There is no phase boundary crossing because the system was already past it. The ASSI detector correctly identifies this as "STABLE" within the Critical Transition zone — a stable attractor in chaos.

**Research implication:** To detect the ocean phase transition you must capture data from **before** the storm onset. The benchmark correctly reflects what Ocius sensor robots would observe mid-ocean — a fully irreducible sea state.

---

## ⚙️ Running from the Terminal (Alternative)

```powershell
# Generate classification data only
py generate_assi_research_data.py

# Generate emergent benchmark only
py generate_universal_emergent_benchmark.py

# Run the standalone classification test (11 standard domains)
py verify_assi_classification.py

# Run the standalone robotic multi-modal test (8 domains)
py verify_robotic_discovery_assi.py
```

---

## 📁 File Reference

| File | Purpose |
|------|---------|
| `core/assi_sensing_engine.py` | Core ASSI engine — classify, detect, summarise |
| `generate_assi_research_data.py` | Generates static NSW Showcase classification data |
| `generate_universal_emergent_benchmark.py` | Generates 6-domain time-series transition data |
| `verify_assi_classification.py` | Standalone benchmark (11 standard domains) |
| `verify_robotic_discovery_assi.py` | Standalone benchmark (8 robotic domains) |
| `data/assi_research_data.json` | Classification output |
| `data/universal_emergent_benchmark.json` | Phase transition timeseries output |

---

## 🔮 Next Research Steps

1. **Hypothesis Testing:** Define a hypothesis (e.g., "Q-CTRL quantum coherence degrades faster under thermal coupling than electromagnetic coupling") and adjust the entropy inputs to test it
2. **Device Integration:** Connect live sensor streams from lab devices and feed real entropy values into `classify_robotic_system()`
3. **Experiment Loop:** Run the generator with different initial conditions to simulate different experimental scenarios before conducting physical experiments
4. **Expand Domains:** Add new domains from the 2024/2025 NSW Showcase booklets as additional test cases

---

*Generated: May 2026 | AP Phillips Universal Laboratory | OMEGA-CORE ASSI Framework v3.0*
