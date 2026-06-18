from monitor_comunitario.scraper.parser import parse_outage_notices_from_text


def test_parser_prefers_explicit_municipality_from_notice_text() -> None:
    notices = parse_outage_notices_from_text(
        """
XAVANTINA
Munic?pio de - SAO JOSE
As informa??es abaixo refletem a situa??o da programa??o at? data e hora.
Bairro: AREIAS BARREIROS-SJ
Data: 20/06/2026
Hor?rio: 08:00 ?s 12:00
""",
        fallback_municipality="XAVANTINA",
    )

    assert len(notices) == 1
    assert notices[0].municipality == "SAO JOSE"
    assert notices[0].neighborhood == "AREIAS BARREIROS-SJ"


def test_parser_uses_fallback_municipality_without_explicit_notice_municipality() -> None:
    notices = parse_outage_notices_from_text(
        """
Bairro: CENTRO
Data: 20/06/2026
Hor?rio: 08:00 ?s 12:00
Descri??o: Manuten??o programada.
""",
        fallback_municipality="FLORIANOPOLIS",
    )

    assert len(notices) == 1
    assert notices[0].municipality == "FLORIANOPOLIS"
    assert notices[0].neighborhood == "CENTRO"
