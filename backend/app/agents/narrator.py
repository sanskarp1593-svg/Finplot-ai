"""Narrator agent – composes the final answer with evidence and charts.

Dual-mode:
  - LLM mode: OpenAI writes natural language
  - Fallback mode: template-based narration (default)
"""

from __future__ import annotations

import json
import time
from typing import Any

from app.agents.hindi import get_templates
from app.agents.state import AgentState
from app.config import OPENAI_API_KEY, OPENAI_MODEL, LLM_TIMEOUT_SECONDS, USE_LLM


def _template_narration(state: AgentState) -> str:
    """Build answer from templates."""
    lang = state.get("language", "en")
    tmpl = get_templates(lang)
    intent = state.get("intent", "general")
    parts: list[str] = []

    if intent == "metric":
        metrics = state.get("metrics", {})
        if metrics:
            parts.append(tmpl["metric_summary"].format(**metrics))
        else:
            parts.append(tmpl["no_data"])

    elif intent == "budget":
        budget_data = state.get("budget_data", {})
        items = budget_data.get("items", [])
        if items:
            for b in items:
                if b["over_budget"]:
                    parts.append(tmpl["budget_over"].format(
                        category=b["category"], spent=b["spent"],
                        limit=b["limit"], over=b["over_by"],
                    ))
                else:
                    parts.append(tmpl["budget_ok"].format(
                        category=b["category"], spent=b["spent"], limit=b["limit"],
                    ))
        else:
            parts.append(tmpl["no_data"])

    elif intent == "compliance":
        comp = state.get("compliance_data", {})
        answer = comp.get("answer", "")
        if answer:
            parts.append(answer)
            for src in comp.get("sources", []):
                parts.append(tmpl["compliance_source"].format(title=src.get("title", "")))
        else:
            parts.append(tmpl["no_data"])

    elif intent == "item_price":
        ipd = state.get("item_price_data", {})
        prices = ipd.get("prices", [])
        item_name = ipd.get("item", "item")
        if prices:
            latest = prices[0]
            parts.append(tmpl["item_last_price"].format(
                item=item_name,
                price=latest.get("rate") or latest.get("amount", 0),
                date=latest.get("date", "?"),
                vendor=latest.get("vendor", "?"),
            ))
            if len(prices) > 1:
                if lang == "hi":
                    parts.append(f"\nपिछले {len(prices)} रिकॉर्ड मिले।")
                else:
                    parts.append(f"\n{len(prices)} price records found.")
                # Check for rate variance
                rates = [p.get("rate") or p.get("amount", 0) for p in prices if p.get("rate") or p.get("amount")]
                if rates and len(set(rates)) > 1:
                    min_r, max_r = min(rates), max(rates)
                    if max_r > min_r * 1.5:
                        warning = "⚠️ Rates differ significantly – could be a typo." if lang == "en" else "⚠️ भावों में बड़ा अंतर है – टाइपो हो सकता है।"
                        parts.append(warning)
        else:
            parts.append(tmpl["item_no_record"].format(item=item_name))

    else:
        parts.append(tmpl["general_fallback"])

    return "\n".join(parts)


def _llm_narration(state: AgentState) -> str:
    """Use OpenAI to compose a natural-language answer."""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)

        context_parts = []
        if state.get("metrics"):
            context_parts.append(f"Metrics: {json.dumps(state['metrics'])}")
        if state.get("budget_data"):
            context_parts.append(f"Budget: {json.dumps(state['budget_data'])}")
        if state.get("compliance_data"):
            context_parts.append(f"Compliance: {json.dumps(state['compliance_data'])}")
        if state.get("item_price_data"):
            context_parts.append(f"Item prices: {json.dumps(state['item_price_data'])}")

        lang_instruction = "Reply in Hindi." if state.get("language") == "hi" else "Reply in English."

        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            timeout=LLM_TIMEOUT_SECONDS,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are FinPilot, a financial assistant for a small Indian business. "
                        "Answer the user's question based on the provided data. "
                        "Be concise, factual, and use ₹ for currency. "
                        "Never say 'buy' or 'don't buy'. Never give definitive legal advice. "
                        "Flag interpretive answers for CA review. "
                        f"{lang_instruction}"
                    ),
                },
                {"role": "user", "content": f"Question: {state['question']}\n\nData:\n" + "\n".join(context_parts)},
            ],
        )
        return response.choices[0].message.content or _template_narration(state)
    except Exception:
        return _template_narration(state)


def narrator_node(state: AgentState) -> dict[str, Any]:
    """Compose the final answer."""
    start = time.time()

    if USE_LLM:
        answer = _llm_narration(state)
    else:
        answer = _template_narration(state)

    # Determine if CA review is needed
    intent = state.get("intent", "general")
    needs_ca = intent in ("compliance",)
    if needs_ca:
        tmpl = get_templates(state.get("language", "en"))
        answer += tmpl["ca_review"]

    duration = int((time.time() - start) * 1000)
    agents = state.get("agents_used", []) + ["narrator"]
    traces = state.get("traces", []) + [
        {
            "agent": "narrator",
            "input_summary": f"Intent: {intent}",
            "output_summary": answer[:80] + "…" if len(answer) > 80 else answer,
            "duration_ms": duration,
        }
    ]

    return {
        "answer": answer,
        "needs_ca_review": needs_ca,
        "agents_used": agents,
        "traces": traces,
    }
