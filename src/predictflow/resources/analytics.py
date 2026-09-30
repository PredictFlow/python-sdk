"""Sales KPIs, revenue trends, day-of-week seasonality, and product growth."""

from __future__ import annotations

from typing import Any

from .._http import AsyncHttpClient, SyncHttpClient


class AnalyticsResource:
    def __init__(self, http: SyncHttpClient) -> None:
        self._http = http

    def overview(self, *, months: int = 12) -> dict[str, Any]:
        return self._http.request("GET", "/analytics", params={"months": months})

    def kpis(self, *, days: int = 30, store_id: str | None = None) -> dict[str, Any]:
        return self._http.request("GET", "/analytics/kpis", params={"days": days, "store_id": store_id})

    def day_of_week(self, *, days: int = 30, store_id: str | None = None) -> dict[str, Any]:
        return self._http.request("GET", "/analytics/day-of-week", params={"days": days, "store_id": store_id})

    def trend(self, *, days: int = 30, store_id: str | None = None, interval: str = "auto") -> dict[str, Any]:
        return self._http.request(
            "GET", "/analytics/trend", params={"days": days, "store_id": store_id, "interval": interval}
        )

    def product_growth(self, *, days: int = 30, store_id: str | None = None, limit: int = 5) -> dict[str, Any]:
        return self._http.request(
            "GET", "/analytics/product-growth", params={"days": days, "store_id": store_id, "limit": limit}
        )

    def projections(self, *, days: int = 30, store_id: str | None = None) -> dict[str, Any]:
        return self._http.request("GET", "/analytics/projections", params={"days": days, "store_id": store_id})


class AsyncAnalyticsResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def overview(self, *, months: int = 12) -> dict[str, Any]:
        return await self._http.request("GET", "/analytics", params={"months": months})

    async def kpis(self, *, days: int = 30, store_id: str | None = None) -> dict[str, Any]:
        return await self._http.request("GET", "/analytics/kpis", params={"days": days, "store_id": store_id})

    async def day_of_week(self, *, days: int = 30, store_id: str | None = None) -> dict[str, Any]:
        return await self._http.request(
            "GET", "/analytics/day-of-week", params={"days": days, "store_id": store_id}
        )

    async def trend(self, *, days: int = 30, store_id: str | None = None, interval: str = "auto") -> dict[str, Any]:
        return await self._http.request(
            "GET", "/analytics/trend", params={"days": days, "store_id": store_id, "interval": interval}
        )

    async def product_growth(
        self, *, days: int = 30, store_id: str | None = None, limit: int = 5
    ) -> dict[str, Any]:
        return await self._http.request(
            "GET", "/analytics/product-growth", params={"days": days, "store_id": store_id, "limit": limit}
        )

    async def projections(self, *, days: int = 30, store_id: str | None = None) -> dict[str, Any]:
        return await self._http.request("GET", "/analytics/projections", params={"days": days, "store_id": store_id})
