from fastapi import APIRouter
import json
from app.security.tool_schema import ToolInvocation
from app.tools.registry import TOOL_REGISTRY


router = APIRouter()
ALLOW_TOOL_EXECUTION = False

def call_llm(user_input: str) -> str:
    """
    Naive LLM stub for red team testing.
    For now, it simply echoes user input.
    """
    return user_input

@router.post("/chat/")
def chat(payload: dict):
    user_input = payload.get("user_input", "")

    model_response = call_llm(user_input)

    # Always treat model output as untrusted text
    try:
        raw = json.loads(model_response)
    except json.JSONDecodeError:
        return {"response": model_response}

    # Validate schema strictly
    try:
        invocation = ToolInvocation(**raw)
    except Exception:
        # JSON was present but invalid or unauthorized
        return {"response": model_response}

    # Enforce allow-list
    tool_fn = TOOL_REGISTRY.get(invocation.tool)
    if not tool_fn:
        return {"response": model_response}

    # Execute tool
    tool_output = tool_fn(invocation.content)

    return {"response": tool_output}