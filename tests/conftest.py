import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

os.environ["DATABASE_URL"] = "postgresql://postgres:postgres@localhost:5432/test_db"

from app.database import get_db  # noqa: E402
from app.main import app  # noqa: E402

SQLITE_URL = "sqlite://"


@pytest.fixture(name="session")
def session_fixture() -> Generator[Session]:
    """Session SQLite in-memory pour les tests."""
    test_engine = create_engine(
        SQLITE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        yield session
    SQLModel.metadata.drop_all(test_engine)


@pytest.fixture(name="client")
def client_fixture(session: Session) -> Generator[TestClient]:
    def get_db_override() -> Generator[Session]:
        yield session

    app.dependency_overrides[get_db] = get_db_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
