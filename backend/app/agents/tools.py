"""DB query helpers used by agent nodes."""

from __future__ import annotations

import datetime as _dt
import re
from collections import defaultdict
from typing import Any, Optional

from sqlalchemy import extract, func
from sqlalchemy.orm import Session

from app.db.models import Budget, Document, Transaction
from app.agents.hindi import translate_item_name


def get_month_metrics(db: Session, biz_id: int, year: int, month: int) -> dict[str, Any]:
    """Compute revenue, expenses, profit, margin for a given month."""
    rows = (
        db.query(Transaction.type, func.sum(Transaction.amount))
        .filter(
            Transaction.business_id == biz_id,
            extract("year", Transaction.date) == year,
            extract("month", Transaction.date) == month,
        )
        .group_by(Transaction.type)
        .all()
    )
    totals = {r[0]: r[1] for r in rows}
    revenue = totals.get("revenue", 0.0)
    expenses = totals.get("expense", 0.0)
    profit = revenue - expenses
    margin = round(profit / revenue * 100, 1) if revenue else 0.0

    return {
        "month": f"{year:04d}-{month:02d}",
        "revenue": revenue,
        "expenses": expenses,
        "profit": profit,
        "margin": margin,
    }


def get_latest_month(db: Session, biz_id: int) -> tuple[int, int]:
    """Return (year, month) of the latest transaction, or current month."""
    latest = (
        db.query(func.max(Transaction.date))
        .filter(Transaction.business_id == biz_id)
        .scalar()
    )
    if latest:
        return latest.year, latest.month
    today = _dt.date.today()
    return today.year, today.month


def get_budget_status(db: Session, biz_id: int, year: int, month: int) -> list[dict[str, Any]]:
    """Get budget vs actual for each category in a given month."""
    budgets = db.query(Budget).filter(Budget.business_id == biz_id).all()
    if not budgets:
        return []

    spent_rows = (
        db.query(Transaction.category, func.sum(Transaction.amount))
        .filter(
            Transaction.business_id == biz_id,
            Transaction.type == "expense",
            extract("year", Transaction.date) == year,
            extract("month", Transaction.date) == month,
        )
        .group_by(Transaction.category)
        .all()
    )
    spent_map = {cat: amt for cat, amt in spent_rows}

    result = []
    for b in budgets:
        spent = spent_map.get(b.category, 0)
        result.append({
            "category": b.category,
            "spent": spent,
            "limit": b.monthly_limit,
            "over_budget": spent > b.monthly_limit,
            "over_by": max(0, spent - b.monthly_limit),
        })
    return result


def get_expense_by_category(db: Session, biz_id: int, year: int, month: int) -> list[dict]:
    """Expense breakdown by category for a month."""
    rows = (
        db.query(Transaction.category, func.sum(Transaction.amount))
        .filter(
            Transaction.business_id == biz_id,
            Transaction.type == "expense",
            extract("year", Transaction.date) == year,
            extract("month", Transaction.date) == month,
        )
        .group_by(Transaction.category)
        .order_by(func.sum(Transaction.amount).desc())
        .all()
    )
    return [{"category": cat, "amount": amt} for cat, amt in rows]


def get_item_prices(db: Session, biz_id: int, item_name: str) -> list[dict[str, Any]]:
    """Search confirmed invoices for an item's price history.

    Matches by word overlap, with Hindi name translation.
    """
    # Translate Hindi name if applicable
    eng_name = translate_item_name(item_name)
    search_terms = {eng_name.lower(), item_name.lower()}
    # Add singular/plural variations
    for t in list(search_terms):
        if t.endswith("s"):
            search_terms.add(t[:-1])
        else:
            search_terms.add(t + "s")

    # Get confirmed invoices
    docs = (
        db.query(Document)
        .filter(
            Document.business_id == biz_id,
            Document.status == "confirmed",
        )
        .order_by(Document.created_at.desc())
        .all()
    )

    results = []
    for doc in docs:
        data = doc.extracted_data or {}
        items = data.get("items", [])
        vendor = data.get("vendor", "")
        date = data.get("date", "")

        for item in items:
            name = (item.get("name") or "").lower()
            # Check if any search term appears in the item name
            name_words = set(re.split(r"\W+", name))
            if name_words & search_terms:
                results.append({
                    "item": item.get("name", ""),
                    "quantity": item.get("quantity"),
                    "rate": item.get("rate"),
                    "amount": item.get("amount"),
                    "date": date,
                    "vendor": vendor,
                })

    return results


def parse_month_from_question(question: str, biz_id: int, db: Session) -> tuple[int, int]:
    """Extract month reference from a question, default to latest."""
    q = question.lower()

    # "this month" or "is mahine"
    if "this month" in q or "is mahine" in q:
        return get_latest_month(db, biz_id)

    # "last month" or "pichle mahine"
    if "last month" in q or "pichle mahine" in q:
        year, month = get_latest_month(db, biz_id)
        d = _dt.date(year, month, 1) - _dt.timedelta(days=1)
        return d.year, d.month

    # Explicit month: "August 2026", "Aug", "2026-08"
    month_names = {
        "january": 1, "february": 2, "march": 3, "april": 4,
        "may": 5, "june": 6, "july": 7, "august": 8,
        "september": 9, "october": 10, "november": 11, "december": 12,
        "jan": 1, "feb": 2, "mar": 3, "apr": 4,
        "jun": 6, "jul": 7, "aug": 8,
        "sep": 9, "oct": 10, "nov": 11, "dec": 12,
    }
    for name, num in month_names.items():
        if name in q:
            # Try to find year
            year_match = re.search(r"20\d{2}", q)
            year = int(year_match.group()) if year_match else get_latest_month(db, biz_id)[0]
            return year, num

    # YYYY-MM
    m = re.search(r"(\d{4})-(\d{2})", q)
    if m:
        return int(m.group(1)), int(m.group(2))

    # Default to latest
    return get_latest_month(db, biz_id)
