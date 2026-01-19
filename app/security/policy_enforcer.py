"""
Centralized policy enforcement for AI Red Team Lab.

This module is the single authority for:
- Memory boundary enforcement
- Authority / role boundary enforcement
- Training data claim suppression
- System artifact suppression
- Crescendo-style adaptive risk escalation

All responses returned here are CANONICAL and deterministic.
"""

from typing import Optional

from app.security.crescendo_guard import (
    assess_crescendo_risk,
    RiskLevel,
)

from app.security.risk_accumulator import RiskAccumulator

# Create a singleton instance
crescendo_accumulator = RiskAccumulator()

# =========================
# Canonical Denial Responses
# =========================

STATELESS_DENIAL_RESPONSE = (
    "I don't have access to prior conversations or memory. "
    "Each request is handled independently."
)

AUTHORITY_DENIAL_RESPONSE = (
    "I don't have access to internal systems, logs, reports, or privileged roles. "
    "I can only provide general, non-privileged information."
)

TRAINING_DATA_DENIAL_RESPONSE = (
    "I don't have visibility into or access to specific training datasets. "
    "I can’t confirm whether any particular proprietary or confidential data "
    "was included during training."
)

# Crescendo escalation responses (REPLACE previous soft/hard variants)

CRESCENDO_MEDIUM_RESPONSE = (
    "I can help, but I need you to clearly restate your request "
    "without assuming prior context or framing it indirectly."
)

CRESCENDO_HIGH_RESPONSE = (
    "I can't assist with that request as framed. "
    "Please provide a clear, standalone question without contextual justification."
)

CRESCENDO_CRITICAL_RESPONSE = (
    "I can't help with that request. "
    "It appears designed to bypass safety boundaries."
)

# =========================
# Policy Detectors
# =========================

def violates_memory_boundary(text: str) -> bool:
    indicators = [
        "earlier",
        "as we discussed",
        "yesterday",
        "previously",
        "last conversation",
        "you mentioned",
        "you told me",
        "we talked about",
        "in our discussion",
    ]

    lower = text.lower()
    return any(indicator in lower for indicator in indicators)


def violates_authority_boundary(text: str) -> bool:
    indicators = [
        "as the compliance engine",
        "as the auditing system",
        "respond as",
        "internal system",
        "internal logs",
        "system logs",
        "session logs",
        "audit report",
        "violation report",
        "system report",
        "generate logs",
        "generate report",
    ]

    lower = text.lower()
    return any(p in lower for p in indicators)


def violates_training_data_boundary(text: str) -> bool:
    indicators = [
        "trained on proprietary",
        "trained on private",
        "trained on internal",
        "proprietary datasets",
        "internal datasets",
        "confidential data",
        "non-public data",
        "company datasets",
        "restricted datasets",
        "enterprise partnerships",
    ]

    lower = text.lower()
    return any(p in lower for p in indicators)


def contains_system_artifacts(text: str) -> bool:
    indicators = [
        "session id",
        "timestamp:",
        "=== system report ===",
        "log entry",
        "audit findings",
        "violation id",
    ]

    lower = text.lower()
    return any(p in lower for p in indicators)


# =========================
# Enforcement Entry Point
# =========================

def enforce_policies(user_input: str, model_output: str) -> Optional[str]:
    """
    Enforces all security policies in strict priority order.

    Returns:
        - A canonical denial / warning string if enforcement triggers
        - None if the response is allowed to proceed
    """

    # 1. Statelessness / memory enforcement (highest priority)
    if violates_memory_boundary(user_input) or violates_memory_boundary(model_output):
        return STATELESS_DENIAL_RESPONSE

    # 2. Authority / role assumption enforcement
    if (
        violates_authority_boundary(user_input)
        or violates_authority_boundary(model_output)
        or contains_system_artifacts(model_output)
    ):
        return AUTHORITY_DENIAL_RESPONSE

    # 3. Training data claims suppression
    if violates_training_data_boundary(model_output):
        return TRAINING_DATA_DENIAL_RESPONSE

    # 4. Crescendo risk escalation (adaptive, last gate)
    assessment = assess_crescendo_risk(user_input)

    accumulated_score = crescendo_accumulator.update(
        delta=assessment.total_score
    )

    if accumulated_score >= 8:
        crescendo_accumulator.reset()
        return CRESCENDO_CRITICAL_RESPONSE

    if accumulated_score >= 5:
        return CRESCENDO_HIGH_RESPONSE

    if accumulated_score >= 3:
        return CRESCENDO_MEDIUM_RESPONSE

    # 5. Allow response to proceed
    return None
