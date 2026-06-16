from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from monitor_comunitario.db.models import MonitoringRun
from monitor_comunitario.db.session import get_session
from monitor_comunitario.schemas.monitoring_runs import MonitoringRunRead
from monitor_comunitario.services.monitoring import run_monitoring_cycle

router = APIRouter(prefix="/admin", tags=["admin"])

SessionDep = Annotated[Session, Depends(get_session)]


@router.get("/runs", response_model=list[MonitoringRunRead])
def list_monitoring_runs(
    session: SessionDep,
    limit: int = 50,
) -> list[MonitoringRun]:
    """List monitoring run history."""
    query = select(MonitoringRun).order_by(MonitoringRun.started_at.desc()).limit(limit)
    return list(session.scalars(query).all())


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
