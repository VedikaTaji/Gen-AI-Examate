import json
import os
import re
from datetime import datetime
from pathlib import Path

import requests
import streamlit as st


# ---------------- CONFIGURATION ----------------

st.set_page_config(
    page_title="AQIExplainer",
    page_icon="🌍",
    layout="wide",
)

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
FEEDBACK_FILE = Path(__file__).resolve().parent / "feedback.jsonl"


# ---------------- CPCB AQI SCALE ----------------

AQI_BANDS = [
    {
        "name": "Good",
        "minimum": 0,
        "maximum": 50,
        "color": "#00B050",
        "text_color": "#000000",
        "health": "Minimal impact.",
    },
    {
        "name": "Satisfactory",
        "minimum": 51,
        "maximum": 100,
        "color": "#92D050",
        "text_color": "#000000",
        "health": "May cause minor breathing discomfort to sensitive people.",
    },
    {
        "name": "Moderately polluted",
        "minimum": 101,
        "maximum": 200,
        "color": "#FFFF00",
        "text_color": "#000000",
        "health": (
            "May cause breathing discomfort to people with lung disease "
            "such as asthma, and discomfort to people with heart disease, "
            "children and older adults."
        ),
    },
    {
        "name": "Poor",
        "minimum": 201,
        "maximum": 300,
        "color": "#FF9900",
        "text_color": "#000000",
        "health": (
            "May cause breathing discomfort to people on prolonged exposure, "
            "and discomfort to people with heart disease."
        ),
    },
    {
        "name": "Very Poor",
        "minimum": 301,
        "maximum": 400,
        "color": "#FF0000",
        "text_color": "#FFFFFF",
        "health": (
            "May cause respiratory illness on prolonged exposure. "
            "Effects may be more pronounced in people with lung and heart diseases."
        ),
    },
    {
        "name": "Severe",
        "minimum": 401,
        "maximum": 500,
        "color": "#800000",
        "text_color": "#FFFFFF",
        "health": (
            "May cause respiratory effects even in healthy people and serious "
            "health impacts in people with lung or heart diseases. "
            "Effects may occur even during light physical activity."
        ),
    },
]


def get_aqi_band(value):
    """Return the CPCB category for an AQI value from 0 to 500."""
    for band in AQI_BANDS:
        if band["minimum"] <= value <= band["maximum"]:
            return band
    return None


def extract_aqi(answer):
    """
    Extract an explicitly stated AQI number.
    This does not calculate or guess an AQI value.
    """
    patterns = [
        r"\bAQI(?:\s+value)?\s*(?:is|of|:|=)?\s*(\d{1,3})\b",
        r"\b(\d{1,3})\s*\(\s*AQI\s*\)",
    ]

    for pattern in patterns:
        match = re.search(pattern, answer, re.IGNORECASE)
        if match:
            value = int(match.group(1))
            if 0 <= value <= 500:
                return value

    return None


def extract_city(question):
    """Extract a simple city/location name from the user's question."""
    match = re.search(
        r"\b(?:in|for|of)\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)?)",
        question,
    )
    if match:
        return match.group(1).strip()
    return "Location not identified"


# ---------------- API RESPONSE HELPERS ----------------

def get_answer(data):
    """Get readable answer text from /ask or /agent response data."""
    if isinstance(data, str):
        return data

    if not isinstance(data, dict):
        return str(data)

    for key in ("answer", "response", "output", "result"):
        value = data.get(key)

        if isinstance(value, str):
            return value

        if isinstance(value, dict):
            nested_answer = get_answer(value)
            if nested_answer:
                return nested_answer

    # LangGraph may return messages in its state.
    messages = data.get("messages")
    if isinstance(messages, list) and messages:
        last_message = messages[-1]
        if isinstance(last_message, dict):
            content = last_message.get("content")
        else:
            content = getattr(last_message, "content", None)

        if isinstance(content, str):
            return content

    return json.dumps(data, indent=2, ensure_ascii=False)


def get_citations(data):
    """Find citations in either a direct API response or nested response."""
    if not isinstance(data, dict):
        return []

    citations = data.get("citations")
    if isinstance(citations, list) and citations:
        return citations

    nested_response = data.get("response")
    if isinstance(nested_response, dict):
        return get_citations(nested_response)

    return []


# ---------------- BACKEND REQUESTS ----------------

def call_backend(question, mode, thread_id):
    if mode == "RAG (/ask)":
        endpoint = f"{API_URL}/ask"
        payload = {"question": question}
    else:
        endpoint = f"{API_URL}/agent"
        payload = {
            "question": question,
            "thread_id": thread_id,
        }

    response = requests.post(endpoint, json=payload, timeout=90)
    response.raise_for_status()
    return response.json()


def resume_agent(thread_id, approved):
    """Resume a paused LangGraph agent using the same thread ID."""
    response = requests.post(
        f"{API_URL}/agent",
        json={
            "thread_id": thread_id,
            "approval": approved,
        },
        timeout=90,
    )
    response.raise_for_status()
    return response.json()


# ---------------- FEEDBACK ----------------

def save_feedback(question, answer, rating):
    record = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "question": question,
        "answer": answer,
        "feedback": rating,
    }

    FEEDBACK_FILE.parent.mkdir(parents=True, exist_ok=True)

    with FEEDBACK_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=False) + "\n")


# ---------------- AQI DISPLAY ----------------

def show_aqi_card(question, answer):
    value = extract_aqi(answer)

    if value is None:
        return

    band = get_aqi_band(value)
    if band is None:
        return

    city = extract_city(question)

    st.markdown(
        f"""
        <div style="
            background-color: {band['color']};
            color: {band['text_color']};
            padding: 18px;
            border-radius: 12px;
            margin: 12px 0;
        ">
            <div style="font-size: 16px; font-weight: 600;">
                CPCB AIR QUALITY — {city}
            </div>
            <div style="font-size: 38px; font-weight: 800;">
                AQI {value}
            </div>
            <div style="font-size: 20px; font-weight: 700;">
                {band['name']}
            </div>
            <div style="font-size: 14px; margin-top: 8px;">
                {band['health']}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_citations(citations):
    if not citations:
        return

    with st.expander("📚 View source citations"):
        for citation in citations:
            if not isinstance(citation, dict):
                st.write(citation)
                continue

            st.write(f"**Source:** {citation.get('title', 'Document')}")
            st.write(f"File: {citation.get('source', 'Unknown')}")
            st.write(f"Page/Row: {citation.get('page', 'Unknown')}")

            similarity = citation.get("similarity")
            if similarity is not None:
                st.write(f"Similarity: {similarity}")

            st.divider()


# ---------------- SIDEBAR ----------------

st.title("🌍 AQIExplainer")
st.caption("Your AI-powered Air Quality Information Assistant")

with st.sidebar:
    st.header("Settings")

    mode = st.radio(
        "Choose response engine",
        ["RAG (/ask)", "Agent (/agent)"],
    )

    st.write(f"**Backend API:** {API_URL}")

    if st.button("Clear chat"):
        st.session_state.messages = []
        st.session_state.thread_id = f"streamlit-{datetime.now().timestamp()}"
        st.rerun()

    st.divider()
    st.subheader("CPCB AQI Colour Scale")

    for band in AQI_BANDS:
        st.markdown(
            f"""
            <div style="display:flex;align-items:center;margin:7px 0;">
                <div style="
                    width:18px;
                    height:18px;
                    background:{band['color']};
                    border:1px solid #888;
                    border-radius:4px;
                    margin-right:10px;">
                </div>
                <span>{band['name']} ({band['minimum']}-{band['maximum']})</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ---------------- SESSION STATE ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = f"streamlit-{datetime.now().timestamp()}"


# ---------------- CHAT HISTORY ----------------

for index, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message["role"] == "assistant":
            show_aqi_card(
                message.get("question", ""),
                message["content"],
            )
            show_citations(message.get("citations", []))

            # A paused agent needs approval/rejection from the same thread.
            if message.get("status") == "approval_required":
                st.warning("The agent is waiting for your approval.")

                approve_col, reject_col = st.columns(2)

                with approve_col:
                    if st.button(
                        "Approve calculation",
                        key=f"approve_{index}",
                    ):
                        try:
                            result = resume_agent(
                                st.session_state.thread_id,
                                True,
                            )
                            message["content"] = get_answer(result)
                            message["citations"] = get_citations(result)
                            message["status"] = result.get(
                                "status", "completed"
                            )
                            st.rerun()
                        except requests.exceptions.RequestException as error:
                            st.error(f"Approval request failed: {error}")

                with reject_col:
                    if st.button(
                        "Reject calculation",
                        key=f"reject_{index}",
                    ):
                        try:
                            result = resume_agent(
                                st.session_state.thread_id,
                                False,
                            )
                            message["content"] = get_answer(result)
                            message["citations"] = get_citations(result)
                            message["status"] = result.get(
                                "status", "completed"
                            )
                            st.rerun()
                        except requests.exceptions.RequestException as error:
                            st.error(f"Rejection request failed: {error}")

            # Save only one rating for each displayed assistant message.
            if not message.get("feedback"):
                helpful_col, not_helpful_col = st.columns(2)

                with helpful_col:
                    if st.button("👍 Helpful", key=f"up_{index}"):
                        save_feedback(
                            message.get("question", ""),
                            message["content"],
                            "positive",
                        )
                        message["feedback"] = "positive"
                        st.success("Feedback saved.")

                with not_helpful_col:
                    if st.button("👎 Not helpful", key=f"down_{index}"):
                        save_feedback(
                            message.get("question", ""),
                            message["content"],
                            "negative",
                        )
                        message["feedback"] = "negative"
                        st.success("Feedback saved.")
            else:
                st.caption(f"Your feedback: {message['feedback']}")


# ---------------- NEW CHAT MESSAGE ----------------

question = st.chat_input("Ask something about air quality...")

if question:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    try:
        with st.spinner("Analysing air quality information..."):
            data = call_backend(
                question,
                mode,
                st.session_state.thread_id,
            )

        answer = get_answer(data)
        citations = get_citations(data)
        status = data.get("status", "completed")

        if status == "approval_required":
            answer = (
                "The agent wants to run the AQI calculator. "
                "Please approve or reject the action below."
            )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
                "question": question,
                "citations": citations,
                "status": status,
            }
        )

        # Rerun once so the new message and any approval buttons
        # are rendered consistently from chat history.
        st.rerun()

    except requests.exceptions.RequestException as error:
        st.error(
            "Could not connect to the FastAPI backend. "
            f"Check that the backend is running. Details: {error}"
        )
    except Exception as error:
        st.error(f"Something went wrong: {error}")
