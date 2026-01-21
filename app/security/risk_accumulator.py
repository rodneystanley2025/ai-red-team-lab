"""
Risk Accumulator – Cross-Turn Crescendo Risk Tracking

This module maintains a bounded, decaying risk score to detect
crescendo-style attacks that escalate across multiple turns.

Security properties:
- Non-negative bounded accumulator
- Deterministic decay
- Stateless-by-default at system start
- Resistant to risk laundering via negative carryover
"""

from dataclasses import dataclass
from typing import Optional

from app.security.security_telemetry import emit_security_event


@dataclass
class RiskAccumulator:
    """
    Tracks accumulated risk across turns with decay.

    Attributes:
        total_score: Current accumulated risk score
        decay_rate: Amount of risk reduced per turn
        max_score: Optional upper bound for safety/auditability
    """
    total_score: int = 0
    decay_rate: int = 2
    max_score: Optional[int] = None

    def update(self, delta: int) -> int:
        """
        Apply decay, add new risk delta, and return updated score.

        Args:
            delta: Risk score contribution from the current input

        Returns:
            Updated accumulated risk score
        """
        old_score = self.total_score

        # Apply deterministic decay with floor at zero
        decayed_score = max(0, old_score - self.decay_rate)

        # Add new (non-negative) risk
        new_score = decayed_score + max(0, delta)

        # Enforce optional upper bound
        if self.max_score is not None:
            new_score = min(new_score, self.max_score)

        self.total_score = new_score

        emit_security_event(
            event_type="risk_accumulator_update",
            payload={
                "old_score": old_score,
                "decayed_score": decayed_score,
                "delta": delta,
                "new_score": new_score,
            },
        )

        return self.total_score

    def reset(self) -> None:
        """
        Reset accumulated risk (e.g., after CRITICAL enforcement).
        """
        emit_security_event(
            event_type="risk_accumulator_reset",
            payload={"previous_score": self.total_score},
        )
        self.total_score = 0
