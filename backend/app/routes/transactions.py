"""Transaction CRUD, CSV import/export endpoints."""

from __future__ import annotations

import csv
import datetime as _dt
import io
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy import extract
from sqlalchemy.orm import Session

from app.db.engine import get_db
from app.db.models import Business, Transaction
from app.schemas.transaction import CSVRow, TransactionCreate, TransactionOut, TransactionListOut

router = APIRouter(prefix="/api", tags=["transactions"])


def _get_biz(db: Session) -> Business:
    biz = db.query(Business).first()
    if not biz:
        raise HTTPException(404, "No business configured. Run seed first.")
    return biz


@router.get("/transactions", response_model=TransactionListOut)
def list_transactions(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    type: Optional[str] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    limit: Optional[int] = Query(None, ge=1, le=200),
    db: Session = Depends(get_db),
) -> TransactionListOut:
    biz = _get_biz(db)
    q = db.query(Transaction).filter(Transaction.business_id == biz.id)

    if start_date:
        q = q.filter(Transaction.date >= _dt.date.fromisoformat(start_date))
    if end_date:
        q = q.filter(Transaction.date <= _dt.date.fromisoformat(end_date))
    if type:
        q = q.filter(Transaction.type == type)
    if category:
        q = q.filter(Transaction.category == category)
    if search:
        like = f"%{search}%"
        q = q.filter(
            Transaction.description.ilike(like) | Transaction.vendor.ilike(like)
        )

    effective_limit = limit or page_size
    total = q.count()
    q = q.order_by(Transaction.date.desc(), Transaction.id.desc())
    rows = q.offset((page - 1) * effective_limit).limit(effective_limit).all()
    return TransactionListOut(
        items=[TransactionOut.model_validate(r) for r in rows],
        total=total,
        page=page,
        page_size=effective_limit,
    )


@router.post("/transactions", response_model=TransactionOut, status_code=200)
def create_transaction(
    body: TransactionCreate,
    db: Session = Depends(get_db),
) -> TransactionOut:
    biz = _get_biz(db)
    txn = Transaction(business_id=biz.id, **body.model_dump())
    db.add(txn)
    db.commit()
    db.refresh(txn)
    return TransactionOut.model_validate(txn)


@router.delete("/transactions/{txn_id}", status_code=200)
def delete_transaction(txn_id: int, db: Session = Depends(get_db)) -> dict:
    biz = _get_biz(db)
    txn = (
        db.query(Transaction)
        .filter(Transaction.id == txn_id, Transaction.business_id == biz.id)
        .first()
    )
    if not txn:
        raise HTTPException(404, "Transaction not found")
    db.delete(txn)
    db.commit()
    return {"status": "deleted", "id": txn_id}


@router.post("/transactions/import", status_code=200)
async def import_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> dict:
    """Import a CSV file. All rows validated first – nothing saved on any error."""
    biz = _get_biz(db)

    content = (await file.read()).decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(content))

    parsed_rows: list[CSVRow] = []
    errors: list[str] = []

    for i, row in enumerate(reader, start=2):
        try:
            parsed_rows.append(CSVRow(**{k.strip(): v.strip() for k, v in row.items() if k}))
        except Exception as exc:
            errors.append(f"Row {i}: {exc}")

    if errors:
        raise HTTPException(422, detail={"message": "CSV validation failed", "errors": errors})

    txns: list[Transaction] = []
    for pr in parsed_rows:
        txn = Transaction(
            business_id=biz.id,
            date=pr.date,
            type=pr.type,
            category=pr.category,
            amount=pr.amount,
            tax_amount=pr.tax_amount or 0,
            description=pr.description or "",
            vendor=pr.vendor or "",
            source="csv",
        )
        db.add(txn)
        txns.append(txn)

    db.commit()
    for t in txns:
        db.refresh(t)
    return {
        "imported_count": len(txns),
        "transactions": [TransactionOut.model_validate(t) for t in txns],
    }



@router.get("/transactions/export")
def export_csv(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    type: Optional[str] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
) -> StreamingResponse:
    biz = _get_biz(db)
    q = db.query(Transaction).filter(Transaction.business_id == biz.id)
    if start_date:
        q = q.filter(Transaction.date >= _dt.date.fromisoformat(start_date))
    if end_date:
        q = q.filter(Transaction.date <= _dt.date.fromisoformat(end_date))
    if type:
        q = q.filter(Transaction.type == type)
    if category:
        q = q.filter(Transaction.category == category)
    if search:
        like = f"%{search}%"
        q = q.filter(
            Transaction.description.ilike(like) | Transaction.vendor.ilike(like)
        )
    q = q.order_by(Transaction.date.desc())
    rows = q.all()

    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["date", "type", "category", "amount", "tax_amount", "description", "vendor"])
    for r in rows:
        writer.writerow([r.date.isoformat(), r.type, r.category, r.amount, r.tax_amount, r.description, r.vendor])
    buf.seek(0)

    return StreamingResponse(
        buf,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=transactions.csv"},
    )


@router.get("/transactions/categories", response_model=dict)
def get_categories(db: Session = Depends(get_db)) -> dict:
    """Return the fixed category lists."""
    from app.db.seed import EXPENSE_CATEGORIES, REVENUE_CATEGORIES
    return {"expense": EXPENSE_CATEGORIES, "revenue": REVENUE_CATEGORIES}
