"""CSV/XLSX/PDF exports of products, sales, inventory, forecasts, reorder, dead stock, and the dashboard.

Every method here returns a `FileDownload` (raw bytes + suggested filename)
rather than trying to JSON-decode a spreadsheet or PDF.
"""

from __future__ import annotations

from .._http import AsyncHttpClient, FileDownload, SyncHttpClient


class ExportsResource:
    def __init__(self, http: SyncHttpClient) -> None:
        self._http = http

    def all_stores_products(self, *, format: str = "xlsx") -> FileDownload:
        return self._http.request_file("GET", "/exports/products", params={"format": format})

    def products(self, store_id: str, *, format: str = "csv") -> FileDownload:
        return self._http.request_file("GET", f"/exports/stores/{store_id}/products", params={"format": format})

    def sales(self, store_id: str, *, format: str = "csv", days: int = 90) -> FileDownload:
        return self._http.request_file(
            "GET", f"/exports/stores/{store_id}/sales", params={"format": format, "days": days}
        )

    def inventory(self, store_id: str, *, format: str = "csv", days: int = 90) -> FileDownload:
        return self._http.request_file(
            "GET", f"/exports/stores/{store_id}/inventory", params={"format": format, "days": days}
        )

    def forecasts(self, store_id: str, *, format: str = "csv", product_id: str | None = None) -> FileDownload:
        return self._http.request_file(
            "GET", f"/exports/stores/{store_id}/forecasts", params={"format": format, "product_id": product_id}
        )

    def reorder(self, store_id: str, *, format: str = "csv") -> FileDownload:
        return self._http.request_file("GET", f"/exports/stores/{store_id}/reorder", params={"format": format})

    def dead_stock(self, store_id: str, *, format: str = "csv") -> FileDownload:
        return self._http.request_file("GET", f"/exports/stores/{store_id}/dead-stock", params={"format": format})

    def dashboard(self, *, format: str = "csv", days: int = 30) -> FileDownload:
        return self._http.request_file("GET", "/exports/dashboard", params={"format": format, "days": days})


class AsyncExportsResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def all_stores_products(self, *, format: str = "xlsx") -> FileDownload:
        return await self._http.request_file("GET", "/exports/products", params={"format": format})

    async def products(self, store_id: str, *, format: str = "csv") -> FileDownload:
        return await self._http.request_file(
            "GET", f"/exports/stores/{store_id}/products", params={"format": format}
        )

    async def sales(self, store_id: str, *, format: str = "csv", days: int = 90) -> FileDownload:
        return await self._http.request_file(
            "GET", f"/exports/stores/{store_id}/sales", params={"format": format, "days": days}
        )

    async def inventory(self, store_id: str, *, format: str = "csv", days: int = 90) -> FileDownload:
        return await self._http.request_file(
            "GET", f"/exports/stores/{store_id}/inventory", params={"format": format, "days": days}
        )

    async def forecasts(self, store_id: str, *, format: str = "csv", product_id: str | None = None) -> FileDownload:
        return await self._http.request_file(
            "GET", f"/exports/stores/{store_id}/forecasts", params={"format": format, "product_id": product_id}
        )

    async def reorder(self, store_id: str, *, format: str = "csv") -> FileDownload:
        return await self._http.request_file("GET", f"/exports/stores/{store_id}/reorder", params={"format": format})

    async def dead_stock(self, store_id: str, *, format: str = "csv") -> FileDownload:
        return await self._http.request_file(
            "GET", f"/exports/stores/{store_id}/dead-stock", params={"format": format}
        )

    async def dashboard(self, *, format: str = "csv", days: int = 30) -> FileDownload:
        return await self._http.request_file("GET", "/exports/dashboard", params={"format": format, "days": days})
