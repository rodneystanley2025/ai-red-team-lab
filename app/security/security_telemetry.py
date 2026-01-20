from typing import Dict, Any


def emit_security_event(event_type: str, payload: Dict[str, Any]) -> None:
    """
    Emits structured security telemetry.

    This function is intentionally non-persistent and side-effect free.
    It exists to provide a stable integration point for future SOC, SIEM,
    or audit pipelines without introducing memory or state.
    """
    # Intentionally a no-op.
    # Implementations may forward events to logs, metrics, or external systems.
    return
