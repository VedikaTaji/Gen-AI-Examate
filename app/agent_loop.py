import re

from app.rag import answer_with_rag
from app.tools import aqi_subindex_calculator

# Recognize pollutant names and their concentration values.
POLLUTANT_PATTERN = re.compile(
    r"\b(?P<pollutant>PM\s*2\.?5|PM\s*10|NO2|O3|CO|SO2|NH3|PB)\b"
    r"\s*(?:concentration\s*)?(?:is|=|:)?\s*"
    r"(?P<value>\d+(?:\.\d+)?)",
    re.IGNORECASE,
)


def extract_pollutants(question):
    """
    Extract pollutant concentrations from a natural-language question.

    Example:
    'Calculate AQI for PM2.5 45 and PM10 80'
    becomes:
    {'PM2.5': 45.0, 'PM10': 80.0}
    """

    pollutant_data = {}

    for match in POLLUTANT_PATTERN.finditer(question):
        name = match.group("pollutant").upper().replace(" ", "")
        value = float(match.group("value"))

        aliases = {
            "PM25": "PM2.5",
            "PM2.5": "PM2.5",
            "PM10": "PM10",
            "NO2": "NO2",
            "O3": "O3",
            "CO": "CO",
            "SO2": "SO2",
            "NH3": "NH3",
            "PB": "Pb",
        }

        canonical_name = aliases[name]
        pollutant_data[canonical_name] = value

    return pollutant_data


def run_agent(question, top_k=5):
    """
    Simple hand-written agent.

    Decision:
    1. Pollutant concentrations found -> calculator tool.
    2. No pollutant concentrations -> RAG tool.
    """

    question = question.strip()

    if not question:
        raise ValueError("Question cannot be empty.")

    if top_k < 1 or top_k > 10:
        raise ValueError("top_k must be between 1 and 10.")

    # Step 1: Inspect the user's question.
    pollutant_data = extract_pollutants(question)

    # Step 2: Decide which tool to call.
    if pollutant_data:
        result = aqi_subindex_calculator(pollutant_data)

        return {
            "agent": "AQI Calculator Agent",
            "selected_tool": "aqi_subindex_calculator",
            "reason": "Pollutant concentrations were detected in the question.",
            "input": pollutant_data,
            "result": result,
        }

    # Step 3: If no concentration is detected, use RAG.
    rag_result = answer_with_rag(question=question, top_k=top_k)

    return {
        "agent": "AQI Knowledge Agent",
        "selected_tool": "rag_search",
        "reason": "No pollutant concentrations were detected. Searching project documents.",
        "result": rag_result,
    }


if __name__ == "__main__":
    print("\nTEST 1: Calculator tool")
    print(run_agent("Calculate AQI for PM2.5 45 and PM10 80"))

    print("\nTEST 2: RAG tool")
    print(run_agent("What does Severe AQI indicate?"))
