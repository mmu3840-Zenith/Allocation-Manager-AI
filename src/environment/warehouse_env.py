"""Computational warehouse/allocation environment.

This is a simulation abstraction for resource allocation.
It is not a physical warehouse-control system.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

from src.items.item import Item
from src.workers.worker_robot import WorkerRobot


@dataclass
class AllocationEnvironment:
    """Environment containing tasks and finite-capacity workers."""

    worker_count: int = 10
    worker_capacity: float = 10.0
    seed: int = 42

    def __post_init__(self) -> None:
        if self.worker_count < 1:
            raise ValueError("worker_count must be positive")

        if self.worker_capacity <= 0:
            raise ValueError("worker_capacity must be positive")

        self.random = random.Random(self.seed)
        self.workers = [
            WorkerRobot(
                worker_id=i,
                capacity=self.worker_capacity,
            )
            for i in range(self.worker_count)
        ]

    def reset(self) -> None:
        """Reset every worker allocation."""
        for worker in self.workers:
            worker.reset()

    def generate_items(
        self,
        count: int,
        min_workload: float = 1.0,
        max_workload: float = 5.0,
        priority_levels: int = 3,
    ) -> list[Item]:
        """Generate deterministic synthetic workloads."""
        if count < 1:
            raise ValueError("count must be positive")

        if min_workload <= 0 or max_workload < min_workload:
            raise ValueError("invalid workload range")

        if priority_levels < 1:
            raise ValueError("priority_levels must be positive")

        return [
            Item(
                item_id=i,
                workload=self.random.uniform(
                    min_workload,
                    max_workload,
                ),
                priority=self.random.randint(
                    1,
                    priority_levels,
                ),
            )
            for i in range(count)
        ]
