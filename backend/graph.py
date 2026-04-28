from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from langgraph.graph import StateGraph, END
from typing import TypedDict

from tools import (
    log_interaction_tool,
    edit_interaction_tool,
    summarize_interaction_tool,
    next_best_action_tool,
    extract_insights_tool
)

# ✅ FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Request Model
# -----------------------------
class AgentInput(BaseModel):
    text: str


# -----------------------------
# State
# -----------------------------
class AgentState(TypedDict):
    input: str
    output: str


# -----------------------------
# Decide tool FIRST
# -----------------------------
def decide_tool(state):
    text = state["input"].lower()

    if "change" in text or "edit" in text:
        return "edit"
    elif "summary" in text:
        return "summary"
    elif "next" in text:
        return "next_action"
    elif "insight" in text:
        return "insights"
    else:
        return "log"
# -----------------------------
# Log node
# -----------------------------
def log_node(state: AgentState):
    print("👉 LOG TOOL CALLED")
    result = log_interaction_tool(state["input"])
    print("✅ LOG DONE")
    return {"output": result}


# -----------------------------
# Edit node
# -----------------------------
def edit_node(state: AgentState):
    print("👉 EDIT TOOL CALLED")

    existing = {
        "hcp_name": "Dr. Sharma",
        "product_discussed": "Paracetamol",
        "interaction_notes": "Doctor interested",
        "interaction_summary": "Positive",
        "next_action": "Follow up next week"
    }

    result = edit_interaction_tool(existing, state["input"])
    print("✅ EDIT DONE")
    return {"output": result}

def summary_node(state: AgentState):
    print("👉 SUMMARY TOOL CALLED")
    result = summarize_interaction_tool(state["input"])
    print("✅ SUMMARY DONE")
    return {"output": result}


def next_action_node(state: AgentState):
    print("👉 NEXT ACTION TOOL CALLED")
    result = next_best_action_tool(state["input"])
    print("✅ NEXT ACTION DONE")
    return {"output": result}


def insights_node(state: AgentState):
    print("👉 INSIGHTS TOOL CALLED")
    result = extract_insights_tool(state["input"])
    print("✅ INSIGHTS DONE")
    return {"output": result}

# -----------------------------
# Build Graph (CORRECT FLOW)
# -----------------------------
builder = StateGraph(AgentState)

# Nodes
builder.add_node("log", log_node)
builder.add_node("edit", edit_node)
builder.add_node("summary", summary_node)
builder.add_node("next_action", next_action_node)
builder.add_node("insights", insights_node)

# 🔥 Entry point = decision
builder.set_conditional_entry_point(
    decide_tool,
    {
        "log": "log",
        "edit": "edit",
        "summary": "summary",
        "next_action": "next_action",
        "insights": "insights"
    }
)
# End both paths
builder.add_edge("log", END)
builder.add_edge("edit", END)
builder.add_edge("summary", END)
builder.add_edge("next_action", END)
builder.add_edge("insights", END)

# Compile
app_graph = builder.compile()


# -----------------------------
# API Endpoint
# -----------------------------
@app.post("/ai-agent")
def run_agent(data: AgentInput):
    print("📩 Incoming request:", data.text)

    result = app_graph.invoke({"input": data.text})

    print("📤 Response ready")
    return {"result": result["output"]}