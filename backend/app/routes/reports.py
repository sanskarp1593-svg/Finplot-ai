"""Reports – P&L and category comparison."""

from __future__ import annotations

from collections import defaultdict

from fastapi import APIRouter, Depends
from sqlalchemy import extract, func
from sqlalchemy.orm import Session

from app.db.engine import get_db
from app.db.models import Business, Transaction

router = APIRouter(prefix="/api", tags=["reports"])


@router.get("/reports/pnl")
def profit_and_loss(db: Session = Depends(get_db)) -> dict:
    """Month-by-month P&L report."""
    biz = db.query(Business).first()
    if not biz:
        return {"months": []}

    rows = (
        db.query(
            extract("year", Transaction.date).label("yr"),
            extract("month", Transaction.date).label("mo"),
            Transaction.type,
            func.sum(Transaction.amount).label("total"),
            func.sum(Transaction.tax_amount).label("total_tax"),
        )
        .filter(Transaction.business_id == biz.id)
        .group_by("yr", "mo", Transaction.type)
        .order_by("yr", "mo")
        .all()
    )

    months_dict: dict[str, dict] = defaultdict(lambda: {"revenue": 0, "expenses": 0, "tax": 0})
    for yr, mo, typ, total, total_tax in rows:
        key = f"{int(yr):04d}-{int(mo):02d}"
        if typ == "revenue":
            months_dict[key]["revenue"] = total
        else:
            months_dict[key]["expenses"] = total
        months_dict[key]["tax"] += total_tax or 0

    result = []
    for month_key in sorted(months_dict):
        d = months_dict[month_key]
        profit = d["revenue"] - d["expenses"]
        margin = round(profit / d["revenue"] * 100, 1) if d["revenue"] else 0
        result.append({
            "month": month_key,
            "revenue": d["revenue"],
            "expenses": d["expenses"],
            "tax": round(d["tax"], 2),
            "profit": profit,
            "margin": margin,
        })
    return {"months": result}


@router.get("/reports/categories")
def category_comparison(db: Session = Depends(get_db)) -> dict:
    """Expense by category across all months."""
    biz = db.query(Business).first()
    if not biz:
        return {"categories": []}

    rows = (
        db.query(
            Transaction.category,
            extract("year", Transaction.date).label("yr"),
            extract("month", Transaction.date).label("mo"),
            func.sum(Transaction.amount).label("total"),
        )
        .filter(Transaction.business_id == biz.id, Transaction.type == "expense")
        .group_by(Transaction.category, "yr", "mo")
        .all()
    )

    # Organize: {category: {month: amount}}
    cat_data: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    all_months: set[str] = set()
    for cat, yr, mo, total in rows:
        key = f"{int(yr):04d}-{int(mo):02d}"
        cat_data[cat][key] = total
        all_months.add(key)

    sorted_months = sorted(all_months)
    categories = []
    for cat in sorted(cat_data):
        categories.append({
            "category": cat,
            "months": {m: cat_data[cat].get(m, 0) for m in sorted_months},
            "total": sum(cat_data[cat].values()),
        })
    categories.sort(key=lambda c: -c["total"])

    return {"months": sorted_months, "categories": categories}
