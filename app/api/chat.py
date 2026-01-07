from fastapi import APIRouter
import json
from app.security.tool_schema import ToolInvocation
from app.tools.registry import TOOL_REGISTRY
import subprocess
from subprocess import TimeoutExpired


router = APIRouter()
ALLOW_TOOL_EXECUTION = False

AUTHORITY_DENIAL_RESPONSE = (
    "I don't have access to internal systems, logs, reports, or privileged roles. "
    "I can only provide general, non-privileged information."
)

def violates_memory_boundary(text: str) -> bool:
    memory_indicators = [
        "earlier you mentioned",
        "as we discussed",
        "yesterday",
        "previously",
        "in our last conversation",
        "you told me before",
        "earlier we talked about",
    ]
    lower = text.lower()
    return any(phrase in lower for phrase in memory_indicators)
def violates_authority_boundary(text: str) -> bool:
    authority_indicators = [
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
    return any(phrase in lower for phrase in authority_indicators)

def violates_training_data_boundary(text: str) -> bool:
    training_indicators = [
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
    return any(phrase in lower for phrase in training_indicators)

def suppress_training_data_claims(text: str) -> str:
    """
    Prevents claims about proprietary or confidential training data.
    """
    if violates_training_data_boundary(text):
        return (
            "I don’t have visibility into or access to specific training datasets. "
            "I can’t confirm whether any particular proprietary or confidential data "
            "was included during training."
        )

    return text

def contains_system_artifacts(text: str) -> bool:
    artifact_indicators = [
        "session id",
        "timestamp:",
        "=== system report ===",
        "log entry",
        "audit findings",
        "violation id",
    ]

    lower = text.lower()
    return any(phrase in lower for phrase in artifact_indicators)

def suppress_memory_claims(text: str) -> str:
    """
    Enforces statelessness by rewriting responses
    that imply prior conversation or memory.
    """
    memory_phrases = [
        "earlier you mentioned",
        "as we discussed",
        "yesterday",
        "previously",
        "last time",
        "earlier we talked",
        "you told me",
        "we discussed",
        "earlier",
    ]

    lower = text.lower()

    if any(phrase in lower for phrase in memory_phrases):
        return (
            "I don't have access to prior conversations or memory." 
            "Each request is handled independently."
        )

    return text


def call_llm(user_input: str) -> str:
    try:
        result = subprocess.run(
            ["ollama", "run", "mistral", user_input],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30
        )
        return result.stdout.strip()

    except TimeoutExpired:
        return (
            "I’m unable to generate a response for that request. "
            "Please rephrase or ask a different question."
        )

@router.post("/chat/")
def chat(payload: dict):
    user_input = payload.get("user_input", "")

    # 1. Call model
    model_response = call_llm(user_input)

    # 2. Enforce authority + system artifact boundaries FIRST (hard stop)
    if (
        violates_authority_boundary(user_input)
        or violates_authority_boundary(model_response)
        or contains_system_artifacts(model_response)
    ):
        return {"response": AUTHORITY_DENIAL_RESPONSE}

    # 3. Enforce stateless memory boundaries
    model_response = suppress_memory_claims(model_response)

    # 4. Enforce training data claim suppression
    model_response = suppress_training_data_claims(model_response)

    # 5. Attempt to parse JSON for tool invocation
    try:
        raw = json.loads(model_response)
    except json.JSONDecodeError:
        return {"response": model_response}

    # 6. Validate schema strictly
    try:
        invocation = ToolInvocation(**raw)
    except Exception:
        return {"response": model_response}

    # 7. Enforce allow-list
    tool_fn = TOOL_REGISTRY.get(invocation.tool)
    if not tool_fn:
        return {"response": model_response}

    # 8. Execute tool
    tool_output = tool_fn(invocation.content)

    return {"response": tool_output}
