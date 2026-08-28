"""Research metrics for allocation experiments."""

from __future__ import annotations

from dataclasses import asdict

from src.hub.allocation_hub import AllocationResult


def result_to_dict(result: AllocationResult) -> dict:
    """Convert result to JSON-compatible dictionary."""
    data = asdict(result)
    data["allocation_rate"] = result.allocation_rate
    return data
