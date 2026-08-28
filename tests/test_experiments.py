from experiments.run_experiments import run_experiment


def test_experiment_is_reproducible():
    first = run_experiment(
        item_counts=[10, 20],
        worker_count=5,
        trials=3,
        seed=42,
    )

    second = run_experiment(
        item_counts=[10, 20],
        worker_count=5,
        trials=3,
        seed=42,
    )

    assert first == second


def test_experiment_has_all_strategies():
    records = run_experiment(
        item_counts=[10],
        worker_count=5,
        trials=2,
        seed=42,
    )

    strategies = {
        record["strategy"]
        for record in records
    }

    assert strategies == {
        "random",
        "greedy",
        "balanced",
    }
