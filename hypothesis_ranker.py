"""
hypothesis_ranker.py — Day 9
Ranks competing hypotheses from agent runs by evidence strength.
Uses causal scan output, reality anchor accuracy, and coherence scores.
"""
from __future__ import annotations
import json
import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class RankedHypothesis:
    id: str
    text: str
    agent: str
    score: float           # 0-1 composite evidence score
    causal_support: float  # how well causal scan supports it
    accuracy_support: float  # reality anchor accuracy for this agent
    coherence: float       # uncertainty engine coherence score
    rank: int = 0
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict:
        return self.__dict__.copy()


def rank_hypotheses(
    hypotheses: list[dict],
    causal_scan_result: dict = None,
    accuracy_by_agent: dict = None,
    coherence_scores: dict = None,
) -> list[RankedHypothesis]:
    """
    Rank a list of hypotheses by composite evidence score.

    Parameters
    ----------
    hypotheses       : list of {id, text, agent} dicts
    causal_scan_result : output from causal_scan_v2 (optional)
    accuracy_by_agent  : {agent: float} from RealityAnchor (optional)
    coherence_scores   : {agent: float} from uncertainty engine (optional)

    Returns
    -------
    List of RankedHypothesis sorted by score descending
    """
    ranked = []
    causal_summary = " ".join(causal_scan_result.get("summary", [])) if causal_scan_result else ""

    for h in hypotheses:
        text = h.get("text", "")
        agent = h.get("agent", "unknown")

        # Causal support: do the variables mentioned in the hypothesis
        # appear as causal leads in the scan?
        causal_support = 0.0
        if causal_scan_result and text:
            lag_leads = causal_scan_result.get("lag_leads", {})
            variables_in_hypothesis = [
                v for v in causal_scan_result.get("variables", [])
                if v.lower() in text.lower()
            ]
            if variables_in_hypothesis:
                supported = sum(
                    1 for v in variables_in_hypothesis
                    if v in lag_leads and lag_leads[v]
                )
                causal_support = supported / len(variables_in_hypothesis)

        # Accuracy support from reality anchor
        accuracy_support = 0.5  # neutral if no data
        if accuracy_by_agent and agent in accuracy_by_agent:
            accuracy_support = accuracy_by_agent[agent]

        # Coherence from uncertainty engine
        coherence = 0.5
        if coherence_scores and agent in coherence_scores:
            coherence = coherence_scores[agent]

        # Composite score (weighted)
        score = (causal_support * 0.4 +
                 accuracy_support * 0.35 +
                 coherence * 0.25)

        ranked.append(RankedHypothesis(
            id=h.get("id", f"h_{len(ranked)}"),
            text=text,
            agent=agent,
            score=round(score, 3),
            causal_support=round(causal_support, 3),
            accuracy_support=round(accuracy_support, 3),
            coherence=round(coherence, 3),
        ))

    ranked.sort(key=lambda h: -h.score)
    for i, h in enumerate(ranked):
        h.rank = i + 1

    return ranked


if __name__ == "__main__":
    print("=== Hypothesis Ranker Tests ===")

    hypotheses = [
        {"id": "h1", "text": "temperature causes humidity to drop", "agent": "scientific_discovery"},
        {"id": "h2", "text": "pressure is the root driver of all changes", "agent": "scientific_discovery"},
        {"id": "h3", "text": "humidity and temperature are unrelated", "agent": "weather_manifold"},
    ]
    causal = {
        "variables": ["temperature", "humidity", "pressure"],
        "lag_leads": {"temperature": ["humidity"]},
        "summary": ["temperature LEADS humidity by 1 step"],
    }
    accuracy = {"scientific_discovery": 0.85, "weather_manifold": 0.45}
    coherence = {"scientific_discovery": 0.75, "weather_manifold": 0.50}

    ranked = rank_hypotheses(hypotheses, causal, accuracy, coherence)

    print("Ranked hypotheses:")
    for h in ranked:
        print(f"  #{h.rank} [{h.score:.2f}] {h.text[:60]} (agent:{h.agent})")

    assert ranked[0].id == "h1", f"Expected h1 to rank first, got {ranked[0].id}"
    assert ranked[-1].id == "h3", f"Expected h3 to rank last"
    print("PASS -- h1 ranked highest (causal + accuracy support)")
    print("ALL TESTS PASSED")
