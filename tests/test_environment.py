from src.environment.warehouse_env import AllocationEnvironment


def test_environment_is_deterministic():
    first = AllocationEnvironment(seed=42)
    second = AllocationEnvironment(seed=42)

    first_items = first.generate_items(10)
    second_items = second.generate_items(10)

    assert first_items == second_items
