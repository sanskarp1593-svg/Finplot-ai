"""Seed the database with sample data for demo / development.

Usage from project root:
    npm run seed                          # resets business #1 to demo data
    backend\\.venv\\Scripts\\python.exe -m app.db.seed --empty   # empty start
"""

from __future__ import annotations

import datetime as _dt
import sys
from pathlib import Path

from sqlalchemy.orm import Session

# Ensure the backend dir is on sys.path when run with -m
_backend_dir = str(Path(__file__).resolve().parent.parent.parent)
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

from app.db.engine import SessionLocal, engine  # noqa: E402
from app.db.models import (  # noqa: E402
    Base,
    Budget,
    Business,
    Document,
    KnowledgeDoc,
    QueryHistory,
    Transaction,
)
from app.config import KNOWLEDGE_DIR  # noqa: E402


# ── Expense categories used throughout the app ───────────────────────────────
EXPENSE_CATEGORIES = [
    "Inventory / Stock",
    "Rent & Utilities",
    "Salaries & Wages",
    "Travel & Transport",
    "Marketing & Ads",
    "Office Supplies",
    "Repairs & Maintenance",
    "Insurance",
    "Taxes & Fees",
    "Miscellaneous",
]

REVENUE_CATEGORIES = [
    "Product Sales",
    "Service Revenue",
    "Other Income",
]


def _seed_transactions(db: Session, biz_id: int) -> None:
    """Create ~35 sample transactions across Jun-Aug 2026."""
    rows: list[dict] = [
        # ── June 2026 ────────────────────────────────────────────────
        dict(date=_dt.date(2026, 6, 2), type="revenue", category="Product Sales", amount=12000, tax_amount=2160, description="Wholesale grocery order", vendor="Direct"),
        dict(date=_dt.date(2026, 6, 3), type="expense", category="Inventory / Stock", amount=8500, tax_amount=1530, description="Rice & dal restock", vendor="Aggarwal Traders"),
        dict(date=_dt.date(2026, 6, 5), type="revenue", category="Product Sales", amount=4200, tax_amount=756, description="Daily counter sales"),
        dict(date=_dt.date(2026, 6, 7), type="expense", category="Rent & Utilities", amount=15000, tax_amount=0, description="Shop rent – June", vendor="Landlord"),
        dict(date=_dt.date(2026, 6, 8), type="expense", category="Salaries & Wages", amount=9000, tax_amount=0, description="Helper salary – June", vendor="Raju"),
        dict(date=_dt.date(2026, 6, 10), type="revenue", category="Product Sales", amount=5600, tax_amount=1008, description="Weekend rush sales"),
        dict(date=_dt.date(2026, 6, 12), type="expense", category="Travel & Transport", amount=800, tax_amount=0, description="Delivery fuel"),
        dict(date=_dt.date(2026, 6, 15), type="revenue", category="Product Sales", amount=3800, tax_amount=684, description="Midweek counter sales"),
        dict(date=_dt.date(2026, 6, 18), type="expense", category="Office Supplies", amount=1200, tax_amount=216, description="Printer paper & ink", vendor="StationeryMart"),
        dict(date=_dt.date(2026, 6, 22), type="revenue", category="Service Revenue", amount=2000, tax_amount=360, description="Home delivery charges collected"),
        dict(date=_dt.date(2026, 6, 25), type="expense", category="Inventory / Stock", amount=6200, tax_amount=1116, description="Cooking oil & spices", vendor="Gupta Wholesalers"),
        dict(date=_dt.date(2026, 6, 28), type="revenue", category="Product Sales", amount=7400, tax_amount=1332, description="Month-end bulk sale"),

        # ── July 2026 ────────────────────────────────────────────────
        dict(date=_dt.date(2026, 7, 1), type="expense", category="Rent & Utilities", amount=15000, tax_amount=0, description="Shop rent – July", vendor="Landlord"),
        dict(date=_dt.date(2026, 7, 2), type="revenue", category="Product Sales", amount=9500, tax_amount=1710, description="Festival week sales"),
        dict(date=_dt.date(2026, 7, 4), type="expense", category="Inventory / Stock", amount=11000, tax_amount=1980, description="Festival stock – sweets & snacks", vendor="Haldiram Distributor"),
        dict(date=_dt.date(2026, 7, 5), type="expense", category="Marketing & Ads", amount=3000, tax_amount=540, description="Festival banner & flyers", vendor="PrintZone"),
        dict(date=_dt.date(2026, 7, 8), type="revenue", category="Product Sales", amount=14200, tax_amount=2556, description="Festival weekend peak"),
        dict(date=_dt.date(2026, 7, 10), type="expense", category="Salaries & Wages", amount=9000, tax_amount=0, description="Helper salary – July", vendor="Raju"),
        dict(date=_dt.date(2026, 7, 12), type="expense", category="Travel & Transport", amount=1500, tax_amount=0, description="Stock pickup auto fare"),
        dict(date=_dt.date(2026, 7, 15), type="revenue", category="Product Sales", amount=6800, tax_amount=1224, description="Regular week sales"),
        dict(date=_dt.date(2026, 7, 18), type="expense", category="Repairs & Maintenance", amount=2500, tax_amount=450, description="AC repair", vendor="CoolTech"),
        dict(date=_dt.date(2026, 7, 22), type="revenue", category="Other Income", amount=1000, tax_amount=0, description="Old carton sale"),
        dict(date=_dt.date(2026, 7, 25), type="expense", category="Inventory / Stock", amount=7800, tax_amount=1404, description="Beverages & packaged food", vendor="Coca-Cola Distributor"),
        dict(date=_dt.date(2026, 7, 30), type="revenue", category="Product Sales", amount=8200, tax_amount=1476, description="Month-end sales push"),

        # ── August 2026 ──────────────────────────────────────────────
        dict(date=_dt.date(2026, 8, 1), type="expense", category="Rent & Utilities", amount=15000, tax_amount=0, description="Shop rent – August", vendor="Landlord"),
        dict(date=_dt.date(2026, 8, 3), type="revenue", category="Product Sales", amount=5200, tax_amount=936, description="Start of month sales"),
        dict(date=_dt.date(2026, 8, 5), type="expense", category="Inventory / Stock", amount=9200, tax_amount=1656, description="Grains & pulses", vendor="Aggarwal Traders"),
        dict(date=_dt.date(2026, 8, 8), type="revenue", category="Product Sales", amount=11500, tax_amount=2070, description="Independence Day week sales"),
        dict(date=_dt.date(2026, 8, 10), type="expense", category="Salaries & Wages", amount=9500, tax_amount=0, description="Helper salary – August", vendor="Raju"),
        dict(date=_dt.date(2026, 8, 10), type="expense", category="Travel & Transport", amount=1800, tax_amount=90, description="Courier charges", vendor="BlueDart"),
        dict(date=_dt.date(2026, 8, 12), type="revenue", category="Service Revenue", amount=5000, tax_amount=900, description="Installation job"),
        dict(date=_dt.date(2026, 8, 15), type="revenue", category="Product Sales", amount=8900, tax_amount=1602, description="Independence Day sale"),
        dict(date=_dt.date(2026, 8, 18), type="expense", category="Insurance", amount=4000, tax_amount=720, description="Shop insurance premium", vendor="LIC"),
        dict(date=_dt.date(2026, 8, 22), type="revenue", category="Product Sales", amount=6300, tax_amount=1134, description="Regular sales"),
        dict(date=_dt.date(2026, 8, 25), type="expense", category="Miscellaneous", amount=600, tax_amount=0, description="Pest control"),
        dict(date=_dt.date(2026, 8, 28), type="revenue", category="Product Sales", amount=7800, tax_amount=1404, description="Month-end sales"),
    ]

    for r in rows:
        db.add(Transaction(business_id=biz_id, source="manual", **r))


def _seed_budgets(db: Session, biz_id: int) -> None:
    """Set monthly budget limits."""
    limits = {
        "Inventory / Stock": 40000,
        "Rent & Utilities": 16000,
        "Salaries & Wages": 10000,
        "Travel & Transport": 3000,
        "Marketing & Ads": 5000,
        "Office Supplies": 2000,
        "Repairs & Maintenance": 3000,
        "Insurance": 5000,
        "Taxes & Fees": 2000,
        "Miscellaneous": 2000,
    }
    for cat, limit in limits.items():
        db.add(Budget(business_id=biz_id, category=cat, monthly_limit=limit))


def _seed_knowledge(db: Session) -> None:
    """Load knowledge docs from data/knowledge/ if they exist."""
    if not KNOWLEDGE_DIR.exists():
        return
    for md_file in sorted(KNOWLEDGE_DIR.glob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        title = content.split("\n", 1)[0].lstrip("# ").strip() or md_file.stem
        existing = db.query(KnowledgeDoc).filter_by(source_file=md_file.name).first()
        if not existing:
            db.add(KnowledgeDoc(title=title, content=content, source_file=md_file.name))


def seed(empty: bool = False, target_engine=None, target_session=None) -> None:
    """Create or reset the database.

    Args:
        empty: If True, start completely empty (no demo data).
        target_engine: Optional SQLAlchemy engine to bind tables to.
        target_session: Optional sessionmaker factory to produce sessions.
    """
    eng = target_engine or engine
    Base.metadata.create_all(bind=eng)
    db_factory = target_session or SessionLocal
    db = db_factory()
    try:
        # Clear all rows
        for model in (QueryHistory, Document, Transaction, Budget, Business, KnowledgeDoc):
            db.query(model).delete()
        db.commit()

        if empty:
            # Create one empty business
            biz = Business(name="My Business", industry="General", language="en")
            db.add(biz)
            db.commit()
            print("[OK] Database reset to empty state.")
            return

        # Demo business
        biz = Business(name="Kumar General Store", industry="Retail", language="en")
        db.add(biz)
        db.flush()  # get biz.id

        _seed_transactions(db, biz.id)
        _seed_budgets(db, biz.id)
        _seed_knowledge(db)
        db.commit()
        print(f"[OK] Seeded business #{biz.id} '{biz.name}' with demo data.")
    finally:
        db.close()



if __name__ == "__main__":
    _empty = "--empty" in sys.argv
    seed(empty=_empty)
