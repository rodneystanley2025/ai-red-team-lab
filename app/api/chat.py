import subprocess

def call_llm(user_input: str) -> str:
    """
    Calls a local Ollama model.
    Output is treated as untrusted text.
    """
    result = subprocess.run(
        ["ollama", "run", "mistral", user_input],
        capture_output=True,
        text=True,
        timeout=30
    )

    return result.stdout.strip()
