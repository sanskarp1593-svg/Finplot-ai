"""Invoice extraction pipeline – orchestrates PDF, OCR, and handwriting."""

from __future__ import annotations

from pathlib import Path

from app.schemas.document import InvoiceExtraction


def extract_invoice(file_path: Path, file_type: str) -> InvoiceExtraction:
    """Run the full extraction pipeline on an uploaded file.

    1. If PDF → extract text with pdfplumber
    2. If image or PDF with no text → try Tesseract OCR
    3. If OCR finds nothing → try Gemini handwriting (if available)
    4. Parse extracted text into structured invoice fields
    5. Validate arithmetic consistency
    """
    text = ""
    upload_source = "print"

    if file_type == "pdf":
        from app.extraction.pdf import extract_pdf_text
        text = extract_pdf_text(file_path)

    if not text.strip():
        # Try OCR (for images, or PDFs with no embedded text)
        from app.extraction.ocr import run_ocr
        text, ocr_ok = run_ocr(file_path)

        if not ocr_ok or not text.strip():
            # Try Gemini for handwriting
            from app.extraction.handwriting import read_handwriting
            hw_text = read_handwriting(file_path)
            if hw_text:
                text = hw_text
                upload_source = "handwriting"

    if not text.strip():
        return InvoiceExtraction(
            verification_flags=["Could not extract any text from the document."],
            upload_source=upload_source,
        )

    # Parse the extracted text
    from app.extraction.parser import parse_invoice_text
    extraction = parse_invoice_text(text)
    extraction.upload_source = upload_source

    # If handwriting, flag every field for verification
    if upload_source == "handwriting":
        extraction.verification_flags.append("Read by AI from handwriting")
        for item in extraction.items:
            item.verification = "Verification required"

    # Validate arithmetic
    from app.extraction.validator import validate_invoice
    extraction = validate_invoice(extraction)

    return extraction
