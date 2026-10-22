"""OCR using Tesseract via pytesseract."""

from __future__ import annotations

from pathlib import Path


def run_ocr(file_path: Path) -> tuple[str, bool]:
    """Run Tesseract OCR on an image or PDF page.

    Returns (extracted_text, success_bool).
    """
    try:
        import pytesseract
        from PIL import Image
        from app.config import TESSERACT_CMD

        # Point pytesseract at the installed binary
        if Path(TESSERACT_CMD).exists():
            pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

        ext = file_path.suffix.lower()

        if ext == ".pdf":
            # For PDF, try converting first page to image
            try:
                import pdfplumber
                with pdfplumber.open(str(file_path)) as pdf:
                    if pdf.pages:
                        page = pdf.pages[0]
                        img = page.to_image(resolution=300).original
                        text = pytesseract.image_to_string(img, lang="eng")
                        return text.strip(), bool(text.strip())
            except Exception:
                pass
            return "", False

        # For images
        img = Image.open(str(file_path))
        text = pytesseract.image_to_string(img, lang="eng")
        return text.strip(), bool(text.strip())

    except ImportError:
        return "", False
    except Exception as exc:
        # Tesseract not installed or other error
        if "tesseract is not installed" in str(exc).lower() or "ocr" in str(exc).lower():
            return "", False
        return "", False
