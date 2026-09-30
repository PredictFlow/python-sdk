"""Product catalog, inventory levels, ABC analysis, forecasting, cost/margin, and competitor pricing."""

from __future__ import annotations

from typing import Any, List  # noqa: UP035 - List used to avoid shadowing the `list` method defined in these classes

from .._http import AsyncHttpClient, SyncHttpClient


class ProductsResource:
    def __init__(self, http: SyncHttpClient) -> None:
        self._http = http

    def list(
        self,
        *,
        store_id: str | None = None,
        search: str | None = None,
        page: int = 1,
        page_size: int = 20,
        sort_by: str = "name",
        sort_order: str = "asc",
        threshold: int = 10,
        overstock_threshold: int = 100,
    ) -> dict[str, Any]:
        return self._http.request(
            "GET",
            "/products",
            params={
                "store_id": store_id,
                "search": search,
                "page": page,
                "page_size": page_size,
                "sort_by": sort_by,
                "sort_order": sort_order,
                "threshold": threshold,
                "overstock_threshold": overstock_threshold,
            },
        )

    def summary(self) -> dict[str, Any]:
        return self._http.request("GET", "/products/summary")

    def get(self, product_id: str) -> dict[str, Any]:
        return self._http.request("GET", f"/products/{product_id}")

    def top_sellers(self, store_id: str, *, days: int = 30, limit: int = 10) -> List[dict[str, Any]]:  # noqa: UP006
        return self._http.request(
            "GET", f"/products/store/{store_id}/top-sellers", params={"days": days, "limit": limit}
        )

    def abc_analysis(self, store_id: str, *, days: int = 90) -> dict[str, Any]:
        return self._http.request("GET", f"/products/store/{store_id}/abc-analysis", params={"days": days})

    def low_stock(self, store_id: str, *, threshold: int = 10) -> dict[str, Any]:
        return self._http.request("GET", f"/products/store/{store_id}/low-stock", params={"threshold": threshold})

    def inventory_health(self, store_id: str, *, threshold: int = 10, overstock_threshold: int = 100) -> dict[str, Any]:
        return self._http.request(
            "GET",
            f"/products/store/{store_id}/inventory-health",
            params={"threshold": threshold, "overstock_threshold": overstock_threshold},
        )

    def accuracy_summary(self, store_id: str) -> dict[str, Any]:
        return self._http.request("GET", f"/products/store/{store_id}/accuracy-summary")

    def reorder_alerts(
        self,
        store_id: str,
        *,
        search: str | None = None,
        urgency: str | None = None,
        lead_time_days: int = 7,
        target_service_level: float = 0.95,
        sort_by: str = "urgency",
    ) -> dict[str, Any]:
        return self._http.request(
            "GET",
            f"/products/store/{store_id}/reorder-alerts",
            params={
                "search": search,
                "urgency": urgency,
                "lead_time_days": lead_time_days,
                "target_service_level": target_service_level,
                "sort_by": sort_by,
            },
        )

    def inventory_history(self, product_id: str) -> List[dict[str, Any]]:  # noqa: UP006
        return self._http.request("GET", f"/products/{product_id}/inventory-history")

    def forecast(self, product_id: str, *, horizon_days: int = 30, model: str = "prophet") -> dict[str, Any]:
        return self._http.request(
            "POST", f"/products/{product_id}/forecast", params={"horizon_days": horizon_days, "model": model}
        )

    def forecast_store(self, store_id: str, *, horizon_days: int = 30, model: str = "prophet") -> dict[str, Any]:
        """Forecasts every product in the store in the background - returns immediately with a batch status."""
        return self._http.request(
            "POST",
            f"/products/store/{store_id}/forecast",
            params={"horizon_days": horizon_days, "model": model},
        )

    def forecast_history(self, product_id: str) -> List[dict[str, Any]]:  # noqa: UP006
        return self._http.request("GET", f"/products/{product_id}/forecast-history")

    def update_cost(
        self,
        product_id: str,
        *,
        cogs: float | None = None,
        shipping_cost: float | None = None,
        other_fees: float | None = None,
    ) -> dict[str, Any]:
        return self._http.request(
            "PATCH",
            f"/products/{product_id}/cost",
            json={"cogs": cogs, "shipping_cost": shipping_cost, "other_fees": other_fees},
        )

    def margin(self, product_id: str) -> dict[str, Any]:
        return self._http.request("GET", f"/products/{product_id}/margin")

    def add_competitor_price(
        self,
        product_id: str,
        *,
        competitor_name: str,
        price: float,
        url: str | None = None,
        observed_at: str | None = None,
    ) -> dict[str, Any]:
        return self._http.request(
            "POST",
            f"/products/{product_id}/competitor-prices",
            json={"competitor_name": competitor_name, "price": price, "url": url, "observed_at": observed_at},
        )

    def list_competitor_prices(self, product_id: str) -> List[dict[str, Any]]:  # noqa: UP006
        return self._http.request("GET", f"/products/{product_id}/competitor-prices")

    def delete_competitor_price(self, product_id: str, competitor_price_id: str) -> None:
        self._http.request("DELETE", f"/products/{product_id}/competitor-prices/{competitor_price_id}")

    def reprice_suggestion(self, product_id: str) -> dict[str, Any]:
        return self._http.request("GET", f"/products/{product_id}/competitor-prices/reprice-suggestion")


class AsyncProductsResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def list(
        self,
        *,
        store_id: str | None = None,
        search: str | None = None,
        page: int = 1,
        page_size: int = 20,
        sort_by: str = "name",
        sort_order: str = "asc",
        threshold: int = 10,
        overstock_threshold: int = 100,
    ) -> dict[str, Any]:
        return await self._http.request(
            "GET",
            "/products",
            params={
                "store_id": store_id,
                "search": search,
                "page": page,
                "page_size": page_size,
                "sort_by": sort_by,
                "sort_order": sort_order,
                "threshold": threshold,
                "overstock_threshold": overstock_threshold,
            },
        )

    async def summary(self) -> dict[str, Any]:
        return await self._http.request("GET", "/products/summary")

    async def get(self, product_id: str) -> dict[str, Any]:
        return await self._http.request("GET", f"/products/{product_id}")

    async def top_sellers(self, store_id: str, *, days: int = 30, limit: int = 10) -> List[dict[str, Any]]:  # noqa: UP006
        return await self._http.request(
            "GET", f"/products/store/{store_id}/top-sellers", params={"days": days, "limit": limit}
        )

    async def abc_analysis(self, store_id: str, *, days: int = 90) -> dict[str, Any]:
        return await self._http.request("GET", f"/products/store/{store_id}/abc-analysis", params={"days": days})

    async def low_stock(self, store_id: str, *, threshold: int = 10) -> dict[str, Any]:
        return await self._http.request(
            "GET", f"/products/store/{store_id}/low-stock", params={"threshold": threshold}
        )

    async def inventory_health(
        self, store_id: str, *, threshold: int = 10, overstock_threshold: int = 100
    ) -> dict[str, Any]:
        return await self._http.request(
            "GET",
            f"/products/store/{store_id}/inventory-health",
            params={"threshold": threshold, "overstock_threshold": overstock_threshold},
        )

    async def accuracy_summary(self, store_id: str) -> dict[str, Any]:
        return await self._http.request("GET", f"/products/store/{store_id}/accuracy-summary")

    async def reorder_alerts(
        self,
        store_id: str,
        *,
        search: str | None = None,
        urgency: str | None = None,
        lead_time_days: int = 7,
        target_service_level: float = 0.95,
        sort_by: str = "urgency",
    ) -> dict[str, Any]:
        return await self._http.request(
            "GET",
            f"/products/store/{store_id}/reorder-alerts",
            params={
                "search": search,
                "urgency": urgency,
                "lead_time_days": lead_time_days,
                "target_service_level": target_service_level,
                "sort_by": sort_by,
            },
        )

    async def inventory_history(self, product_id: str) -> List[dict[str, Any]]:  # noqa: UP006
        return await self._http.request("GET", f"/products/{product_id}/inventory-history")

    async def forecast(self, product_id: str, *, horizon_days: int = 30, model: str = "prophet") -> dict[str, Any]:
        return await self._http.request(
            "POST", f"/products/{product_id}/forecast", params={"horizon_days": horizon_days, "model": model}
        )

    async def forecast_store(self, store_id: str, *, horizon_days: int = 30, model: str = "prophet") -> dict[str, Any]:
        return await self._http.request(
            "POST",
            f"/products/store/{store_id}/forecast",
            params={"horizon_days": horizon_days, "model": model},
        )

    async def forecast_history(self, product_id: str) -> List[dict[str, Any]]:  # noqa: UP006
        return await self._http.request("GET", f"/products/{product_id}/forecast-history")

    async def update_cost(
        self,
        product_id: str,
        *,
        cogs: float | None = None,
        shipping_cost: float | None = None,
        other_fees: float | None = None,
    ) -> dict[str, Any]:
        return await self._http.request(
            "PATCH",
            f"/products/{product_id}/cost",
            json={"cogs": cogs, "shipping_cost": shipping_cost, "other_fees": other_fees},
        )

    async def margin(self, product_id: str) -> dict[str, Any]:
        return await self._http.request("GET", f"/products/{product_id}/margin")

    async def add_competitor_price(
        self,
        product_id: str,
        *,
        competitor_name: str,
        price: float,
        url: str | None = None,
        observed_at: str | None = None,
    ) -> dict[str, Any]:
        return await self._http.request(
            "POST",
            f"/products/{product_id}/competitor-prices",
            json={"competitor_name": competitor_name, "price": price, "url": url, "observed_at": observed_at},
        )

    async def list_competitor_prices(self, product_id: str) -> List[dict[str, Any]]:  # noqa: UP006
        return await self._http.request("GET", f"/products/{product_id}/competitor-prices")

    async def delete_competitor_price(self, product_id: str, competitor_price_id: str) -> None:
        await self._http.request("DELETE", f"/products/{product_id}/competitor-prices/{competitor_price_id}")

    async def reprice_suggestion(self, product_id: str) -> dict[str, Any]:
        return await self._http.request("GET", f"/products/{product_id}/competitor-prices/reprice-suggestion")
