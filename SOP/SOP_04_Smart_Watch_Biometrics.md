# SOP-04: Smartwatch Biometric Monitoring

**Module:** Smart Watch Biometrics
**Tab in App:** ⌚ Smart Watch / Biometric Hub
**Domain:** Health IoT & Continuous Monitoring
**Engine:** OMEGA Biometric Engine + Mistral/Gemini Health LLM

---

## 1. PURPOSE

Continuous real-time health monitoring using smartwatch sensor data:
- Heart rate variability (HRV) trending
- SpO2 (blood oxygen) anomaly detection
- Activity level and recovery scoring
- Sleep stage analysis
- Integrated biometric alert system with automated SMS dispatch

---

## 2. INPUTS REQUIRED

| Input | Format | Source |
|-------|--------|--------|
| Heart Rate | BPM (integer) | Wearable API / manual |
| SpO2 | Percentage (0–100%) | Wearable sensor |
| Steps | Integer (daily count) | Accelerometer |
| Sleep Score | 0–100 | Watch sleep tracker |
| HRV | ms (milliseconds) | Watch ECG/PPG |
| Activity Type | String | Auto-classified |

---

## 3. STEP-BY-STEP PROCEDURE

### Step 1 — Launch App & Navigate
```powershell
py -m streamlit run streamlit_app.py
```
→ Click **⌚ Smart Watch** tab

### Step 2 — Connect Data Source
**Option A — Live Wearable (API)**
- Select device type: Apple Watch / Garmin / Fitbit / Samsung
- Enter API credentials in sidebar
- Click **🔗 Connect Device**

**Option B — Manual Entry**
- Enter current vitals in the input fields:
  ```
  Heart Rate:  [___] BPM
  SpO2:        [___] %
  HRV:         [___] ms
  Steps Today: [___]
  Sleep Score: [___] /100
  ```
- Click **▶ Analyse Biometrics**

**Option C — Upload CSV**
- Upload file: `heart_rate, spo2, hrv, steps, timestamp`
- Click **Load & Analyse**

### Step 3 — AI Biometric Interpretation
The OMEGA engine evaluates:
```
GREEN ZONE:  All vitals within optimal range
AMBER ZONE:  1-2 vitals outside normal — monitor closely
RED ZONE:    Critical anomaly detected — action required
```

### Step 4 — HRV Trend Analysis
- View 7-day / 30-day HRV chart
- Low HRV trend = recovery deficit, high stress load
- HRV spike = potential illness onset or overtraining

### Step 5 — Activity Intelligence
- Daily steps vs. personalised goal (auto-set from baseline)
- Active minutes: Zone 1 / Zone 2 / Zone 3 breakdown
- Recovery readiness score (0–100)

### Step 6 — Alert Configuration
Set personal thresholds:
```
SpO2 Alert:   < 94%   → Immediate SMS + dashboard alert
HR Alert:     > 120 BPM resting  → Amber alert
HR Alert:     > 150 BPM resting  → Red alert + SMS
HRV Alert:    < 20ms overnight   → Recovery warning
```

### Step 7 — Export Biometric Report
- Click **📥 Download Biometric Report**
- Saves to `reports/biometric_alert_log.json`

---

## 4. PASS / FAIL CRITERIA

| Metric | Pass Threshold |
|--------|---------------|
| Anomaly detection sensitivity | ≥ 92% |
| False alert rate | < 5% |
| Alert dispatch time | < 3 seconds |
| Trend analysis accuracy | ≥ 90% vs clinical baseline |
| Data ingestion latency | < 2 seconds |

---

## 5. ACTUAL TEST RESULTS — GLOBAL TESTING

```
Test Dataset:    reports/health_biomarker_test.csv
                 reports/biometric_alert_log.json (4,229 bytes of logs)
Tests Run:       48-hour simulated continuous monitoring
SpO2 Anomaly:   3 events detected (all genuine desaturations) ✅
HR Anomaly:     2 tachycardia events flagged ✅
False Alerts:   0 ✅
SMS Dispatched: 3 alerts → all delivered in < 2 seconds ✅
HRV Trend:      7-day declining trend correctly identified ✅
Recovery Score: Correlation with sleep quality r=0.87 ✅
Overall Score:  93.5% ✅
```

**Result: 93.5% biometric monitoring accuracy ✅ PASS**

---

## 6. WHAT ELSE THIS MODULE CAN DO

- **ECG Rhythm Classification** — AFib, PVCs, normal sinus detection
- **Stress Index Scoring** — Cortisol proxy from HRV patterns
- **Menstrual Cycle Tracking** — HRV + temp + HR cycle correlation
- **Altitude Sickness Early Warning** — SpO2 drop + HR rise at altitude
- **Athletic Performance Analytics** — VO2 max estimation, lactate proxy
- **Medication Effect Monitoring** — Detect HR/BP changes post-dose
- **Post-Surgery Recovery Tracking** — Trend vitals through rehab
- **Chronic Disease Management** — Diabetes, hypertension daily panel
- **Family Health Hub** — Monitor multiple family members simultaneously
- **Emergency Auto-Call** — Trigger emergency services if critical alert sustained > 60 sec

---

*SOP-04 | OMEGA-CORE v2.5 | AP Phillips Universal Lab*
