"""Central allocation manager."""

from __future__ import annotations

from dataclasses import dataclass

from src.items.item import Item
from src.workers.worker_robot import WorkerRobot


@dataclass
class AllocationResult:
    """Recorded result of one allocation operation."""

    strategy: str
    total_items: int
    allocated_items: int
    unallocated_items: int
    total_workload: float
    allocated_workload: float
    utilization_mean: float
    utilization_std: float
    load_imbalance: float
    objective_score: float

    @property
    def allocation_rate(self) -> float:
        """Return fraction of tasks allocated."""
        if self.total_items == 0:
            return 1.0

        return self.allocated_items / self.total_items


class AllocationHub:
    """Validate and execute allocations against workers."""

    def __init__(self, workers: list[WorkerRobot]) -> None:
        if not workers:
            raise ValueError("At least one worker is required")

        self.workers = workers

    def reset(self) -> None:
        """Reset all workers."""
        for worker in self.workers:
            worker.reset()

    def allocate(
        self,
        items: list[Item],
        strategy,
    ) -> AllocationResult:
        """Execute a supplied allocation strategy."""
        if not items:
            raise ValueError("At least one item is required")

        self.reset()

        return strategy.allocate(
            items=items,
            workers=self.workers,
        )
