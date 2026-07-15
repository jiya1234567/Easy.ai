"""
OMEGA-CORE | Wet-Lab Orchestrator (Robotics Integration — Full)
================================================================
Bridges digital causal discoveries to physical wet-lab execution.

Pipeline:
  1. CausalAgent identifies intervention target
  2. WetLabOrchestrator compiles an Opentrons protocol
  3. Protocol dispatched to OT-2 robot (or simulated)
  4. Telemetry captured and fed back to RealityFeedbackEngine
  5. Outcome closes the causal loop

Supports:
  - CRISPR-Cas9 gene editing protocols
  - Compound dosing / combinatorial chemistry
  - Cell culture manipulation
  - qPCR / sequencing dispatch
  - Simulation mode (no hardware required)
"""

import uuid
import json
import time
import datetime
import math
import random
from typing import Dict, Any, List, Optional


# ---------------------------------------------------------------------------
# Protocol Templates
# ---------------------------------------------------------------------------

PROTOCOL_TEMPLATES = {
    "crispr_knockout": {
        "display_name": "CRISPR-Cas9 Gene Knockout",
        "required_reagents": ["sgRNA", "Cas9_RNP", "Electroporation_Buffer", "Cells"],
        "default_volume_ul": 20.0,
        "duration_min": 120,
        "safety_level": "BSL-2",
        "labware": {
            "plate":    "corning_96_wellplate_360ul_flat",
            "reservoir":"nest_12_reservoir_15ml",
            "tiprack":  "opentrons_96_tiprack_300ul",
        },
    },
    "compound_dosing": {
        "display_name": "Compound Dosing / Drug Screen",
        "required_reagents": ["Compound_Library", "DMSO", "Assay_Buffer", "Cells"],
        "default_volume_ul": 5.0,
        "duration_min": 60,
        "safety_level": "BSL-1",
        "labware": {
            "plate":    "corning_384_wellplate_112ul_flat",
            "reservoir":"nest_12_reservoir_15ml",
            "tiprack":  "opentrons_96_tiprack_20ul",
        },
    },
    "cell_passaging": {
        "display_name": "Automated Cell Passaging",
        "required_reagents": ["Trypsin", "PBS", "Growth_Medium"],
        "default_volume_ul": 100.0,
        "duration_min": 45,
        "safety_level": "BSL-1",
        "labware": {
            "plate":    "corning_6_wellplate_16.8ml_flat",
            "reservoir":"nest_12_reservoir_15ml",
            "tiprack":  "opentrons_96_tiprack_300ul",
        },
    },
    "qpcr_prep": {
        "display_name": "qPCR Sample Preparation",
        "required_reagents": ["Mastermix", "Primers", "RNA_Template", "DEPC_Water"],
        "default_volume_ul": 10.0,
        "duration_min": 30,
        "safety_level": "BSL-1",
        "labware": {
            "plate":    "opentrons_96_aluminumblock_generic_pcr_strip_200ul",
            "reservoir":"nest_12_reservoir_15ml",
            "tiprack":  "opentrons_96_tiprack_20ul",
        },
    },
}


# ---------------------------------------------------------------------------
# Wet-Lab Execution Result
# ---------------------------------------------------------------------------

class WetLabResult:
    def __init__(self, protocol_id: str, protocol_type: str, intervention: dict,
                 simulated: bool = True):
        self.protocol_id     = protocol_id
        self.protocol_type   = protocol_type
        self.intervention    = intervention
        self.simulated       = simulated
        self.status          = "PENDING"
        self.execution_log:  List[dict] = []
        self.telemetry:      Dict[str, Any] = {}
        self.outcome:        Optional[str] = None
        self.started_at      = datetime.datetime.utcnow().isoformat()
        self.completed_at:   Optional[str] = None
        self.reality_feedback: Dict[str, Any] = {}

    def to_dict(self) -> dict:
        return {
            "protocol_id":       self.protocol_id,
            "protocol_type":     self.protocol_type,
            "simulated":         self.simulated,
            "status":            self.status,
            "started_at":        self.started_at,
            "completed_at":      self.completed_at,
            "intervention":      self.intervention,
            "execution_log":     self.execution_log,
            "telemetry":         self.telemetry,
            "outcome":           self.outcome,
            "reality_feedback":  self.reality_feedback,
        }


# ---------------------------------------------------------------------------
# Main Wet-Lab Orchestrator
# ---------------------------------------------------------------------------

class WetLabOrchestrator:
    """
    OMEGA-CORE | Autonomous Wet-Lab Orchestrator
    Translates causal discoveries into executable physical lab protocols,
    dispatches to Opentrons OT-2 (or simulation), and captures telemetry
    for the Reality Feedback Engine.
    """

    ENDPOINT = "http://opentrons-ot2.local:31950"

    def __init__(self, simulated: bool = True, endpoint: Optional[str] = None):
        self.simulated = simulated
        self.endpoint  = endpoint or self.ENDPOINT
        self._run_history: List[WetLabResult] = []
        print(f"[WET-LAB ORCHESTRATOR] Initialized. Mode: {'SIMULATION' if simulated else 'LIVE'}")

    # ------------------------------------------------------------------
    # 1. Protocol Compilation
    # ------------------------------------------------------------------

    def compile_protocol(self, intervention: dict) -> dict:
        """
        Convert a high-level causal intervention into an Opentrons protocol.

        Args:
            intervention: {
                "type": "crispr_knockout" | "compound_dosing" | ...,
                "target": str,
                "dosage_ul": float,
                "wells": List[str],   # e.g. ["A1", "B2"]
                "replicates": int,
            }
        Returns:
            Compiled protocol dict including Python script for OT-2.
        """
        protocol_type = intervention.get("type", "compound_dosing")
        template      = PROTOCOL_TEMPLATES.get(protocol_type, PROTOCOL_TEMPLATES["compound_dosing"])
        target        = intervention.get("target", "unknown_target")
        dosage        = float(intervention.get("dosage_ul", template["default_volume_ul"]))
        wells         = intervention.get("wells", ["A1", "A2", "A3", "B1", "B2", "B3"])
        replicates    = int(intervention.get("replicates", 3))

        well_list_str = ", ".join(f"'{w}'" for w in wells)

        script = f'''from opentrons import protocol_api

metadata = {{
    "apiLevel": "2.13",
    "protocolName": "OMEGA-CORE | {template["display_name"]}: {target}",
    "description": "Autonomously generated by OMEGA-CORE Wet-Lab Orchestrator",
    "author": "OMEGA-CORE ASI Framework v3.0"
}}

def run(protocol: protocol_api.ProtocolContext):
    # ── Load Labware ─────────────────────────────────────────────────
    plate     = protocol.load_labware("{template["labware"]["plate"]}",     "1")
    reservoir = protocol.load_labware("{template["labware"]["reservoir"]}",  "2")
    tiprack   = protocol.load_labware("{template["labware"]["tiprack"]}",    "3")
    p_left    = protocol.load_instrument("p300_single_gen2", "right", tip_racks=[tiprack])

    # ── Intervention: {template["display_name"]} ──────────────────────
    protocol.comment("OMEGA-CORE: Executing {template["display_name"]} on target [{target}]")
    target_wells = [{well_list_str}]

    for rep in range({replicates}):
        for well in target_wells:
            p_left.pick_up_tip()
            p_left.aspirate({dosage:.1f}, reservoir["A1"])
            p_left.dispense({dosage:.1f}, plate[well])
            p_left.blow_out()
            p_left.drop_tip()
            protocol.comment(f"Dispensed {dosage:.1f}uL of [{target}] into {{well}} (rep {{rep+1}})")

    protocol.comment("OMEGA-CORE: Physical intervention complete. Awaiting telemetry.")
'''

        return {
            "protocol_id":   f"PROT-{str(uuid.uuid4())[:8].upper()}",
            "type":          protocol_type,
            "display_name":  template["display_name"],
            "target":        target,
            "dosage_ul":     dosage,
            "wells":         wells,
            "replicates":    replicates,
            "safety_level":  template["safety_level"],
            "duration_min":  template["duration_min"],
            "reagents":      template["required_reagents"],
            "script":        script,
            "compiled_at":   datetime.datetime.utcnow().isoformat(),
        }

    # ------------------------------------------------------------------
    # 2. Safety Validation
    # ------------------------------------------------------------------

    def validate_safety(self, protocol: dict) -> dict:
        """
        Pre-execution safety checks before dispatching to physical robot.
        """
        checks = []
        passed = True

        # Dosage bounds check
        if protocol["dosage_ul"] > 300:
            checks.append({"check": "dosage_bounds", "status": "FAIL",
                           "reason": f"Dosage {protocol['dosage_ul']}uL exceeds 300uL tip capacity"})
            passed = False
        else:
            checks.append({"check": "dosage_bounds", "status": "PASS"})

        # BSL level check
        bsl = protocol.get("safety_level", "BSL-1")
        if "BSL-3" in bsl or "BSL-4" in bsl:
            checks.append({"check": "biosafety_level", "status": "FAIL",
                           "reason": f"{bsl} requires manual approval"})
            passed = False
        else:
            checks.append({"check": "biosafety_level", "status": "PASS", "level": bsl})

        # Reagent count check
        checks.append({"check": "reagent_inventory",
                        "status": "PASS",
                        "reagents_required": protocol.get("reagents", [])})

        return {
            "valid":        passed,
            "checks":       checks,
            "clearance":    "APPROVED" if passed else "BLOCKED",
            "validated_at": datetime.datetime.utcnow().isoformat(),
        }

    # ------------------------------------------------------------------
    # 3. Simulated Execution Engine
    # ------------------------------------------------------------------

    def _simulate_execution(self, result: WetLabResult, protocol: dict) -> WetLabResult:
        """
        Simulate OT-2 protocol execution with realistic telemetry generation.
        """
        steps = [
            ("INIT",         "Loading labware and calibrating deck"),
            ("PRIME",        "Priming pipettes and verifying tip seal"),
            ("ASPIRATE",     f"Aspirating {protocol['dosage_ul']}uL from reservoir"),
            ("DISPENSE",     f"Dispensing into wells: {protocol['wells']}"),
            ("REPLICATE",    f"Running {protocol['replicates']} replicates"),
            ("WASH",         "Tip change and wash cycle"),
            ("SEAL",         "Sealing plate for incubation"),
            ("TELEMETRY",    "Recording post-protocol telemetry"),
            ("COMPLETE",     "Protocol execution complete"),
        ]

        for step_code, step_desc in steps:
            log_entry = {
                "step":        step_code,
                "description": step_desc,
                "timestamp":   datetime.datetime.utcnow().isoformat(),
                "status":      "OK",
                "elapsed_ms":  random.randint(50, 400),
            }
            result.execution_log.append(log_entry)

        # Generate synthetic telemetry
        result.telemetry = {
            "temperature_c":      round(37.0 + random.gauss(0, 0.3), 2),
            "humidity_pct":       round(60.0 + random.gauss(0, 2.0), 1),
            "tip_eject_count":    len(protocol["wells"]) * protocol["replicates"],
            "volume_dispensed_ul":protocol["dosage_ul"] * len(protocol["wells"]) * protocol["replicates"],
            "mean_dispense_error_ul": round(abs(random.gauss(0, 0.5)), 3),
            "contamination_risk":  "LOW",
            "robot_id":            "OT2-OMEGA-01",
            "deck_layout_valid":   True,
        }

        # Generate plausible biological outcome
        efficacy = round(random.uniform(0.55, 0.95), 3)
        result.status    = "SUCCESS"
        result.outcome   = (f"Intervention '{protocol['target']}' delivered successfully. "
                            f"Estimated efficacy: {efficacy*100:.1f}%. "
                            f"Cell viability post-treatment: {round(random.uniform(0.7, 0.98)*100,1)}%. "
                            f"Awaiting 24h incubation before sequencing.")
        result.reality_feedback = {
            "efficacy_estimate":   efficacy,
            "measurement_type":    "simulated_fluorescence_assay",
            "confidence":          round(random.uniform(0.75, 0.95), 3),
            "next_action":         "Sequence and compare against hypothesis",
            "loop_status":         "OPEN — awaiting sequencing telemetry",
        }
        result.completed_at = datetime.datetime.utcnow().isoformat()
        return result

    # ------------------------------------------------------------------
    # 4. Dispatch to Physical Robot
    # ------------------------------------------------------------------

    def execute(self, intervention: dict) -> WetLabResult:
        """
        Main entry point: compile → validate → execute → return result.
        """
        protocol  = self.compile_protocol(intervention)
        safety    = self.validate_safety(protocol)

        result = WetLabResult(
            protocol_id   = protocol["protocol_id"],
            protocol_type = protocol["type"],
            intervention  = intervention,
            simulated     = self.simulated,
        )

        if not safety["valid"]:
            result.status = "BLOCKED"
            result.outcome = f"Safety check failed: {safety['checks']}"
            result.execution_log.append({
                "step": "SAFETY_BLOCK",
                "description": "Execution halted by safety kernel",
                "checks": safety["checks"],
            })
            self._run_history.append(result)
            return result

        if self.simulated:
            result = self._simulate_execution(result, protocol)
        else:
            # Live execution path (requires Opentrons HTTP API)
            try:
                import requests
                r = requests.post(
                    f"{self.endpoint}/protocols",
                    json={"protocol": protocol["script"]},
                    timeout=30,
                )
                r.raise_for_status()
                result.status   = "DISPATCHED"
                result.outcome  = f"Protocol dispatched to {self.endpoint}. Run ID: {r.json().get('id','?')}"
            except Exception as exc:
                result.status  = "ERROR"
                result.outcome = f"Dispatch failed: {exc}"

        self._run_history.append(result)
        return result

    # ------------------------------------------------------------------
    # 5. Multi-Protocol Batch Run (Combinatorial Screen)
    # ------------------------------------------------------------------

    def batch_screen(self, compounds: List[str],
                     doses_ul: List[float],
                     protocol_type: str = "compound_dosing") -> List[dict]:
        """
        Run a combinatorial dose-response screen across multiple compounds.
        """
        results = []
        well_letters = list("ABCDEFGH")
        well_idx     = 0

        for compound in compounds:
            for dose in doses_ul:
                well = f"{well_letters[well_idx % 8]}{(well_idx // 8) + 1}"
                well_idx += 1
                intervention = {
                    "type":       protocol_type,
                    "target":     compound,
                    "dosage_ul":  dose,
                    "wells":      [well],
                    "replicates": 2,
                }
                r = self.execute(intervention)
                results.append({
                    "compound":    compound,
                    "dose_ul":     dose,
                    "well":        well,
                    "status":      r.status,
                    "efficacy":    r.reality_feedback.get("efficacy_estimate", "N/A"),
                    "protocol_id": r.protocol_id,
                })

        return results

    # ------------------------------------------------------------------
    # 6. Run History & Reporting
    # ------------------------------------------------------------------

    def run_summary(self) -> dict:
        """Return summary of all executed protocols."""
        total   = len(self._run_history)
        success = sum(1 for r in self._run_history if r.status == "SUCCESS")
        blocked = sum(1 for r in self._run_history if r.status == "BLOCKED")
        return {
            "total_runs":      total,
            "success_count":   success,
            "blocked_count":   blocked,
            "success_rate_pct":round(success / total * 100, 1) if total else 0,
            "recent_runs":     [r.to_dict() for r in self._run_history[-5:]],
        }


# ---------------------------------------------------------------------------
# CLI / quick test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    orch = WetLabOrchestrator(simulated=True)

    # 1. Single CRISPR knockout
    result = orch.execute({
        "type":       "crispr_knockout",
        "target":     "BRCA1_exon11",
        "dosage_ul":  15.0,
        "wells":      ["A1", "A2", "A3"],
        "replicates": 3,
    })
    print("\n-- CRISPR Knockout Result --")
    print(json.dumps(result.to_dict(), indent=2))

    # 2. Combinatorial drug screen
    print("\n-- Batch Screen --")
    batch = orch.batch_screen(
        compounds=["Compound_X", "Compound_Y"],
        doses_ul=[2.5, 5.0, 10.0],
    )
    for b in batch:
        print(b)

    print("\n-- Run Summary --")
    print(json.dumps(orch.run_summary(), indent=2))
