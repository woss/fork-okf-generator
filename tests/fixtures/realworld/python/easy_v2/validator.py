"""Input validation utilities — new in v2."""

import re


def validate_email(email: str) -> bool:
    """Check if a string looks like a valid email address.

    Args:
        email: The email string to validate.

    Returns:
        True if the email matches a basic pattern, False otherwise.
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """Check if a string looks like a US phone number.

    Args:
        phone: The phone string to validate.

    Returns:
        True if the phone matches a basic pattern, False otherwise.
    """
    cleaned = re.sub(r"[^\d]", "", phone)
    return len(cleaned) == 10 or (len(cleaned) == 11 and cleaned.startswith("1"))
