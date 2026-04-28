from langgraph.graph import StateGraph, END
from typing import TypedDict
from tools import log_interaction_tool, edit_interaction_tool
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# -----------------------------
# State
# -----------------------------
class AgentState(TypedDict):
    input: str
    output: str


# -----------------------------
# Request Schema
# -----------------------------
class InputRequest(BaseModel):
    input: str


# -----------------------------
# Router (Decision Function)
# -----------------------------
def decide_tool(state: AgentState):
    text = state["input"].lower()

    if "change" in text or "edit" in text:
        return "edit"

    return "log"


# -----------------------------
# Log node
# -----------------------------
def log_node(state: AgentState):
    result = log_interaction_tool(state["input"])
    return {"output": result}


# -----------------------------
# Edit node
# -----------------------------
def edit_node(state: AgentState):
    existing = {
        "hcp_name": "Dr. Sharma",
        "product_discussed": "Paracetamol",
        "interaction_notes": "Doctor interested",
        "interaction_summary": "Positive",
        "next_action": "Follow up next week"
    }

    result = edit_interaction_tool(existing, state["input"])
    return {"output": result}


# -----------------------------
# Build Graph
# -----------------------------
builder = StateGraph(AgentState)

builder.add_node("log", log_node)
builder.add_node("edit", edit_node)

# ❌ REMOVE dummy router node

builder.set_entry_point("log")

builder.add_conditional_edges(
    "log",
    decide_tool,
    {
        "log": "log",
        "edit": "edit"
    }
)

builder.add_edge("edit", END)
builder.add_edge("log", END)

app_graph = builder.compile()


# -----------------------------
# FASTAPI ENDPOINT (IMPORTANT)
# -----------------------------
@app.post("/agent")
def run_agent(req: InputRequest):
    result = app_graph.invoke({"input": req.input})
    return result