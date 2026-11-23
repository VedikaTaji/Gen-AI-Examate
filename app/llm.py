import json
import os
from contextvars import ContextVar
from pathlib import Path

import requests
from dotenv import load_dotenv

from app.guardrails import estimate_tokens

# Real token usage reported by the provider for the current request
LAST_USAGE: ContextVar[dict | None] = ContextVar("last_usage", default=None)

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
PROMPT_DIR = BASE_DIR / "prompts"

# Load private environment variables
load_dotenv(BASE_DIR / ".env", override=True)


def load_prompt(filename):
    """Read a prompt file from the prompts folder."""

    prompt_path = PROMPT_DIR / filename

    with prompt_path.open("r", encoding="utf-8") as file:
        return file.read()


def _record_token_usage(usage, input_keys, output_keys, system_prompt, user_prompt, text):
    usage = usage if isinstance(usage, dict) else {}

    def provider_count(keys):
        for key in keys:
            value = usage.get(key)
            if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
                return value
        return None

    tokens_in = provider_count(input_keys)
    tokens_out = provider_count(output_keys)
    LAST_USAGE.set(
        {
            "tokens_in": tokens_in
            if tokens_in is not None
            else estimate_tokens(f"{system_prompt}\n{user_prompt}"),
            "tokens_out": tokens_out if tokens_out is not None else estimate_tokens(text),
        }
    )


def parse_response(response_text):
    """Convert the LLM response into the required JSON format."""

    try:
        result = json.loads(response_text)

        required_keys = {"answer", "confidence", "follow_up"}

        if not required_keys.issubset(result):
            raise ValueError("LLM response is missing required JSON fields.")

        confidence = str(result["confidence"]).lower()

        if confidence not in ["high", "medium", "low"]:
            confidence = "low"

        return {
            "answer": str(result["answer"]),
            "confidence": confidence,
            "follow_up": str(result["follow_up"]),
        }

    except (json.JSONDecodeError, TypeError) as error:
        raise ValueError("LLM returned an invalid JSON response.") from error


def call_groq(system_prompt, user_prompt):
    """Send a request to the Groq API."""

    api_key = os.getenv("GROQ_API_KEY", "").strip()
    model = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

    if not api_key or api_key.startswith("your_"):
        raise ValueError("GROQ_API_KEY is missing in your .env file.")

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.2,
        "max_completion_tokens": 2000,
    }

    # gpt-oss models "think" before answering; keep that short so the
    # token budget is left for the actual JSON answer.
    if "gpt-oss" in model:
        payload["reasoning_effort"] = "low"

    response = requests.post(url, headers=headers, json=payload, timeout=45)

    if not response.ok:
        print("\nGROQ API ERROR:")
        print("Status Code:", response.status_code)
        print("Error Details:", response.text)

    response.raise_for_status()

    response_data = response.json()
    text = response_data["choices"][0]["message"]["content"]
    _record_token_usage(
        response_data.get("usage"),
        ("prompt_tokens", "input_tokens"),
        ("completion_tokens", "output_tokens"),
        system_prompt,
        user_prompt,
        text,
    )
    return text

def call_gemini(system_prompt, user_prompt):
    """Send a request to the Gemini API."""

    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

    if not api_key or api_key.startswith("your_"):
        raise ValueError("GEMINI_API_KEY is missing in your .env file.")

    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        f"models/{model}:generateContent"
    )

    headers = {"x-goog-api-key": api_key, "Content-Type": "application/json"}

    payload = {
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "contents": [{"parts": [{"text": user_prompt}]}],
        "generationConfig": {
            "temperature": 0.2,
            "responseMimeType": "application/json",
            "maxOutputTokens": 500,
        },
    }

    response = requests.post(url, headers=headers, json=payload, timeout=45)

    response.raise_for_status()

    response_data = response.json()
    text = response_data["candidates"][0]["content"]["parts"][0]["text"]
    _record_token_usage(
        response_data.get("usageMetadata"),
        ("promptTokenCount", "prompt_token_count"),
        ("candidatesTokenCount", "outputTokenCount", "candidates_token_count"),
        system_prompt,
        user_prompt,
        text,
    )
    return text


def generate_aqi_response(question, records, prompt_version="v2"):
    """Generate an AQI answer using the selected LLM provider."""

    system_prompt = load_prompt("system.md")

    if prompt_version not in ["v1", "v2"]:
        raise ValueError("prompt_version must be v1 or v2.")

    task_prompt = load_prompt(f"task_{prompt_version}.md")

    # Give the LLM the available AQI records as context
    records_context = json.dumps(records, ensure_ascii=False, indent=2)

    user_prompt = f"""
{task_prompt}

USER QUESTION:
{question}

AVAILABLE AQI DATA:
{records_context}

Remember: return valid JSON only.
"""

    provider = os.getenv("LLM_PROVIDER", "groq").lower()

    try:
        if provider == "groq":
            raw_response = call_groq(system_prompt, user_prompt)

        elif provider == "gemini":
            raw_response = call_gemini(system_prompt, user_prompt)

        else:
            raise ValueError("Invalid LLM_PROVIDER. Choose groq or gemini.")

        return parse_response(raw_response)

    except requests.RequestException as error:
        raise RuntimeError(f"{provider} API request failed: {error}") from error
