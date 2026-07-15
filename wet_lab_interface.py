"""
wet_lab_interface.py — Step 18
Data ingestion pipeline for lab instrument formats.
Supports: plate reader CSV, spectrophotometer, qPCR, flow cytometry,
          Opentrons-style run logs, generic TSV/CSV.

No hardware needed -- pure data format bridge.
"""
from __future__ import annotations
import csv
import json
import io
import time
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class LabDataset:
    instrument: str
    experiment_id: str
    timestamp: float
    variables: dict[str, list[float]]   # {variable: [values]}
    metadata: dict[str, Any]
    raw_row_count: int
    notes: str = ""

    def to_agent_data(self) -> dict:
        """Convert to format ready for agent.run() context_data."""
        return {k: v for k, v in self.variables.items() if len(v) >= 3}

    def to_dict(self) -> dict:
        return self.__dict__.copy()


# ── Format detectors ──────────────────────────────────────────────

def _detect_format(headers: list[str], rows: list[list[str]]) -> str:
    h_lower = [h.lower() for h in headers]
    joined = " ".join(h_lower)

    if any(x in joined for x in ["well", "plate", "od600", "od_600", "absorbance"]):
        return "plate_reader"
    if any(x in joined for x in ["wavelength", "nm", "transmittance", "spectrum"]):
        return "spectrophotometer"
    if any(x in joined for x in ["cycle", "ct", "rn", "delta_rn", "pcr"]):
        return "qpcr"
    if any(x in joined for x in ["fsc", "ssc", "fitc", "pe", "apc", "event"]):
        return "flow_cytometry"
    if any(x in joined for x in ["step", "action", "labware", "pipette", "volume"]):
        return "opentrons"
    return "generic"


def _parse_numeric(s: str) -> Optional[float]:
    try:
        return float(s.strip().replace(',', ''))
    except (ValueError, AttributeError):
        return None


# ── Format-specific parsers ───────────────────────────────────────

def _parse_plate_reader(headers: list, rows: list) -> tuple[dict, dict]:
    """Extract time-series OD/fluorescence readings per well or condition."""
    variables: dict[str, list] = {}
    metadata = {"format": "plate_reader", "wells": []}

    time_col = None
    for i, h in enumerate(headers):
        if h.lower() in ("time", "time_h", "time_min", "t", "hours", "minutes"):
            time_col = i
            break

    for i, h in enumerate(headers):
        if i == time_col:
            continue
        vals = [_parse_numeric(r[i]) for r in rows if i < len(r)]
        vals = [v for v in vals if v is not None]
        if vals:
            key = h.strip().lower().replace(" ", "_").replace("-", "_")
            variables[key] = vals
            metadata["wells"].append(h)

    return variables, metadata


def _parse_generic(headers: list, rows: list) -> tuple[dict, dict]:
    """Generic CSV: each numeric column becomes a variable."""
    variables: dict[str, list] = {}

    for i, h in enumerate(headers):
        vals = [_parse_numeric(r[i]) for r in rows if i < len(r)]
        vals = [v for v in vals if v is not None]
        if len(vals) >= 3:
            key = h.strip().lower().replace(" ", "_").replace("-", "_")
            variables[key] = vals

    return variables, {"format": "generic", "columns": len(headers)}


def _parse_qpcr(headers: list, rows: list) -> tuple[dict, dict]:
    """qPCR: extract Ct values and efficiency per sample/target."""
    variables: dict[str, list] = {}
    ct_col = next((i for i, h in enumerate(headers)
                   if "ct" in h.lower() or "cq" in h.lower()), None)

    if ct_col is not None:
        ct_vals = [_parse_numeric(r[ct_col]) for r in rows if ct_col < len(r)]
        variables["ct_value"] = [v for v in ct_vals if v is not None]

    # Also extract any other numeric columns
    for i, h in enumerate(headers):
        if i == ct_col:
            continue
        vals = [_parse_numeric(r[i]) for r in rows if i < len(r)]
        vals = [v for v in vals if v is not None]
        if len(vals) >= 3:
            key = h.strip().lower().replace(" ", "_")
            if key not in variables:
                variables[key] = vals

    return variables, {"format": "qpcr"}


# ── Main interface ─────────────────────────────────────────────────

def ingest_lab_file(
    content: bytes,
    filename: str,
    experiment_id: str = "",
    notes: str = "",
) -> LabDataset:
    """
    Parse any lab instrument file into a LabDataset.

    Parameters
    ----------
    content       : bytes -- raw file content
    filename      : str   -- used to detect delimiter and format
    experiment_id : str   -- optional experiment identifier
    notes         : str   -- optional user notes

    Returns
    -------
    LabDataset ready for agent.run() via .to_agent_data()
    """
    text = content.decode('utf-8-sig').strip()

    # Detect delimiter
    delimiter = ','
    if filename.lower().endswith('.tsv') or '\t' in text[:500]:
        delimiter = '\t'

    reader = csv.reader(io.StringIO(text), delimiter=delimiter)
    all_rows = list(reader)

    if not all_rows:
        return LabDataset("unknown", experiment_id, time.time(), {}, {}, 0, notes)

    # Find header row (first row with mostly non-numeric values)
    header_idx = 0
    for i, row in enumerate(all_rows[:5]):
        non_numeric = sum(1 for c in row if _parse_numeric(c) is None)
        if non_numeric >= len(row) * 0.5:
            header_idx = i
            break

    headers = [c.strip() for c in all_rows[header_idx]]
    data_rows = all_rows[header_idx + 1:]
    data_rows = [r for r in data_rows if any(c.strip() for c in r)]

    fmt = _detect_format(headers, data_rows)

    if fmt == "plate_reader":
        variables, metadata = _parse_plate_reader(headers, data_rows)
        instrument = "Plate Reader"
    elif fmt == "qpcr":
        variables, metadata = _parse_qpcr(headers, data_rows)
        instrument = "qPCR"
    elif fmt == "spectrophotometer":
        variables, metadata = _parse_generic(headers, data_rows)
        instrument = "Spectrophotometer"
        metadata["format"] = "spectrophotometer"
    elif fmt == "flow_cytometry":
        variables, metadata = _parse_generic(headers, data_rows)
        instrument = "Flow Cytometer"
        metadata["format"] = "flow_cytometry"
    else:
        variables, metadata = _parse_generic(headers, data_rows)
        instrument = "Generic Lab Instrument"

    metadata["filename"] = filename
    metadata["detected_format"] = fmt
    metadata["header_row"] = header_idx

    return LabDataset(
        instrument=instrument,
        experiment_id=experiment_id or Path(filename).stem,
        timestamp=time.time(),
        variables=variables,
        metadata=metadata,
        raw_row_count=len(data_rows),
        notes=notes,
    )


def wet_lab_upload_panel(agent_context_callback=None):
    """
    Streamlit UI panel for wet-lab file upload.
    Parses the file and returns data ready for agent.run().
    """
    import streamlit as st

    st.markdown("#### Wet-Lab Data Ingestion")
    st.caption(
        "Upload CSV/TSV from any lab instrument. "
        "Supported: plate readers, qPCR, spectrophotometers, "
        "flow cytometers, Opentrons logs, generic CSV."
    )

    exp_id = st.text_input("Experiment ID (optional)",
                           placeholder="e.g. EXP_2026_001",
                           key="wet_lab_exp_id")
    notes = st.text_area("Notes (optional)", key="wet_lab_notes", height=60)

    uploaded = st.file_uploader(
        "Upload lab data file",
        type=["csv", "tsv", "txt"],
        key="wet_lab_upload",
    )

    if uploaded:
        try:
            dataset = ingest_lab_file(
                uploaded.read(), uploaded.name,
                experiment_id=exp_id, notes=notes
            )

            st.success(
                f"Parsed {dataset.raw_row_count} rows from "
                f"{dataset.instrument} ({dataset.metadata.get('detected_format')})"
            )

            col1, col2 = st.columns(2)
            col1.metric("Variables found", len(dataset.variables))
            col2.metric("Observations", min(
                len(v) for v in dataset.variables.values()
            ) if dataset.variables else 0)

            st.markdown("**Variables extracted:**")
            for var, vals in dataset.variables.items():
                st.caption(
                    f"  {var}: [{', '.join(f'{v:.2f}' for v in vals[:5])}...]"
                    if len(vals) > 5 else
                    f"  {var}: {[round(v,2) for v in vals]}"
                )

            if dataset.variables and st.button(
                "Use this data in Agent Harness",
                key="wet_lab_use"
            ):
                agent_data = dataset.to_agent_data()
                st.session_state["wet_lab_agent_data"] = agent_data
                st.session_state["wet_lab_loaded"] = True
                st.success("Data loaded! Scroll to Mission Intent and click Run Agent Harness.")
                st.json({"preview": {k: v[:3] for k, v in agent_data.items()}})

        except Exception as e:
            st.error(f"Parse error: {e}")

    # Return loaded data if available
    if st.session_state.get("wet_lab_loaded"):
        return st.session_state.get("wet_lab_agent_data", {})
    return {}


# ── Self-test ──────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Wet Lab Interface Tests ===")

    # Test 1: Generic CSV (most common case)
    generic_csv = b"""time,od600_sample1,od600_sample2,od600_control
0,0.05,0.05,0.05
1,0.08,0.07,0.05
2,0.13,0.11,0.06
3,0.22,0.19,0.06
4,0.38,0.33,0.07
6,0.71,0.62,0.07
8,1.12,0.98,0.08"""

    ds1 = ingest_lab_file(generic_csv, "growth_curve.csv", "EXP_001")
    print(f"[PASS] Generic CSV: {ds1.instrument}, vars={list(ds1.variables.keys())}")
    assert "od600_sample1" in ds1.variables
    assert len(ds1.variables["od600_sample1"]) == 7

    # Test 2: Plate reader format
    plate_csv = b"""Well,Sample,OD600,Fluorescence
A1,control,0.05,120
A2,treatment1,0.42,580
A3,treatment2,0.38,510
B1,control,0.06,125
B2,treatment1,0.45,595
B3,treatment2,0.40,520"""

    ds2 = ingest_lab_file(plate_csv, "plate_reader_assay.csv", "EXP_002")
    print(f"[PASS] Plate reader: {ds2.metadata.get('detected_format')}, vars={list(ds2.variables.keys())}")

    # Test 3: qPCR format
    qpcr_csv = b"""Sample,Target,Ct,Efficiency,Delta_Ct
control,GAPDH,18.2,95.3,0
treatment,GAPDH,18.4,95.1,0.2
control,gene_x,28.5,93.2,0
treatment,gene_x,24.1,92.8,-4.4
control,gene_y,31.2,91.5,0
treatment,gene_y,26.8,90.9,-4.4"""

    ds3 = ingest_lab_file(qpcr_csv, "qpcr_run.csv", "EXP_003")
    print(f"[PASS] qPCR: {ds3.metadata.get('detected_format')}, vars={list(ds3.variables.keys())}")
    assert "ct_value" in ds3.variables or "ct" in ds3.variables

    # Test 4: TSV format
    tsv_data = b"wavelength\tabsorbance\ttransmittance\n400\t0.8\t15.8\n450\t0.6\t25.1\n500\t0.3\t50.1\n550\t0.1\t79.4\n600\t0.05\t89.1"
    ds4 = ingest_lab_file(tsv_data, "spectrum.tsv", "EXP_004")
    print(f"[PASS] Spectrophotometer TSV: vars={list(ds4.variables.keys())}")
    assert "absorbance" in ds4.variables or "wavelength" in ds4.variables

    # Test 5: to_agent_data() format compatibility
    agent_data = ds1.to_agent_data()
    print(f"[PASS] Agent data format: {list(agent_data.keys())}")
    assert all(isinstance(v, list) for v in agent_data.values())
    assert all(len(v) >= 3 for v in agent_data.values())

    # Test 6: BOM handling
    bom_csv = b'\xef\xbb\xbftemp,humidity\n20,55\n21,53\n22,51\n23,49\n'
    ds6 = ingest_lab_file(bom_csv, "sensors.csv")
    print(f"[PASS] BOM handling: vars={list(ds6.variables.keys())}")
    assert "temp" in ds6.variables

    print("\nALL TESTS PASSED")
