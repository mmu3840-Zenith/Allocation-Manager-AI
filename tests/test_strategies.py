from src.environment.warehouse_env import AllocationEnvironment
from src.hub.allocation_hub import AllocationHub
from src.strategies.strategies import (
    BalancedAllocation,
    GreedyAllocation,
    RandomAllocation,
)


def test_strategies_produce_valid_results():
    environment = AllocationEnvironment(
        worker_count=5,
        worker_capacity=10,
        seed=42,
    )

    items = environment.generate_items(20)

    for strategy in [
        RandomAllocation(seed=42),
        GreedyAllocation(),
        BalancedAllocation(),
    ]:
        hub = AllocationHub(environment.workers)
        result = hub.allocate(items, strategy)

        assert result.total_items == 20
        assert result.allocated_items <= 20
        assert result.unallocated_items >= 0
        assert 0.0 <= result.allocation_rate <= 1.0
        assert result.utilization_mean >= 0.0
        assert result.load_imbalance >= 0.0
