"""Bounded agent execution with retry and recovery hooks."""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar


Result = TypeVar("Result")


@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int = 3
    backoff_seconds: float = 0.05


class AgentLoop(Generic[Result]):
    def __init__(self, policy: RetryPolicy = RetryPolicy()):
        if policy.max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")
        self.policy = policy
        self.events: list[dict[str, object]] = []

    def run(self, action: Callable[[], Result], recover: Callable[[Exception, int], None] | None = None) -> Result:
        last_error: Exception | None = None
        for attempt in range(1, self.policy.max_attempts + 1):
            self.events.append({"event": "attempt", "attempt": attempt})
            try:
                result = action()
                self.events.append({"event": "success", "attempt": attempt})
                return result
            except Exception as error:
                last_error = error
                self.events.append({"event": "failure", "attempt": attempt, "error": str(error)})
                if recover is not None:
                    recover(error, attempt)
                if attempt < self.policy.max_attempts:
                    time.sleep(self.policy.backoff_seconds * attempt)
        raise RuntimeError(f"Agent action failed after {self.policy.max_attempts} attempts") from last_error
