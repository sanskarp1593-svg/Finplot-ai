"""Pydantic schemas for budgets."""

from __future__ import annotations

import datetime as _dt
from typing import Optional

from pydantic import BaseModel, Field


class BudgetCreate(BaseModel):
    category: str = Field(..., min_length=1, max_length=100)
    monthly_limit: float = Field(..., gt=0)


class BudgetOut(BaseModel):
    id: int
    business_id: int
    category: str
    monthly_limit: float
    created_at: _dt.datetime

    model_config = {"from_attributes": True}


class BudgetUpdate(BaseModel):
    """Bulk update: list of category→limit pairs."""
    budgets: list[BudgetCreate]
