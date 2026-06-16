from monitor_comunitario.db.models import Base
from monitor_comunitario.db.session import engine


def init_db() -> None:
    """Create database tables for local development.

    Alembic migrations will be added as the project matures. For the first
    functional slice, creating tables on startup keeps local setup simple.
    """
    Base.metadata.create_all(bind=engine)
