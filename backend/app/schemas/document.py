"""Pydantic schemas for uploaded documents / invoices."""

from __future__ import annotations

import datetime as _dt
from typing import Any, Optional

from pydantic import BaseModel


class InvoiceItem(BaseModel):
    name: str = ""
    quantity: Optional[float] = None
    rate: Optional[float] = None
    amount: Optional[float] = None
    verification: Optional[str] = None  # "Verification required" or None


class InvoiceExtraction(BaseModel):
    vendor: Optional[str] = None
    date: Optional[str] = None      # ISO date string or None
    items: list[InvoiceItem] = []
    subtotal: Optional[float] = None
    tax_amount: Optional[float] = None
    total: Optional[float] = None
    notes: Optional[str] = None
    verification_flags: list[str] = []   # list of fields needing review
    upload_source: str = "print"         # "print" | "handwriting"


class DocumentOut(BaseModel):
    id: int
    business_id: int
    filename: str
    original_name: str
    file_type: str
    extracted_data: Optional[dict[str, Any]] = None
    status: str
    upload_source: Optional[str] = None
    is_verified: bool
    created_at: _dt.datetime

    model_config = {"from_attributes": True}


class InvoiceConfirm(BaseModel):
    """User-corrected invoice data to confirm and save as transactions."""
    vendor: str = ""
    date: str   # ISO date
    items: list[InvoiceItem] = []
    subtotal: float
    tax_amount: float = 0.0
    total: float
    category: str = "Inventory / Stock"
