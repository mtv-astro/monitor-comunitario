from pathlib import Path

from alembic import command
from alembic.config import Config

from monitor_comunitario.core.config import get_settings


def get_project_root() -> Path:
    """Return the repository root from inside the installed package."""
    return Path(__file__).resolve().parents[3]


def get_alembic_config() -> Config:
    """Build an Alembic config using the current application settings."""
    project_root = get_project_root()
    settings = get_settings()

    config = Config(str(project_root / "alembic.ini"))
    config.set_main_option("script_location", str(project_root / "migrations"))
    config.set_main_option("sqlalchemy.url", settings.database_url.replace("%", "%%"))

    return config


def upgrade_database(revision: str = "head") -> None:
    """Apply database migrations up to the requested revision."""
    command.upgrade(get_alembic_config(), revision)


def downgrade_database(revision: str = "-1") -> None:
    """Downgrade database migrations."""
    command.downgrade(get_alembic_config(), revision)


def stamp_database(revision: str = "head") -> None:
    """Mark the database as being at a revision without running migrations."""
    command.stamp(get_alembic_config(), revision)


def show_current_revision() -> None:
    """Print the current database revision."""
    command.current(get_alembic_config(), verbose=True)


def show_migration_history() -> None:
    """Print Alembic migration history."""
    command.history(get_alembic_config(), verbose=True)


def create_revision(message: str, autogenerate: bool = False) -> None:
    """Create a new Alembic revision."""
    command.revision(
        get_alembic_config(),
        message=message,
        autogenerate=autogenerate,
    )
