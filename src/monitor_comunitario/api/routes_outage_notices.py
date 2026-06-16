from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from monitor_comunitario.db.models import OutageNotice
from monitor_comunitario.db.session import get_session
from monitor_comunitario.schemas.outage_notices import OutageNoticeRead

router = APIRouter(prefix="/outage-notices", tags=["outage-notices"])

SessionDep = Annotated[Session, Depends(get_session)]


@router.get("", response_model=list[OutageNoticeRead])
def list_outage_notices(
    session: SessionDep,
    municipality: str | None = None,
    limit: int = 50,
) -> list[OutageNotice]:
    """List persisted Celesc outage notices."""
    query = select(OutageNotice).order_by(OutageNotice.created_at.desc()).limit(limit)

    if municipality:
        query = query.where(OutageNotice.municipality == municipality)

    return list(session.scalars(query).all())
