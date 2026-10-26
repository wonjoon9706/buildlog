from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from app.core.config import get_settings


def normalize_database_url(database_url: str) -> str:
    if database_url.startswith("postgresql://"):
        return database_url.replace("postgresql://", "postgresql+psycopg://", 1)

    return database_url


def create_database_engine(database_url: str) -> Engine:
    normalized_url = normalize_database_url(database_url)
    connect_args = (
        {"check_same_thread": False} if normalized_url.startswith("sqlite") else {}
    )
    return create_engine(normalized_url, connect_args=connect_args, pool_pre_ping=True)


engine = create_database_engine(get_settings().database_url)
