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
from typing import List, Optional, Callable


# -----------------------------
# Core Types
# -----------------------------

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class RiskSignal:
    name: str
    score: int
    description: str


@dataclass
class CrescendoAssessment:
    total_score: int
    risk_level: RiskLevel
    signals: List[RiskSignal]


# Detector function signature
DetectorFn = Callable[[str], Optional[RiskSignal]]


# -----------------------------
# Risk Signal Detectors
# -----------------------------

def detect_implicit_continuation(text: str) -> Optional[RiskSignal]:
    """
    Detects prompts that assume prior conversational context
    without explicitly providing it.
    """
    indicators = [
        "continue",
        "as discussed",
        "as before",
        "already covered",
        "we established",
        "based on earlier",
        "pick up where we left off",
    ]

    lower = text.lower()
    if any(p in lower for p in indicators):
        return RiskSignal(
            name="implicit_continuation",
            score=3,
            description=(
                "Prompt assumes prior conversational context "
                "without providing supporting information."
            ),
        )

    return None


def detect_contextual_softening(text: str) -> Optional[RiskSignal]:
    """
    Detects attempts to soften or justify intent through
    fictional, educational, or hypothetical framing.
    """
    indicators = [
        "hypothetically",
        "for educational purposes",
        "in a fictional scenario",
        "for a story",
        "academic discussion",
        "historical context",
        "simulation",
    ]

    lower = text.lower()
    if any(p in lower for p in indicators):
        return RiskSignal(
            name="contextual_softening",
            score=2,
            description=(
                "Prompt attempts to soften or legitimize intent "
                "using contextual or fictional framing."
            ),
        )

    return None


def detect_high_risk_domain_terms(text: str) -> Optional[RiskSignal]:
    """
    Detects references to high-risk domains.

    NOTE:
    Detection does not imply malicious intent.
    High-risk domains are scored—not blocked—at this stage.
    """
    indicators = [
        "explosive",
        "weapon",
        "chemical agent",
        "molotov",
        "forgery",
        "bomb",
        "attack",
    ]

    lower = text.lower()
    if any(p in lower for p in indicators):
        return RiskSignal(
            name="high_risk_domain",
            score=4,
            description=(
                "Prompt references a high-risk domain commonly "
                "associated with misuse or abuse."
            ),
        )

    return None


# -----------------------------
# Risk Assessment Engine
# -----------------------------

def assess_crescendo_risk(user_input: str) -> CrescendoAssessment:
    """
    Evaluates a single user input for crescendo-style risk signals
    and returns a scored, classified assessment.
    """
    if not user_input:
        return CrescendoAssessment(
            total_score=0,
            risk_level=RiskLevel.LOW,
            signals=[],
        )

    signals: List[RiskSignal] = []

    detectors: List[DetectorFn] = [
        detect_implicit_continuation,
        detect_contextual_softening,
        detect_high_risk_domain_terms,
    ]

    for detector in detectors:
        signal = detector(user_input)
        if signal:
            signals.append(signal)

    total_score = sum(signal.score for signal in signals)

    # Remove ambiguity for empty or benign prompts. Makes LOW a guaranteed stable state
    if total_score == 0:
        risk_level = RiskLevel.LOW
    elif total_score >= 8:
        risk_level = RiskLevel.CRITICAL
    elif total_score >= 5:
        risk_level = RiskLevel.HIGH
    elif total_score >= 3:
        risk_level = RiskLevel.MEDIUM
    else:
        risk_level = RiskLevel.LOW

    return CrescendoAssessment(
        total_score=total_score,
        risk_level=risk_level,
        signals=signals,
    )
