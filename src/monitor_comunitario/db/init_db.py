from monitor_comunitario.core.config import get_settings
from monitor_comunitario.db.models import Base
from monitor_comunitario.db.session import engine

settings = get_settings()


def init_db() -> None:
    """Create database tables only for local SQLite development.

    Production-like databases should be managed with Alembic migrations:

        uv run monitor-comunitario db-upgrade
    """
    if settings.database_url.startswith("sqlite"):
        Base.metadata.create_all(bind=engine)
