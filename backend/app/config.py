"""Application configuration – loaded once at import time."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# ── locate .env relative to *this* file (backend/app/config.py → backend/.env)
_BACKEND_DIR = Path(__file__).resolve().parent.parent
_ENV_PATH = _BACKEND_DIR / ".env"
load_dotenv(_ENV_PATH)

# ── paths ────────────────────────────────────────────────────────────────────
PROJECT_ROOT = _BACKEND_DIR.parent
DATA_DIR = PROJECT_ROOT / "data"
KNOWLEDGE_DIR = DATA_DIR / "knowledge"
CHROMA_DIR = DATA_DIR / "chroma"
UPLOAD_DIR = DATA_DIR / "uploads"

# ── database ─────────────────────────────────────────────────────────────────
_db_env = os.getenv("DATABASE_URL", "").strip()
if _db_env:
    if _db_env.startswith("sqlite:///") and not _db_env.startswith("sqlite:////") and ":memory:" not in _db_env:
        rel_path = _db_env[len("sqlite:///"):]
        abs_db_path = (PROJECT_ROOT / rel_path).resolve()
        abs_db_path.parent.mkdir(parents=True, exist_ok=True)
        DATABASE_URL = f"sqlite:///{abs_db_path.as_posix()}"
    else:
        DATABASE_URL = _db_env
else:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DATABASE_URL = f"sqlite:///{(DATA_DIR / 'finpilot.db').as_posix()}"

# ── OpenAI (optional) ────────────────────────────────────────────────────────
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
LLM_TIMEOUT_SECONDS: int = int(os.getenv("LLM_TIMEOUT_SECONDS", "20"))
FORCE_FALLBACK_ROUTER: bool = os.getenv("FORCE_FALLBACK_ROUTER", "false").lower() in (
    "true",
    "1",
    "yes",
)

# ── Gemini (optional – handwriting) ──────────────────────────────────────────
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-flash-latest")

# ── CORS ─────────────────────────────────────────────────────────────────────
CORS_ORIGINS: list[str] = [
    o.strip()
    for o in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
    if o.strip()
]

# ── uploads ──────────────────────────────────────────────────────────────────
MAX_UPLOAD_MB: int = int(os.getenv("MAX_UPLOAD_MB", "5"))

# ── RAG ──────────────────────────────────────────────────────────────────────
RAG_TOP_K: int = int(os.getenv("RAG_TOP_K", "3"))
RAG_MIN_SIMILARITY: float = float(os.getenv("RAG_MIN_SIMILARITY", "0.45"))

# ── Tesseract OCR ────────────────────────────────────────────────────────────
TESSERACT_CMD: str = os.getenv(
    "TESSERACT_CMD",
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
)

# ── derived flags ────────────────────────────────────────────────────────────
USE_LLM: bool = bool(OPENAI_API_KEY) and not FORCE_FALLBACK_ROUTER
USE_GEMINI: bool = bool(GEMINI_API_KEY)
