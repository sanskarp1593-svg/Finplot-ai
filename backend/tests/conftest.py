"""Test configuration and shared fixtures."""

import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ensure backend directory is on sys.path
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.config import DATA_DIR
from app.db.engine import get_db
from app.db.models import Base
from app.db.seed import seed
from app.main import app
from app.rag.ingest import ingest

# Use a test SQLite database inside DATA_DIR
DATA_DIR.mkdir(parents=True, exist_ok=True)
test_db_file = DATA_DIR / "test_finpilot.db"
TEST_DB_URL = f"sqlite:///{test_db_file.as_posix()}"
test_engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_data():
    """Seed the database and ingest knowledge docs once per test session."""
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    
    # Ingest RAG knowledge docs
    ingest()
    
    # Run database seed
    seed(target_engine=test_engine, target_session=TestingSessionLocal)
    
    yield
    
    # Clean up test database file if desired
    if test_db_file.exists():
        try:
            test_db_file.unlink()
        except Exception:
            pass



@pytest.fixture
def db_session():
    """Provide a transactional DB session for testing."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db_session):
    """Provide a FastAPI TestClient with overridden get_db."""
    def _override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
