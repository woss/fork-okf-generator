"""Data connector module."""

class WorldBankConnector:
    """Fetches World Bank development indicators."""

    def get_indicator(self, code: str, country: str = "all") -> list:
        """Fetch a specific indicator by code."""
        return []

    def search(self, query: str) -> list:
        """Search indicators by keyword."""
        return []
