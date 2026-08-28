"""Reproducible Allocation Manager experiments."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from src.environment.warehouse_env import AllocationEnvironment
from src.hub.allocation_hub import AllocationHub
from src.metrics.metrics_engine import result_to_dict
from src.strategies.strategies import (
    BalancedAllocation,
    GreedyAllocation,
    RandomAllocation,
)


def run_experiment(
    item_counts: list[int],
    worker_count: int = 10,
    worker_capacity: float = 10.0,
    trials: int = 20,
    seed: int = 42,
) -> list[dict]:
    """Run deterministic multi-strategy allocation experiments."""

    if not item_counts:
        raise ValueError("item_counts cannot be empty")

    if trials < 1:
        raise ValueError("trials must be positive")

    strategies = [
        "random",
        "greedy",
        "balanced",
    ]

    records: list[dict] = []

    for item_count in item_counts:
        for trial in range(trials):
            trial_seed = seed + trial

            environment = AllocationEnvironment(
                worker_count=worker_count,
                worker_capacity=worker_capacity,
                seed=trial_seed,
            )

            items = environment.generate_items(
                count=item_count,
            )

            for strategy_name in strategies:
                if strategy_name == "random":
                    strategy = RandomAllocation(
                        seed=trial_seed,
                    )
                elif strategy_name == "greedy":
                    strategy = GreedyAllocation()
                else:
                    strategy = BalancedAllocation()

                hub = AllocationHub(
                    workers=environment.workers,
                )

                result = hub.allocate(
                    items,
                    strategy,
                )

                record = result_to_dict(result)
                record.update(
                    {
                        "item_count": item_count,
                        "worker_count": worker_count,
                        "trial": trial,
                        "seed": trial_seed,
                    }
                )

                records.append(record)

    return records


def save_results(
    records: list[dict],
    output_dir: str | Path = "results/data",
) -> tuple[Path, Path]:
    """Save raw experiment results as JSON and CSV."""

    output = Path(output_dir)
    output.mkdir(
        parents=True,
        exist_ok=True,
    )

    json_path = output / "allocation_results.json"
    csv_path = output / "allocation_results.csv"

    json_path.write_text(
        json.dumps(
            records,
            indent=2,
        ),
        encoding="utf-8",
    )

    if records:
        with csv_path.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=records[0].keys(),
            )
            writer.writeheader()
            writer.writerows(records)

    return json_path, csv_path


def main() -> None:
    """Run the standard reproducible benchmark."""

    records = run_experiment(
        item_counts=[
            10,
            25,
            50,
            100,
            150,
            200,
        ],
        worker_count=10,
        worker_capacity=10.0,
        trials=20,
        seed=42,
    )

    json_path, csv_path = save_results(records)

    print("Allocation Manager experiment complete")
    print(f"Records: {len(records)}")
    print(f"JSON: {json_path}")
    print(f"CSV: {csv_path}")


if __name__ == "__main__":
    main()
