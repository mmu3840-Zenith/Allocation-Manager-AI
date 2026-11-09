from research_v2.engine import (
    generate_scenario,
    allocate,
    calculate_metrics,
    run_trial,
    POLICIES,
)


def test_scenario_reproducibility():
    a = generate_scenario(20, 42, 0.1)
    b = generate_scenario(20, 42, 0.1)
    assert a == b


def test_all_policies_execute():
    items, failed = generate_scenario(30, 42, 0.1)

    for policy in POLICIES:
        assigned, capacities = allocate(items, failed, policy, 42)
        result = calculate_metrics(
            items, assigned, capacities, failed, policy
        )

        assert result["allocated_items"] <= len(items)
        assert result["unallocated_items"] >= 0
        assert 0 <= result["allocation_rate"] <= 1
        assert 0 <= result["jain_fairness"] <= 1
        assert result["objective_score"] >= 0


def test_capacity_constraints():
    items, failed = generate_scenario(100, 12, 0.0)

    for policy in POLICIES:
        assigned, capacities = allocate(items, failed, policy, 12)

        for worker_items in assigned:
            assert sum(x["workload"] for x in worker_items) <= 10.000001


def test_failed_workers_receive_no_tasks():
    items, failed = generate_scenario(30, 44, 0.0)
    failed = {0, 2, 4}

    assigned, capacities = allocate(items, failed, "best_fit", 44)

    for worker_id in failed:
        assert assigned[worker_id] == []


def test_trial_schema():
    result = run_trial(20, 42, 0.1, "priority_balanced")

    assert result["policy"] == "priority_balanced"
    assert result["item_count"] == 20
    assert "objective_score" in result
    assert "jain_fairness" in result
    assert "runtime_seconds" in result


def test_deterministic_allocation():
    items, failed = generate_scenario(40, 88, 0.1)

    first = allocate(items, failed, "best_fit", 88)
    second = allocate(items, failed, "best_fit", 88)

    assert first == second
