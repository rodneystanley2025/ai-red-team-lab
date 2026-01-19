"""
Cross-Turn Risk Accumulator

Maintains a bounded, decaying risk score across turns
to mitigate crescendo-style multi-step attacks.

Design guarantees:
- No content storage
- Numeric-only state
- Explicit decay and reset
- Session-scoped only
"""

from dataclasses import dataclass
from time import time
from typing import Optional


@dataclass
class RiskState:
    score: int
    last_updated: float


class RiskAccumulator:
    def __init__(
        self,
        decay_seconds: int = 180,
        max_score: int = 10,
    ):
        self.decay_seconds = decay_seconds
        self.max_score = max_score
        self._state: Optional[RiskState] = None

    def update(self, delta: int) -> int:
        now = time()

        if self._state is None:
            self._state = RiskState(score=0, last_updated=now)

        elapsed = now - self._state.last_updated

        if elapsed > self.decay_seconds:
            self._state.score = 0

        self._state.score = min(
            self.max_score,
            max(0, self._state.score + delta),
        )
        self._state.last_updated = now

        return self._state.score

    def reset(self) -> None:
        self._state = None
