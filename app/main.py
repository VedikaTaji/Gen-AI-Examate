
import json
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from app.smart_search import SmartSearch


app = FastAPI(
    title="AQIExplainer API",
    description="API for Maharashtra city-wise AQI information",
    version="1.0.0"
)

DATA_FILE = Path("data/records.json")


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


class QuestionRequest(BaseModel):
    question: str


@app.get("/health")
def health():

    return {
        "status": "healthy",
        "project": "AQIExplainer",
        "total_records": len(records)
    }


@app.get("/records")
def get_records(limit: int = Query(default=20, ge=1, le=500)):

    return {
        "total": len(records),
        "records": records[:limit]
    }


@app.get("/records/{record_id}")
def get_record(record_id: int):

    for record in records:
        if record["id"] == record_id:
            return record

    raise HTTPException(
        status_code=404,
        detail="AQI record not found"
    )


@app.get("/search")
def search_records(
    q: str = Query(..., min_length=1),
    limit: int = Query(default=10, ge=1, le=100)
):

    results = search_engine.search(q, limit)

    return {
        "query": q,
        "total_matches": len(results),
        "results": results
    }


@app.post("/questions")
def ask_question(request: QuestionRequest):

    question = request.question.strip().lower()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

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

    return {
        "question": request.question,
        "answer": answer
    }
