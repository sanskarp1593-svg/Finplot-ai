"""Knowledge base listing."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.engine import get_db
from app.db.models import KnowledgeDoc

router = APIRouter(prefix="/api", tags=["knowledge"])


@router.get("/knowledge")
def list_knowledge(db: Session = Depends(get_db)) -> list[dict]:
    docs = db.query(KnowledgeDoc).order_by(KnowledgeDoc.title).all()
    return [
        {
            "id": d.id,
            "title": d.title,
            "content": d.content,
            "source_file": d.source_file,
            "created_at": d.created_at.isoformat() if d.created_at else None,
        }
        for d in docs
    ]
