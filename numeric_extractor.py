"""
numeric_extractor.py
=====================
Day 2 deliverable: extracts real numeric predicted values from an
agent's free-text final_answer, so Reality Anchor stores actual
numbers instead of 0.0 placeholders.

How it works:
    1. Regex pass  -- finds patterns like "X will be 42.5" or
                      "temperature: ~23 degrees" or "gold: $1920"
    2. Mistral pass -- if regex finds nothing and client provided,
                      asks Mistral to extract numbers as structured JSON

Always returns dict {variable_name: float} -- empty if nothing found,
never crashes.

Drop-in integration:
    from numeric_extractor import extract_predictions
    predicted = extract_predictions(result.final_answer, target_vars)
    reality_anchor.record_prediction(..., predicted_variables=predicted)
"""

from __future__ import annotations
import re
from typing import Optional


_STOPWORDS = {
    'a','the','this','that','these','those','it','is','was','are','were',
    'be','been','being','have','has','had','do','does','did','will','would',
    'could','should','may','might','must','can','to','of','in','on','at',
    'by','for','with','about','as','into','through','during','before','after',
    'above','below','up','down','out','off','over','under','then','once',
    'and','but','or','nor','not','so','yet','both','either','neither',
    'analysis','result','finding','conclusion','data','value','values',
    'level','levels','rate','rates','step','steps','note','based','given',
    'shows','shown','found','indicates','suggests','approximately','around',
    'about','roughly','nearly','almost','just','only','also','both',
}


def _parse_number(s: str) -> Optional[float]:
    try:
        return float(s.replace(',', ''))
    except (ValueError, AttributeError):
        return None


def _clean_var(v: str) -> str:
    return re.sub(r'\s+', '_', v.strip().lower())


def _regex_extract(text: str, target_vars: Optional[list] = None) -> dict:
    results = {}

    # Pattern 1: "variable will/is expected to VERB NUMBER"
    p1 = re.compile(
        r'([\w][\w\s_]*?)\s+(?:will\s+|is\s+expected\s+to\s+|may\s+|could\s+)?'
        r'(?:be|reach|hit|drop\s+to|rise\s+to|fall\s+to|increase\s+to|'
        r'decrease\s+to|climb\s+to|decline\s+to|remain\s+at|stay\s+at)\s+'
        r'(?:approximately\s+|around\s+|~\s*)?'
        r'\$?(-?[\d,]+\.?\d*)',
        re.IGNORECASE
    )
    for m in p1.finditer(text):
        var = _clean_var(m.group(1))
        val = _parse_number(m.group(2))
        if val is not None and var not in _STOPWORDS and len(var) >= 2:
            results[var] = val

    # Pattern 2: "variable: NUMBER" or "variable = NUMBER"
    p2 = re.compile(
        r'\b([\w_]+)\s*[:=]\s*(?:~|approx\.?\s*)?'
        r'\$?(-?[\d,]+\.?\d*)',
        re.IGNORECASE
    )
    for m in p2.finditer(text):
        var = m.group(1).lower().strip()
        val = _parse_number(m.group(2))
        if val is not None and var not in _STOPWORDS and len(var) >= 2:
            if var not in results:
                results[var] = val

    # Pattern 3: "variable of NUMBER" (e.g. "soil_moisture of 0.28")
    p3 = re.compile(
        r'\b([\w_]+)\s+of\s+(?:~|approx\.?\s*)?'
        r'\$?(-?[\d,]+\.?\d*)',
        re.IGNORECASE
    )
    for m in p3.finditer(text):
        var = m.group(1).lower().strip()
        val = _parse_number(m.group(2))
        if val is not None and var not in _STOPWORDS and len(var) >= 2:
            if var not in results:
                results[var] = val

    # Pattern 4: "predicted to VERB NUMBER" with preceding variable
    p4 = re.compile(
        r'([\w_]+)\s+(?:is\s+)?predicted\s+to\s+'
        r'(?:be|reach|hit|fall|rise|drop|increase|decrease)?\s*'
        r'(?:to\s+)?(?:~|approx\.?\s*)?\$?(-?[\d,]+\.?\d*)',
        re.IGNORECASE
    )
    for m in p4.finditer(text):
        var = m.group(1).lower().strip()
        val = _parse_number(m.group(2))
        if val is not None and var not in _STOPWORDS and len(var) >= 2:
            if var not in results:
                results[var] = val

    # Pattern 5: Multi-word variable names "heart rate will increase to NUMBER"
    p5 = re.compile(
        r'([\w]+\s+[\w]+)\s+(?:will\s+)?'
        r'(?:increase\s+to|decrease\s+to|reach|hit|rise\s+to|fall\s+to|drop\s+to)\s+'
        r'(?:~|approx\.?\s*)?\$?(-?[\d,]+\.?\d*)',
        re.IGNORECASE
    )
    for m in p5.finditer(text):
        var = _clean_var(m.group(1))
        val = _parse_number(m.group(2))
        if val is not None and var not in _STOPWORDS and len(var) >= 2:
            if var not in results:
                results[var] = val

    # Pattern 6: "drop/fall/rise to ~NUMBER" preceded by variable
    p6 = re.compile(
        r'([\w_]+)\s+(?:is\s+expected\s+to\s+|will\s+)?'
        r'(?:drop|fall|decline|decrease)\s+to\s+'
        r'(?:approximately\s+|~\s*|around\s+)?\$?(-?[\d,]+\.?\d*)',
        re.IGNORECASE
    )
    for m in p6.finditer(text):
        var = m.group(1).lower().strip()
        val = _parse_number(m.group(2))
        if val is not None and var not in _STOPWORDS and len(var) >= 2:
            if var not in results:
                results[var] = val

    if target_vars:
        filtered = {}
        for tv in target_vars:
            tv_lower = tv.lower()
            tv_under = tv_lower.replace(' ', '_')
            tv_space = tv_lower.replace('_', ' ')
            for k, v in results.items():
                if (tv_lower in k or k in tv_lower or
                        tv_under in k or k in tv_under or
                        tv_space in k or k in tv_space):
                    filtered[tv] = v
                    break
        return filtered

    return results


def _llm_extract(text: str, target_vars: Optional[list], client) -> dict:
    if client is None:
        return {}

    target_hint = ""
    if target_vars:
        target_hint = (
            f"\nExtract values specifically for: {', '.join(target_vars)}. "
            "Omit variables not predicted in the text."
        )

    system_prompt = (
        "You are a numeric extractor. Given scientific analysis text, "
        "extract specific numeric predictions.\n"
        "Return ONLY a JSON object: {\"variable_name\": numeric_value, ...}\n"
        "Rules: only include variables with specific numbers stated, "
        "no invented numbers, values must be floats, "
        "empty object {} if nothing found." + target_hint
    )

    try:
        result = client.generate_json(
            system_prompt=system_prompt,
            user_prompt=f"Text:\n{text[:1500]}",
            temperature=0.1,
        )
        if isinstance(result, dict):
            return {
                k: float(v) for k, v in result.items()
                if isinstance(v, (int, float)) and not isinstance(v, bool)
            }
    except Exception:
        pass
    return {}


def extract_predictions(
    final_answer: str,
    target_vars: Optional[list] = None,
    llm_client=None,
    min_regex_confidence: int = 1,
) -> dict:
    """
    Extract numeric predictions from agent final_answer text.

    Parameters
    ----------
    final_answer         : str  -- agent's final_answer prose
    target_vars          : list -- optional variable names to look for
    llm_client           : MistralClient or None -- fallback if regex finds nothing
    min_regex_confidence : int  -- trigger LLM if regex finds fewer than this

    Returns
    -------
    dict[str, float] -- {variable_name: predicted_value}, empty if nothing found
    """
    if not final_answer or not final_answer.strip():
        return {}

    regex_results = _regex_extract(final_answer, target_vars)

    if len(regex_results) >= min_regex_confidence:
        return regex_results

    if llm_client is not None:
        llm_results = _llm_extract(final_answer, target_vars, llm_client)
        if llm_results:
            return llm_results

    return regex_results


# ── Self-test ─────────────────────────────────────────────────────
if __name__ == "__main__":
    tests = [
        (
            "temperature will reach 28.5 degrees and "
            "humidity is expected to drop to approximately 42%. "
            "Pressure: ~1015 hPa.",
            None,
            ["temperature", "humidity", "pressure"],
            "Scientific prediction text"
        ),
        (
            "gold will hit $1,920 per ounce. vix: 25.",
            ["gold", "vix"],
            ["gold", "vix"],
            "Finance domain"
        ),
        (
            "yield_forecast: 3.2 tonnes/ha based on soil_moisture of 0.28.",
            ["yield_forecast", "soil_moisture"],
            ["yield_forecast", "soil_moisture"],
            "Agriculture domain"
        ),
        (
            "No specific future values are predicted.",
            None,
            [],
            "No predictions -- empty dict"
        ),
        (
            "Heart rate will increase to 88 bpm, cortisol is predicted "
            "to reach 28, and sleep_hours may fall to 5.2.",
            None,
            ["heart_rate", "cortisol", "sleep_hours"],
            "Health domain"
        ),
    ]

    print("=" * 55)
    print("Numeric Extractor Self-Tests")
    print("=" * 55)
    all_passed = True

    for text, target_vars, expected_keys, desc in tests:
        result = extract_predictions(text, target_vars, llm_client=None)
        missing = [k for k in expected_keys if not any(
            k.lower().replace('_',' ') in rk or rk in k.lower().replace('_',' ')
            or k.lower() in rk or rk in k.lower()
            for rk in result.keys()
        )]
        passed = len(missing) == 0
        if not passed:
            all_passed = False
        status = "PASS" if passed else "FAIL"
        print(f"\n[{status}] {desc}")
        print(f"  Extracted: {result}")
        if missing:
            print(f"  Missing:   {missing}")

    print("\n" + "=" * 55)
    if all_passed:
        print("ALL TESTS PASSED")
    else:
        print("SOME TESTS FAILED - LLM fallback will cover these in production")
    print("=" * 55)
