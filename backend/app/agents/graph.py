"""LangGraph StateGraph – 6-agent workflow for the AI assistant.

Nodes:
  router → metric_agent | budget_agent | compliance_agent | item_price_agent
         → narrator

The graph routes to exactly one specialist agent based on the router's
classification, then passes through the narrator to compose the final answer.
"""

from __future__ import annotations

import re
import time
from typing import Any

from langgraph.graph import END, StateGraph

from app.agents.hindi import get_templates, translate_item_name
from app.agents.narrator import narrator_node
from app.agents.router import router_node
from app.agents.state import AgentState
from app.agents.tools import (
    get_budget_status,
    get_expense_by_category,
    get_item_prices,
    get_latest_month,
    get_month_metrics,
    parse_month_from_question,
)
from app.schemas.query import AgentTrace, ChartData, QueryResponse, SourceCitation

from sqlalchemy.orm import Session


# ── Specialist agent nodes ───────────────────────────────────────────────────

def metric_agent(state: AgentState) -> dict[str, Any]:
    """Compute financial metrics for the requested period."""
    start = time.time()
    db: Session = state["_db"]
    biz_id = state["business_id"]

    year, month = parse_month_from_question(state["question"], biz_id, db)
    metrics = get_month_metrics(db, biz_id, year, month)

    # Build chart data
    cats = get_expense_by_category(db, biz_id, year, month)
    chart = {
        "chart_type": "pie",
        "title": f"Expenses by Category – {year}-{month:02d}",
        "labels": [c["category"] for c in cats],
        "datasets": [{"data": [c["amount"] for c in cats]}],
    }

    duration = int((time.time() - start) * 1000)
    return {
        "metrics": metrics,
        "chart_data": [chart],
        "agents_used": state.get("agents_used", []) + ["metric"],
        "traces": state.get("traces", []) + [{
            "agent": "metric",
            "input_summary": f"Month: {year}-{month:02d}",
            "output_summary": f"Rev ₹{metrics['revenue']:,.0f}, Exp ₹{metrics['expenses']:,.0f}, Profit ₹{metrics['profit']:,.0f}",
            "duration_ms": duration,
        }],
    }


def budget_agent(state: AgentState) -> dict[str, Any]:
    """Check budget status for the requested period."""
    start = time.time()
    db: Session = state["_db"]
    biz_id = state["business_id"]

    year, month = parse_month_from_question(state["question"], biz_id, db)
    items = get_budget_status(db, biz_id, year, month)

    # Chart
    chart = {
        "chart_type": "bar",
        "title": f"Budget vs Actual – {year}-{month:02d}",
        "labels": [i["category"] for i in items],
        "datasets": [
            {"label": "Spent", "data": [i["spent"] for i in items]},
            {"label": "Budget", "data": [i["limit"] for i in items]},
        ],
    }

    duration = int((time.time() - start) * 1000)
    return {
        "budget_data": {"items": items, "month": f"{year}-{month:02d}"},
        "chart_data": [chart],
        "agents_used": state.get("agents_used", []) + ["budget"],
        "traces": state.get("traces", []) + [{
            "agent": "budget",
            "input_summary": f"Month: {year}-{month:02d}",
            "output_summary": f"{sum(1 for i in items if i['over_budget'])} categories over budget",
            "duration_ms": duration,
        }],
    }


def compliance_agent(state: AgentState) -> dict[str, Any]:
    """RAG lookup in the knowledge base."""
    start = time.time()

    answer = ""
    sources: list[dict] = []
    try:
        from app.rag.retrieve import retrieve
        results = retrieve(state["question"])
        if results:
            answer = results[0]["content"]
            sources = [{"title": r["title"], "excerpt": r["content"][:200], "similarity": r["similarity"]} for r in results]
        else:
            tmpl = get_templates(state.get("language", "en"))
            answer = "No relevant source found in the knowledge base."
    except Exception:
        answer = "Knowledge base is not yet initialized. Run `npm run ingest` first."

    duration = int((time.time() - start) * 1000)
    return {
        "compliance_data": {"answer": answer, "sources": sources},
        "sources": sources,
        "agents_used": state.get("agents_used", []) + ["compliance"],
        "traces": state.get("traces", []) + [{
            "agent": "compliance",
            "input_summary": state["question"][:80],
            "output_summary": f"Found {len(sources)} sources",
            "duration_ms": duration,
        }],
    }


def item_price_agent(state: AgentState) -> dict[str, Any]:
    """Look up item prices from confirmed invoices."""
    start = time.time()
    db: Session = state["_db"]
    biz_id = state["business_id"]
    question = state["question"]

    # Extract item name from question
    # Try patterns like "onion price", "price of rice", "last rate for dal"
    item_name = "item"
    patterns = [
        r"(?:price|rate|daam|bhav|keemat)\s+(?:of|for|ka|ki)?\s*(.+?)[\s?]*$",
        r"(.+?)\s+(?:price|rate|daam|bhav|keemat)",
        r"(?:last|latest)\s+(.+?)\s+(?:price|rate)",
        r"(?:buy|khareed)\s+(.+?)[\s?]*(?:at|for|\?|$)",
    ]
    for pat in patterns:
        m = re.search(pat, question, re.IGNORECASE)
        if m:
            item_name = m.group(1).strip().rstrip("?.,!")
            break

    item_name = translate_item_name(item_name)
    prices = get_item_prices(db, biz_id, item_name)

    duration = int((time.time() - start) * 1000)
    return {
        "item_price_data": {"item": item_name, "prices": prices},
        "agents_used": state.get("agents_used", []) + ["item_price"],
        "traces": state.get("traces", []) + [{
            "agent": "item_price",
            "input_summary": f"Item: {item_name}",
            "output_summary": f"Found {len(prices)} price records",
            "duration_ms": duration,
        }],
    }


def general_agent(state: AgentState) -> dict[str, Any]:
    """Passthrough for unclassified questions."""
    return {
        "agents_used": state.get("agents_used", []) + ["general"],
        "traces": state.get("traces", []) + [{
            "agent": "general",
            "input_summary": state["question"][:80],
            "output_summary": "Unclassified question",
            "duration_ms": 0,
        }],
    }


# ── Graph construction ───────────────────────────────────────────────────────

def _route_by_intent(state: AgentState) -> str:
    """Conditional edge: route to the appropriate specialist."""
    intent = state.get("intent", "general")
    mapping = {
        "metric": "metric_agent",
        "budget": "budget_agent",
        "compliance": "compliance_agent",
        "item_price": "item_price_agent",
    }
    return mapping.get(intent, "general_agent")


def _build_graph() -> StateGraph:
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("router", router_node)
    graph.add_node("metric_agent", metric_agent)
    graph.add_node("budget_agent", budget_agent)
    graph.add_node("compliance_agent", compliance_agent)
    graph.add_node("item_price_agent", item_price_agent)
    graph.add_node("general_agent", general_agent)
    graph.add_node("narrator", narrator_node)

    # Entry
    graph.set_entry_point("router")

    # Conditional routing after classification
    graph.add_conditional_edges("router", _route_by_intent)

    # All specialists → narrator → END
    for agent in ("metric_agent", "budget_agent", "compliance_agent", "item_price_agent", "general_agent"):
        graph.add_edge(agent, "narrator")
    graph.add_edge("narrator", END)

    return graph


_compiled_graph = _build_graph().compile()


# ── Public API ───────────────────────────────────────────────────────────────

def run_agent_workflow(
    question: str,
    language: str,
    business_id: int,
    db: Session,
) -> QueryResponse:
    """Run the full 6-agent LangGraph workflow and return a QueryResponse."""
    initial_state: AgentState = {
        "question": question,
        "language": language,
        "business_id": business_id,
        "_db": db,
        "agents_used": [],
        "traces": [],
        "chart_data": [],
        "sources": [],
    }

    result = _compiled_graph.invoke(initial_state)

    # Build response
    traces = [AgentTrace(**t) for t in result.get("traces", [])]
    charts = [ChartData(**c) for c in result.get("chart_data", [])]
    sources = [SourceCitation(**s) for s in result.get("sources", [])]

    return QueryResponse(
        answer=result.get("answer", ""),
        agents_used=result.get("agents_used", []),
        traces=traces,
        charts=charts,
        sources=sources,
        needs_ca_review=result.get("needs_ca_review", False),
        language=language,
    )
