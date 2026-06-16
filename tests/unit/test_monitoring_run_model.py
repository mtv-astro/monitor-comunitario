from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from monitor_comunitario.db.models import Base, MonitoringRun, MonitoringRunStatus


def test_monitoring_run_model_persists_metrics() -> None:
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    testing_session_local = sessionmaker(bind=engine, expire_on_commit=False)

    Base.metadata.create_all(bind=engine)

    with testing_session_local() as session:
        run = MonitoringRun(
            status=MonitoringRunStatus.SUCCESS.value,
            municipalities_found=168,
            municipalities_captured=2,
            notices_found=2,
            notices_persisted=2,
            notices_created=1,
            users_checked=3,
            matches_created=2,
            notifications_created=2,
            raw_snapshot_path="snapshots/example.json",
        )

        session.add(run)
        session.commit()
        session.refresh(run)

        assert run.id >= 1
        assert run.status == "success"
        assert run.municipalities_found == 168
        assert run.notifications_created == 2
        assert run.raw_snapshot_path == "snapshots/example.json"
