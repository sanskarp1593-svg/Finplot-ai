"""AI Assistant – run agent workflow, return answer + traces."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.engine import get_db
from app.db.models import Business, QueryHistory
from app.schemas.query import QueryHistoryOut, QueryRequest, QueryResponse

router = APIRouter(prefix="/api", tags=["assistant"])


def _get_biz(db: Session) -> Business:
    biz = db.query(Business).first()
    if not biz:
        raise HTTPException(404, "No business configured.")
    return biz


@router.post("/assistant/query", response_model=QueryResponse)
def run_query(
    body: QueryRequest,
    db: Session = Depends(get_db),
) -> QueryResponse:
    biz = _get_biz(db)

    from app.agents.graph import run_agent_workflow

    result: QueryResponse = run_agent_workflow(
        question=body.question,
        language=body.language or biz.language,
        business_id=biz.id,
        db=db,
    )

    # Persist to history
    qh = QueryHistory(
        business_id=biz.id,
        question=body.question,
        answer=result.answer,
        agents_used=result.agents_used,
        language=result.language,
    )
    db.add(qh)
    db.commit()

    return result


@router.get("/assistant/history", response_model=list[QueryHistoryOut])
def query_history(db: Session = Depends(get_db)) -> list[QueryHistoryOut]:
    biz = _get_biz(db)
    rows = (
        db.query(QueryHistory)
        .filter(QueryHistory.business_id == biz.id)
        .order_by(QueryHistory.created_at.desc())
        .limit(100)
        .all()
    )
    return [QueryHistoryOut.model_validate(r) for r in rows]
