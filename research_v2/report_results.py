import csv
import json
from pathlib import Path
from collections import defaultdict
from statistics import mean

root = Path("research_v2/results")

with (root / "summary.csv").open(newline="", encoding="utf-8") as f:
    summary = list(csv.DictReader(f))

with (root / "paired_analysis.csv").open(newline="", encoding="utf-8") as f:
    paired = list(csv.DictReader(f))

with (root / "experiment_manifest.json").open(encoding="utf-8") as f:
    manifest = json.load(f)

print("\n========== EXPERIMENT MANIFEST ==========")
for key, value in manifest.items():
    print(f"{key}: {value}")

print("\n========== OVERALL POLICY PERFORMANCE ==========")
policies = sorted({r["policy"] for r in summary})

metrics = [
    "allocation_rate_mean",
    "workload_completion_rate_mean",
    "priority_completion_rate_mean",
    "jain_fairness_mean",
    "load_imbalance_mean",
    "objective_score_mean",
]

for policy in policies:
    records = [r for r in summary if r["policy"] == policy]
    print(f"\n{policy} (across {len(records)} workload/failure groups)")
    for metric in metrics:
        print(f"  {metric}: {mean(float(r[metric]) for r in records):.4f}")

print("\n========== BEST POLICY BY SCENARIO ==========")
for count in sorted({int(r["item_count"]) for r in summary}):
    for failure in sorted({float(r["failure_probability"]) for r in summary}):
        group = [
            r for r in summary
            if int(r["item_count"]) == count
            and float(r["failure_probability"]) == failure
        ]
        group.sort(
            key=lambda r: float(r["objective_score_mean"]),
            reverse=True
        )
        best = group[0]
        print(
            f"Tasks={count:3d} | failures={failure:.0%} | "
            f"best={best['policy']:18s} | "
            f"objective={float(best['objective_score_mean']):.4f} | "
            f"workload={float(best['workload_completion_rate_mean']):.4f} | "
            f"fairness={float(best['jain_fairness_mean']):.4f}"
        )

print("\n========== PAIRED COMPARISON VS FIRST FIT ==========")
by_policy = defaultdict(list)

for r in paired:
    by_policy[r["policy"]].append(r)

for policy, records in sorted(by_policy.items()):
    differences = [
        float(r["mean_paired_objective_difference"])
        for r in records
    ]
    positive = sum(x > 0 for x in differences)
    negative = sum(x < 0 for x in differences)
    neutral = sum(x == 0 for x in differences)

    print(
        f"{policy:18s} | "
        f"mean condition difference={mean(differences):+.5f} | "
        f"conditions better={positive} | worse={negative} | tied={neutral}"
    )

print("\n========== DATA INTEGRITY ==========")
with (root / "trials.csv").open(newline="", encoding="utf-8") as f:
    trials = list(csv.DictReader(f))

keys = {
    (r["item_count"], r["seed"], r["failure_probability"], r["policy"])
    for r in trials
}

print(f"Trial rows: {len(trials)}")
print(f"Unique trial keys: {len(keys)}")
print(f"Summary groups: {len(summary)}")
print(f"Paired comparison groups: {len(paired)}")
print("Expected rows:", manifest["expected_rows"])
print("Row count valid:", len(trials) == manifest["expected_rows"])
print("Unique keys valid:", len(keys) == len(trials))
