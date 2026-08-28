"""Computational worker model."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class WorkerRobot:
    """Simulated worker with finite computational capacity."""

    worker_id: int
    capacity: float = 10.0
    allocated_workload: float = 0.0
    assigned_items: list[int] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.worker_id < 0:
            raise ValueError("worker_id must be non-negative")

        if self.capacity <= 0:
            raise ValueError("capacity must be positive")

    @property
    def remaining_capacity(self) -> float:
        """Return unused worker capacity."""
        return max(0.0, self.capacity - self.allocated_workload)

    @property
    def utilization(self) -> float:
        """Return normalized utilization in [0, 1]."""
        return min(
            1.0,
            self.allocated_workload / self.capacity,
        )

    def can_accept(self, workload: float) -> bool:
        """Return whether this worker can accept workload."""
        if workload <= 0:
            raise ValueError("workload must be positive")

        return self.remaining_capacity >= workload

    def assign(self, item_id: int, workload: float) -> bool:
        """Attempt to assign one item."""
        if not self.can_accept(workload):
            return False

        self.allocated_workload += workload
        self.assigned_items.append(item_id)
        return True

    def reset(self) -> None:
        """Clear current allocations."""
        self.allocated_workload = 0.0
        self.assigned_items.clear()
