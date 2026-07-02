"""Utility functions for string and data manipulation."""

from typing import Optional, Sequence, TypeVar
from datetime import datetime, timedelta
import hashlib
import json

T = TypeVar("T")


def slugify(text: str, max_length: int = 80) -> str:
    """Convert arbitrary text into a URL-safe slug.

    Args:
        text: Input string to slugify.
        max_length: Maximum length of the resulting slug (default 80).

    Returns:
        Lowercase slug with non-alphanumeric characters replaced by hyphens.
    """
    slug = "".join(c if c.isalnum() else "-" for c in text.lower()).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug[:max_length].rstrip("-")


def chunk_list(items: Sequence[T], chunk_size: int = 100) -> list[list[T]]:
    """Split a sequence into fixed-size chunks.

    Args:
        items: Sequence of items to chunk.
        chunk_size: Maximum number of items per chunk (default 100).

    Returns:
        List of chunks, each a list of up to ``chunk_size`` items.
    """
    return [list(items[i : i + chunk_size]) for i in range(0, len(items), chunk_size)]


def compute_checksum(data: str, algorithm: str = "sha256") -> str:
    """Compute hex digest of a string using the specified hash algorithm.

    Args:
        data: Input string to hash.
        algorithm: Hash algorithm name (``sha256``, ``sha1``, ``md5``).

    Returns:
        Hex digest string.

    Raises:
        ValueError: If the algorithm is not supported by ``hashlib``.
    """
    try:
        hasher = hashlib.new(algorithm)
    except ValueError:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")
    hasher.update(data.encode("utf-8"))
    return hasher.hexdigest()


def parse_iso_date(value: str | None) -> datetime | None:
    """Safely parse an ISO 8601 date string, returning None on failure.

    Args:
        value: ISO 8601 date string or None.

    Returns:
        Parsed datetime, or None if the input is None or unparseable.
    """
    if value is None:
        return None
    try:
        return datetime.fromisoformat(value)
    except (ValueError, TypeError):
        return None


def format_timedelta(delta: timedelta, precision: int = 2) -> str:
    """Format a timedelta into a human-readable string.

    Args:
        delta: The timedelta to format.
        precision: Number of most significant units to show (default 2).

    Returns:
        String like ``"3 days, 4 hours"`` or ``"5 minutes, 10 seconds"``.
    """
    total_seconds = int(delta.total_seconds())
    units = [
        ("day", 86400),
        ("hour", 3600),
        ("minute", 60),
        ("second", 1),
    ]
    parts = []
    for name, divisor in units:
        if total_seconds >= divisor or parts:
            count, total_seconds = divmod(total_seconds, divisor)
            if count:
                parts.append(f"{count} {name}{'s' if count != 1 else ''}")
    return ", ".join(parts[:precision]) if parts else "0 seconds"


def merge_dicts(base: dict, overlay: dict, deep: bool = True) -> dict:
    """Merge two dictionaries, with ``overlay`` values taking priority.

    Args:
        base: Base dictionary.
        overlay: Overlay dictionary whose values override base values.
        deep: If True, recursively merge nested dictionaries (default True).

    Returns:
        New merged dictionary (neither input is mutated).
    """
    result = base.copy()
    for key, value in overlay.items():
        if deep and key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    return result
