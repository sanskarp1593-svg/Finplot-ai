"""Pydantic schemas for business settings."""

from __future__ import annotations

import datetime as _dt

from pydantic import BaseModel, Field


class BusinessSettings(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    industry: str = Field("General", max_length=100)
    language: str = Field("en", pattern="^(en|hi)$")


class BusinessOut(BaseModel):
    id: int
    name: str
    industry: str
    language: str
    created_at: _dt.datetime

    model_config = {"from_attributes": True}
