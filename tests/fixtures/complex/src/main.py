"""Core application module."""

import json
from datetime import datetime
from typing import Optional


class UserManager:
    """Manages user accounts and authentication."""

    def __init__(self, db_url: str, max_retries: int = 3):
        self.db_url = db_url
        self.max_retries = max_retries
        self._cache: dict[str, dict] = {}

    def get_user(self, user_id: str) -> Optional[dict]:
        """Fetch a user by ID from the database.

        Args:
            user_id: The unique identifier for the user.

        Returns:
            User dict or None if not found.
        """
        return self._cache.get(user_id)

    def create_user(self, email: str, name: str) -> dict:
        """Create a new user account.

        Args:
            email: User's email address.
            name: User's display name.

        Returns:
            The newly created user dict.
        """
        now = datetime.utcnow().isoformat()
        user = {"email": email, "name": name, "created_at": now}
        self._cache[email] = user
        return user


def validate_email(email: str) -> bool:
    """Check if an email address is valid.

    Uses a simple regex to validate email format.

    Args:
        email: The email string to validate.

    Returns:
        True if valid, False otherwise.
    """
    import re
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))
