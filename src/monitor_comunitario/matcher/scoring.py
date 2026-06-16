from dataclasses import dataclass
from enum import StrEnum

from rapidfuzz import fuzz

from monitor_comunitario.matcher.normalizer import normalize_text


class MatchLevel(StrEnum):
    MUNICIPALITY = "municipality"
    NEIGHBORHOOD = "neighborhood"
    STREET = "street"
    FUZZY = "fuzzy"
    UNCERTAIN = "uncertain"
    NONE = "none"


@dataclass(frozen=True)
class MatchResult:
    level: MatchLevel
    score: float
    reason: str


def score_text(left: str, right: str) -> float:
    """Return a 0-100 fuzzy score for two normalized text values."""
    left_norm = normalize_text(left)
    right_norm = normalize_text(right)

    if not left_norm or not right_norm:
        return 0.0

    return float(fuzz.token_set_ratio(left_norm, right_norm))
