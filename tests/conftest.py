import pytest
from fastapi.testclient import TestClient

from app import guardrails
from app.guardrails import answer_cache
from app.main import app


@pytest.fixture(autouse=True)
def clear_cache(tmp_path, monkeypatch):
    answer_cache._data.clear()
    answer_cache.hits = answer_cache.misses = 0
    monkeypatch.setattr(guardrails, "METRICS_FILE", tmp_path / "requests.jsonl")

@pytest.fixture
def client():
    return TestClient(app)