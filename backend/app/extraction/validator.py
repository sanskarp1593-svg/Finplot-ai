"""Arithmetic validation for extracted invoices."""

from __future__ import annotations

from app.schemas.document import InvoiceExtraction


def validate_invoice(extraction: InvoiceExtraction) -> InvoiceExtraction:
    """Cross-check arithmetic consistency of extracted invoice data.

    Checks:
    1. qty × rate = amount for each item
    2. Sum of item amounts ≈ subtotal
    3. subtotal + tax ≈ total
    """
    tolerance = 1.0  # allow ₹1 rounding differences

    for item in extraction.items:
        if item.quantity and item.rate and item.amount:
            expected = round(item.quantity * item.rate, 2)
            if abs(expected - item.amount) > tolerance:
                item.verification = "Verification required"
                extraction.verification_flags.append(
                    f"Item '{item.name}': {item.quantity} × {item.rate} = {expected}, "
                    f"but amount shows {item.amount}"
                )

    # Check items sum vs subtotal
    items_with_amount = [i for i in extraction.items if i.amount is not None]
    if items_with_amount and extraction.subtotal is not None:
        items_sum = sum(i.amount for i in items_with_amount)  # type: ignore
        if abs(items_sum - extraction.subtotal) > tolerance:
            extraction.verification_flags.append(
                f"Item total ({items_sum}) doesn't match subtotal ({extraction.subtotal})"
            )

    # Check subtotal + tax vs total
    if extraction.subtotal is not None and extraction.total is not None:
        tax = extraction.tax_amount or 0
        expected_total = extraction.subtotal + tax
        if abs(expected_total - extraction.total) > tolerance:
            extraction.verification_flags.append(
                f"Subtotal ({extraction.subtotal}) + tax ({tax}) = {expected_total}, "
                f"but total shows {extraction.total}"
            )

    return extraction
