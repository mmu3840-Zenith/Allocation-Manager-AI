"""Allocation strategy implementations."""

from __future__ import annotations

import random
import statistics
from dataclasses import dataclass

from src.hub.allocation_hub import AllocationResult
from src.items.item import Item
from src.workers.worker_robot import WorkerRobot


def _build_result(
    strategy: str,
    items: list[Item],
    workers: list[WorkerRobot],
) -> AllocationResult:
    """Build standardized experimental metrics."""

    total_workload = sum(item.workload for item in items)

    allocated_ids = {
        item_id
        for worker in workers
        for item_id in worker.assigned_items
    }

    allocated_workload = sum(
        item.workload
        for item in items
        if item.item_id in allocated_ids
    )

    utilizations = [
        worker.utilization
        for worker in workers
    ]

    mean_utilization = statistics.fmean(utilizations)
    std_utilization = (
        statistics.pstdev(utilizations)
        if len(utilizations) > 1
        else 0.0
    )

    load_imbalance = max(utilizations) - min(utilizations)

    allocation_rate = (
        len(allocated_ids) / len(items)
        if items
        else 1.0
    )

    objective_score = (
        allocation_rate
        - 0.5 * load_imbalance
        - 0.25 * std_utilization
    )

    return AllocationResult(
        strategy=strategy,
        total_items=len(items),
        allocated_items=len(allocated_ids),
        unallocated_items=len(items) - len(allocated_ids),
        total_workload=total_workload,
        allocated_workload=allocated_workload,
        utilization_mean=mean_utilization,
        utilization_std=std_utilization,
        load_imbalance=load_imbalance,
        objective_score=objective_score,
    )


class RandomAllocation:
    """Random feasible allocation baseline."""

    name = "random"

    def __init__(self, seed: int = 42) -> None:
        self.seed = seed

    def allocate(
        self,
        items: list[Item],
        workers: list[WorkerRobot],
    ) -> AllocationResult:
        rng = random.Random(self.seed)

        shuffled = list(items)
        rng.shuffle(shuffled)

        for item in shuffled:
            candidates = [
                worker
                for worker in workers
                if worker.can_accept(item.workload)
            ]

            if candidates:
                worker = rng.choice(candidates)
                worker.assign(
                    item.item_id,
                    item.workload,
                )

        return _build_result(
            self.name,
            items,
            workers,
        )


class GreedyAllocation:
    """Greedy allocation to the worker with most remaining capacity."""

    name = "greedy"

    def allocate(
        self,
        items: list[Item],
        workers: list[WorkerRobot],
    ) -> AllocationResult:

        ordered = sorted(
            items,
            key=lambda item: (
                -item.priority,
                -item.workload,
                item.item_id,
            ),
        )

        for item in ordered:
            candidates = [
                worker
                for worker in workers
                if worker.can_accept(item.workload)
            ]

            if candidates:
                worker = max(
                    candidates,
                    key=lambda worker: (
                        worker.remaining_capacity,
                        -worker.worker_id,
                    ),
                )

                worker.assign(
                    item.item_id,
                    item.workload,
                )

        return _build_result(
            self.name,
            items,
            workers,
        )


class BalancedAllocation:
    """Load-balancing allocation strategy."""

    name = "balanced"

    def allocate(
        self,
        items: list[Item],
        workers: list[WorkerRobot],
    ) -> AllocationResult:

        ordered = sorted(
            items,
            key=lambda item: (
                -item.priority,
                -item.workload,
                item.item_id,
            ),
        )

        for item in ordered:
            candidates = [
                worker
                for worker in workers
                if worker.can_accept(item.workload)
            ]

            if candidates:
                worker = min(
                    candidates,
                    key=lambda worker: (
                        worker.allocated_workload,
                        worker.worker_id,
                    ),
                )

                worker.assign(
                    item.item_id,
                    item.workload,
                )

        return _build_result(
            self.name,
            items,
            workers,
        )
