# llm_client.py
import requests
import logging

# Configurable
OLLAMA_HOST = "http://localhost:11434"
MODEL_NAME = "mistral:latest"
MAX_PROMPT_CHARS = 2000
TIMEOUT_SECONDS = 60

# Logging setup
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def truncate_prompt(prompt: str, max_length: int = MAX_PROMPT_CHARS) -> str:
    if len(prompt) <= max_length:
        return prompt
    logger.warning(f"Prompt length ({len(prompt)}) exceeds max; truncating to {max_length}")
    return prompt[:max_length].rstrip() + "\n\n[Prompt truncated]"

def call_local_llm(prompt: str, model: str = MODEL_NAME, timeout: int = TIMEOUT_SECONDS) -> str:
    """
    Sends prompt to Ollama's /api/generate endpoint.
    Includes basic diagnostics and prompt truncation.
    """
    safe_prompt = truncate_prompt(prompt)
    payload = {
        "model": model,
        "prompt": safe_prompt,
        "stream": False
    }

    try:
        logger.info(f"Sending prompt to Ollama model '{model}'")
        response = requests.post(f"{OLLAMA_HOST}/api/generate", json=payload, timeout=timeout)
        response.raise_for_status()
        result = response.json()
        return result.get("response", "[ERROR] No 'response' key in LLM result.")
    
    except requests.exceptions.Timeout:
        logger.error("Request timed out after %s seconds", timeout)
        return "[ERROR] LLM request timed out."

    except requests.exceptions.ConnectionError as ce:
        logger.error("Could not connect to Ollama at %s: %s", OLLAMA_HOST, ce)
        return "[ERROR] Could not connect to Ollama instance."

    except Exception as e:
        logger.exception("Unexpected error during LLM call.")
        return f"[ERROR] Unexpected error: {e}"
