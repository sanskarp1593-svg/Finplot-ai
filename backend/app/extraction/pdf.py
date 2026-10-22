"""PDF text and table extraction using pdfplumber."""

from __future__ import annotations

from pathlib import Path


def extract_pdf_text(file_path: Path) -> str:
    """Extract text from all pages of a PDF using pdfplumber.

    Returns concatenated text from all pages. Falls back to empty string
    if pdfplumber can't read the file.
    """
    try:
        import pdfplumber
    except ImportError:
        return ""

    lines: list[str] = []
    try:
        with pdfplumber.open(str(file_path)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                lines.append(page_text)

                # Also try to extract tables for structured data
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        if row:
                            cells = [str(c).strip() for c in row if c]
                            if cells:
                                lines.append(" | ".join(cells))
    except Exception:
        pass

    return "\n".join(lines)
