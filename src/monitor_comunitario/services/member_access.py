from hashlib import sha256
from secrets import choice, compare_digest

ACCESS_CODE_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
ACCESS_CODE_LENGTH = 10


def normalize_access_code(value: str) -> str:
    """Normalize a human-entered access code for hashing and verification."""
    return "".join(character for character in value.upper() if character.isalnum())


def generate_access_code() -> str:
    """Generate a one-time visible member access code."""
    raw_code = "".join(choice(ACCESS_CODE_ALPHABET) for _ in range(ACCESS_CODE_LENGTH))
    return f"{raw_code[:5]}-{raw_code[5:]}"


def hash_access_code(value: str) -> str:
    """Hash an access code without storing the plain code."""
    normalized_value = normalize_access_code(value)

    if not normalized_value:
        return ""

    return sha256(normalized_value.encode("utf-8")).hexdigest()


def verify_access_code(provided_code: str, expected_hash: str) -> bool:
    """Return whether a provided access code matches a stored hash."""
    if not expected_hash:
        return False

    provided_hash = hash_access_code(provided_code)
    return compare_digest(provided_hash, expected_hash)
