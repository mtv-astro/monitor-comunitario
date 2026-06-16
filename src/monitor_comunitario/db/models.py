from datetime import datetime
from enum import StrEnum

from sqlalchemy import Boolean, DateTime, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class NotificationStatus(StrEnum):
    CREATED = "created"
    READ = "read"
    DISMISSED = "dismissed"
    FAILED = "failed"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(160))
    phone: Mapped[str] = mapped_column(String(40))
    municipality: Mapped[str] = mapped_column(String(120))
    neighborhood: Mapped[str] = mapped_column(String(160), default="")
    street: Mapped[str] = mapped_column(String(200), default="")
    number: Mapped[str] = mapped_column(String(40), default="")
    zipcode: Mapped[str] = mapped_column(String(20), default="")
    accept_municipality_wide_alerts: Mapped[bool] = mapped_column(Boolean, default=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class OutageNotice(Base):
    __tablename__ = "outage_notices"

    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[str] = mapped_column(String(80), default="celesc")
    source_url: Mapped[str] = mapped_column(String(500))
    municipality: Mapped[str] = mapped_column(String(120), index=True)
    neighborhood: Mapped[str] = mapped_column(String(160), default="")
    street: Mapped[str] = mapped_column(String(200), default="")
    description: Mapped[str] = mapped_column(Text, default="")
    raw_text: Mapped[str] = mapped_column(Text, default="")
    content_hash: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
