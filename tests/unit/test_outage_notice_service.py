from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from monitor_comunitario.db.models import Base
from monitor_comunitario.scraper.parser import ParsedOutageNotice
from monitor_comunitario.services.outage_notices import (
    build_notice_content_hash,
    persist_parsed_notice,
)


def test_build_notice_content_hash_is_stable() -> None:
    notice = ParsedOutageNotice(
        municipality="Florianópolis",
        neighborhood="Campeche",
        street="Avenida Pequeno Príncipe",
        description="Manutenção preventiva.",
        raw_text="FLORIANÓPOLIS\nBairro: Campeche\nMotivo: Manutenção preventiva.",
    )

    first_hash = build_notice_content_hash(notice, "https://example.com")
    second_hash = build_notice_content_hash(notice, "https://example.com")

    assert first_hash == second_hash


def test_persist_parsed_notice_deduplicates_by_hash() -> None:
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    testing_session_local = sessionmaker(bind=engine, expire_on_commit=False)

    Base.metadata.create_all(bind=engine)

    parsed_notice = ParsedOutageNotice(
        municipality="Florianópolis",
        neighborhood="Campeche",
        street="Avenida Pequeno Príncipe",
        description="Manutenção preventiva.",
        raw_text="FLORIANÓPOLIS\nBairro: Campeche\nMotivo: Manutenção preventiva.",
    )

    with testing_session_local() as session:
        first_notice, first_created = persist_parsed_notice(
            session=session,
            parsed_notice=parsed_notice,
            source_url="https://example.com",
        )

        second_notice, second_created = persist_parsed_notice(
            session=session,
            parsed_notice=parsed_notice,
            source_url="https://example.com",
        )

    assert first_created is True
    assert second_created is False
    assert first_notice.id == second_notice.id
