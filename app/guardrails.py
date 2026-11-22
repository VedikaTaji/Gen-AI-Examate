"""Production guardrails: input limits, prompt-injection screening, TTL cache, metrics."""

import json
import logging
import re
import time
from collections import OrderedDict
from pathlib import Path
from threading import Lock

logger = logging.getLogger("aqiexplainer")

# ---------------------------------------------------------------- limits
MAX_QUESTION_CHARS = 500
MAX_TOP_K = 10

INJECTION_PATTERNS = [
    r"ignore (all |any |the )?(previous|prior|above) (instructions|prompts?|rules)",
    r"disregard (all |any |the )?(previous|prior|above)",
    r"forget (all |your |the )?(previous|prior|above)? ?(instructions|rules)",
    r"reveal (your |the )?(system|hidden|secret) (prompt|instructions)",
    r"(print|show|repeat|output) (your |the )?(system|initial) prompt",
    r"you are now (?!aqiexplainer)",
    r"\bjailbreak\b|\bdan mode\b",
    r"(api[_ -]?key|\.env|secret key)",
]
_INJECTION_RE = re.compile("|".join(INJECTION_PATTERNS), re.IGNORECASE)


class InputRejected(ValueError):
    """Raised when a question violates input limits or looks like prompt injection."""


def validate_question(question: str) -> str:
    question = (question or "").strip()
    if not question:
        raise InputRejected("Question cannot be empty.")
    if len(question) > MAX_QUESTION_CHARS:
        raise InputRejected(f"Question too long (max {MAX_QUESTION_CHARS} characters).")
    if _INJECTION_RE.search(question):
        raise InputRejected("Request blocked: possible prompt-injection attempt.")
    return question


# ----------------------------------------------------------------- cache
class TTLCache:
    """Small thread-safe LRU cache with expiry. No external service needed."""

    def __init__(self, max_items=256, ttl_seconds=900):
        self.max_items, self.ttl = max_items, ttl_seconds
        self._data = OrderedDict()
        self._lock = Lock()
        self.hits = 0
        self.misses = 0

    @staticmethod
    def make_key(question, top_k):
        return f"{' '.join(question.lower().split())}|{top_k}"

    def get(self, key):
        with self._lock:
            item = self._data.get(key)
            if item and time.time() - item[0] < self.ttl:
                self._data.move_to_end(key)
                self.hits += 1
                return item[1]
            if item:
                del self._data[key]
            self.misses += 1
            return None

    def set(self, key, value):
        with self._lock:
            self._data[key] = (time.time(), value)
            self._data.move_to_end(key)
            while len(self._data) > self.max_items:
                self._data.popitem(last=False)

    def stats(self):
        total = self.hits + self.misses
        return {
            "size": len(self._data),
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": round(self.hits / total, 3) if total else 0.0,
        }


answer_cache = TTLCache()

# --------------------------------------------------------------- metrics
METRICS_FILE = Path(__file__).resolve().parent.parent / "logs" / "requests.jsonl"


def estimate_tokens(text) -> int:
    """~4 characters per token. Used when the provider does not return usage."""
    return max(1, len(str(text)) // 4)


def log_request(endpoint, latency_ms, tokens_in, tokens_out, cache_hit, status):
    entry = {
        "ts": round(time.time(), 3),
        "endpoint": endpoint,
        "latency_ms": round(latency_ms, 1),
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "cache_hit": cache_hit,
        "status": status,
    }
    logger.info("request %s", json.dumps(entry))
    try:
        METRICS_FILE.parent.mkdir(exist_ok=True)
        with METRICS_FILE.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:  # read-only filesystems must never break a request
        pass
    return entry