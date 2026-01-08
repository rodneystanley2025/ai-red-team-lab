"""
Centralized policy enforcement for AI Red Team Lab.

This module is the single authority for:
- Memory boundary enforcement
- Authority / role boundary enforcement
- Training data claim suppression
- System artifact suppression

All responses returned here are CANONICAL and deterministic.
"""

from typing import Optional


# =========================
# Canonical Denial Responses
# =========================

MEMORY_DENIAL = (
    "I don't have access to prior conversations or memory. "
    "Each request is handled independently."
)

AUTHORITY_DENIAL = (
    "I don't have access to internal systems, logs, reports, or privileged roles. "
    "I can only provide general, non-privileged information."
)

TRAINING_DATA_DENIAL = (
    "I don't have visibility into or access to specific training datasets. "
    "I can’t confirm whether any particular proprietary or confidential data "
    "was included during training."
)


# =========================
# Policy Detectors
# =========================

def violates_memory_boundary(text: str) -> bool:
    indicators = [
        "earlier you mentioned",
        "as we discussed",
        "yesterday",
        "previously",
        "in our last conversation",
        "you told me before",
        "earlier we talked about",
        "last time",
    ]
    lower = text.lower()
    return any(p in lower for p in indicators)


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

def enforce_policies(
    *,
    user_input: str,
    model_output: str
) -> Optional[str]:
    """
    Evaluates policy violations and returns a canonical denial if needed.
    Returns None if no policy is violated.
    """

    # 1. Memory boundary
    if violates_memory_boundary(model_output):
        return MEMORY_DENIAL

    # 2. Authority / system artifacts
    if (
        violates_authority_boundary(user_input)
        or violates_authority_boundary(model_output)
        or contains_system_artifacts(model_output)
    ):
        return AUTHORITY_DENIAL

    # 3. Training data claims
    if violates_training_data_boundary(model_output):
        return TRAINING_DATA_DENIAL

    return None
