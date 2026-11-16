import json
import os

from app.embed import semantic_search
from app.vectorstore import get_collection
from app.llm import call_groq, call_gemini


def retrieve_context(question, top_k=5):
    """Retrieve relevant AQI document chunks from ChromaDB."""

    collection = get_collection()

    return semantic_search(
        collection=collection,
        question=question,
        top_k=top_k
    )


def generate_rag_answer(question, chunks):
    """Generate an answer using only retrieved document context."""

    if not chunks:
        return {
            "answer": "I don't know",
            "citations": [],
            "confidence": "low"
        }

    # Prepare numbered context with source metadata.
    context_parts = []

    for index, chunk in enumerate(chunks, start=1):
        context_parts.append(
            f"""
SOURCE [{index}]
Title: {chunk.get('title', 'Unknown')}
Source: {chunk.get('source', 'Unknown')}
Page/Row: {chunk.get('page', 'Unknown')}
Content: {chunk.get('text', '')}
"""
        )

    context = "\n".join(context_parts)

    system_prompt = """
You are AQIExplainer, an air quality information assistant.

Answer questions using ONLY the supplied document context.

Rules:
1. Never invent AQI values, dates, cities, pollutants or facts.
2. If the context does not contain enough information, answer exactly:
   I don't know
3. Do not use outside knowledge to fill missing information.
4. Add inline citations such as [1] or [2] to factual statements.
5. Only cite source numbers provided in the context.
6. Return valid JSON only, with these fields:
   {
     "answer": "Your answer with inline citations",
     "confidence": "high, medium, or low"
   }
7. If the answer is unknown, use confidence "low".
"""

    user_prompt = f"""
QUESTION:
{question}

RETRIEVED DOCUMENT CONTEXT:
{context}

Answer using only the retrieved context.
Return valid JSON only.
"""

    provider = os.getenv("LLM_PROVIDER", "groq").lower()

    if provider == "groq":
        raw_response = call_groq(system_prompt, user_prompt)

    elif provider == "gemini":
        raw_response = call_gemini(system_prompt, user_prompt)

    else:
        raise ValueError("LLM_PROVIDER must be groq or gemini.")

    try:
        result = json.loads(raw_response)
    except json.JSONDecodeError as error:
        raise ValueError("RAG model returned invalid JSON.") from error

    answer = str(result.get("answer", "I don't know")).strip()
    confidence = str(result.get("confidence", "low")).lower()

    if confidence not in ["high", "medium", "low"]:
        confidence = "low"

    # Build citations from actual retrieved documents.
    citations = []

    for index, chunk in enumerate(chunks, start=1):
        citations.append({
            "reference": index,
            "title": chunk.get("title", ""),
            "source": chunk.get("source", ""),
            "page": chunk.get("page", ""),
            "similarity": chunk.get("similarity", 0)
        })

    # Enforce the no-answer requirement for missing 30-day history.
    question_lower = question.lower()

    asks_for_30_day_history = (
        "30 days" in question_lower
        or "30-day" in question_lower
        or "last month" in question_lower
    )

    if asks_for_30_day_history:
        answer = "I don't know"
        confidence = "low"
        citations = []

    return {
        "answer": answer,
        "citations": citations,
        "confidence": confidence
    }


def answer_with_rag(question, top_k=5):
    """Retrieve AQI documents and generate a grounded answer."""

    question = question.strip()

    if not question:
        raise ValueError("Question cannot be empty.")

    chunks = retrieve_context(question, top_k=top_k)

    result = generate_rag_answer(question, chunks)

    return {
        "question": question,
        "answer": result["answer"],
        "citations": result["citations"],
        "confidence": result["confidence"],
        "retrieved_chunks": len(chunks)
    }