from hashlib import sha256

from sqlalchemy import select
from sqlalchemy.orm import Session

from monitor_comunitario.db.models import OutageNotice
from monitor_comunitario.scraper.parser import ParsedOutageNotice


def build_notice_content_hash(notice: ParsedOutageNotice, source_url: str) -> str:
    """Build a stable hash to deduplicate outage notices."""
    hash_input = "|".join(
        [
            source_url.strip(),
            notice.municipality.strip().casefold(),
            notice.neighborhood.strip().casefold(),
            notice.street.strip().casefold(),
            notice.description.strip().casefold(),
            notice.raw_text.strip().casefold(),
        ]
    )

    return sha256(hash_input.encode("utf-8")).hexdigest()


def get_notice_by_hash(session: Session, content_hash: str) -> OutageNotice | None:
    """Return an existing notice by hash, if present."""
    statement = select(OutageNotice).where(OutageNotice.content_hash == content_hash)
    return session.scalar(statement)


def persist_parsed_notice(
    session: Session,
    parsed_notice: ParsedOutageNotice,
    source_url: str,
) -> tuple[OutageNotice, bool]:
    """Persist one parsed notice.

    Returns a tuple `(notice, created)` where `created` is false when an
    identical notice already exists.
    """
    content_hash = build_notice_content_hash(parsed_notice, source_url)
    existing = get_notice_by_hash(session, content_hash)

    if existing is not None:
        return existing, False

    notice = OutageNotice(
        source="celesc",
        source_url=source_url,
        municipality=parsed_notice.municipality,
        neighborhood=parsed_notice.neighborhood,
        street=parsed_notice.street,
        description=parsed_notice.description,
        raw_text=parsed_notice.raw_text,
        content_hash=content_hash,
    )

    session.add(notice)
    session.commit()
    session.refresh(notice)

    return notice, True


def persist_parsed_notices(
    session: Session,
    parsed_notices: list[ParsedOutageNotice],
    source_url: str,
) -> tuple[list[OutageNotice], int]:
    """Persist parsed notices and return all records plus created count."""
    notices: list[OutageNotice] = []
    created_count = 0

    for parsed_notice in parsed_notices:
        notice, created = persist_parsed_notice(
            session=session,
            parsed_notice=parsed_notice,
            source_url=source_url,
        )
        notices.append(notice)

        if created:
            created_count += 1

    return notices, created_count
