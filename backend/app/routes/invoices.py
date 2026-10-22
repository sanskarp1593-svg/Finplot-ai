"""Invoice upload, extraction, confirm/reject endpoints."""

from __future__ import annotations

import datetime as _dt
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.config import MAX_UPLOAD_MB, UPLOAD_DIR
from app.db.engine import get_db
from app.db.models import Business, Document, Transaction
from app.schemas.document import DocumentOut, InvoiceConfirm, InvoiceExtraction

router = APIRouter(prefix="/api", tags=["invoices"])

ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff"}


def _get_biz(db: Session) -> Business:
    biz = db.query(Business).first()
    if not biz:
        raise HTTPException(404, "No business configured.")
    return biz


@router.post("/invoices/upload", response_model=DocumentOut, status_code=201)
async def upload_invoice(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> DocumentOut:
    biz = _get_biz(db)

    # Validate extension
    ext = Path(file.filename or "").suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"Unsupported file type '{ext}'. Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}")

    # Read and check size
    content = await file.read()
    if len(content) > MAX_UPLOAD_MB * 1024 * 1024:
        raise HTTPException(400, f"File exceeds {MAX_UPLOAD_MB} MB limit.")

    # Save to disk
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    stored_name = f"{uuid.uuid4().hex}{ext}"
    file_path = UPLOAD_DIR / stored_name
    file_path.write_bytes(content)

    file_type = "pdf" if ext == ".pdf" else "image"

    # Run extraction pipeline
    try:
        from app.extraction import extract_invoice
        extraction: InvoiceExtraction = extract_invoice(file_path, file_type)
    except Exception as exc:
        extraction = InvoiceExtraction(
            verification_flags=[f"Extraction failed: {exc}"],
        )

    doc = Document(
        business_id=biz.id,
        filename=stored_name,
        original_name=file.filename or "unknown",
        file_type=file_type,
        extracted_data=extraction.model_dump(),
        status="pending",
        upload_source=extraction.upload_source,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return DocumentOut.model_validate(doc)


@router.get("/invoices", response_model=list[DocumentOut])
def list_invoices(db: Session = Depends(get_db)) -> list[DocumentOut]:
    biz = _get_biz(db)
    docs = (
        db.query(Document)
        .filter(Document.business_id == biz.id)
        .order_by(Document.created_at.desc())
        .all()
    )
    return [DocumentOut.model_validate(d) for d in docs]


@router.get("/invoices/{doc_id}", response_model=DocumentOut)
def get_invoice(doc_id: int, db: Session = Depends(get_db)) -> DocumentOut:
    biz = _get_biz(db)
    doc = (
        db.query(Document)
        .filter(Document.id == doc_id, Document.business_id == biz.id)
        .first()
    )
    if not doc:
        raise HTTPException(404, "Invoice not found")
    return DocumentOut.model_validate(doc)


@router.post("/invoices/{doc_id}/confirm", response_model=DocumentOut)
def confirm_invoice(
    doc_id: int,
    body: InvoiceConfirm,
    db: Session = Depends(get_db),
) -> DocumentOut:
    """User corrected fields → save as transaction(s) and mark confirmed."""
    biz = _get_biz(db)
    doc = (
        db.query(Document)
        .filter(Document.id == doc_id, Document.business_id == biz.id)
        .first()
    )
    if not doc:
        raise HTTPException(404, "Invoice not found")
    if doc.status == "confirmed":
        raise HTTPException(400, "Invoice already confirmed")

    # Create transaction from confirmed data
    txn = Transaction(
        business_id=biz.id,
        date=_dt.date.fromisoformat(body.date),
        type="expense",
        category=body.category,
        amount=body.total,
        tax_amount=body.tax_amount,
        description=f"Invoice from {body.vendor}" if body.vendor else "Invoice",
        vendor=body.vendor,
        source="invoice",
    )
    db.add(txn)

    doc.status = "confirmed"
    doc.is_verified = True
    doc.extracted_data = body.model_dump()
    db.commit()
    db.refresh(doc)
    return DocumentOut.model_validate(doc)


@router.delete("/invoices/{doc_id}", status_code=204)
def reject_invoice(doc_id: int, db: Session = Depends(get_db)) -> None:
    biz = _get_biz(db)
    doc = (
        db.query(Document)
        .filter(Document.id == doc_id, Document.business_id == biz.id)
        .first()
    )
    if not doc:
        raise HTTPException(404, "Invoice not found")
    doc.status = "rejected"
    db.commit()
