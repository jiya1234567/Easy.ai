"""
manual_validator.py
====================
Day 3 deliverable: closes the World Lab prediction->reality loop
via manual CSV/JSON upload rather than an auto feed.

User workflow:
    1. Agent makes a prediction (stored in Reality Anchor)
    2. User runs real experiment / collects real data
    3. User uploads CSV or JSON with actual outcomes
    4. This module matches actual values to pending predictions
    5. RealityAnchor.validate() is called with real numbers
    6. SelfImprovementEngine.propose_calibrations() runs automatically

Streamlit UI function: validation_upload_panel()
Standalone function:   validate_from_file(filepath, reality_anchor)
"""

from __future__ import annotations
import json
import csv
import io
import time
from pathlib import Path
from typing import Any, Optional


def parse_upload(content: bytes, filename: str) -> dict[str, float]:
    """
    Parse uploaded file content into {variable_name: actual_value} dict.

    Supports:
    - CSV with headers: variable,value  OR  variable_name,actual_value
    - JSON: {"variable": value, ...}
    - Single-row CSV: temperature,28.5,humidity,42.0,...

    Parameters
    ----------
    content  : bytes  -- raw file bytes from st.file_uploader
    filename : str    -- original filename (used to detect format)

    Returns
    -------
    dict[str, float] -- {variable_name: actual_value}
    """
    text = content.decode('utf-8-sig').strip()

    if filename.lower().endswith('.json'):
        return _parse_json(text)
    elif filename.lower().endswith('.csv'):
        return _parse_csv(text)
    else:
        # Try JSON first, then CSV
        try:
            return _parse_json(text)
        except Exception:
            return _parse_csv(text)


def _parse_json(text: str) -> dict[str, float]:
    data = json.loads(text)
    if isinstance(data, dict):
        result = {}
        for k, v in data.items():
            try:
                result[str(k).lower()] = float(v)
            except (TypeError, ValueError):
                pass
        return result
    raise ValueError("JSON must be a flat object {variable: value}")


def _parse_csv(text: str) -> dict[str, float]:
    result = {}
    reader = csv.reader(io.StringIO(text))
    rows = list(reader)

    if not rows:
        return result

    # Try header row formats:
    # Format A: variable,value (two columns)
    # Format B: variable_name,actual_value (two columns)
    # Format C: name,measured,unit (three columns, use column 1)
    first_row = [c.strip().lower() for c in rows[0]]

    # Detect flat alternating format: str,num,str,num (single row)
    is_flat = (
        len(rows) == 1 and
        len(first_row) > 2 and
        not _is_numeric(first_row[0]) and
        _is_numeric(first_row[1] if len(first_row) > 1 else '')
    )

    if not is_flat and len(first_row) >= 2 and not _is_numeric(first_row[0]):
        # Has headers
        var_col = 0
        val_col = 1
        for i, h in enumerate(first_row):
            if h in ('value', 'actual', 'actual_value', 'measured',
                     'result', 'outcome', 'reading'):
                val_col = i
                break
        for row in rows[1:]:
            if len(row) > val_col:
                var = row[var_col].strip().lower().replace(' ', '_')
                try:
                    result[var] = float(row[val_col].strip().replace(',', ''))
                except ValueError:
                    pass
    else:
        # No headers -- try single-row key-value pairs: temp,28.5,humidity,42.0
        flat = [c.strip() for row in rows for c in row]
        i = 0
        while i < len(flat) - 1:
            key = flat[i].lower().replace(' ', '_')
            if not _is_numeric(key) and _is_numeric(flat[i + 1]):
                try:
                    result[key] = float(flat[i + 1].replace(',', ''))
                    i += 2
                    continue
                except ValueError:
                    pass
            i += 1

    return result


def _is_numeric(s: str) -> bool:
    try:
        float(s.replace(',', ''))
        return True
    except (ValueError, AttributeError):
        return False


def match_actuals_to_predictions(
    actuals: dict[str, float],
    pending_predictions: list,
) -> list[tuple]:
    """
    Match uploaded actual values to pending predictions.

    A match occurs when a prediction's predicted_variables keys
    overlap with the uploaded actual values.

    Parameters
    ----------
    actuals             : dict[str, float] -- from parse_upload()
    pending_predictions : list[Prediction] -- from RealityAnchor.recent()

    Returns
    -------
    list of (prediction, matched_actuals_dict) tuples
    """
    matches = []
    actuals_lower = {k.lower(): v for k, v in actuals.items()}

    for pred in pending_predictions:
        if pred.validated:
            continue
        pred_vars = {k.lower() for k in pred.predicted_variables.keys()}
        matched = {
            orig_k: actuals_lower[orig_k.lower()]
            for orig_k in pred.predicted_variables.keys()
            if orig_k.lower() in actuals_lower
        }
        if matched:
            matches.append((pred, matched))

    return matches


def validate_from_file(
    filepath: str,
    reality_anchor,
    calibration_engine=None,
) -> dict[str, Any]:
    """
    Standalone (non-Streamlit) validation from a file path.
    Useful for scripted / automated testing.

    Returns summary dict of what was validated.
    """
    path = Path(filepath)
    content = path.read_bytes()
    actuals = parse_upload(content, path.name)

    if not actuals:
        return {"error": "No numeric values found in file", "file": filepath}

    pending = reality_anchor.recent(n=50)
    matches = match_actuals_to_predictions(actuals, pending)

    results = []
    for pred, matched_actuals in matches:
        accuracy = reality_anchor.validate(pred.id, matched_actuals)
        result = {
            "prediction_id": pred.id,
            "agent": pred.agent,
            "accuracy": accuracy,
            "matched_variables": matched_actuals,
            "prediction_text": pred.prediction_text[:100],
        }
        results.append(result)

        if calibration_engine is not None:
            calibration_engine.propose_calibrations(reality_anchor, pred.agent)

    return {
        "file": filepath,
        "actuals_parsed": actuals,
        "predictions_matched": len(results),
        "results": results,
        "timestamp": time.time(),
    }


def validation_upload_panel(reality_anchor, calibration_engine=None):
    """
    Streamlit UI panel for manual upload validation.
    Call this from any tab or from reality_validation_panel().
    """
    import streamlit as st

    st.markdown("#### Upload Actual Outcomes -- Reality Anchor Validation")
    st.caption(
        "Upload a CSV or JSON file with actual measured values. "
        "The system will match them to pending predictions and compute accuracy."
    )

    # Show pending predictions count
    summary = reality_anchor.summary()
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Predictions", summary["total_predictions"])
    col2.metric("Validated", summary["validated"])
    col3.metric("Pending", summary["pending"])

    if summary["pending"] == 0:
        st.info("No pending predictions to validate. Run the Auto-Chain to generate predictions first.")
        return

    st.markdown("---")

    # File format guidance
    with st.expander("File format guide"):
        st.markdown("""
**CSV format (two-column with headers):**
```
variable,value
temperature,28.5
humidity,42.0
pressure,1015.0
```

**CSV format (single row, no headers):**
```
temperature,28.5,humidity,42.0,pressure,1015.0
```

**JSON format:**
```json
{"temperature": 28.5, "humidity": 42.0, "pressure": 1015.0}
```
        """)

    uploaded = st.file_uploader(
        "Upload actual outcome file (CSV or JSON)",
        type=["csv", "json"],
        key="reality_upload",
    )

    if uploaded is not None:
        try:
            actuals = parse_upload(uploaded.read(), uploaded.name)
            if not actuals:
                st.error("No numeric values found in uploaded file. Check the format guide above.")
                return

            st.success(f"Parsed {len(actuals)} actual values: {actuals}")

            pending = reality_anchor.recent(n=50)
            matches = match_actuals_to_predictions(actuals, pending)

            if not matches:
                st.warning(
                    "No pending predictions match the uploaded variables. "
                    f"Uploaded variables: {list(actuals.keys())}. "
                    "Check that variable names match what was used during the agent run."
                )
                return

            st.markdown(f"**Found {len(matches)} matching prediction(s):**")

            for pred, matched_actuals in matches:
                with st.expander(
                    f"Prediction {pred.id} — {pred.agent} — "
                    f"{pred.prediction_text[:60]}..."
                ):
                    st.markdown("**Predicted values:**")
                    st.json(pred.predicted_variables)
                    st.markdown("**Actual values from upload:**")
                    st.json(matched_actuals)

                    if st.button(
                        f"Validate this prediction",
                        key=f"validate_upload_{pred.id}"
                    ):
                        accuracy = reality_anchor.validate(pred.id, matched_actuals)

                        if accuracy >= 0.8:
                            st.success(f"Accuracy: {accuracy:.0%} -- Strong prediction")
                        elif accuracy >= 0.5:
                            st.warning(f"Accuracy: {accuracy:.0%} -- Moderate prediction")
                        else:
                            st.error(f"Accuracy: {accuracy:.0%} -- Poor prediction")

                        if calibration_engine is not None:
                            notes = calibration_engine.propose_calibrations(
                                reality_anchor, pred.agent
                            )
                            if notes:
                                st.info(
                                    f"{len(notes)} calibration note(s) proposed "
                                    f"for {pred.agent} agent. "
                                    "Review in the Self-Improvement panel."
                                )

                        st.rerun()

        except Exception as e:
            st.error(f"Error parsing file: {e}")


# ── Self-test ─────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("Manual Validator Self-Tests")
    print("=" * 55)

    # Test 1: JSON parsing
    json_bytes = b'{"temperature": 28.5, "humidity": 42.0, "pressure": 1015.0}'
    result = parse_upload(json_bytes, "actuals.json")
    assert result == {"temperature": 28.5, "humidity": 42.0, "pressure": 1015.0}
    print("\n[PASS] JSON parsing:", result)

    # Test 2: CSV with headers
    csv_bytes = b"variable,value\ntemperature,28.5\nhumidity,42.0\npressure,1015.0"
    result2 = parse_upload(csv_bytes, "actuals.csv")
    assert "temperature" in result2 and result2["temperature"] == 28.5
    print("[PASS] CSV with headers:", result2)

    # Test 3: Single-row CSV (no headers)
    csv_flat = b"temperature,28.5,humidity,42.0,pressure,1015.0"
    result3 = parse_upload(csv_flat, "actuals.csv")
    assert "temperature" in result3
    print("[PASS] Single-row CSV:", result3)

    # Test 4: match_actuals_to_predictions
    class FakePred:
        def __init__(self, id_, vars_):
            self.id = id_
            self.agent = "test"
            self.validated = False
            self.predicted_variables = vars_
            self.prediction_text = "Test prediction"

    preds = [
        FakePred("p1", {"temperature": 30.0, "humidity": 45.0}),
        FakePred("p2", {"gold": 1920.0}),
    ]
    actuals = {"temperature": 28.5, "humidity": 42.0}
    matches = match_actuals_to_predictions(actuals, preds)
    assert len(matches) == 1
    assert matches[0][0].id == "p1"
    print("[PASS] Prediction matching:", [(m[0].id, m[1]) for m in matches])

    # Test 5: UTF-8 BOM handling
    bom_bytes = b'\xef\xbb\xbf{"temperature": 28.5}'
    result5 = parse_upload(bom_bytes, "actuals.json")
    assert result5["temperature"] == 28.5
    print("[PASS] BOM handling:", result5)

    print("\n" + "=" * 55)
    print("ALL TESTS PASSED")
    print("=" * 55)
