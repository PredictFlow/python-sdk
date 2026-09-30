"""Price elasticity, optimization, simulation, cross-elasticity, and batch repricing."""

from __future__ import annotations

from typing import Any

from .._http import AsyncHttpClient, SyncHttpClient


class PricingResource:
    def __init__(self, http: SyncHttpClient) -> None:
        self._http = http

    def elasticity(self, product_id: str) -> dict[str, Any]:
        return self._http.request("GET", f"/pricing/product/{product_id}/elasticity")

    def optimize(
        self,
        product_id: str,
        *,
        strategy: str = "maximize_revenue",
        competitor_price: float | None = None,
        cost_override: float | None = None,
    ) -> dict[str, Any]:
        return self._http.request(
            "POST",
            f"/pricing/product/{product_id}/optimize",
            params={"strategy": strategy, "competitor_price": competitor_price, "cost_override": cost_override},
        )

    def simulate(self, product_id: str, *, new_price: float, cost_override: float | None = None) -> dict[str, Any]:
        return self._http.request(
            "POST",
            f"/pricing/product/{product_id}/simulate",
            params={"new_price": new_price, "cost_override": cost_override},
        )

    def batch_optimize(
        self, store_id: str, *, strategy: str = "maximize_revenue", limit: int = 50
    ) -> list[dict[str, Any]]:
        return self._http.request(
            "POST", f"/pricing/store/{store_id}/batch-optimize", params={"strategy": strategy, "limit": limit}
        )

    def cross_elasticity(self, product_id: str, related_product_id: str, *, lookback_days: int = 180) -> dict[str, Any]:
        return self._http.request(
            "GET",
            f"/pricing/product/{product_id}/cross-elasticity/{related_product_id}",
            params={"lookback_days": lookback_days},
        )


class AsyncPricingResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def elasticity(self, product_id: str) -> dict[str, Any]:
        return await self._http.request("GET", f"/pricing/product/{product_id}/elasticity")

    async def optimize(
        self,
        product_id: str,
        *,
        strategy: str = "maximize_revenue",
        competitor_price: float | None = None,
        cost_override: float | None = None,
    ) -> dict[str, Any]:
        return await self._http.request(
            "POST",
            f"/pricing/product/{product_id}/optimize",
            params={"strategy": strategy, "competitor_price": competitor_price, "cost_override": cost_override},
        )

    async def simulate(
        self, product_id: str, *, new_price: float, cost_override: float | None = None
    ) -> dict[str, Any]:
        return await self._http.request(
            "POST",
            f"/pricing/product/{product_id}/simulate",
            params={"new_price": new_price, "cost_override": cost_override},
        )

    async def batch_optimize(
        self, store_id: str, *, strategy: str = "maximize_revenue", limit: int = 50
    ) -> list[dict[str, Any]]:
        return await self._http.request(
            "POST", f"/pricing/store/{store_id}/batch-optimize", params={"strategy": strategy, "limit": limit}
        )

    async def cross_elasticity(
        self, product_id: str, related_product_id: str, *, lookback_days: int = 180
    ) -> dict[str, Any]:
        return await self._http.request(
            "GET",
            f"/pricing/product/{product_id}/cross-elasticity/{related_product_id}",
            params={"lookback_days": lookback_days},
        )
