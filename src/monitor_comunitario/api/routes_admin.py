from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from monitor_comunitario.api.security import require_admin_api_key
from monitor_comunitario.core.config import get_settings
from monitor_comunitario.db.models import MonitoringRun
from monitor_comunitario.db.session import get_session
from monitor_comunitario.schemas.diagnostics import (
    DatabaseDiagnostics,
    DiagnosticsRead,
    NotificationDiagnostics,
    SchedulerDiagnostics,
)
from monitor_comunitario.schemas.monitoring_runs import MonitoringRunRead
from monitor_comunitario.services.monitoring import run_monitoring_cycle

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(require_admin_api_key)],
)

SessionDep = Annotated[Session, Depends(get_session)]


def _get_latest_monitoring_run(session: Session) -> MonitoringRun | None:
    """Return the most recent monitoring run, if one exists."""
    query = select(MonitoringRun).order_by(
        MonitoringRun.started_at.desc(),
        MonitoringRun.id.desc(),
    )
    return session.scalar(query)


@router.get("/diagnostics", response_model=DiagnosticsRead)
def get_admin_diagnostics(session: SessionDep) -> DiagnosticsRead:
    """Return frontend-friendly operational diagnostics for admin usage."""
    settings = get_settings()
    latest_run = _get_latest_monitoring_run(session)

    return DiagnosticsRead(
        status="ok",
        environment=settings.app_env,
        timezone=settings.app_timezone,
        database=DatabaseDiagnostics(status="ok"),
        scheduler=SchedulerDiagnostics(
            enabled=settings.scheduler_enabled,
            hour=settings.scheduler_hour,
            minute=settings.scheduler_minute,
        ),
        notifications=NotificationDiagnostics(
            provider=settings.notification_provider,
            evolution_enabled=settings.evolution_enabled,
        ),
        latest_run=MonitoringRunRead.model_validate(latest_run) if latest_run else None,
    )


@router.get("/runs", response_model=list[MonitoringRunRead])
def list_monitoring_runs(
    session: SessionDep,
    limit: int = 50,
) -> list[MonitoringRun]:
    """List monitoring run history."""
    query = select(MonitoringRun).order_by(MonitoringRun.started_at.desc()).limit(limit)
    return list(session.scalars(query).all())


@router.get("/runs/latest", response_model=MonitoringRunRead | None)
def get_latest_monitoring_run(session: SessionDep) -> MonitoringRun | None:
    """Return the latest monitoring run, if one exists."""
    return _get_latest_monitoring_run(session)


@router.get("/runs/{run_id}", response_model=MonitoringRunRead)
def get_monitoring_run(
    run_id: int,
    session: SessionDep,
) -> MonitoringRun:
    """Return one monitoring run."""
    run = session.get(MonitoringRun, run_id)

    if run is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Monitoring run not found.",
        )

    return run


@router.post("/runs/manual", response_model=MonitoringRunRead)
def trigger_manual_monitoring_run(
    limit: int = 0,
) -> MonitoringRun:
    """Run monitoring manually.

    This is synchronous for the MVP. In production, this can be moved to a
    background queue if the full scrape becomes slow.
    """
    max_options = limit if limit > 0 else None
    result = run_monitoring_cycle(limit=max_options)
    return result.run
