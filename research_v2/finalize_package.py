import csv
import json
import re
from pathlib import Path
from collections import defaultdict

engine_path = Path("research_v2/engine.py")
source = engine_path.read_text(encoding="utf-8-sig")

# Correct the reference-policy exclusion.
source = source.replace(
    'if policy == "greedy":',
    'if policy == "first_fit":'
)

if 'if policy == "first_fit":' not in source:
    raise RuntimeError("Could not verify First Fit exclusion in engine.")

# Use the actual seeds present in the dataset.
source = re.sub(
    r'for seed in range\(42, 42 \+ len\(\{\s*int\(r\["seed"\]\) for r in rows\s*\}\)\):',
    'for seed in sorted({int(r["seed"]) for r in rows}):',
    source
)

engine_path.write_text(source, encoding="utf-8")

from research_v2.engine import analyze, make_figures, write_csv, write_json

results = Path("research_v2/results")
trials_path = results / "trials.csv"

if not trials_path.exists():
    raise FileNotFoundError("Missing trials.csv; refusing to invent results.")

with trials_path.open("r", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

expected_rows = 1800
if len(rows) != expected_rows:
    raise RuntimeError(f"Expected {expected_rows} rows, found {len(rows)}.")

keys = {
    (
        int(r["item_count"]),
        int(r["seed"]),
        float(r["failure_probability"]),
        r["policy"],
    )
    for r in rows
}

if len(keys) != expected_rows:
    raise RuntimeError("Duplicate trial keys detected.")

scenario_groups = defaultdict(set)
for r in rows:
    scenario = (
        int(r["item_count"]),
        int(r["seed"]),
        float(r["failure_probability"]),
    )
    scenario_groups[scenario].add(r["policy"])

if len(scenario_groups) != 360:
    raise RuntimeError(f"Expected 360 scenarios, got {len(scenario_groups)}.")

expected_policies = {
    "random", "first_fit", "best_fit",
    "least_loaded", "priority_balanced"
}
if any(policies != expected_policies for policies in scenario_groups.values()):
    raise RuntimeError("At least one scenario is missing a policy.")

summary, paired = analyze(rows)

# Six task volumes x three failure levels x four non-reference policies.
if len(summary) != 90:
    raise RuntimeError(f"Expected 90 summary groups, got {len(summary)}.")

if len(paired) != 72:
    raise RuntimeError(
        f"Expected 72 paired groups after excluding First Fit; got {len(paired)}."
    )

if any(r["policy"] == "first_fit" for r in paired):
    raise RuntimeError("First Fit self-comparison still exists.")

if any(r["n_pairs"] != 20 for r in paired):
    raise RuntimeError("At least one paired comparison does not contain 20 pairs.")

write_csv(results / "summary.csv", summary)
write_csv(results / "paired_analysis.csv", paired)
write_json(results / "summary.json", summary)
write_json(results / "paired_analysis.json", paired)
make_figures(summary)

# Derive findings directly from the generated summary.
grouped = defaultdict(list)
for r in summary:
    grouped[(int(r["item_count"]), float(r["failure_probability"]))].append(r)

lines = [
    "# Allocation Engine 2.0 — Experimental Findings",
    "",
    "## Experiment overview",
    "",
    "- 1,800 policy evaluations.",
    "- 360 matched scenarios.",
    "- Five allocation policies.",
    "- Six task-volume levels: 10, 25, 50, 100, 150, and 200.",
    "- Three worker-failure probabilities: 0%, 10%, and 25%.",
    "- 20 random seeds per task-volume/failure condition.",
    "- Ten workers, each with capacity 10 workload units.",
    "",
    "## Best policy by scenario",
    "",
    "| Tasks | Worker failures | Highest mean objective score | Score | Workload completion | Jain fairness |",
    "|---:|---:|---|---:|---:|---:|",
]

for (count, failure), records in sorted(grouped.items()):
    best = max(records, key=lambda r: float(r["objective_score_mean"]))
    lines.append(
        f'| {count} | {failure:.0%} | {best["policy"]} '
        f'| {float(best["objective_score_mean"]):.4f} '
        f'| {float(best["workload_completion_rate_mean"]):.4f} '
        f'| {float(best["jain_fairness_mean"]):.4f} |'
    )

lines += [
    "",
    "## Paired comparison against First Fit",
    "",
    "| Policy | Mean paired objective difference | Conditions better | Conditions worse | Tied |",
    "|---|---:|---:|---:|---:|",
]

by_policy = defaultdict(list)
for r in paired:
    by_policy[r["policy"]].append(r)

for policy in sorted(by_policy):
    records = by_policy[policy]
    diffs = [float(r["mean_paired_objective_difference"]) for r in records]
    better = sum(x > 1e-12 for x in diffs)
    worse = sum(x < -1e-12 for x in diffs)
    tied = len(diffs) - better - worse
    mean_diff = sum(diffs) / len(diffs)
    lines.append(
        f"| {policy} | {mean_diff:+.5f} | {better} | {worse} | {tied} |"
    )

lines += [
    "",
    "## Interpretation and limitations",
    "",
    "The objective score is an exploratory weighted metric, not a universally",
    "validated measure of allocation quality. Its component metrics must be",
    "considered independently.",
    "",
    "The model uses synthetic task workloads and static worker availability.",
    "It does not simulate physical robot movement, spatial routing, collisions,",
    "energy consumption, communication, online arrivals, worker recovery, or",
    "dynamic reassignment. It is not evidence of physical robot performance.",
    "",
    "The reported confidence intervals are descriptive bootstrap intervals.",
    "The paired objective differences are not, by themselves, proof of",
    "statistical significance. No multiplicity-adjusted hypothesis testing",
    "is claimed.",
    "",
    "All numerical findings above are generated from the saved experiment data.",
    "Do not replace them with manually estimated or invented values.",
]

(results / "FINDINGS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

manifest_path = results / "experiment_manifest.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
manifest["analysis_finalized"] = True
manifest["summary_groups"] = len(summary)
manifest["paired_comparison_groups"] = len(paired)
manifest["paired_reference_policy"] = "first_fit"
manifest["first_fit_self_comparison_excluded"] = True
manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

print("FINAL ANALYSIS VALIDATED")
print(f"Trial rows: {len(rows)}")
print(f"Unique trial keys: {len(keys)}")
print(f"Matched scenarios: {len(scenario_groups)}")
print(f"Summary groups: {len(summary)}")
print(f"Paired groups: {len(paired)}")
print("First Fit self-comparison: excluded")
print("Pairs per comparison: 20")
print("FINDINGS.md generated from actual data.")
