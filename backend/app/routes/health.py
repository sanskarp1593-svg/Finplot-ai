"""Health check endpoint."""

from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health")
def health() -> dict[str, str]:
    from app.config import USE_GEMINI
    return {"status": "ok", "gemini": "on" if USE_GEMINI else "off"}
