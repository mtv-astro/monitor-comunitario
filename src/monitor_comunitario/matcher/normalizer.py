import re
import unicodedata

_STREET_PREFIXES = {
    "r": "rua",
    "r.": "rua",
    "rua": "rua",
    "av": "avenida",
    "av.": "avenida",
    "avenida": "avenida",
    "serv": "servidao",
    "serv.": "servidao",
    "servidao": "servidao",
    "rod": "rodovia",
    "rod.": "rodovia",
    "rodovia": "rodovia",
    "estr": "estrada",
    "estr.": "estrada",
    "estrada": "estrada",
}


def strip_accents(value: str) -> str:
    """Remove accents without changing the semantic value of the text."""
    normalized = unicodedata.normalize("NFKD", value)
    return "".join(char for char in normalized if not unicodedata.combining(char))


def normalize_text(value: str) -> str:
    """Normalize free text for safer comparisons."""
    value = strip_accents(value)
    value = value.lower().strip()
    value = re.sub(r"[^\w\s.-]", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def normalize_street_name(value: str) -> str:
    """
    Normalize street names before fuzzy matching.

    Celesc notices may use variants such as "Rua", "R.", "Servidão",
    "Serv." or all-caps text. We normalize these variants so the matcher
    can compare user input against public outage notices with fewer
    false negatives.
    """
    text = normalize_text(value)
    if not text:
        return ""

    parts = text.split(" ")
    first = parts[0]
    normalized_prefix = _STREET_PREFIXES.get(first)

    if normalized_prefix:
        parts[0] = normalized_prefix

    return " ".join(parts)


def normalize_municipality(value: str) -> str:
    """Normalize municipality names."""
    return normalize_text(value)


def normalize_neighborhood(value: str) -> str:
    """Normalize neighborhood names."""
    return normalize_text(value)
