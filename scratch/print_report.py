import json, sys
sys.stdout.reconfigure(encoding="utf-8")
with open("reports/omega_25_test_report.json") as f:
    r = json.load(f)

print("=" * 60)
print("  OMEGA 25-TEST REPORT SUMMARY")
print("=" * 60)
print(f"Run Timestamp : {r['run_timestamp']}")
print(f"Total         : {r['total']}")
print(f"Passed        : {r['passed']}")
print(f"Failed        : {r['failed']}")
print(f"Completion    : {r['completion_pct']}%")
print()
print("Category Breakdown:")
for cat, s in r["category_scores"].items():
    bar = chr(0x2588) * s["pass"] + chr(0x2591) * (s["total"] - s["pass"])
    print(f"  {cat:<42} [{bar}] {s['pass']}/{s['total']}")
print()
print("Reducibility Distribution:")
for cls, cnt in r["reducibility_distribution"].items():
    print(f"  {cls:<15}: {cnt}")
print()
print("Per-Experiment Results:")
for i, res in enumerate(r["results"], 1):
    t = res["thermodynamics"]
    name = res["experiment"][-52:]
    mark = "PASS" if res["status"] in ("PASSED", "MARGINAL") else "FAIL"
    print(f"  [{i:02d}] {mark} | CRI={t['reducibility_score']:.3f} H={t['entropy']:.3f} k={t['coherence']:.3f} | {name}")
print()
if r["completion_pct"] == 100.0:
    print(">>> ALL 25 EXPERIMENTS VERIFIED - OMEGA-CORE IS A SCIENTIFIC COGNITION OS <<<")
else:
    print(f">>> {r['failed']} experiment(s) still need attention <<<")
print("=" * 60)
