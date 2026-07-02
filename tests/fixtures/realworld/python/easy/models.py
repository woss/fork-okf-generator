"""Data models for the utility library domain."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum, auto


class Priority(Enum):
    """Priority level for a task or notification."""

    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CRITICAL = auto()


@dataclass
class TimestampMixin:
    """Mixin dataclass providing created and updated timestamps."""

    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime | None = None


@dataclass
class User(TimestampMixin):
    """Represents a user in the system.

    Attributes:
        user_id: Unique identifier for the user.
        email: User's email address.
        display_name: Optional human-readable name.
        is_active: Whether the user account is active.
        priority: User's notification priority level.
    """

    user_id: str
    email: str
    display_name: str | None = None
    is_active: bool = True
    priority: Priority = Priority.MEDIUM


@dataclass
class AdminUser(User):
    """An administrative user with elevated system access."""

    role: str = "admin"
    permissions: list[str] = field(default_factory=lambda: ["read", "write", "delete"])
    access_level: int = 10


@dataclass
class AuditEntry(TimestampMixin):
    """Immutable audit log entry recording a system action."""

    entry_id: str
    actor: str
    action: str
    resource: str
    details: dict = field(default_factory=dict)
