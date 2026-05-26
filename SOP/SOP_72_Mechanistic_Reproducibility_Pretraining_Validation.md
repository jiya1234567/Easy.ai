# SOP-72: Mechanistic Reproducibility & Causal Validation Protocol

## 1. OBJECTIVE
To establish the operational protocol for executing and interpreting **mechanistic state pretraining validations** on the OMEGA-CORE state-transition engine. This protocol replaces statistical error testing with physical trajectory auditing across biological, atmospheric, and economic manifolds.

---

## 2. SYSTEM OPERATION STEPS

### STEP 1: Launch the Lab Interface
1. Execute the app launcher from the root directory:
   ```cmd
   run_app.bat
   ```
   *Alternative:* Open your terminal in the workspace and execute:
   ```cmd
   py -m streamlit run streamlit_app.py
   ```
2. Open the URL in your browser (default: `http://localhost:8501`).
3. Click the **`🧬 MECHANISTIC REPRODUCIBILITY`** button in the Command Center button grid.

---

### STEP 2: Initiate State Pretraining
1. Navigate to the **`⚡ L7 State Pretraining`** sub-tab.
2. Select your target **Causal Transition Dataset** (e.g., `🧬 Oncology Evolution` or `🌪️ Weather Tipping`) from the drop-down selector.
3. Review the **Telemetry Trajectory Preview** in the expander to inspect the loaded shape and columns (e.g., confirming `KRAS_activation` or `pressure_gradient` variables are loaded).
4. Calibrate your Hyperparameters:
   - **State Learning Rate**: Controls the step size of latent gradient updates ($10^{-5}$ to $10^{-3}$).
   - **Thermodynamic Regularization ($\beta$)**: Adjusts the penalty for physical violations (higher = stricter adherence to the Second Law).
   - **Cooperative Coupling ($g$)**: Adjusts interaction strength across adjacent nodes on the hypergraph.
5. Click **`🚀 INITIATE OMEGA CORE PRETRAINING`**.
6. **Interpret the Telemetry Curves**:
   - **Manifold Loss (Blue Curve)**: Should decay smoothly and asymptotically. Spikes indicate high prediction "surprise" at phase transition boundaries.
   - **Thermodynamic Entropy (Red Curve)**: Tracks disorder boundaries. A successful pretraining should show convergence under the defined $\beta$ envelope.
   - **Epistemic Tension (Green Curve)**: Tracks adversarial convergence. A rising curve that stabilizes near $80\text{--}95\%$ indicates a healthy tension between the physics and biology watchdogs.

---

### STEP 3: Run the 10 Essential Tests Suite
1. Navigate to the **`🧪 10 Essential Tests Suite`** sub-tab.
2. Choose your **Target State Manifold to Test** (e.g., `Oncology (Pathology)`).
3. Click **`🧪 RUN MECHANISTIC FIDELITY SUITE`**.
4. **Interpret the Validation Results**:
   - **Overall Mechanistic Fidelity**: A composite score of causal reproduction accuracy. Target thresholds:
     - $> 90\%$ (🟢 PASSED): Mechanistically sound causal pathway reproduction.
     - $80\text{--}90\%$ (🟢 STABLE): Safe operating envelope with marginal variance.
     - $< 80\%$ (🔴 DRIFT): Manifold misalignment; recalibration required.
   - **Test 1 (Counterfactual Validity)**: Confirms if applying an intervention ($do(X)$) shifts the trajectory correctly.
   - **Test 3 (Mechanistic Reproduction)**: Validates if the exact biochemical pathway steps are reproduced (rather than statistical classification).
   - **Test 6 (Phase Transition Detection)**: Ensures tipping hazards (like storm lock-in or panic cascades) are detected early.

---

### STEP 4: Stress-Test via Causal Perturbations
1. Navigate to the **`🌪️ Causal Perturbation Playpen`** sub-tab.
2. Select an active **Domain** (e.g., `Oncology (Pathology)`) and choose a **Perturbation Vector** (e.g., `Oxygen Depletion (Hypoxia)`).
3. Adjust the **Perturbation Stress Level** slider:
   - **$0.0 \to 0.3$ (Equilibrium)**: Low stress; the system remains in its stable basin.
   - **$0.4 \to 0.7$ (Adaptive)**: Metabolic or dynamic structural shifts occur to resist stress.
   - **$0.8 \to 1.0$ (Critical)**: Tipping points are crossed; bifurcation risk triggers a warning.
4. Click **`⚡ PERTURB & RECALIBRATE TRAJECTORY`**.
5. **Interpret the Dynamic Waterfall Trace**:
   - Inspect the **Thermodynamic Metrics Recalibration** metrics ($H, \kappa, \eta, \mathcal{B}$) to quantify the exact physical state shifts.
   - Review the **Dynamic Mechanistic Causal Cascade**: The engine highlights the active biochemical or structural step triggered under your stress level (e.g., showing the transition from *Hypoxia* $\to$ *Warburg Glycolysis* $\to$ *Clonal Resistance*).

---

## 3. METRIC INTERPRETATION MANUAL

| Metric | Scientific Meaning | High Value Effect | Low Value Effect |
| :--- | :--- | :--- | :--- |
| **Shannon Entropy ($H$)** | Structural disorder / clonal heterogeneity | Highly complex, unstable, multi-attractor state (e.g., drug resistance). | Compressible, highly ordered, predictable state (e.g., homeostatic tissue). |
| **Phase Coherence ($\kappa$)** | Systemic alignment & synchronization | Critical sync; high feedback loop sensitivity (e.g., panic selling, seizure, storm lock-in). | Decoupled elements; high noise, low collective coordination. |
| **Emergence Order ($\eta$)** | Level of self-organizing cooperative dynamics | Emergence of macro-scale structures (e.g., angiogenesis, cyclonic eye). | Dissipative noise; raw atomic/molecular scattering. |
| **Bifurcation Hazard ($\mathcal{B}$)** | Proximity to a critical tipping hazard | High threat of systemic state collapse or abrupt transition (Tipping Point). | Low risk; system is protected by strong homeostatic attractors. |
| **Reducibility Score** | Computational compressibility | Analytical math/formulas can shortcut prediction (Kepler orbit). | Irreducible; requires step-by-step unfolding simulation (Weather, cancer). |
