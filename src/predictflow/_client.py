"""The synchronous PredictFlow client."""

from __future__ import annotations

from ._config import ClientConfig, resolve_config
from ._http import SyncHttpClient
from .resources import (
    AlertsResource,
    AnalyticsResource,
    ExportsResource,
    PredictionsResource,
    PricingResource,
    ProductsResource,
    ScenariosResource,
    StoresResource,
)


class PredictFlow:
    """The unified, synchronous entry point for the PredictFlow API.

    Example:
        >>> from predictflow import PredictFlow
        >>> client = PredictFlow(api_key="pk_live_...")
        >>> forecast = client.products.forecast("prod_123", horizon_days=30)

    Also usable as a context manager to close the underlying HTTP
    connection pool deterministically:
        >>> with PredictFlow(api_key="pk_live_...") as client:
        ...     stores = client.stores.list()
    """

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        timeout_seconds: float | None = None,
        max_retries: int | None = None,
        default_headers: dict[str, str] | None = None,
    ) -> None:
        self.config: ClientConfig = resolve_config(
            api_key,
            base_url=base_url,
            timeout_seconds=timeout_seconds,
            max_retries=max_retries,
            default_headers=default_headers,
        )
        self._http = SyncHttpClient(self.config)

        self.stores = StoresResource(self._http)
        self.products = ProductsResource(self._http)
        self.predictions = PredictionsResource(self._http)
        self.analytics = AnalyticsResource(self._http)
        self.pricing = PricingResource(self._http)
        self.scenarios = ScenariosResource(self._http)
        self.alerts = AlertsResource(self._http)
        self.exports = ExportsResource(self._http)

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> PredictFlow:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    def health(self) -> dict[str, str]:
        """Checks API connectivity. /health lives at the bare origin, not
        under /api/v1, so this falls back to the root URL if the
        configured base_url includes the /api/v1 prefix (the default).
        """
        try:
            return self._http.request("GET", "/health")
        except Exception:
            from urllib.parse import urlsplit, urlunsplit

            parts = urlsplit(self.config.base_url)
            root_url = urlunsplit((parts.scheme, parts.netloc, "/health", "", ""))
            return self._http.request_absolute("GET", root_url)
