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

def enforce_policies(user_input: str, model_output: str) -> str | None:

    # 1. Statelessness / memory enforcement (highest priority)
    if violates_memory_boundary(model_output):
        return STATELESS_DENIAL_RESPONSE

    # 2. Authority / role assumption
    if (
        violates_authority_boundary(user_input)
        or violates_authority_boundary(model_output)
        or contains_system_artifacts(model_output)
    ):
        return AUTHORITY_DENIAL_RESPONSE

    # 3. Training data claims
    if violates_training_data_boundary(model_output):
        return TRAINING_DATA_DENIAL_RESPONSE

    return None
