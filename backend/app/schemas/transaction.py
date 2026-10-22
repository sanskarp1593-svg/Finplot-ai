"""Pydantic schemas for transactions."""

from __future__ import annotations

import datetime as _dt
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class TransactionCreate(BaseModel):
    date: _dt.date
    type: str = Field(..., pattern="^(revenue|expense)$")
    category: str = Field(..., min_length=1, max_length=100)
    amount: float = Field(..., gt=0)
    tax_amount: Optional[float] = 0.0
    description: Optional[str] = ""
    vendor: Optional[str] = ""
    source: str = "manual"


class TransactionOut(BaseModel):
    id: int
    business_id: int
    date: _dt.date
    type: str
    category: str
    amount: float
    tax_amount: float | None
    description: str | None
    vendor: str | None
    source: str
    created_at: _dt.datetime

    model_config = {"from_attributes": True}


class TransactionListOut(BaseModel):
    items: list[TransactionOut]
    total: int
    page: int
    page_size: int


class TransactionFilter(BaseModel):
    start_date: Optional[_dt.date] = None
    end_date: Optional[_dt.date] = None
    type: Optional[str] = None
    category: Optional[str] = None
    search: Optional[str] = None
    page: int = 1
    page_size: int = 50


class CSVRow(BaseModel):
    """One row from a CSV import."""
    date: _dt.date
    type: str
    category: str
    amount: float
    tax_amount: Optional[float] = 0.0
    description: Optional[str] = ""
    vendor: Optional[str] = ""

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: str) -> str:
        v = v.strip().lower()
        if v not in ("revenue", "expense"):
            raise ValueError("type must be 'revenue' or 'expense'")
        return v

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("amount must be positive")
        return v
