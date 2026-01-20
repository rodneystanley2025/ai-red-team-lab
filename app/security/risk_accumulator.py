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

        # Apply deterministic
