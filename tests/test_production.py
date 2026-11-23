import json
from unittest.mock import patch

from app.llm import LAST_USAGE


def read_request_logs(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_every_response_has_a_correlated_latency_log(client, tmp_path, monkeypatch):
    from app import guardrails

    metrics_file = tmp_path / "requests.jsonl"
    monkeypatch.setattr(guardrails, "METRICS_FILE", metrics_file)

    response = client.get("/health")

    assert response.status_code == 200
    request_id = response.headers["X-Request-ID"]
    [entry] = read_request_logs(metrics_file)
    assert entry["request_id"] == request_id
    assert entry["endpoint"] == "/health"
    assert entry["status_code"] == 200
    assert entry["latency_ms"] >= 0
    assert entry["total_tokens"] == entry["tokens_in"] + entry["tokens_out"]


def test_failed_api_response_is_logged(client, tmp_path, monkeypatch):
    from app import guardrails

    metrics_file = tmp_path / "requests.jsonl"
    monkeypatch.setattr(guardrails, "METRICS_FILE", metrics_file)

    def failed_rag(*, question, top_k):
        LAST_USAGE.set({"tokens_in": 44, "tokens_out": 8})
        raise RuntimeError("provider down")

    with patch("app.main.answer_with_rag", side_effect=failed_rag):
        response = client.post("/ask", json={"question": "What is AQI?"})

    assert response.status_code == 500
    [entry] = read_request_logs(metrics_file)
    assert entry["status_code"] == 500
    assert entry["request_id"] == response.headers["X-Request-ID"]
    assert entry["tokens_in"] == 44
    assert entry["tokens_out"] == 8


def test_llm_usage_and_cache_status_are_logged(client, tmp_path, monkeypatch):
    from app import guardrails

    metrics_file = tmp_path / "requests.jsonl"
    monkeypatch.setattr(guardrails, "METRICS_FILE", metrics_file)
    fake = {
        "question": "What is AQI?",
        "answer": "AQI measures air quality.",
        "citations": [],
        "confidence": "high",
        "retrieved_chunks": 1,
    }

    def answer_with_usage(*, question, top_k):
        LAST_USAGE.set({"tokens_in": 91, "tokens_out": 17})
        return fake

    with patch("app.main.answer_with_rag", side_effect=answer_with_usage):
        first = client.post("/ask", json={"question": "What is AQI?"})
        second = client.post("/ask", json={"question": "What is AQI?"})

    entries = read_request_logs(metrics_file)
    assert first.headers["X-Cache"] == "MISS"
    assert second.headers["X-Cache"] == "HIT"
    assert entries[0]["tokens_in"] == 91
    assert entries[0]["tokens_out"] == 17
    assert entries[0]["total_tokens"] == 108
    assert entries[0]["cache_hit"] is False
    assert entries[1]["cache_hit"] is True
    assert entries[1]["tokens_in"] == entries[1]["tokens_out"] == 0


def test_invalid_questions_use_the_same_limit(client):
    too_long = "x" * 501

    responses = [
        client.post("/questions", json={"question": too_long}),
        client.post("/chat", json={"question": too_long}),
        client.post("/ask", json={"question": too_long}),
        client.post("/agent", json={"question": too_long}),
        client.get("/search", params={"q": too_long}),
        client.get("/search/semantic", params={"q": too_long}),
    ]

    assert all(response.status_code == 400 for response in responses)
    assert all("500 characters" in response.json()["detail"] for response in responses)