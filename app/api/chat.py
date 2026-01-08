from fastapi import APIRouter
import json
import subprocess
from subprocess import TimeoutExpired

from app.security.tool_schema import ToolInvocation
from app.tools.registry import TOOL_REGISTRY
from app.security.policy_enforcer import enforce_policies

router = APIRouter()
ALLOW_TOOL_EXECUTION = False


def call_llm(user_input: str) -> str:
    """
    Calls a local Ollama model.
    Output is treated as untrusted text.
    """
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

    # 2. Enforce policies (single authority)
    denial = enforce_policies(
        user_input=user_input,
        model_output=model_response
    )
    if denial:
        return {"response": denial}

    # 3. Attempt to parse JSON for tool invocation
    try:
        raw = json.loads(model_response)
    except json.JSONDecodeError:
        return {"response": model_response}

    # 4. Validate schema strictly
    try:
        invocation = ToolInvocation(**raw)
    except Exception:
        return {"response": model_response}

    # 5. Enforce allow-list
    tool_fn = TOOL_REGISTRY.get(invocation.tool)
    if not tool_fn:
        return {"response": model_response}

    # 6. Execute tool
    tool_output = tool_fn(invocation.content)

    return {"response": tool_output}
