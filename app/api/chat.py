from fastapi import APIRouter
import json
from tools.generate_report import generate_report

router = APIRouter()

@router.post("/chat/")
def chat(payload: dict):
    user_input = payload.get("user_input", "")

    # 1. Call your existing LLM function
    model_response = call_llm(user_input)

    # model_response MUST be a string

    # 2. Attempt to parse model output as JSON
    try:
        parsed = json.loads(model_response)
    except json.JSONDecodeError:
        # Not JSON → return raw model output
        return {"response": model_response}

    # 3. Check for tool invocation
    if isinstance(parsed, dict) and parsed.get("tool") == "generate_report":
        content = parsed.get("content", "")

        # 4. Invoke tool
        tool_output = generate_report(content)

        # 5. Return tool output
        return {"response": tool_output}

    # 6. Fallback
    return {"response": model_response}