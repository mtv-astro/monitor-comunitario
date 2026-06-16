from monitor_comunitario.scraper.celesc_page import (
    MunicipalityOption,
    build_safe_snapshot_slug,
    is_placeholder_municipality_option,
)


def test_build_safe_snapshot_slug_removes_accents_and_symbols() -> None:
    assert build_safe_snapshot_slug("Florianópolis / Centro") == "florianopolis-centro"


def test_is_placeholder_municipality_option_detects_placeholder() -> None:
    option = MunicipalityOption(label="Selecione o município", value="0")

    assert is_placeholder_municipality_option(option) is True


def test_is_placeholder_municipality_option_accepts_real_city() -> None:
    option = MunicipalityOption(label="Florianópolis", value="4205407")

    assert is_placeholder_municipality_option(option) is False
