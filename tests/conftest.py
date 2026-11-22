import pytest
from fastapi.testclient import TestClient

from app.guardrails import answer_cache
from app.main import app


@pytest.fixture(autouse=True)
def clear_cache():
    answer_cache._data.clear()
    answer_cache.hits = answer_cache.misses = 0

@pytest.fixture
def client():
    return TestClient(app)