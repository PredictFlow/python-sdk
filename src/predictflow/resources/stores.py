"""Store management, connection testing, and catalog/order syncing."""

from __future__ import annotations

from typing import (  # noqa: UP035 - List used to avoid shadowing the `list` method defined in these classes
    Any,
    BinaryIO,
    List,
)

from .._http import AsyncHttpClient, SyncHttpClient


def _csv_files(file: BinaryIO | bytes | str, filename: str) -> dict[str, Any]:
    content = file.encode("utf-8") if isinstance(file, str) else file
    return {"file": (filename, content, "text/csv")}


class StoresResource:
    def __init__(self, http: SyncHttpClient) -> None:
        self._http = http

    def list(self) -> List[dict[str, Any]]:  # noqa: UP006
        return self._http.request("GET", "/stores")

    def create(self, *, platform: str, name: str, store_url: str = "") -> dict[str, Any]:
        return self._http.request(
            "POST", "/stores", json={"platform": platform, "name": name, "store_url": store_url}
        )

    def get(self, store_id: str) -> dict[str, Any]:
        return self._http.request("GET", f"/stores/{store_id}")

    def update(self, store_id: str, **fields: Any) -> dict[str, Any]:
        """fields may include name, store_url, status, currency - see StoreUpdate on the backend."""
        return self._http.request("PATCH", f"/stores/{store_id}", json=fields)

    def delete(self, store_id: str) -> None:
        self._http.request("DELETE", f"/stores/{store_id}")

    def set_woocommerce_credentials(self, store_id: str, *, consumer_key: str, consumer_secret: str) -> dict[str, Any]:
        """Only WooCommerce stores support setting credentials this way today."""
        return self._http.request(
            "PUT",
            f"/stores/{store_id}/credentials",
            json={"consumer_key": consumer_key, "consumer_secret": consumer_secret},
        )

    def test_connection(self, store_id: str) -> dict[str, Any]:
        return self._http.request("POST", f"/stores/{store_id}/test-connection")

    def sync(self, store_id: str, *, full: bool = False) -> dict[str, Any]:
        return self._http.request("POST", f"/stores/{store_id}/sync", params={"full": full})

    def sync_history(self, store_id: str) -> List[dict[str, Any]]:  # noqa: UP006
        return self._http.request("GET", f"/stores/{store_id}/sync-history")

    def import_products_csv(
        self, store_id: str, file: BinaryIO | bytes | str, filename: str = "products.csv"
    ) -> dict[str, Any]:
        return self._http.request("POST", f"/stores/{store_id}/import/products", files=_csv_files(file, filename))

    def import_orders_csv(
        self, store_id: str, file: BinaryIO | bytes | str, filename: str = "orders.csv"
    ) -> dict[str, Any]:
        return self._http.request("POST", f"/stores/{store_id}/import/orders", files=_csv_files(file, filename))


class AsyncStoresResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def list(self) -> List[dict[str, Any]]:  # noqa: UP006
        return await self._http.request("GET", "/stores")

    async def create(self, *, platform: str, name: str, store_url: str = "") -> dict[str, Any]:
        return await self._http.request(
            "POST", "/stores", json={"platform": platform, "name": name, "store_url": store_url}
        )

    async def get(self, store_id: str) -> dict[str, Any]:
        return await self._http.request("GET", f"/stores/{store_id}")

    async def update(self, store_id: str, **fields: Any) -> dict[str, Any]:
        return await self._http.request("PATCH", f"/stores/{store_id}", json=fields)

    async def delete(self, store_id: str) -> None:
        await self._http.request("DELETE", f"/stores/{store_id}")

    async def set_woocommerce_credentials(
        self, store_id: str, *, consumer_key: str, consumer_secret: str
    ) -> dict[str, Any]:
        return await self._http.request(
            "PUT",
            f"/stores/{store_id}/credentials",
            json={"consumer_key": consumer_key, "consumer_secret": consumer_secret},
        )

    async def test_connection(self, store_id: str) -> dict[str, Any]:
        return await self._http.request("POST", f"/stores/{store_id}/test-connection")

    async def sync(self, store_id: str, *, full: bool = False) -> dict[str, Any]:
        return await self._http.request("POST", f"/stores/{store_id}/sync", params={"full": full})

    async def sync_history(self, store_id: str) -> List[dict[str, Any]]:  # noqa: UP006
        return await self._http.request("GET", f"/stores/{store_id}/sync-history")

    async def import_products_csv(
        self, store_id: str, file: BinaryIO | bytes | str, filename: str = "products.csv"
    ) -> dict[str, Any]:
        return await self._http.request(
            "POST", f"/stores/{store_id}/import/products", files=_csv_files(file, filename)
        )

    async def import_orders_csv(
        self, store_id: str, file: BinaryIO | bytes | str, filename: str = "orders.csv"
    ) -> dict[str, Any]:
        return await self._http.request(
            "POST", f"/stores/{store_id}/import/orders", files=_csv_files(file, filename)
        )
