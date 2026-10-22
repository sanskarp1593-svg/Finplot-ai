"""FinPilot API – FastAPI application entry point."""

from __future__ import annotations

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import CORS_ORIGINS, DATA_DIR, UPLOAD_DIR
from app.db.engine import engine
from app.db.models import Base
from app.routes import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown events."""
    # Create tables on startup
    Base.metadata.create_all(bind=engine)
    # Ensure data directories exist
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    yield


app = FastAPI(title="FinPilot API", lifespan=lifespan)

allowed_origins = {
    "http://localhost:5173",
    "http://localhost:3000",
    *CORS_ORIGINS,
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=sorted(allowed_origins),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
