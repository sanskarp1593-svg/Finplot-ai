"""LangGraph state schema for the agent workflow."""

from __future__ import annotations

from typing import Any, Optional

from typing_extensions import TypedDict


class AgentState(TypedDict, total=False):
    """Shared state passed between agent nodes."""
    # Input
    question: str
    language: str  # "en" or "hi"
    business_id: int

    # Router output
    intent: str  # "metric" | "budget" | "compliance" | "item_price" | "general"

    # Agent outputs
    metrics: dict[str, Any]
    budget_data: dict[str, Any]
    compliance_data: dict[str, Any]
    item_price_data: dict[str, Any]
    chart_data: list[dict[str, Any]]
    sources: list[dict[str, Any]]

    # Narrator output
    answer: str
    needs_ca_review: bool
    agents_used: list[str]
    traces: list[dict[str, Any]]

    # DB session reference (not serialized)
    _db: Any
