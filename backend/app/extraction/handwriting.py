"""Handwriting reading via Google Gemini – copy-only, no interpretation."""

from __future__ import annotations

import base64
import json
from pathlib import Path


def read_handwriting(file_path: Path) -> str:
    """Send image to Gemini to transcribe handwritten text.

    - Only called when Tesseract found no printed text.
    - Prompt instructs Gemini to copy text exactly, no filling in.
    - Returns empty string if Gemini unavailable or fails.
    """
    from app.config import GEMINI_API_KEY, GEMINI_MODEL, USE_GEMINI

    if not USE_GEMINI:
        return ""

    try:
        import httpx

        # Read and base64 encode the image
        image_bytes = file_path.read_bytes()
        b64 = base64.b64encode(image_bytes).decode("utf-8")

        ext = file_path.suffix.lower()
        mime_types = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".webp": "image/webp",
            ".bmp": "image/bmp",
            ".tiff": "image/tiff",
            ".pdf": "application/pdf",
        }
        mime = mime_types.get(ext, "image/jpeg")

        prompt = (
            "This is a photo of a handwritten bill or note. "
            "Copy the text EXACTLY as written. Do not calculate, fill in, "
            "or change anything. If something is unreadable, write [unreadable]. "
            "Output only the transcribed text, nothing else."
        )

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": mime,
                                "data": b64,
                            }
                        },
                    ]
                }
            ]
        }

        resp = httpx.post(url, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        # Extract text from response
        candidates = data.get("candidates", [])
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            return "".join(p.get("text", "") for p in parts).strip()
        return ""

    except Exception:
        return ""
