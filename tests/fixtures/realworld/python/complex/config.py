"""Application configuration management for the payment service."""

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
from os import environ


class Environment(Enum):
    """Deployment environment for the service."""

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


@dataclass
class Settings:
    """Central configuration object loaded from environment variables.

    Attributes:
        version: Application version string.
        debug: Enable debug-level logging and error detail.
        payment_gateway_key: Secret API key for the payment gateway.
        max_retries: Number of times to retry failed gateway calls.
        allowed_currencies: Set of ISO currency codes the service accepts.
    """

    version: str = field(default_factory=lambda: environ.get("APP_VERSION", "0.1.0"))
    debug: bool = field(default_factory=lambda: environ.get("DEBUG", "0") == "1")
    payment_gateway_key: str = field(
        default_factory=lambda: environ.get("PAYMENT_GATEWAY_KEY", "sk_test_default")
    )
    max_retries: int = 3
    allowed_currencies: frozenset[str] = field(
        default_factory=lambda: frozenset({"USD", "EUR", "GBP", "CAD", "AUD"})
    )
    environment: Environment = Environment.DEVELOPMENT

    def is_production(self) -> bool:
        """Check whether the service is running in production mode."""
        return self.environment == Environment.PRODUCTION

    def is_currency_allowed(self, currency: str) -> bool:
        """Check whether a currency code is in the allowed set.

        Args:
            currency: Three-letter ISO 4217 currency code.

        Returns:
            True if the currency is accepted by this service.
        """
        return currency.upper() in self.allowed_currencies
