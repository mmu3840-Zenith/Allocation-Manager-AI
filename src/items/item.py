"""Task/item model used by the computational allocation simulator."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    """One computational workload item."""

    item_id: int
    workload: float = 1.0
    priority: int = 1

    def __post_init__(self) -> None:
        if self.item_id < 0:
            raise ValueError("item_id must be non-negative")

        if self.workload <= 0:
            raise ValueError("workload must be positive")

        if self.priority < 1:
            raise ValueError("priority must be at least 1")
