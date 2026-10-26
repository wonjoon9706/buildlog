from app.db.session import normalize_database_url


def test_supabase_postgresql_url_uses_psycopg_driver() -> None:
    database_url = "postgresql://user:password@example.supabase.co:5432/postgres"

    assert normalize_database_url(database_url) == (
        "postgresql+psycopg://user:password@example.supabase.co:5432/postgres"
    )


def test_sqlite_url_is_not_changed() -> None:
    database_url = "sqlite+pysqlite:///:memory:"

    assert normalize_database_url(database_url) == database_url
