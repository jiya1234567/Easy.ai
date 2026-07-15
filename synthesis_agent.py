"""
synthesis_agent.py — Step 17
Cross-domain synthesis: combines findings from multiple domain agents
into unified cross-domain hypotheses and identifies universal patterns.
"""
from __future__ import annotations
import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class SynthesisResult:
    synthesis_id: str
    domains_synthesised: list[str]
    universal_patterns: list[str]
    cross_domain_hypotheses: list[str]
    conflicting_findings: list[str]
    confidence: float
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict:
        return self.__dict__.copy()

    def summary(self) -> str:
        lines = [
            f"Cross-Domain Synthesis [{', '.join(self.domains_synthesised)}]",
            f"Confidence: {self.confidence:.0%}",
            "",
            "Universal Patterns:",
        ]
        for p in self.universal_patterns:
            lines.append(f"  - {p}")
        lines.append("\nCross-Domain Hypotheses:")
        for h in self.cross_domain_hypotheses:
            lines.append(f"  - {h}")
        if self.conflicting_findings:
            lines.append("\nConflicting Findings (require resolution):")
            for c in self.conflicting_findings:
                lines.append(f"  ! {c}")
        return "\n".join(lines)


def synthesise_domains(
    domain_results: dict[str, Any],
    state_tensors: dict[str, Any] = None,
    causal_scans: dict[str, Any] = None,
) -> SynthesisResult:
    """
    Synthesise findings from multiple domain agent runs.

    Parameters
    ----------
    domain_results : {domain: AgentResult or dict with 'final_answer'}
    state_tensors  : {domain: StateTensor} -- optional
    causal_scans   : {domain: causal_scan_v2 output} -- optional

    Returns
    -------
    SynthesisResult with cross-domain patterns and hypotheses
    """
    domains = list(domain_results.keys())
    universal_patterns = []
    cross_domain_hypotheses = []
    conflicting_findings = []

    # 1. State tensor comparison -- find domains in similar states
    if state_tensors and len(state_tensors) >= 2:
        domain_list = list(state_tensors.keys())

        # Find domains with high bifurcation (tipping points)
        high_bif = [d for d, st in state_tensors.items()
                    if hasattr(st, 'bifurcation_B') and st.bifurcation_B > 0.6]
        if len(high_bif) >= 2:
            universal_patterns.append(
                f"Multiple domains approaching tipping points simultaneously: "
                f"{', '.join(high_bif)} -- suggests systemic stress"
            )
            cross_domain_hypotheses.append(
                f"H: Tipping points in {' and '.join(high_bif)} may share "
                f"a common driver not visible within any single domain"
            )

        # Find domains with high coherence
        high_coh = [d for d, st in state_tensors.items()
                    if hasattr(st, 'coherence_K') and st.coherence_K > 0.8]
        if high_coh:
            universal_patterns.append(
                f"High internal coherence in: {', '.join(high_coh)} "
                f"-- variables moving in lockstep"
            )

        # Find domains with conflicting entropy levels
        high_ent = [d for d, st in state_tensors.items()
                    if hasattr(st, 'entropy_H') and st.entropy_H > 0.7]
        low_ent = [d for d, st in state_tensors.items()
                   if hasattr(st, 'entropy_H') and st.entropy_H < 0.3]
        if high_ent and low_ent:
            conflicting_findings.append(
                f"Entropy conflict: {high_ent} show disorder while "
                f"{low_ent} show order -- may indicate domain decoupling"
            )

    # 2. Causal scan comparison -- find variables appearing in multiple domains
    if causal_scans and len(causal_scans) >= 2:
        # Find variable names that appear as lag-leads in multiple domains
        all_lag_leads: dict[str, list] = {}
        for domain, scan in causal_scans.items():
            if isinstance(scan, dict):
                for cause, effects in scan.get("lag_leads", {}).items():
                    for effect in effects:
                        pattern = f"{cause}->{ effect}"
                        all_lag_leads.setdefault(pattern, []).append(domain)

        for pattern, found_in in all_lag_leads.items():
            if len(found_in) >= 2:
                universal_patterns.append(
                    f"Lead-lag pattern '{pattern}' appears in multiple domains: "
                    f"{', '.join(found_in)} -- may be a universal mechanism"
                )

        # Find regime changes appearing in multiple domains
        all_regime = []
        for domain, scan in causal_scans.items():
            if isinstance(scan, dict) and scan.get("regime_changes"):
                all_regime.append(domain)
        if len(all_regime) >= 2:
            universal_patterns.append(
                f"Regime changes detected simultaneously in: {', '.join(all_regime)} "
                f"-- suggests coordinated systemic shift"
            )
            cross_domain_hypotheses.append(
                f"H: Concurrent regime changes in {' and '.join(all_regime)} "
                f"may reflect a single upstream causal event"
            )

    # 3. Text-based synthesis from final answers
    all_answers = {}
    for domain, result in domain_results.items():
        if hasattr(result, 'final_answer'):
            all_answers[domain] = result.final_answer
        elif isinstance(result, dict) and 'final_answer' in result:
            all_answers[domain] = result['final_answer']

    # Find common scientific terms appearing across multiple domains
    common_terms = ["correlation", "causal", "regime", "threshold", "lag",
                    "bifurcation", "entropy", "coherence", "nonlinear",
                    "stress", "critical", "tipping"]
    for term in common_terms:
        appearing_in = [d for d, ans in all_answers.items()
                       if term.lower() in ans.lower()]
        if len(appearing_in) >= 2:
            universal_patterns.append(
                f"Concept '{term}' appears in findings across: "
                f"{', '.join(appearing_in)}"
            )

    # Confidence based on richness of synthesis
    n_patterns = len(universal_patterns)
    n_hypotheses = len(cross_domain_hypotheses)
    confidence = min(0.9, 0.3 + n_patterns * 0.08 + n_hypotheses * 0.1)

    return SynthesisResult(
        synthesis_id=f"synth_{int(time.time())}",
        domains_synthesised=domains,
        universal_patterns=universal_patterns[:10],
        cross_domain_hypotheses=cross_domain_hypotheses[:5],
        conflicting_findings=conflicting_findings[:5],
        confidence=round(confidence, 3),
    )


if __name__ == "__main__":
    print("=== Synthesis Agent Tests ===")

    # Mock state tensors
    class FakeTensor:
        def __init__(self, H, K, B):
            self.entropy_H = H
            self.coherence_K = K
            self.bifurcation_B = B

    state_tensors = {
        "finance": FakeTensor(0.7, 0.6, 0.8),
        "weather": FakeTensor(0.6, 0.7, 0.75),
        "health": FakeTensor(0.3, 0.9, 0.2),
    }

    causal_scans = {
        "finance": {"lag_leads": {"rate": ["gold"]}, "regime_changes": ["rate<->vix: r flips"]},
        "weather": {"lag_leads": {"pressure": ["humidity"]}, "regime_changes": ["temp<->humidity: r flips"]},
        "health": {"lag_leads": {}, "regime_changes": []},
    }

    domain_results = {
        "finance": {"final_answer": "Rising rates show causal lag effect on gold prices"},
        "weather": {"final_answer": "Pressure leads humidity with a causal lag relationship"},
        "health": {"final_answer": "Heart rate coherence is high with cortisol"},
    }

    result = synthesise_domains(domain_results, state_tensors, causal_scans)
    print(result.summary())

    assert len(result.domains_synthesised) == 3
    assert len(result.universal_patterns) > 0
    assert result.confidence > 0.3
    print(f"\n[PASS] Patterns found: {len(result.universal_patterns)}")
    print(f"[PASS] Hypotheses: {len(result.cross_domain_hypotheses)}")
    print(f"[PASS] Confidence: {result.confidence}")
    print("ALL TESTS PASSED")
