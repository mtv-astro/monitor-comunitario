from monitor_comunitario.cli import mask_database_url


def test_mask_database_url_keeps_sqlite_url() -> None:
    database_url = "sqlite:///./data/monitor_comunitario.db"

    assert mask_database_url(database_url) == database_url


def test_mask_database_url_masks_postgres_password() -> None:
    database_url = "postgresql://user:secret-password@example.supabase.co:5432/postgres"

    masked = mask_database_url(database_url)

    assert masked == "postgresql://user:***@example.supabase.co:5432/postgres"
    assert "secret-password" not in masked


def test_mask_database_url_masks_query_urls() -> None:
    database_url = "postgresql+psycopg://admin:secret@db.example.com/app?sslmode=require"

    masked = mask_database_url(database_url)

    assert masked == "postgresql+psycopg://admin:***@db.example.com/app?sslmode=require"
    assert "secret" not in masked


def test_mask_database_url_keeps_url_without_credentials() -> None:
    database_url = "postgresql://db.example.com:5432/app"

    assert mask_database_url(database_url) == database_url
