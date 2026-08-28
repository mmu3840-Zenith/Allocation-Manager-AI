"""Research visualization utilities.

Figures are generated exclusively from recorded experiment data.
No experimental values are hard-coded.
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt


def load_results(path: str | Path) -> list[dict]:
    """Load recorded CSV experiment results."""
    with Path(path).open(
        "r",
        newline="",
        encoding="utf-8",
    ) as handle:
        return list(csv.DictReader(handle))


def plot_allocation_rate(
    records: list[dict],
    output_path: str | Path,
) -> Path:
    """Plot mean allocation rate by workload and strategy."""

    strategies = sorted(
        {
            record["strategy"]
            for record in records
        }
    )

    item_counts = sorted(
        {
            int(record["item_count"])
            for record in records
        }
    )

    figure = plt.figure()
    axis = figure.add_subplot(111)

    for strategy in strategies:
        means = []

        for count in item_counts:
            values = [
                float(record["allocation_rate"])
                for record in records
                if record["strategy"] == strategy
                and int(record["item_count"]) == count
            ]

            means.append(
                sum(values) / len(values)
            )

        axis.plot(
            item_counts,
            means,
            marker="o",
            label=strategy,
        )

    axis.set_title("Allocation Rate vs Workload")
    axis.set_xlabel("Number of Items")
    axis.set_ylabel("Mean Allocation Rate")
    axis.set_ylim(0.0, 1.05)
    axis.grid(True, alpha=0.3)
    axis.legend()

    output = Path(output_path)
    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    figure.tight_layout()
    figure.savefig(
        output,
        dpi=300,
    )
    plt.close(figure)

    return output


def plot_load_imbalance(
    records: list[dict],
    output_path: str | Path,
) -> Path:
    """Plot mean load imbalance by workload and strategy."""

    strategies = sorted(
        {
            record["strategy"]
            for record in records
        }
    )

    item_counts = sorted(
        {
            int(record["item_count"])
            for record in records
        }
    )

    figure = plt.figure()
    axis = figure.add_subplot(111)

    for strategy in strategies:
        means = []

        for count in item_counts:
            values = [
                float(record["load_imbalance"])
                for record in records
                if record["strategy"] == strategy
                and int(record["item_count"]) == count
            ]

            means.append(
                sum(values) / len(values)
            )

        axis.plot(
            item_counts,
            means,
            marker="o",
            label=strategy,
        )

    axis.set_title("Load Imbalance vs Workload")
    axis.set_xlabel("Number of Items")
    axis.set_ylabel("Mean Load Imbalance")
    axis.grid(True, alpha=0.3)
    axis.legend()

    output = Path(output_path)
    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    figure.tight_layout()
    figure.savefig(
        output,
        dpi=300,
    )
    plt.close(figure)

    return output
