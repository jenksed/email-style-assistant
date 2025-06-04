# llm_client.py
import requests

MAX_PROMPT_CHARS = 2000

def truncate_prompt(prompt: str, max_length: int = MAX_PROMPT_CHARS) -> str:
    if len(prompt) <= max_length:
        return prompt
    return prompt[:max_length].rstrip() + "\n\n[Prompt truncated]"

def call_local_llm(
    prompt: str,
    model: str = "mistral:latest",
    timeout: int = 60
) -> str:
    """
    Sends `prompt` to Ollama’s /api/generate endpoint.
    - Truncates if over MAX_PROMPT_CHARS.
    - Applies a request timeout.
    """
    url = "http://localhost:11434/api/generate"
    safe_prompt = truncate_prompt(prompt)

    payload = {
        "model": model,
        "prompt": safe_prompt,
        "stream": False
    }
    try:
        resp = requests.post(url, json=payload, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        return data.get("response", "[ERROR] No \"response\" field returned.")
    except requests.exceptions.Timeout:
        return "[ERROR] LLM request timed out."
    except requests.exceptions.ConnectionError:
        return "[ERROR] Could not connect to local Ollama at localhost:11434."
    except Exception as e:
        return f"[ERROR] Unexpected error: {e}"
