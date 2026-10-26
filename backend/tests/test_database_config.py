from sqlalchemy import text

from app.db.session import create_database_engine


def test_sqlite_engine_enables_foreign_keys() -> None:
    database_engine = create_database_engine("sqlite+pysqlite:///:memory:")

    with database_engine.connect() as connection:
        foreign_keys_enabled = connection.scalar(text("PRAGMA foreign_keys"))

    assert database_engine.dialect.name == "sqlite"
    assert foreign_keys_enabled == 1
