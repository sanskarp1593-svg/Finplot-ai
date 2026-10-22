"""Pydantic schemas for the AI assistant."""

from __future__ import annotations

import datetime as _dt
from typing import Any, Optional

from pydantic import BaseModel


class QueryRequest(BaseModel):
    question: str
    language: str = "en"  # "en" or "hi"


class AgentTrace(BaseModel):
    """Trace of a single agent's execution."""
    agent: str                  # "router", "metric", "budget", …
    input_summary: str = ""
    output_summary: str = ""
    duration_ms: int = 0


class ChartData(BaseModel):
    """Optional chart to render alongside the answer."""
    chart_type: str = "bar"     # "bar" | "line" | "pie"
    title: str = ""
    labels: list[str] = []
    datasets: list[dict[str, Any]] = []


class SourceCitation(BaseModel):
    """A retrieved knowledge-base source."""
    title: str
    excerpt: str
    similarity: float = 0.0


class QueryResponse(BaseModel):
    answer: str
    agents_used: list[str] = []
    traces: list[AgentTrace] = []
    charts: list[ChartData] = []
    sources: list[SourceCitation] = []
    needs_ca_review: bool = False
    language: str = "en"


class QueryHistoryOut(BaseModel):
    id: int
    question: str
    answer: str
    agents_used: list[str] | None
    language: str
    created_at: _dt.datetime

    model_config = {"from_attributes": True}
