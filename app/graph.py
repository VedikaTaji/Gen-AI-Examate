import json
from typing import Annotated, TypedDict

from langchain_core.messages import AIMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.types import Command, interrupt

from app.agent_loop import extract_pollutants
from app.rag import answer_with_rag
from app.tools import aqi_subindex_calculator

# --------------------------------------------------
# 1. DEFINE AGENT STATE
# --------------------------------------------------


class AgentState(TypedDict, total=False):
    question: str
    pollutants: dict
    selected_tool: str
    approval_status: str
    response: dict
    messages: Annotated[list, add_messages]


# --------------------------------------------------
# 2. ROUTE NODE
# --------------------------------------------------


def route_node(state: AgentState):

    question = state["question"]

    pollutants = extract_pollutants(question)

    if pollutants:
        return {"selected_tool": "aqi_subindex_calculator", "pollutants": pollutants}

    return {"selected_tool": "rag_search"}


# --------------------------------------------------
# 3. HUMAN APPROVAL NODE
# --------------------------------------------------


def approval_node(state: AgentState):

    decision = interrupt(
        {
            "message": "Approval required to execute AQI calculator.",
            "tool": "aqi_subindex_calculator",
            "pollutants": state["pollutants"],
            "question": state["question"],
            "instruction": "Approve or reject this calculation.",
        }
    )

    approved = decision is True or (
        isinstance(decision, dict) and decision.get("approved") is True
    )

    return {"approval_status": "approved" if approved else "rejected"}


# --------------------------------------------------
# 4. CALCULATOR NODE
# --------------------------------------------------


def calculator_node(state: AgentState):

    result = aqi_subindex_calculator(state["pollutants"])

    response = {
        "agent": "LangGraph AQI Agent",
        "selected_tool": "aqi_subindex_calculator",
        "result": result,
    }

    return {"response": response, "messages": [AIMessage(content=json.dumps(response))]}


# --------------------------------------------------
# 5. RAG NODE
# --------------------------------------------------


def rag_node(state: AgentState):

    result = answer_with_rag(question=state["question"], top_k=5)

    response = {
        "agent": "LangGraph AQI Agent",
        "selected_tool": "rag_search",
        "result": result,
    }

    return {"response": response, "messages": [AIMessage(content=json.dumps(response))]}


# --------------------------------------------------
# 6. REJECTION NODE
# --------------------------------------------------


def rejected_node(state: AgentState):

    response = {
        "agent": "LangGraph AQI Agent",
        "status": "rejected",
        "message": "The AQI calculation was not approved.",
    }

    return {"response": response, "messages": [AIMessage(content=json.dumps(response))]}


# --------------------------------------------------
# 7. CONDITIONAL ROUTING
# --------------------------------------------------


def select_tool(state: AgentState):

    if state["selected_tool"] == "aqi_subindex_calculator":
        return "approval"

    return "rag"


def check_approval(state: AgentState):

    if state["approval_status"] == "approved":
        return "calculate"

    return "rejected"


# --------------------------------------------------
# 8. BUILD LANGGRAPH WORKFLOW
# --------------------------------------------------

builder = StateGraph(AgentState)

builder.add_node("route", route_node)
builder.add_node("approval", approval_node)
builder.add_node("calculate", calculator_node)
builder.add_node("rag", rag_node)
builder.add_node("rejected", rejected_node)

builder.add_edge(START, "route")

builder.add_conditional_edges(
    "route", select_tool, {"approval": "approval", "rag": "rag"}
)

builder.add_conditional_edges(
    "approval", check_approval, {"calculate": "calculate", "rejected": "rejected"}
)

builder.add_edge("calculate", END)
builder.add_edge("rag", END)
builder.add_edge("rejected", END)


# --------------------------------------------------
# 9. MEMORY / CHECKPOINTER
# --------------------------------------------------

memory = MemorySaver()

agent_graph = builder.compile(checkpointer=memory)


# --------------------------------------------------
# 10. GRAPH EXECUTION FUNCTION
# --------------------------------------------------


def run_agent_graph(question=None, thread_id="default", approval=None):

    if not thread_id or not thread_id.strip():
        raise ValueError("thread_id cannot be empty.")

    config = {"configurable": {"thread_id": thread_id}}

    # First request: start a new graph invocation.
    if approval is None:
        if not question or not question.strip():
            raise ValueError("Question cannot be empty.")

        question = question.strip()

        inputs = {"question": question, "messages": [HumanMessage(content=question)]}

        result = agent_graph.invoke(inputs, config=config)

    # Second request: resume after approval/rejection.
    else:
        result = agent_graph.invoke(
            Command(resume={"approved": approval}), config=config
        )

    # Check if graph is waiting for approval.
    if "__interrupt__" in result:
        pending = result["__interrupt__"]

        return {
            "status": "approval_required",
            "thread_id": thread_id,
            "approval_request": [item.value for item in pending],
        }

    # Completed response.
    messages = result.get("messages", [])

    return {
        "status": "completed",
        "thread_id": thread_id,
        "result": result.get("response"),
        "memory": {"message_count": len(messages)},
    }


# --------------------------------------------------
# 11. BASIC TESTS
# --------------------------------------------------

if __name__ == "__main__":
    print("\nTEST 1: RAG through LangGraph")

    print(
        run_agent_graph(question="What is the Air Quality Index?", thread_id="rag-test")
    )

    print("\nTEST 2: Calculator approval request")

    print(
        run_agent_graph(
            question="Calculate AQI for PM2.5 45 and PM10 80",
            thread_id="calculator-test",
        )
    )

    print("\nTEST 3: Approve calculator execution")

    print(run_agent_graph(thread_id="calculator-test", approval=True))
