"""Generate research figures from recorded experiment results."""

from pathlib import Path

from src.metrics.plotter import (
    load_results,
    plot_allocation_rate,
    plot_load_imbalance,
)


def main() -> None:
    """Generate all standard figures."""
    data_path = Path(
        "results/data/allocation_results.csv"
    )

    if not data_path.exists():
        raise FileNotFoundError(
            "Run experiments before generating figures."
        )

    records = load_results(data_path)

    plot_allocation_rate(
        records,
        "results/figures/allocation_rate.png",
    )

    plot_load_imbalance(
        records,
        "results/figures/load_imbalance.png",
    )

    print("Research figures generated.")


if __name__ == "__main__":
    main()
