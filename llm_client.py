# llm_client.py
import logging
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Configurable
MODEL_NAME = "mistralai/Mistral-7B-v0.1"  # Hugging Face model ID for Mistral
MAX_PROMPT_CHARS = 2000
MAX_NEW_TOKENS = 300

# Logging setup
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Detect device (MPS for Apple Silicon or CPU fallback)
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
logger.info(f"Using device: {device}")

# Load tokenizer and model once at import to avoid overhead on every call
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME).to(device)
    model.eval()
    logger.info(f"Loaded model '{MODEL_NAME}' on device {device}")
except Exception as e:
    logger.error(f"Failed to load model '{MODEL_NAME}': {e}")
    tokenizer = None
    model = None

def truncate_prompt(prompt: str, max_length: int = MAX_PROMPT_CHARS) -> str:
    if len(prompt) <= max_length:
        return prompt
    logger.warning(f"Prompt length ({len(prompt)}) exceeds max; truncating to {max_length}")
    return prompt[:max_length].rstrip() + "\n\n[Prompt truncated]"

def call_local_llm(prompt: str) -> str:
    """
    Generates text from prompt using a local Hugging Face model on MPS/CPU.
    Truncates prompt if too long.
    """
    if model is None or tokenizer is None:
        logger.error("Model or tokenizer not loaded.")
        return "[ERROR] Model not loaded."

    safe_prompt = truncate_prompt(prompt)

    try:
        inputs = tokenizer(safe_prompt, return_tensors="pt").to(device)
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=MAX_NEW_TOKENS,
                do_sample=True,
                temperature=0.7,
            )
        decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return decoded
    except Exception as e:
        logger.exception("Exception during model generation:")
        return f"[ERROR] Exception during model generation: {e}"
