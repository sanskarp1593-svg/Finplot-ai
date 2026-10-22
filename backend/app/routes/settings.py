"""Business settings and budget management."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.engine import get_db
from app.db.models import Budget, Business
from app.schemas.budget import BudgetOut, BudgetUpdate
from app.schemas.business import BusinessOut, BusinessSettings

router = APIRouter(prefix="/api", tags=["settings"])


def _get_biz(db: Session) -> Business:
    biz = db.query(Business).first()
    if not biz:
        raise HTTPException(404, "No business configured.")
    return biz


@router.get("/settings", response_model=dict)
def get_settings(db: Session = Depends(get_db)) -> dict:
    biz = _get_biz(db)
    budgets = db.query(Budget).filter(Budget.business_id == biz.id).all()
    return {
        "business": BusinessOut.model_validate(biz).model_dump(),
        "budgets": [BudgetOut.model_validate(b).model_dump() for b in budgets],
    }


@router.put("/settings", response_model=BusinessOut)
def update_settings(
    body: BusinessSettings,
    db: Session = Depends(get_db),
) -> BusinessOut:
    biz = _get_biz(db)
    biz.name = body.name
    biz.industry = body.industry
    biz.language = body.language
    db.commit()
    db.refresh(biz)
    return BusinessOut.model_validate(biz)


@router.put("/settings/budgets", response_model=list[BudgetOut])
def update_budgets(
    body: BudgetUpdate,
    db: Session = Depends(get_db),
) -> list[BudgetOut]:
    biz = _get_biz(db)

    # Delete existing budgets and replace
    db.query(Budget).filter(Budget.business_id == biz.id).delete()
    new_budgets = []
    for item in body.budgets:
        b = Budget(business_id=biz.id, category=item.category, monthly_limit=item.monthly_limit)
        db.add(b)
        new_budgets.append(b)
    db.commit()
    for b in new_budgets:
        db.refresh(b)
    return [BudgetOut.model_validate(b) for b in new_budgets]
