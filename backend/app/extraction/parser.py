"""Parse raw extracted text into structured invoice fields."""

from __future__ import annotations

import re
from typing import Optional

from app.schemas.document import InvoiceExtraction, InvoiceItem


def _find_amount(text: str, patterns: list[str]) -> Optional[float]:
    """Try multiple regex patterns to find a monetary amount."""
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            try:
                val = m.group(1).replace(",", "").strip()
                return float(val)
            except (ValueError, IndexError):
                continue
    return None


def _find_date(text: str) -> Optional[str]:
    """Try to find a date in the text and return as ISO string."""
    # DD/MM/YYYY or DD-MM-YYYY
    m = re.search(r"(\d{1,2})[/\-.](\d{1,2})[/\-.](\d{4})", text)
    if m:
        day, month, year = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if 1 <= month <= 12 and 1 <= day <= 31:
            return f"{year:04d}-{month:02d}-{day:02d}"
        # Maybe MM/DD/YYYY
        if 1 <= day <= 12 and 1 <= month <= 31:
            return f"{year:04d}-{day:02d}-{month:02d}"

    # YYYY-MM-DD
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", text)
    if m:
        return m.group(0)

    return None


def _find_vendor(text: str) -> Optional[str]:
    """Try to extract vendor/seller name from the first few lines."""
    lines = text.strip().split("\n")
    # Usually vendor name is in the first 3 lines
    for line in lines[:5]:
        line = line.strip()
        # Skip very short lines, pure numbers, or common headers
        if len(line) < 3:
            continue
        if re.match(r"^[\d\s.,/\-]+$", line):
            continue
        if re.match(r"(?i)^(invoice|bill|tax|gst|date|total|sub)", line):
            continue
        # This looks like a business name
        return line
    return None


def _parse_items(text: str) -> list[InvoiceItem]:
    """Try to extract line items from the text.

    Looks for patterns like:
        Item name    Qty    Rate    Amount
        Rice         10     45      450
    """
    items: list[InvoiceItem] = []

    # Look for table-like rows: text followed by numbers
    # Pattern: words + optional qty + optional rate + amount
    pattern = re.compile(
        r"^(.+?)\s+"                              # item name
        r"(\d+(?:\.\d+)?)\s+"                     # quantity
        r"[₹Rs.]*\s*(\d[\d,]*(?:\.\d+)?)\s+"     # rate
        r"[₹Rs.]*\s*(\d[\d,]*(?:\.\d+)?)\s*$",   # amount
        re.MULTILINE,
    )

    for m in pattern.finditer(text):
        name = m.group(1).strip()
        # Skip header rows
        if re.match(r"(?i)(item|description|particular|product|name|sr\.?)", name):
            continue
        try:
            qty = float(m.group(2).replace(",", ""))
            rate = float(m.group(3).replace(",", ""))
            amount = float(m.group(4).replace(",", ""))
            items.append(InvoiceItem(name=name, quantity=qty, rate=rate, amount=amount))
        except ValueError:
            continue

    # Simpler: just item + amount
    if not items:
        simple_pattern = re.compile(
            r"^(.{3,40}?)\s+[₹Rs.]*\s*(\d[\d,]*(?:\.\d{1,2})?)\s*$",
            re.MULTILINE,
        )
        for m in simple_pattern.finditer(text):
            name = m.group(1).strip()
            if re.match(r"(?i)(total|sub|tax|gst|grand|discount|balance|date|invoice)", name):
                continue
            try:
                amount = float(m.group(2).replace(",", ""))
                items.append(InvoiceItem(name=name, amount=amount))
            except ValueError:
                continue

    return items


def parse_invoice_text(text: str) -> InvoiceExtraction:
    """Parse extracted text into structured InvoiceExtraction."""
    flags: list[str] = []

    vendor = _find_vendor(text)
    date = _find_date(text)
    items = _parse_items(text)

    subtotal = _find_amount(text, [
        r"(?:sub\s*total|subtotal)[:\s]*[₹Rs.]*\s*([\d,]+(?:\.\d+)?)",
    ])
    tax_amount = _find_amount(text, [
        r"(?:gst|tax|cgst\s*\+?\s*sgst|igst)[:\s]*[₹Rs.]*\s*([\d,]+(?:\.\d+)?)",
        r"(?:tax\s*amount)[:\s]*[₹Rs.]*\s*([\d,]+(?:\.\d+)?)",
    ])
    total = _find_amount(text, [
        r"(?:grand\s*total|total\s*amount|net\s*amount|total)[:\s]*[₹Rs.]*\s*([\d,]+(?:\.\d+)?)",
    ])

    # Flag missing fields
    if not vendor:
        flags.append("Vendor name not found – Verification required")
    if not date:
        flags.append("Date not found – Verification required")
    if not items:
        flags.append("No line items extracted – Verification required")
    if total is None:
        flags.append("Total amount not found – Verification required")

    return InvoiceExtraction(
        vendor=vendor,
        date=date,
        items=items,
        subtotal=subtotal,
        tax_amount=tax_amount,
        total=total,
        verification_flags=flags,
    )
