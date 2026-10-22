"""Router agent – classifies question intent.

Dual-mode:
  - LLM mode: OpenAI classifies the question
  - Fallback mode: keyword-based deterministic router (default)
"""

from __future__ import annotations

import json
import re
import time
from typing import Any

from app.agents.state import AgentState
from app.agents.hindi import detect_hindi_intent, HINDI_KEYWORDS
from app.config import OPENAI_API_KEY, OPENAI_MODEL, LLM_TIMEOUT_SECONDS, USE_LLM


# ── Keyword fallback router ─────────────────────────────────────────────────

METRIC_KEYWORDS = [
    "revenue", "income", "sales", "earning",
    "expense", "spending", "cost", "expenditure",
    "profit", "loss", "margin", "munafa", "kamai",
    "how much", "kitna", "total", "average",
    "this month", "last month", "is mahine", "pichle mahine",
]

BUDGET_KEYWORDS = [
    "budget", "over budget", "overspend", "limit",
    "bajet", "kharcha limit", "zyada kharcha",
]

COMPLIANCE_KEYWORDS = [
    "gst", "tax", "tds", "invoice rule", "compliance",
    "record keeping", "digital payment", "section",
    "penalty", "return filing", "registration",
    "audit", "books of account",
]

ITEM_PRICE_KEYWORDS = [
    "price", "rate", "cost of", "last price",
    "should i buy", "onion", "rice", "dal",
    "daam", "bhav", "khareedna", "pyaaz", "pyaaj",
    "compare", "offer",
]


def _keyword_router(question: str) -> str:
    """Deterministic keyword-based classification."""
    q = question.lower().strip()

    # Check Hindi intent first
    hindi_intent = detect_hindi_intent(q)
    if hindi_intent:
        return hindi_intent

    # Score each category
    scores = {
        "item_price": sum(1 for kw in ITEM_PRICE_KEYWORDS if kw in q),
        "budget": sum(1 for kw in BUDGET_KEYWORDS if kw in q),
        "compliance": sum(1 for kw in COMPLIANCE_KEYWORDS if kw in q),
        "metric": sum(1 for kw in METRIC_KEYWORDS if kw in q),
    }

    best = max(scores, key=scores.get)  # type: ignore
    if scores[best] > 0:
        return best
    return "general"


def _llm_router(question: str) -> str:
    """Use OpenAI to classify the question."""
    try:
        from openai import OpenAI

        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            timeout=LLM_TIMEOUT_SECONDS,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You classify user questions about a small business into one category.\n"
                        "Reply with JSON: {\"intent\": \"<category>\"}\n"
                        "Categories:\n"
                        "- metric: questions about revenue, expenses, profit, margin, trends\n"
                        "- budget: questions about budgets, spending limits, over-budget\n"
                        "- compliance: questions about GST, TDS, tax rules, record-keeping, invoicing rules\n"
                        "- item_price: questions about item prices, rates, buying decisions\n"
                        "- general: anything else, greetings, unclear\n"
                    ),
                },
                {"role": "user", "content": question},
            ],
        )
        text = response.choices[0].message.content or ""
        data = json.loads(text)
        intent = data.get("intent", "general")
        if intent in ("metric", "budget", "compliance", "item_price", "general"):
            return intent
        return "general"
    except Exception:
        # Fall back to keyword router on any failure
        return _keyword_router(question)


# ── Node function ────────────────────────────────────────────────────────────

def router_node(state: AgentState) -> dict[str, Any]:
    """Classify the user's question intent."""
    start = time.time()
    question = state["question"]

    if USE_LLM:
        intent = _llm_router(question)
    else:
        intent = _keyword_router(question)

    duration = int((time.time() - start) * 1000)

    return {
        "intent": intent,
        "agents_used": ["router"],
        "traces": [
            {
                "agent": "router",
                "input_summary": question[:100],
                "output_summary": f"Intent: {intent}",
                "duration_ms": duration,
            }
        ],
    }
