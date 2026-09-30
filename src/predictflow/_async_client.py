"""The asynchronous PredictFlow client - same surface as PredictFlow, awaited."""

from __future__ import annotations

from ._config import ClientConfig, resolve_config
from ._http import AsyncHttpClient
from .resources import (
    AsyncAlertsResource,
    AsyncAnalyticsResource,
    AsyncExportsResource,
    AsyncPredictionsResource,
    AsyncPricingResource,
    AsyncProductsResource,
    AsyncScenariosResource,
    AsyncStoresResource,
)


class AsyncPredictFlow:
    """The unified, asynchronous entry point for the PredictFlow API.

    Example:
        >>> from predictflow import AsyncPredictFlow
        >>> async with AsyncPredictFlow(api_key="pk_live_...") as client:
        ...     forecast = await client.products.forecast("prod_123", horizon_days=30)
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
        self._http = AsyncHttpClient(self.config)

        self.stores = AsyncStoresResource(self._http)
        self.products = AsyncProductsResource(self._http)
        self.predictions = AsyncPredictionsResource(self._http)
        self.analytics = AsyncAnalyticsResource(self._http)
        self.pricing = AsyncPricingResource(self._http)
        self.scenarios = AsyncScenariosResource(self._http)
        self.alerts = AsyncAlertsResource(self._http)
        self.exports = AsyncExportsResource(self._http)

    async def aclose(self) -> None:
        await self._http.aclose()

    async def __aenter__(self) -> AsyncPredictFlow:
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        await self.aclose()

    async def health(self) -> dict[str, str]:
        try:
            return await self._http.request("GET", "/health")
        except Exception:
            from urllib.parse import urlsplit, urlunsplit

            parts = urlsplit(self.config.base_url)
            root_url = urlunsplit((parts.scheme, parts.netloc, "/health", "", ""))
            return await self._http.request_absolute("GET", root_url)
