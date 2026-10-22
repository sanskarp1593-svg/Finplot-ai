"""Dashboard API – summary, sparklines, category breakdown, budget progress."""

from __future__ import annotations

import datetime as _dt
from collections import defaultdict

from fastapi import APIRouter, Depends, Query
from sqlalchemy import extract, func
from sqlalchemy.orm import Session

from app.db.engine import get_db
from app.db.models import Budget, Business, Transaction
from app.config import USE_GEMINI
from app.schemas.dashboard import (
    BudgetProgress,
    CategoryBreakdown,
    DashboardData,
    MonthChange,
    MonthSummary,
    SparklinePoint,
)

router = APIRouter(prefix="/api", tags=["dashboard"])


def _month_summary(db: Session, biz_id: int, year: int, month: int) -> MonthSummary:
    """Compute revenue/expenses/profit/margin for one month."""
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
    margin = (profit / revenue * 100) if revenue else 0.0
    return MonthSummary(
        month=f"{year:04d}-{month:02d}",
        revenue=revenue,
        expenses=expenses,
        profit=profit,
        margin=round(margin, 1),
    )


def _pct_change(current: float, previous: float) -> float | None:
    if previous == 0:
        return None
    return round((current - previous) / abs(previous) * 100, 1)


@router.get("/dashboard", response_model=DashboardData)
def dashboard(
    month: str = Query(None, description="YYYY-MM, defaults to latest month with data"),
    db: Session = Depends(get_db),
) -> DashboardData:
    biz = db.query(Business).first()
    if not biz:
        return DashboardData(
            summary=MonthSummary(month="", revenue=0, expenses=0, profit=0, margin=0),
            change=MonthChange(),
            sparkline_revenue=[],
            sparkline_expenses=[],
            sparkline_profit=[],
            trend=[],
            category_breakdown=[],
            budget_progress=[],
            gemini_available=USE_GEMINI,
        )

    # Determine target month
    if month:
        year, mo = int(month[:4]), int(month[5:7])
    else:
        # Latest month with transactions
        latest = (
            db.query(func.max(Transaction.date))
            .filter(Transaction.business_id == biz.id)
            .scalar()
        )
        if latest is None:
            year, mo = _dt.date.today().year, _dt.date.today().month
        else:
            year, mo = latest.year, latest.month

    summary = _month_summary(db, biz.id, year, mo)

    # Previous month for comparison
    prev_date = _dt.date(year, mo, 1) - _dt.timedelta(days=1)
    prev_summary = _month_summary(db, biz.id, prev_date.year, prev_date.month)
    change = MonthChange(
        revenue_change=_pct_change(summary.revenue, prev_summary.revenue),
        expenses_change=_pct_change(summary.expenses, prev_summary.expenses),
        profit_change=_pct_change(summary.profit, prev_summary.profit),
    )

    # Sparklines + trend (last 6 months)
    sparkline_rev, sparkline_exp, sparkline_pro = [], [], []
    trend = []
    for i in range(5, -1, -1):
        d = _dt.date(year, mo, 1)
        for _ in range(i):
            d = (d - _dt.timedelta(days=1)).replace(day=1)
        ms = _month_summary(db, biz.id, d.year, d.month)
        sparkline_rev.append(SparklinePoint(month=ms.month, value=ms.revenue))
        sparkline_exp.append(SparklinePoint(month=ms.month, value=ms.expenses))
        sparkline_pro.append(SparklinePoint(month=ms.month, value=ms.profit))
        trend.append(ms)

    # Category breakdown for target month
    cat_rows = (
        db.query(Transaction.category, func.sum(Transaction.amount))
        .filter(
            Transaction.business_id == biz.id,
            Transaction.type == "expense",
            extract("year", Transaction.date) == year,
            extract("month", Transaction.date) == mo,
        )
        .group_by(Transaction.category)
        .all()
    )
    total_exp = summary.expenses or 1
    category_breakdown = [
        CategoryBreakdown(
            category=cat,
            amount=amt,
            percentage=round(amt / total_exp * 100, 1),
        )
        for cat, amt in sorted(cat_rows, key=lambda r: -r[1])
    ]

    # Budget progress for target month
    budgets = db.query(Budget).filter(Budget.business_id == biz.id).all()
    budget_progress = []
    spent_by_cat: dict[str, float] = {cat: amt for cat, amt in cat_rows}
    for b in budgets:
        spent = spent_by_cat.get(b.category, 0.0)
        pct = round(spent / b.monthly_limit * 100, 1) if b.monthly_limit else 0
        budget_progress.append(
            BudgetProgress(
                category=b.category,
                spent=spent,
                limit=b.monthly_limit,
                percentage=pct,
                over_budget=spent > b.monthly_limit,
            )
        )

    return DashboardData(
        summary=summary,
        change=change,
        sparkline_revenue=sparkline_rev,
        sparkline_expenses=sparkline_exp,
        sparkline_profit=sparkline_pro,
        trend=trend,
        category_breakdown=category_breakdown,
        budget_progress=budget_progress,
        gemini_available=USE_GEMINI,
    )
