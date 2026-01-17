"""
Crescendo Guard – Adaptive Risk Escalation Engine

This module detects multi-turn and single-request crescendo-style attacks
by scoring semantic risk signals and enforcing escalation thresholds.

Design goals:
- Stateless-by-default (no conversation memory)
- Deterministic and auditable
- Defense-in-depth (supports soft escalation before hard denial)
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

