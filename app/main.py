import json
import logging
import time
import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query, Request, Response
from pydantic import BaseModel

from app.graph import run_agent_graph
from app.guardrails import (
    MAX_TOP_K,
    InputRejected,
    answer_cache,
    log_request,
    validate_question,
)
from app.llm import LAST_USAGE, generate_aqi_response
from app.rag import answer_with_rag
from app.smart_search import SmartSearch
from app.vectorstore import search_chunks

app = FastAPI(
    title="AQIExplainer API",
    description="API for Maharashtra city-wise AQI information",
    version="1.0.0",
)

logging.basicConfig(level=logging.INFO)


@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    request_id = uuid.uuid4().hex
    started = time.perf_counter()
    request.state.cache_hit = False
    request.state.llm_usage = None
    LAST_USAGE.set(None)
    status_code = 500

    try:
        response = await call_next(request)
        status_code = response.status_code
    finally:
        usage = request.state.llm_usage or LAST_USAGE.get() or {}
        log_request(
            endpoint=request.url.path,
            latency_ms=(time.perf_counter() - started) * 1000,
            tokens_in=usage.get("tokens_in", 0),
            tokens_out=usage.get("tokens_out", 0),
            cache_hit=request.state.cache_hit,
            status=status_code,
            request_id=request_id,
        )

    response.headers["X-Request-ID"] = request_id
    return response

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "records.json"

def load_records():

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            records = json.load(file)

        # Add IDs if the source records do not already contain them
        for index, record in enumerate(records, start=1):
            record.setdefault("id", index)

        return records

    except FileNotFoundError:
        raise RuntimeError("data/records.json was not found.")

    except json.JSONDecodeError:
        raise RuntimeError("records.json contains invalid JSON.")


records = load_records()
search_engine = SmartSearch(records)
MAX_THREAD_ID_CHARS = 128


def require_question(question):
    try:
        return validate_question(question)
    except InputRejected as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


class QuestionRequest(BaseModel):
    question: str


class ChatRequest(BaseModel):
    question: str
    prompt_version: str = "v2"


class AskRequest(BaseModel):
    question: str
    top_k: int = 5


class AgentRequest(BaseModel):
    question: str = None
    thread_id: str = "default"
    approval: bool = None


@app.get("/health")
def health():

    return {
        "status": "healthy",
        "project": "AQIExplainer",
        "total_records": len(records),
    }


@app.get("/records")
def get_records(limit: int = Query(default=20, ge=1, le=500)):

    return {"total": len(records), "records": records[:limit]}


@app.get("/records/{record_id}")
def get_record(record_id: int):

    for record in records:
        if record["id"] == record_id:
            return record

    raise HTTPException(status_code=404, detail="AQI record not found")


@app.get("/search")
def search_records(
    q: str = Query(...), limit: int = Query(default=10, ge=1, le=100)
):
    q = require_question(q)

    results = search_engine.search(q, limit)

    return {"query": q, "total_matches": len(results), "results": results}


@app.post("/questions")
def ask_question(request: QuestionRequest):

    question = require_question(request.question).lower()

    if not records:
        return {"question": request.question, "answer": "No AQI data available."}

    if "highest" in question or "most polluted" in question:
        result = max(records, key=lambda r: r["aqi_value"])

        answer = (
            f"{result['city']} has the highest AQI "
            f"of {result['aqi_value']} ({result['aqi_category']})."
        )

    elif "lowest" in question or "cleanest" in question:
        result = min(records, key=lambda r: r["aqi_value"])

        answer = (
            f"{result['city']} has the lowest AQI "
            f"of {result['aqi_value']} ({result['aqi_category']})."
        )

    else:
        results = search_engine.search(question, limit=3)

        if results:
            answer = "Matching AQI records: " + "; ".join(
                f"{r['city']}: AQI {r['aqi_value']} ({r['aqi_category']})"
                for r in results
            )
        else:
            answer = "I could not find matching AQI information in the records."

    return {"question": request.question, "answer": answer}


@app.post("/chat")
def chat(request: ChatRequest, http_request: Request):

    question = require_question(request.question)

    try:
        result = generate_aqi_response(
            question=question, records=records, prompt_version=request.prompt_version
        )

        return result

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except RuntimeError as error:
        raise HTTPException(status_code=502, detail=str(error))
    finally:
        http_request.state.llm_usage = LAST_USAGE.get()


@app.get("/search/semantic")
def semantic_search_endpoint(q: str, limit: int = 5):
    """Search AQI documents using semantic similarity."""

    question = require_question(q)

    if limit < 1 or limit > 20:
        raise HTTPException(status_code=400, detail="Limit must be between 1 and 20.")

    try:
        results = search_chunks(question, top_k=limit)

        return {"query": question, "total_results": len(results), "results": results}

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except (RuntimeError, OSError) as error:
        raise HTTPException(status_code=500, detail=f"Semantic search failed: {error}")


@app.get("/metrics")
def metrics():
    """Cache statistics for quick production monitoring."""
    return {"cache": answer_cache.stats()}


@app.post("/ask")
def ask_with_rag(request: AskRequest, response: Response, http_request: Request):
    """Answer AQI questions using RAG, with limits, caching and request logging."""

    question = require_question(request.question)

    if request.top_k < 1 or request.top_k > MAX_TOP_K:
        raise HTTPException(
            status_code=400, detail=f"top_k must be between 1 and {MAX_TOP_K}."
        )

    key = answer_cache.make_key(question, request.top_k)
    cached = answer_cache.get(key)

    if cached is not None:
        http_request.state.cache_hit = True
        response.headers["X-Cache"] = "HIT"
        return cached

    LAST_USAGE.set(None)
    try:
        result = answer_with_rag(question=question, top_k=request.top_k)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    except (RuntimeError, OSError) as error:
        raise HTTPException(status_code=500, detail=f"RAG request failed: {error}")
    finally:
        http_request.state.llm_usage = LAST_USAGE.get()

    answer_cache.set(key, result)
    response.headers["X-Cache"] = "MISS"
    return result


@app.post("/agent")
def agent_endpoint(request: AgentRequest, http_request: Request):

    try:
        if not request.thread_id.strip():
            raise HTTPException(status_code=400, detail="thread_id cannot be empty.")

        if len(request.thread_id) > MAX_THREAD_ID_CHARS:
            raise HTTPException(
                status_code=400,
                detail=f"thread_id too long (max {MAX_THREAD_ID_CHARS} characters).",
            )

        if request.approval is None or request.question is not None:
            request.question = require_question(request.question)

        try:
            result = run_agent_graph(
                question=request.question,
                thread_id=request.thread_id,
                approval=request.approval,
            )
        finally:
            http_request.state.llm_usage = LAST_USAGE.get()

        return result

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except (RuntimeError, OSError) as error:
        raise HTTPException(status_code=500, detail=f"Agent execution failed: {error}")
