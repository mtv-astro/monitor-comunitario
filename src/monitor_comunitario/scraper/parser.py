import re
from dataclasses import dataclass


@dataclass(frozen=True)
class ParsedOutageNotice:
    """Structured notice extracted from Celesc public text."""

    municipality: str
    raw_text: str
    neighborhood: str = ""
    street: str = ""
    description: str = ""


_NOISE_PREFIXES = (
    "Usamos apenas os cookies",
    "Clique aqui para conhecer nossa Pol?tica de Privacidade",
)

_NOISE_LINES = {
    "estou ciente",
    "sem iframes",
}

_FOOTER_MARKERS = {
    "AJUDA",
    "ENTENDA",
    "CONSULTE",
    "NOSSOS SITES",
}

_NON_NOTICE_UPPERCASE_LINES = {
    "AJUDA",
    "ENTENDA",
    "CONSULTE",
    "NOSSOS SITES",
    "LIBRAS",
    "VOZ",
}

_NOTICE_HINT_PATTERN = re.compile(
    r"\b(data|hor[a?]rio|bairro|rua|avenida|servid[a?]o|rodovia|desligamento)\b",
    re.IGNORECASE,
)

_MUNICIPALITY_LINE_PATTERN = re.compile(
    r"\bMunic\S*pio\s+de\s*-\s*(?P<value>[^\n\r]+)",
    re.IGNORECASE,
)

_FIELD_PATTERNS = {
    "neighborhood": re.compile(r"\bBairro\s*:\s*(?P<value>.+)", re.IGNORECASE),
    "street": re.compile(
        r"\b(?:Rua|R\.|Avenida|Av\.|Servid[a?]o|Rodovia)\s*:\s*(?P<value>.+)",
        re.IGNORECASE,
    ),
    "description": re.compile(r"\b(?:Motivo|Descri[c?][a?]o)\s*:\s*(?P<value>.+)", re.IGNORECASE),
}


def clean_page_text(text: str) -> str:
    """Normalize visible page text before parsing."""
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [re.sub(r"\s+", " ", line).strip() for line in normalized.split("\n")]

    cleaned: list[str] = []
    previous = ""

    for line in lines:
        if not line:
            continue

        lower_line = line.lower()

        if lower_line in _NOISE_LINES:
            continue

        if any(line.startswith(prefix) for prefix in _NOISE_PREFIXES):
            continue

        if line == previous:
            continue

        cleaned.append(line)
        previous = line

    return "\n".join(cleaned).strip()


def extract_relevant_outage_section(text: str) -> str:
    """Return the text section most relevant to outage notices."""
    cleaned = clean_page_text(text)

    start_markers = [
        "Avisos de Desligamentos",
        "Interrup??es Programadas de Energia",
        "O que ? um desligamento programado?",
    ]

    marker_indexes = [cleaned.find(marker) for marker in start_markers if cleaned.find(marker) >= 0]
    start_index = min(marker_indexes) if marker_indexes else 0
    section = cleaned[start_index:]

    for marker in _FOOTER_MARKERS:
        found = section.find(f"\n{marker}")
        if found > 0:
            section = section[:found]
            break

    return section.strip()


def _looks_like_municipality(line: str) -> bool:
    """Return whether a line can represent a municipality heading."""
    if not line or ":" in line:
        return False

    if line.upper() in _NON_NOTICE_UPPERCASE_LINES:
        return False

    letters = [char for char in line if char.isalpha()]

    if not letters:
        return False

    uppercase_letters = [char for char in letters if char.isupper()]
    uppercase_ratio = len(uppercase_letters) / len(letters)

    return uppercase_ratio >= 0.75 and 3 <= len(line) <= 80


def _block_has_notice_hint(block: list[str]) -> bool:
    """Return whether a candidate block looks like an outage notice."""
    joined = "\n".join(block)
    return bool(_NOTICE_HINT_PATTERN.search(joined))


def _extract_field(block_text: str, field: str) -> str:
    pattern = _FIELD_PATTERNS[field]
    match = pattern.search(block_text)

    if not match:
        return ""

    return match.group("value").strip()


def _extract_notice_municipality(block_text: str) -> str:
    """Extract the municipality explicitly printed inside a Celesc notice block."""
    match = _MUNICIPALITY_LINE_PATTERN.search(block_text)

    if not match:
        return ""

    return match.group("value").strip()


def _build_notice_from_block(municipality: str, block: list[str]) -> ParsedOutageNotice:
    block_text = "\n".join(block).strip()
    description = _extract_field(block_text, "description") or block_text
    notice_municipality = _extract_notice_municipality(block_text) or municipality.strip()

    return ParsedOutageNotice(
        municipality=notice_municipality,
        neighborhood=_extract_field(block_text, "neighborhood"),
        street=_extract_field(block_text, "street"),
        description=description,
        raw_text=block_text,
    )


def parse_outage_notices_from_text(
    text: str,
    fallback_municipality: str = "",
) -> list[ParsedOutageNotice]:
    """Parse outage notices from visible page text.

    The parser supports two modes:
    1. municipality headings in the text;
    2. a fallback municipality supplied by the selector capture.

    When Celesc prints an explicit "Munic?pio de - ..." line inside the
    notice, that value is preferred over headings/dropdown fallback text.
    """
    section = extract_relevant_outage_section(text)
    lines = [line.strip() for line in section.splitlines() if line.strip()]

    notices: list[ParsedOutageNotice] = []
    current_municipality = fallback_municipality.strip()
    current_block: list[str] = []

    for line in lines:
        if _looks_like_municipality(line):
            if current_municipality and current_block and _block_has_notice_hint(current_block):
                notices.append(_build_notice_from_block(current_municipality, current_block))

            current_municipality = line
            current_block = []
            continue

        if current_municipality:
            current_block.append(line)

    if current_municipality and current_block and _block_has_notice_hint(current_block):
        notices.append(_build_notice_from_block(current_municipality, current_block))

    return notices
