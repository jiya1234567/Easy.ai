"""
uncertainty.py
===============
Gap 3 fix: Calibrated uncertainty quantification.

Instead of trusting Mistral's self-reported confidence (subjective),
this measures actual disagreement between Mistral (primary) and
Phi3 (challenger) as a more honest uncertainty signal.

High agreement -> low epistemic uncertainty (both models converge)
High disagreement -> high epistemic uncertainty (genuinely unclear)
"""

from __future__ import annotations
import re
from dataclasses import dataclass


@dataclass
class UncertaintyScore:
    agreement_score: float       # 0-1, semantic overlap between primary/challenger
    epistemic_uncertainty: float  # 1 - agreement_score
    confidence_label: str         # "high" | "moderate" | "low"
    disagreement_points: list[str]  # specific points of disagreement found
    explanation: str

    def to_dict(self) -> dict:
        return {
            "agreement_score": round(self.agreement_score, 3),
            "epistemic_uncertainty": round(self.epistemic_uncertainty, 3),
            "confidence_label": self.confidence_label,
            "disagreement_points": self.disagreement_points,
            "explanation": self.explanation,
        }


# Words/phrases that signal explicit disagreement in the challenger's text
DISAGREEMENT_MARKERS = [
    "however", "but", "although", "alternatively", "instead",
    "disagree", "incorrect", "missed", "overlooked", "should consider",
    "more likely", "rather than", "contrary to", "challenge", "question",
    "unlikely", "doubtful", "insufficient evidence", "not necessarily",
]

AGREEMENT_MARKERS = [
    "agree", "confirms", "consistent with", "supports", "aligns with",
    "correct", "valid", "sound reasoning", "well-supported",
]


def _word_overlap_ratio(text_a: str, text_b: str) -> float:
    """Simple lexical overlap as a baseline similarity signal."""
    words_a = set(re.findall(r"\b[a-z]{4,}\b", text_a.lower()))
    words_b = set(re.findall(r"\b[a-z]{4,}\b", text_b.lower()))
    if not words_a or not words_b:
        return 0.5
    intersection = words_a & words_b
    union = words_a | words_b
    return len(intersection) / len(union) if union else 0.5


def compute_uncertainty(primary_text: str, challenger_text: str) -> UncertaintyScore:
    """
    Compute an uncertainty score from the primary (Mistral) and
    challenger (Phi3) reasoning texts.

    Combines:
    1. Lexical overlap (do they use similar concepts/variables?)
    2. Explicit disagreement markers in challenger text
    3. Explicit agreement markers in challenger text
    """
    if not challenger_text or not challenger_text.strip():
        # No debate happened (use_debate=False) — can't compute real uncertainty
        return UncertaintyScore(
            agreement_score=0.5,
            epistemic_uncertainty=0.5,
            confidence_label="unknown",
            disagreement_points=[],
            explanation="No challenger response available — debate was not run, "
                        "so disagreement-based uncertainty cannot be computed.",
        )

    lower_challenger = challenger_text.lower()

    overlap = _word_overlap_ratio(primary_text, challenger_text)

    disagreement_hits = [m for m in DISAGREEMENT_MARKERS if m in lower_challenger]
    agreement_hits = [m for m in AGREEMENT_MARKERS if m in lower_challenger]

    # Base score blends lexical overlap (weighted lightly, since short texts
    # naturally have low raw overlap) with explicit marker signals (weighted
    # heavily, since these are direct statements of stance).
    base = 0.5 + (overlap * 0.3)
    marker_adjustment = (len(agreement_hits) * 0.12) - (len(disagreement_hits) * 0.15)
    agreement_score = max(0.0, min(1.0, base + marker_adjustment))

    epistemic_uncertainty = 1.0 - agreement_score

    if agreement_score >= 0.65:
        label = "high"
    elif agreement_score >= 0.40:
        label = "moderate"
    else:
        label = "low"

    # Extract sentences containing disagreement markers as specific points
    sentences = re.split(r'(?<=[.!?])\s+', challenger_text)
    disagreement_points = [
        s.strip() for s in sentences
        if any(m in s.lower() for m in DISAGREEMENT_MARKERS)
    ][:3]  # cap at 3 for readability

    explanation = (
        f"Primary and challenger share {overlap:.0%} lexical overlap. "
        f"Found {len(disagreement_hits)} disagreement marker(s) and "
        f"{len(agreement_hits)} agreement marker(s) in challenger response. "
        f"Resulting confidence label: {label}."
    )

    return UncertaintyScore(
        agreement_score=agreement_score,
        epistemic_uncertainty=epistemic_uncertainty,
        confidence_label=label,
        disagreement_points=disagreement_points,
        explanation=explanation,
    )


# ── Self-test ─────────────────────────────────────────────────────
if __name__ == "__main__":
    primary = (
        "The observed correlation between mutation score and expression level "
        "suggests a direct causal relationship driven by transcriptional activity."
    )

    # Case 1: high agreement
    challenger_agree = (
        "This analysis is well-supported. The correlation confirms transcriptional "
        "activity as the primary driver of expression level changes."
    )

    # Case 2: high disagreement
    challenger_disagree = (
        "However, this conclusion is unlikely to hold. The correlation is more likely "
        "explained by an unmeasured confounding variable rather than direct causation. "
        "The primary analysis overlooked epigenetic regulation entirely."
    )

    print("=== Case 1: High agreement ===")
    score1 = compute_uncertainty(primary, challenger_agree)
    print(score1.to_dict())

    print("\n=== Case 2: High disagreement ===")
    score2 = compute_uncertainty(primary, challenger_disagree)
    print(score2.to_dict())

    print("\n=== Case 3: No debate ===")
    score3 = compute_uncertainty(primary, "")
    print(score3.to_dict())
