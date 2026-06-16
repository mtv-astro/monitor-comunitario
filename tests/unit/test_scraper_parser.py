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
    Ajuda
    Atendimento online
    """

    section = extract_relevant_outage_section(raw_text)

    assert section.startswith("Avisos de Desligamentos")
    assert "IMPORTANTE" in section
    assert "Atendimento online" not in section


def test_parse_outage_notices_is_conservative_until_snapshots_define_blocks() -> None:
    assert parse_outage_notices_from_text("Avisos de Desligamentos") == []
