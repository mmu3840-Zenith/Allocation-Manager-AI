import csv
import json
from pathlib import Path
from research_v2.engine import analyze, make_figures, write_csv, write_json

results = Path("research_v2/results")
trials_path = results / "trials.csv"

if not trials_path.exists():
    trials_path = results / "checkpoint.csv"

if not trials_path.exists():
    raise FileNotFoundError("No saved experiment data found.")

with trials_path.open("r", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

expected = 1800
if len(rows) != expected:
    raise RuntimeError(f"Expected {expected} rows, found {len(rows)}")

keys = {
    (int(r["item_count"]), int(r["seed"]),
     float(r["failure_probability"]), r["policy"])
    for r in rows
}

if len(keys) != expected:
    raise RuntimeError(f"Duplicate trial keys: {expected - len(keys)}")

summary, paired = analyze(rows)

# Ensure First Fit is not compared against itself.
if any(r["policy"] == "first_fit" for r in paired):
    raise RuntimeError("First Fit self-comparison remains in paired analysis.")

write_csv(results / "trials.csv", rows)
write_csv(results / "summary.csv", summary)
write_csv(results / "paired_analysis.csv", paired)
write_json(results / "summary.json", summary)
write_json(results / "paired_analysis.json", paired)
make_figures(summary)

print("ANALYSIS REBUILT SUCCESSFULLY")
print(f"Raw experiment rows: {len(rows)}")
print(f"Unique trial keys: {len(keys)}")
print(f"Summary groups: {len(summary)}")
print(f"Paired comparisons: {len(paired)}")
print("First Fit self-comparison: excluded")
print("Figures regenerated.")
