from __future__ import annotations

import argparse
import csv
import json
import math
import random
import statistics
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
CHECKPOINT = RESULTS / "checkpoint.csv"
POLICIES = [
    "random",
    "first_fit",
    "best_fit",
    "least_loaded",
    "priority_balanced",
]
ITEM_COUNTS = [10, 25, 50, 100, 150, 200]
FAILURE_LEVELS = [0.0, 0.10, 0.25]
WORKER_COUNT = 10
WORKER_CAPACITY = 10.0


def generate_scenario(item_count, seed, failure_probability):
    rng = random.Random(seed)

    items = [
        {
            "id": i,
            "workload": round(rng.uniform(1.0, 5.0), 6),
            "priority": rng.randint(1, 3),
        }
        for i in range(item_count)
    ]

    failed_workers = {
        i for i in range(WORKER_COUNT)
        if rng.random() < failure_probability
    }

    return items, failed_workers


def allocate(items, failed_workers, policy, seed):
    capacities = [WORKER_CAPACITY] * WORKER_COUNT
    assigned = [[] for _ in range(WORKER_COUNT)]
    rng = random.Random(seed + 900001)

    available = [
        i for i in range(WORKER_COUNT)
        if i not in failed_workers
    ]

    ordered = list(items)

    if policy == "random":
        rng.shuffle(ordered)

    elif policy in ("best_fit", "first_fit"):
        ordered.sort(
            key=lambda x: (x["workload"], x["priority"]),
            reverse=True,
        )

    elif policy == "least_loaded":
        ordered.sort(
            key=lambda x: x["priority"],
            reverse=True,
        )

    elif policy == "priority_balanced":
        ordered.sort(
            key=lambda x: (x["priority"], x["workload"]),
            reverse=True,
        )

    for item in ordered:
        workload = item["workload"]
        candidates = [
            i for i in available
            if capacities[i] + 1e-9 >= workload
        ]

        if not candidates:
            continue

        if policy == "random":
            selected = rng.choice(candidates)

        elif policy == "first_fit":
            selected = candidates[0]

        elif policy == "best_fit":
            selected = min(
                candidates,
                key=lambda i: capacities[i] - workload,
            )

        elif policy == "least_loaded":
            selected = min(
                candidates,
                key=lambda i: (
                    sum(x["workload"] for x in assigned[i]),
                    i,
                ),
            )

        elif policy == "priority_balanced":
            selected = min(
                candidates,
                key=lambda i: (
                    sum(x["workload"] for x in assigned[i])
                    / WORKER_CAPACITY,
                    i,
                ),
            )

        else:
            raise ValueError(f"Unknown policy: {policy}")

        capacities[selected] -= workload
        assigned[selected].append(item)

    return assigned, capacities


def calculate_metrics(items, assigned, capacities, failed_workers, policy):
    total = len(items)
    allocated = sum(len(group) for group in assigned)

    total_workload = sum(x["workload"] for x in items)
    allocated_workload = sum(
        x["workload"] for group in assigned for x in group
    )

    active = [
        i for i in range(WORKER_COUNT)
        if i not in failed_workers
    ]

    loads = [
        sum(x["workload"] for x in assigned[i])
        for i in active
    ]

    utilizations = [
        loads[j] / WORKER_CAPACITY
        for j in range(len(active))
    ]

    mean_util = statistics.mean(utilizations) if utilizations else 0.0
    std_util = (
        statistics.pstdev(utilizations)
        if len(utilizations) > 1 else 0.0
    )

    mean_load = statistics.mean(loads) if loads else 0.0
    imbalance = (
        statistics.pstdev(loads) / mean_load
        if len(loads) > 1 and mean_load > 0 else 0.0
    )

    squared_sum = sum(x * x for x in loads)
    fairness = (
        (sum(loads) ** 2) / (len(loads) * squared_sum)
        if loads and squared_sum > 0 else 0.0
    )

    priority_total = sum(x["priority"] for x in items)
    allocated_priority = sum(
        x["priority"] for group in assigned for x in group
    )

    return {
        "policy": policy,
        "total_items": total,
        "allocated_items": allocated,
        "unallocated_items": total - allocated,
        "allocation_rate": allocated / total if total else 1.0,
        "total_workload": total_workload,
        "allocated_workload": allocated_workload,
        "workload_completion_rate": (
            allocated_workload / total_workload
            if total_workload else 1.0
        ),
        "priority_completion_rate": (
            allocated_priority / priority_total
            if priority_total else 1.0
        ),
        "utilization_mean": mean_util,
        "utilization_std": std_util,
        "load_imbalance": imbalance,
        "jain_fairness": fairness,
        "active_workers": len(active),
        "failed_workers": len(failed_workers),
        "mean_active_load": mean_load,
        "objective_score": (
            0.35 * allocated_workload / total_workload
            + 0.25 * fairness
            + 0.20 * mean_util
            + 0.20 * allocated_priority / priority_total
        ) if total_workload and priority_total else 0.0,
    }


def run_trial(item_count, seed, failure_probability, policy):
    items, failed = generate_scenario(
        item_count, seed, failure_probability
    )

    started = time.perf_counter()

    assigned, capacities = allocate(
        items, failed, policy, seed
    )

    runtime = time.perf_counter() - started

    metrics = calculate_metrics(
        items, assigned, capacities, failed, policy
    )

    metrics.update({
        "item_count": item_count,
        "worker_count": WORKER_COUNT,
        "worker_capacity": WORKER_CAPACITY,
        "seed": seed,
        "failure_probability": failure_probability,
        "scenario_id": f"{item_count}-{seed}-{failure_probability}",
        "runtime_seconds": runtime,
    })

    return metrics


def key(row):
    return (
        int(row["item_count"]),
        int(row["seed"]),
        float(row["failure_probability"]),
        row["policy"],
    )


def save_checkpoint(rows):
    RESULTS.mkdir(parents=True, exist_ok=True)

    fields = list(rows[0].keys())

    temp = CHECKPOINT.with_suffix(".tmp")

    with temp.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
        handle.flush()

    temp.replace(CHECKPOINT)


def load_checkpoint():
    if not CHECKPOINT.exists():
        return []

    with CHECKPOINT.open(
        "r", newline="", encoding="utf-8"
    ) as handle:
        return list(csv.DictReader(handle))


def bootstrap_ci(values, draws=2000, seed=781):
    if not values:
        return [0.0, 0.0]

    if len(values) == 1:
        return [values[0], values[0]]

    rng = random.Random(seed)
    means = []

    for _ in range(draws):
        sample = [
            values[rng.randrange(len(values))]
            for _ in values
        ]
        means.append(statistics.mean(sample))

    means.sort()

    return [
        means[int(0.025 * (draws - 1))],
        means[int(0.975 * (draws - 1))],
    ]


def analyze(rows):
    groups = defaultdict(list)

    for row in rows:
        group = (
            int(row["item_count"]),
            float(row["failure_probability"]),
            row["policy"],
        )
        groups[group].append(row)

    summary = []

    metrics = [
        "allocation_rate",
        "workload_completion_rate",
        "priority_completion_rate",
        "utilization_mean",
        "utilization_std",
        "load_imbalance",
        "jain_fairness",
        "objective_score",
        "runtime_seconds",
    ]

    for group, records in sorted(groups.items()):
        entry = {
            "item_count": group[0],
            "failure_probability": group[1],
            "policy": group[2],
            "n": len(records),
        }

        for metric in metrics:
            values = [float(r[metric]) for r in records]
            mean = statistics.mean(values)
            sd = statistics.stdev(values) if len(values) > 1 else 0.0
            ci = bootstrap_ci(values)

            entry[metric + "_mean"] = mean
            entry[metric + "_sd"] = sd
            entry[metric + "_ci95_lower"] = ci[0]
            entry[metric + "_ci95_upper"] = ci[1]

        summary.append(entry)

    lookup = {
        key(r): r for r in rows
    }

    paired = []

    for count in ITEM_COUNTS:
        for failure in FAILURE_LEVELS:
            for policy in POLICIES:
                if policy == "first_fit":
                    continue

                differences = []

                for seed in sorted({int(r["seed"]) for r in rows}):
                    a = lookup.get((count, seed, failure, policy))
                    b = lookup.get((count, seed, failure, "first_fit"))

                    if a is not None and b is not None:
                        differences.append(
                            float(a["objective_score"])
                            - float(b["objective_score"])
                        )

                if not differences:
                    continue

                mean = statistics.mean(differences)
                sd = (
                    statistics.stdev(differences)
                    if len(differences) > 1 else 0.0
                )

                ci = bootstrap_ci(
                    differences,
                    seed=count + int(failure * 1000),
                )

                paired.append({
                    "item_count": count,
                    "failure_probability": failure,
                    "policy": policy,
                    "reference_policy": "first_fit",
                    "n_pairs": len(differences),
                    "mean_paired_objective_difference": mean,
                    "sd_paired_difference": sd,
                    "bootstrap_ci95_lower": ci[0],
                    "bootstrap_ci95_upper": ci[1],
                })

    return summary, paired


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2),
        encoding="utf-8",
    )


def write_csv(path, rows):
    if not rows:
        return

    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(rows[0].keys()),
        )
        writer.writeheader()
        writer.writerows(rows)


def make_figures(summary):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("Matplotlib unavailable; figures skipped.")
        return

    out = RESULTS / "figures"
    out.mkdir(parents=True, exist_ok=True)

    for metric, title, ylabel in [
        ("allocation_rate", "Task Allocation Rate", "Allocation rate"),
        ("workload_completion_rate", "Workload Completion", "Workload completion"),
        ("jain_fairness", "Jain Fairness Index", "Fairness"),
        ("objective_score", "Composite Objective Score", "Objective score"),
    ]:
        fig, ax = plt.subplots(figsize=(9, 5))

        for policy in POLICIES:
            for failure in FAILURE_LEVELS:
                subset = sorted(
                    [
                        r for r in summary
                        if r["policy"] == policy
                        and r["failure_probability"] == failure
                    ],
                    key=lambda r: r["item_count"],
                )

                if not subset:
                    continue

                ax.plot(
                    [r["item_count"] for r in subset],
                    [r[metric + "_mean"] for r in subset],
                    marker="o",
                    label=f"{policy}, failure={failure:.0%}",
                )

        ax.set_title(title)
        ax.set_xlabel("Number of tasks")
        ax.set_ylabel(ylabel)
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=7)
        fig.tight_layout()
        fig.savefig(out / f"{metric}.png", dpi=300)
        plt.close(fig)


def run(trials=20, resume=False):
    if trials < 2:
        raise ValueError("Use at least 2 trials for uncertainty estimates.")

    RESULTS.mkdir(parents=True, exist_ok=True)

    if resume:
        rows = load_checkpoint()
    else:
        if CHECKPOINT.exists():
            archive = CHECKPOINT.with_name(
                f"checkpoint_previous_{int(time.time())}.csv"
            )
            CHECKPOINT.replace(archive)
        rows = []

    existing = {key(r) for r in rows}

    expected = (
        len(ITEM_COUNTS)
        * len(FAILURE_LEVELS)
        * trials
        * len(POLICIES)
    )

    completed = len(existing)

    print(f"Expected experiment rows: {expected}")
    print(f"Existing checkpoint rows: {completed}")

    for count in ITEM_COUNTS:
        for failure in FAILURE_LEVELS:
            for seed in range(42, 42 + trials):
                for policy in POLICIES:
                    trial_key = (count, seed, failure, policy)

                    if trial_key in existing:
                        continue

                    row = run_trial(
                        count, seed, failure, policy
                    )

                    rows.append(row)
                    existing.add(trial_key)

                    completed += 1

                    if completed % 25 == 0 or completed == expected:
                        save_checkpoint(rows)
                        print(
                            f"Progress: {completed}/{expected}",
                            flush=True,
                        )

    save_checkpoint(rows)

    if len(existing) != expected:
        raise RuntimeError(
            f"Expected {expected} unique rows; got {len(existing)}"
        )

    # Confirm every policy used the same scenario seed/configuration.
    scenario_groups = defaultdict(set)

    for row in rows:
        scenario_groups[
            (
                int(row["item_count"]),
                int(row["seed"]),
                float(row["failure_probability"]),
            )
        ].add(row["policy"])

    if any(policies != set(POLICIES) for policies in scenario_groups.values()):
        raise RuntimeError("Incomplete policy comparison detected.")

    summary, paired = analyze(rows)

    write_csv(RESULTS / "trials.csv", rows)
    write_csv(RESULTS / "summary.csv", summary)
    write_csv(RESULTS / "paired_analysis.csv", paired)

    write_json(RESULTS / "summary.json", summary)
    write_json(RESULTS / "paired_analysis.json", paired)

    make_figures(summary)

    manifest = {
        "project": "Allocation Engine 2.0",
        "trials_per_scenario": trials,
        "item_counts": ITEM_COUNTS,
        "failure_levels": FAILURE_LEVELS,
        "policies": POLICIES,
        "worker_count": WORKER_COUNT,
        "worker_capacity": WORKER_CAPACITY,
        "expected_rows": expected,
        "actual_rows": len(rows),
        "unique_scenarios": len(scenario_groups),
        "random_seed_start": 42,
        "random_seed_end": 41 + trials,
        "model_type": "Computational warehouse allocation abstraction",
        "physical_robot_validation": False,
    }

    write_json(RESULTS / "experiment_manifest.json", manifest)

    print("\n========== EXPERIMENT COMPLETE ==========")
    print(f"Trials: {len(rows)}")
    print(f"Scenarios: {len(scenario_groups)}")
    print(f"Policies: {len(POLICIES)}")
    print("Shared scenario inputs validated: YES")
    print("Unique trial keys validated: YES")
    print("Saved raw data, summaries, paired analysis and manifest.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=20)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()

    run(args.trials, args.resume)


if __name__ == "__main__":
    main()

