from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session

from .models import (
    User,
    OutageNotice,
    UserOutageMatch,
    Notification,
    MonitoringRun,
)
from .session import SessionLocal


def _serialize(model: Any) -> dict[str, Any]:
    """Serialize a SQLAlchemy model into a plain dictionary."""
    data: dict[str, Any] = {}
    for column in model.__table__.columns:  # type: ignore[attr-defined]
        value = getattr(model, column.name)
        if isinstance(value, datetime):
            data[column.name] = value.isoformat()
        else:
            data[column.name] = value
    return data


def export_data(output_path: str) -> None:
    """Export tables to a JSON file."""
    path = Path(output_path)
    with SessionLocal() as session:
        result = {
            "users": [_serialize(obj) for obj in session.query(User).all()],
            "outage_notices": [_serialize(obj) for obj in session.query(OutageNotice).all()],
            "user_outage_matches": [_serialize(obj) for obj in session.query(UserOutageMatch).all()],
            "notifications": [_serialize(obj) for obj in session.query(Notification).all()],
            "monitoring_runs": [_serialize(obj) for obj in session.query(MonitoringRun).all()],
        }
    with path.open("w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)


def import_data(input_path: str) -> None:
    """Import data from a previously exported JSON file.

    Existing rows with the same primary key will be merged.
    """
    path = Path(input_path)
    with path.open("r", encoding="utf-8") as f:
        payload = json.load(f)

    with SessionLocal() as session:
        for item in payload.get("users", []):
            obj = User(**{k: v for k, v in item.items()})  # type: ignore[arg-type]
            session.merge(obj)
        for item in payload.get("outage_notices", []):
            obj = OutageNotice(**{k: v for k, v in item.items()})  # type: ignore[arg-type]
            session.merge(obj)
        for item in payload.get("user_outage_matches", []):
            obj = UserOutageMatch(**{k: v for k, v in item.items()})  # type: ignore[arg-type]
            session.merge(obj)
        for item in payload.get("notifications", []):
            obj = Notification(**{k: v for k, v in item.items()})  # type: ignore[arg-type]
            session.merge(obj)
        for item in payload.get("monitoring_runs", []):
            obj = MonitoringRun(**{k: v for k, v in item.items()})  # type: ignore[arg-type]
            session.merge(obj)
        session.commit()


def seed_demo() -> None:
    """Seed the database with fake data for demonstration purposes.

    Generates users, outage notices, matches, notifications and a monitoring run.
    """
    from random import choice, randint

    # Some sample pools for fake data
    names = ["Ana", "Bruno", "Carlos", "Débora", "Eduardo", "Fernanda"]
    municipalities = ["Florianópolis", "São José", "Palhoça"]
    streets = ["Rua A", "Rua B", "Avenida Central", "Servidão Verde"]
    descriptions = [
        "Manutenção programada na rede elétrica.",
        "Melhoria na infraestrutura de distribuição.",
        "Substituição de transformador.",
    ]

    with SessionLocal() as session:
        users: list[User] = []
        for _ in range(3):
            user = User(
                name=choice(names),
                phone=f"+55{randint(1000000000, 9999999999)}",
                municipality=choice(municipalities),
                neighborhood="Centro",
                street=choice(streets),
                number=str(randint(1, 500)),
                zipcode="88000-000",
                accept_municipality_wide_alerts=True,
                is_active=True,
            )
            session.add(user)
            users.append(user)

        notices: list[OutageNotice] = []
        for i in range(2):
            notice = OutageNotice(
                source="celesc",
                source_url="https://www.celesc.com.br/avisos",
                municipality=choice(municipalities),
                neighborhood="Centro",
                street=choice(streets),
                description=choice(descriptions),
                raw_text="Texto do aviso.",
                content_hash=f"seed-{i}-{randint(1000,9999)}",
            )
            session.add(notice)
            notices.append(notice)

        session.commit()

        matches: list[UserOutageMatch] = []
        notifications_list: list[Notification] = []
        for user in users:
            for notice in notices:
                match = UserOutageMatch(
                    user_id=user.id,
                    outage_notice_id=notice.id,
                    match_level="municipality",
                    match_score=0.8,
                    match_reason="Seed demo",
                )
                session.add(match)
                matches.append(match)

                notification = Notification(
                    user_id=user.id,
                    outage_notice_id=notice.id,
                    channel="app",
                    status="created",
                    title="Aviso de desligamento",
                    message=notice.description,
                )
                session.add(notification)
                notifications_list.append(notification)

        # Create summary run
        run = MonitoringRun(
            status="success",
            municipalities_found=len(municipalities),
            municipalities_captured=len(notices),
            notices_found=len(notices),
            notices_persisted=len(notices),
            notices_created=len(notices),
            users_checked=len(users),
            matches_created=len(matches),
            notifications_created=len(notifications_list),
            error_message="",
            raw_snapshot_path="",
        )
        session.add(run)
        session.commit()
