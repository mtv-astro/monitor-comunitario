from monitor_comunitario.scraper.parser import (
    clean_page_text,
    extract_relevant_outage_section,
    parse_outage_notices_from_text,
)


def test_clean_page_text_removes_empty_noise_and_adjacent_duplicates() -> None:
    raw_text = """
    Estou ciente

    Avisos de Desligamentos
    Avisos de Desligamentos
    Sem Iframes
    IMPORTANTE: Somente são listados os municípios que possuem desligamentos agendados.
    """

    assert clean_page_text(raw_text) == (
        "Avisos de Desligamentos\n"
        "IMPORTANTE: Somente são listados os municípios que possuem desligamentos agendados."
    )


def test_extract_relevant_outage_section_stops_before_footer() -> None:
    raw_text = """
    Menu
    Avisos de Desligamentos
    O que é um desligamento programado?
    IMPORTANTE: Somente são listados os municípios que possuem desligamentos agendados.
    AJUDA
    Atendimento online
    """

    section = extract_relevant_outage_section(raw_text)

    assert section.startswith("Avisos de Desligamentos")
    assert "IMPORTANTE" in section
    assert "Atendimento online" not in section


def test_parse_outage_notices_returns_empty_when_only_institutional_text_exists() -> None:
    text = """
    Avisos de Desligamentos
    O que é um desligamento programado?
    São interrupções realizadas, de forma programada.
    IMPORTANTE: Somente são listados os municípios que possuem desligamentos agendados.
    """

    assert parse_outage_notices_from_text(text) == []


def test_parse_outage_notices_extracts_simple_notice_block() -> None:
    text = """
    Avisos de Desligamentos
    FLORIANÓPOLIS
    Data: 20/06/2026
    Horário: 08:00 às 12:00
    Bairro: Campeche
    Rua: Avenida Pequeno Príncipe
    Motivo: Manutenção preventiva na rede elétrica.
    AJUDA
    Atendimento online
    """

    notices = parse_outage_notices_from_text(text)

    assert len(notices) == 1

    notice = notices[0]

    assert notice.municipality == "FLORIANÓPOLIS"
    assert notice.neighborhood == "Campeche"
    assert notice.street == "Avenida Pequeno Príncipe"
    assert notice.description == "Manutenção preventiva na rede elétrica."
    assert "Horário" in notice.raw_text
