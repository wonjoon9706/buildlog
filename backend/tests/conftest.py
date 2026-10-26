import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

os.environ["APP_ENV"] = "test"
os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"

from app.db.base import Base
from app.db.session import create_database_engine, get_db
from app.main import app
from app.models import AuthSession, ErrorLog, StudyLog, Todo, User  # noqa: F401

test_engine = create_database_engine(
    "sqlite+pysqlite:///:memory:",
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    expire_on_commit=False,
)


@pytest.fixture
def db_session() -> Generator[Session]:
    Base.metadata.create_all(bind=test_engine)
    with TestingSessionLocal() as session:
        yield session
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client(db_session: Session) -> Generator[TestClient]:
    def override_get_db() -> Generator[Session]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
