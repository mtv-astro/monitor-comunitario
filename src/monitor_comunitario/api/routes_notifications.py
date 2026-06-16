from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from monitor_comunitario.db.models import Notification, NotificationStatus, utc_now
from monitor_comunitario.db.session import get_session
from monitor_comunitario.schemas.notifications import NotificationRead

router = APIRouter(tags=["notifications"])

SessionDep = Annotated[Session, Depends(get_session)]


@router.get("/notifications", response_model=list[NotificationRead])
def list_notifications(
    session: SessionDep,
    user_id: int | None = None,
    unread_only: bool = False,
    limit: int = 50,
) -> list[Notification]:
    """List in-app notifications."""
    query = select(Notification).order_by(Notification.created_at.desc()).limit(limit)

    if user_id is not None:
        query = query.where(Notification.user_id == user_id)

    if unread_only:
        query = query.where(Notification.read_at.is_(None))

    return list(session.scalars(query).all())


@router.get("/users/{user_id}/notifications", response_model=list[NotificationRead])
def list_user_notifications(
    user_id: int,
    session: SessionDep,
    unread_only: bool = False,
    limit: int = 50,
) -> list[Notification]:
    """List notifications for one user."""
    return list_notifications(
        session=session,
        user_id=user_id,
        unread_only=unread_only,
        limit=limit,
    )


@router.patch("/notifications/{notification_id}/read", response_model=NotificationRead)
def mark_notification_as_read(
    notification_id: int,
    session: SessionDep,
) -> Notification:
    """Mark one notification as read."""
    notification = session.get(Notification, notification_id)

    if notification is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found.",
        )

    notification.status = NotificationStatus.READ.value
    notification.read_at = utc_now()

    session.add(notification)
    session.commit()
    session.refresh(notification)

    return notification
