"""
OMEGA-CORE ADK Stress Test — Master Runner
===========================================
Executes all three tracks sequentially and produces a unified
scorecard report with pass/fail, metrics, and recommendations.

Usage:
    py stress_test/run_all_tracks.py
"""

import sys
import json
import datetime
import time

# Add parent to path
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stress_test.track1_adk_agent import run_track1_stress_test
from stress_test.track2_optimizer import run_track2_stress_test
from stress_test.track3_cloud_refactor import run_track3_stress_test


BANNER = """
╔══════════════════════════════════════════════════════════════╗
║      OMEGA-CORE  ·  ADK HACKATHON STRESS TEST SUITE         ║
║      Universal Lab AP Phillips  ·  v3.0.0                   ║
╠══════════════════════════════════════════════════════════════╣
║  Track 1 │ Build    → ADK Net-New Agent + MCP Registry       ║
║  Track 2 │ Optimize → Multi-Step Reasoning + Auto-Refinement ║
║  Track 3 │ Cloud    → GCP Marketplace + Gemini Enterprise    ║
╚══════════════════════════════════════════════════════════════╝
"""

RECOMMENDATIONS = {
    1: {
        "PASS": "✓ ADK agent is production-ready. Next: connect live Gemini API for dynamic planning.",
        "FAIL": "○ Improve MCP tool reliability. Target ≥80% success rate per intent."
    },
    2: {
        "PASS": "✓ Agent is optimized for production. Next: run A/B test on refined vs original prompt in staging.",
        "FAIL": "○ Increase edge case coverage. Focus on null/empty input handling and retry logic."
    },
    "PARTIAL": "○ API contract and core isolation pass. Complete 4 remaining Cloud readiness items: Secret Manager, VPC Controls, Cloud Armor, SLA Monitoring.",
    3: {
        "PASS": "✓ Marketplace-ready. Submit listing to Google Cloud Marketplace partner portal.",
        "PARTIAL": "○ Address TODO items before marketplace submission.",
        "FAIL": "○ Critical cloud readiness gaps found. Review API contract and tenant isolation failures."
    }
}


def compute_overall_grade(track_results: list[dict]) -> tuple[str, float]:
    """Compute letter grade from all track results."""
    scores = []
    for r in track_results:
        if r["status"] == "PASS":
            scores.append(100)
        elif r["status"] == "PARTIAL":
            scores.append(70)
        else:
            scores.append(40)

    # Bonus points from key metrics
    for r in track_results:
        if r.get("avg_success_rate"):
            scores.append(r["avg_success_rate"])
        if r.get("refined_success_rate"):
            scores.append(r["refined_success_rate"])
        if r.get("api_contract_pass_rate"):
            scores.append(r["api_contract_pass_rate"])

    avg = sum(scores) / len(scores)

    if avg >= 90:   grade = "A"
    elif avg >= 80: grade = "B+"
    elif avg >= 70: grade = "B"
    elif avg >= 60: grade = "C"
    else:           grade = "D"

    return grade, round(avg, 1)


def print_final_scorecard(results: list[dict], grade: str, score: float, duration: float):
    print("\n")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║              OMEGA-CORE ADK STRESS TEST SCORECARD           ║")
    print("╠══════════════════════════════════════════════════════════════╣")

    track_labels = {1: "Track 1 · ADK Agent Build", 2: "Track 2 · Agent Optimize", 3: "Track 3 · Cloud Refactor"}
    for r in results:
        t = r["track"]
        status = r["status"]
        bar = "✓ PASS   " if status == "PASS" else "○ PARTIAL" if status == "PARTIAL" else "✗ FAIL   "
        print(f"║  {bar}  │  {track_labels[t]:<38}║")

    print("╠══════════════════════════════════════════════════════════════╣")
    print(f"║  OVERALL GRADE : {grade:<6}  │  COMPOSITE SCORE : {score:.1f}/100          ║")
    print(f"║  DURATION      : {duration:.1f}s    │  TIMESTAMP : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}    ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print("║  KEY METRICS                                                 ║")

    for r in results:
        t = r["track"]
        if t == 1:
            print(f"║   T1 MCP invocations   : {r.get('mcp_invocations', '?'):<5} │ Tools registered : {r.get('tools_registered', '?')}          ║")
            print(f"║   T1 Avg success rate  : {r.get('avg_success_rate', '?'):.1f}%                                  ║")
        elif t == 2:
            print(f"║   T2 Baseline→Refined  : {r.get('baseline_success_rate', '?'):.1f}% → {r.get('refined_success_rate', '?'):.1f}% (+{r.get('improvement_pct', '?'):.1f}%)               ║")
            print(f"║   T2 Stall protection  : {'✓ ACTIVE' if r.get('stall_protection') else '✗ INACTIVE'}                                   ║")
        elif t == 3:
            print(f"║   T3 API pass rate     : {r.get('api_contract_pass_rate', '?'):.1f}%  │ Readiness : {r.get('deployment_readiness_pct', '?'):.1f}%           ║")
            print(f"║   T3 Marketplace ready : {'✓ YES' if r.get('marketplace_ready') else '○ PARTIAL'}                                    ║")

    print("╠══════════════════════════════════════════════════════════════╣")
    print("║  RECOMMENDATIONS                                             ║")
    for r in results:
        t = r["track"]
        recs = RECOMMENDATIONS.get(t, {})
        rec = recs.get(r["status"], recs.get("PARTIAL", "Review results"))
        # Word-wrap to 58 chars
        words = rec.split()
        lines = []
        current = ""
        for w in words:
            if len(current) + len(w) + 1 <= 58:
                current = current + " " + w if current else w
            else:
                lines.append(current)
                current = w
        if current:
            lines.append(current)
        for i, line in enumerate(lines):
            prefix = f"  T{t} " if i == 0 else "     "
            print(f"║  {prefix}{line:<55}║")

    print("╚══════════════════════════════════════════════════════════════╝")


def save_report(results: list[dict], grade: str, score: float, duration: float):
    """Save JSON report to reports/."""
    os.makedirs("reports", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report = {
        "report_type": "ADK_STRESS_TEST",
        "version": "3.0.0",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "duration_seconds": round(duration, 2),
        "overall_grade": grade,
        "composite_score": score,
        "tracks": results,
        "next_steps": [
            "Connect live Gemini API for dynamic agent planning (Track 1)",
            "Deploy refined system prompt to production (Track 2)",
            "Complete 4 remaining Cloud readiness items (Track 3)",
            "Submit to Google Cloud Marketplace partner portal"
        ]
    }
    path = f"reports/adk_stress_test_{timestamp}.json"
    with open(path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\n  📄 Full report saved → {path}")
    return path


def main():
    print(BANNER)
    print(f"  Started: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Running 3 tracks...\n")

    overall_start = time.time()
    results = []

    # ── TRACK 1 ──
    try:
        t1 = run_track1_stress_test()
        results.append(t1)
    except Exception as e:
        print(f"\n  ✗ Track 1 crashed: {e}")
        results.append({"track": 1, "status": "FAIL", "error": str(e)})

    # ── TRACK 2 ──
    try:
        t2 = run_track2_stress_test()
        results.append(t2)
    except Exception as e:
        print(f"\n  ✗ Track 2 crashed: {e}")
        results.append({"track": 2, "status": "FAIL", "error": str(e)})

    # ── TRACK 3 ──
    try:
        t3 = run_track3_stress_test()
        results.append(t3)
    except Exception as e:
        print(f"\n  ✗ Track 3 crashed: {e}")
        results.append({"track": 3, "status": "FAIL", "error": str(e)})

    duration = time.time() - overall_start
    grade, score = compute_overall_grade(results)

    print_final_scorecard(results, grade, score, duration)
    report_path = save_report(results, grade, score, duration)

    return results


if __name__ == "__main__":
    main()
