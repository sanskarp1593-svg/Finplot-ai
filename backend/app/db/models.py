"""SQLAlchemy ORM models for FinPilot."""

from __future__ import annotations

import datetime as _dt

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    """Shared declarative base for all models."""


# ── Business ─────────────────────────────────────────────────────────────────

class Business(Base):
    __tablename__ = "businesses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False, default="My Business")
    industry = Column(String(100), nullable=False, default="General")
    language = Column(String(5), nullable=False, default="en")  # "en" or "hi"
    created_at = Column(DateTime, default=_dt.datetime.utcnow)

    transactions = relationship("Transaction", back_populates="business", cascade="all, delete-orphan")
    budgets = relationship("Budget", back_populates="business", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="business", cascade="all, delete-orphan")
    queries = relationship("QueryHistory", back_populates="business", cascade="all, delete-orphan")


# ── Transaction ──────────────────────────────────────────────────────────────

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    date = Column(Date, nullable=False)
    type = Column(String(10), nullable=False)        # "revenue" | "expense"
    category = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)
    tax_amount = Column(Float, nullable=True, default=0.0)
    description = Column(Text, nullable=True, default="")
    vendor = Column(String(200), nullable=True, default="")
    source = Column(String(10), nullable=False, default="manual")  # manual | csv | invoice
    created_at = Column(DateTime, default=_dt.datetime.utcnow)

    business = relationship("Business", back_populates="transactions")


# ── Budget ───────────────────────────────────────────────────────────────────

class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    category = Column(String(100), nullable=False)
    monthly_limit = Column(Float, nullable=False)
    created_at = Column(DateTime, default=_dt.datetime.utcnow)

    business = relationship("Business", back_populates="budgets")


# ── Document (uploaded invoices) ─────────────────────────────────────────────

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    filename = Column(String(300), nullable=False)          # stored filename
    original_name = Column(String(300), nullable=False)     # user's filename
    file_type = Column(String(10), nullable=False)          # pdf | image
    extracted_data = Column(JSON, nullable=True)            # parsed invoice fields
    status = Column(String(12), nullable=False, default="pending")  # pending | confirmed | rejected
    upload_source = Column(String(15), nullable=True)       # print | handwriting
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=_dt.datetime.utcnow)

    business = relationship("Business", back_populates="documents")


# ── Query History ────────────────────────────────────────────────────────────

class QueryHistory(Base):
    __tablename__ = "query_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    agents_used = Column(JSON, nullable=True)               # ["router", "metric", …]
    language = Column(String(5), nullable=False, default="en")
    created_at = Column(DateTime, default=_dt.datetime.utcnow)

    business = relationship("Business", back_populates="queries")


# ── Knowledge Document ───────────────────────────────────────────────────────

class KnowledgeDoc(Base):
    __tablename__ = "knowledge_docs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(300), nullable=False)
    content = Column(Text, nullable=False)
    source_file = Column(String(300), nullable=True)
    created_at = Column(DateTime, default=_dt.datetime.utcnow)
