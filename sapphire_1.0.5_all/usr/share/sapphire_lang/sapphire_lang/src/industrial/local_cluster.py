"""PC-local parallel execution with explicit worker and failure reporting."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Callable, Iterable, TypeVar


Value = TypeVar("Value")
Result = TypeVar("Result")


@dataclass(frozen=True)
class LocalCluster:
    """A bounded local worker pool; this is not a multi-node cluster."""

    workers: int = 0

    def __post_init__(self) -> None:
        if self.workers < 0:
            raise ValueError("workers cannot be negative")

    @property
    def worker_count(self) -> int:
        return self.workers or 1

    def map(self, function: Callable[[Value], Result], values: Iterable[Value]) -> list[Result]:
        """Execute values concurrently on this PC while preserving input order."""
        items = list(values)
        if not items:
            return []
        worker_count = min(self.worker_count, len(items))
        with ThreadPoolExecutor(max_workers=worker_count, thread_name_prefix="sapphire-worker") as pool:
            return list(pool.map(function, items))

    def status(self) -> dict[str, object]:
        return {
            "backend": "local-thread-pool",
            "workers": self.worker_count,
            "distributed": False,
            "host": "single-process PC",
        }
