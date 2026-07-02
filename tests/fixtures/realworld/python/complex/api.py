"""REST API entry point for the payment processing service."""

from typing import Optional, Union
from functools import wraps
from datetime import datetime
import logging
import json

from .config import Settings, Environment
from .services.payment import PaymentService, PaymentResult, PaymentError

logger = logging.getLogger(__name__)
settings = Settings()


def json_response(func):
    """Decorator that wraps the return value as a JSON-serializable dict.

    Expects the wrapped function to return a dict or a Pydantic-like model
    with a ``to_dict()`` method.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if hasattr(result, "to_dict"):
                result = result.to_dict()
            return {"success": True, "data": result, "error": None}
        except PaymentError as exc:
            logger.error("PaymentError in %s: %s", func.__name__, exc)
            return {"success": False, "data": None, "error": str(exc)}
        except Exception as exc:
            logger.exception("Unhandled exception in %s", func.__name__)
            return {"success": False, "data": None, "error": "Internal server error"}

    return wrapper


class PaymentAPI:
    """High-level API for processing payments through external gateways."""

    def __init__(self, service: PaymentService | None = None) -> None:
        self._service = service or PaymentService(api_key=settings.payment_gateway_key)

    @property
    def service(self) -> PaymentService:
        """Return the underlying payment service instance."""
        return self._service

    @json_response
    def charge(
        self,
        customer_id: str,
        amount_cents: int,
        currency: str = "USD",
        metadata: dict | None = None,
    ) -> dict:
        """Charge a customer a given amount.

        Args:
            customer_id: Unique identifier for the customer.
            amount_cents: Amount in the smallest currency unit.
            currency: Three-letter ISO 4217 currency code.
            metadata: Optional key-value pairs to attach to the charge.

        Returns:
            A dict containing the payment result fields.
        """
        if amount_cents <= 0:
            raise PaymentError("Amount must be a positive integer.")
        result = self._service.process_payment(
            customer_id=customer_id,
            amount_cents=amount_cents,
            currency=currency.upper(),
            metadata=metadata or {},
        )
        return result.to_dict()

    def get_charge(self, charge_id: str) -> dict | None:
        """Retrieve details for a previously created charge.

        Args:
            charge_id: The unique identifier returned by the gateway.

        Returns:
            Charge details dict, or None if not found.
        """
        result = self._service.lookup_charge(charge_id, idempotency_key=None)
        return result.to_dict() if result else None

    @classmethod
    def health_check(cls) -> dict:
        """Return the current health status of the API and its dependencies.

        Returns:
            Dict with ``status``, ``timestamp``, and ``version`` keys.
        """
        return {
            "status": "ok",
            "timestamp": datetime.utcnow().isoformat(),
            "version": settings.version,
        }

    @staticmethod
    def validate_amount(amount_cents: int) -> bool:
        """Check that an amount is within acceptable bounds.

        Args:
            amount_cents: Amount in cents to validate.

        Returns:
            True if the amount is valid, False otherwise.
        """
        return 1 <= amount_cents <= 9_999_999
