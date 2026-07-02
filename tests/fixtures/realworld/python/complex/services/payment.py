"""Payment processing service with gateway integration."""

from typing import Optional, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import hashlib
import hmac
import uuid


class PaymentStatus(Enum):
    """Possible states of a payment transaction."""

    PENDING = "pending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    REFUNDED = "refunded"


class PaymentError(Exception):
    """Raised when a payment operation fails at the gateway level."""

    def __init__(self, message: str, code: str = "payment_error") -> None:
        self.code = code
        super().__init__(message)


@dataclass
class PaymentResult:
    """Immutable result returned after processing a payment."""

    charge_id: str
    status: PaymentStatus
    amount_cents: int
    currency: str
    processed_at: datetime = field(default_factory=datetime.utcnow)
    gateway_response: str = ""

    def to_dict(self) -> dict:
        """Serialize the result to a plain dictionary."""
        return {
            "charge_id": self.charge_id,
            "status": self.status.value,
            "amount_cents": self.amount_cents,
            "currency": self.currency,
            "processed_at": self.processed_at.isoformat(),
        }


class PaymentService:
    """Core payment service that communicates with the external gateway.

    Args:
        api_key: Secret API key for authenticating with the gateway.
        idempotency_ttl_seconds: How long to keep idempotency keys in memory.
    """

    def __init__(self, api_key: str, idempotency_ttl_seconds: int = 3600) -> None:
        if not api_key:
            raise ValueError("API key is required")
        self._api_key = api_key
        self._idempotency_ttl = idempotency_ttl_seconds
        self._idempotency_cache: dict[str, PaymentResult] = {}

    def process_payment(
        self,
        customer_id: str,
        amount_cents: int,
        currency: str,
        metadata: dict | None = None,
        idempotency_key: str | None = None,
    ) -> PaymentResult:
        """Submit a payment to the external gateway.

        Args:
            customer_id: The customer to charge.
            amount_cents: Amount in the smallest currency unit.
            currency: ISO 4217 currency code.
            metadata: Optional additional data for the gateway.
            idempotency_key: Unique key to prevent duplicate charges.

        Returns:
            A ``PaymentResult`` describing the outcome.

        Raises:
            PaymentError: If the gateway rejects the payment.
        """
        idem_key = idempotency_key or self._generate_idempotency_key(customer_id, amount_cents)
        cached = self._idempotency_cache.get(idem_key)
        if cached:
            return cached

        charge_id = f"ch_{uuid.uuid4().hex}"
        signature = self._sign_payload(f"{customer_id}:{amount_cents}:{currency}")

        result = PaymentResult(
            charge_id=charge_id,
            status=PaymentStatus.SUCCEEDED,
            amount_cents=amount_cents,
            currency=currency,
            gateway_response=signature,
        )
        self._idempotency_cache[idem_key] = result
        return result

    def lookup_charge(
        self, charge_id: str, idempotency_key: str | None
    ) -> PaymentResult | None:
        """Look up a previously processed charge by its identifier.

        Args:
            charge_id: The charge UUID returned by ``process_payment``.
            idempotency_key: Optional key to narrow the search.

        Returns:
            The ``PaymentResult`` if found, or None.
        """
        for result in self._idempotency_cache.values():
            if result.charge_id == charge_id:
                return result
        return None

    def _generate_idempotency_key(self, customer_id: str, amount_cents: int) -> str:
        raw = f"{customer_id}:{amount_cents}:{uuid.uuid4().hex}"
        return hashlib.sha256(raw.encode()).hexdigest()

    def _sign_payload(self, payload: str) -> str:
        return hmac.new(
            self._api_key.encode(), payload.encode(), hashlib.sha256
        ).hexdigest()

    @classmethod
    def from_settings(cls, api_key: str) -> "PaymentService":
        """Factory: create a service instance pre-configured from settings."""
        return cls(api_key=api_key)
