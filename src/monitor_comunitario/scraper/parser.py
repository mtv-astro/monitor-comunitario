import re
from dataclasses import dataclass


@dataclass(frozen=True)
class ParsedOutageNotice:
    """Structured notice extracted from Celesc public text.

    This is intentionally small for the first scraper slice. The parser will
    become more specific after we collect real snapshots from the page.
    """

    municipality: str
    raw_text: str


_NOISE_PREFIXES = (
    "Usamos apenas os cookies",
    "Clique aqui para conhecer nossa Política de Privacidade",
)

_NOISE_LINES = {
    "estou ciente",
    "sem iframes",
}


def clean_page_text(text: str) -> str:
    """Normalize visible page text before parsing.

    The Celesc page includes repeated cookie/banner/navigation text. We keep
    the function conservative for now: normalize line endings, strip spaces,
    remove empty lines and adjacent duplicates.
    """
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
    """Return the text section most relevant to outage notices.

    The public page can include large amounts of navigation/footer text. This
    helper keeps the outage-related content around the explanatory section.
    """
    cleaned = clean_page_text(text)

    start_markers = [
        "Avisos de Desligamentos",
        "O que é um desligamento programado?",
    ]

    end_markers = [
        "AJUDA",
        "Ajuda",
        "ENTENDA",
        "Entenda",
        "CONSULTE",
        "Consulte",
        "NOSSOS SITES",
    ]

    marker_indexes = [
        cleaned.find(marker)
        for marker in start_markers
        if cleaned.find(marker) >= 0
    ]

    start_index = min(marker_indexes) if marker_indexes else 0
    section = cleaned[start_index:]

    for marker in end_markers:
        found = section.find(f"\n{marker}")
        if found > 0:
            section = section[:found]
            break

    return section.strip()


def parse_outage_notices_from_text(text: str) -> list[ParsedOutageNotice]:
    """Parse outage notices from visible page text.

    The current implementation is intentionally conservative. It returns an
    empty list until real notice blocks are identified from captured snapshots.
    """
    _ = extract_relevant_outage_section(text)
    return []
