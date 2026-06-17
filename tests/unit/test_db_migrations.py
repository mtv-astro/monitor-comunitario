from pathlib import Path

from monitor_comunitario.db.migrations import get_alembic_config, get_project_root


def test_project_root_contains_alembic_ini() -> None:
    project_root = get_project_root()

    assert (project_root / "alembic.ini").exists()


def test_alembic_config_points_to_migrations() -> None:
    config = get_alembic_config()
    script_location = config.get_main_option("script_location")

    assert script_location is not None
    assert Path(script_location).name == "migrations"
