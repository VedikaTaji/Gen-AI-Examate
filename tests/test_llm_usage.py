from unittest.mock import Mock

import pytest

from app import llm
from app.guardrails import estimate_tokens


class FakeResponse:
    def __init__(self, data):
        self.data = data
        self.ok = True

    def raise_for_status(self):
        return None

    def json(self):
        return self.data


@pytest.mark.parametrize(
    ("provider", "response_data", "input_count", "output_count"),
    [
        (
            "groq",
            {
                "choices": [{"message": {"content": "{}"}}],
                "usage": {"prompt_tokens": 31, "completion_tokens": 12},
            },
            31,
            12,
        ),
        (
            "gemini",
            {
                "candidates": [{"content": {"parts": [{"text": "{}"}]}}],
                "usageMetadata": {"promptTokenCount": 29, "candidatesTokenCount": 9},
            },
            29,
            9,
        ),
    ],
)
def test_provider_usage_is_preserved(
    provider, response_data, input_count, output_count, monkeypatch
):
    monkeypatch.setenv(f"{provider.upper()}_API_KEY", "test-key")
    monkeypatch.setattr(llm.requests, "post", Mock(return_value=FakeResponse(response_data)))
    llm.LAST_USAGE.set(None)

    if provider == "groq":
        llm.call_groq("system", "question")
    else:
        llm.call_gemini("system", "question")

    assert llm.LAST_USAGE.get() == {
        "tokens_in": input_count,
        "tokens_out": output_count,
    }


def test_missing_provider_usage_uses_estimates(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "test-key")
    monkeypatch.setattr(
        llm.requests,
        "post",
        Mock(
            return_value=FakeResponse(
                {"choices": [{"message": {"content": "generated answer"}}]}
            )
        ),
    )
    llm.LAST_USAGE.set(None)

    llm.call_groq("system", "question")

    assert llm.LAST_USAGE.get() == {
        "tokens_in": estimate_tokens("system\nquestion"),
        "tokens_out": estimate_tokens("generated answer"),
    }