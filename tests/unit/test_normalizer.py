from monitor_comunitario.matcher.normalizer import (
    normalize_municipality,
    normalize_street_name,
    normalize_text,
)


def test_normalize_text_removes_accents_and_extra_spaces() -> None:
    assert normalize_text("  São   José  ") == "sao jose"


def test_normalize_street_name_expands_common_prefix() -> None:
    assert normalize_street_name("R. João Pessoa") == "rua joao pessoa"


def test_normalize_municipality_keeps_words() -> None:
    assert normalize_municipality("Florianópolis") == "florianopolis"
