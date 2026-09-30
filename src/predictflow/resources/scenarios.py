"""What-if scenario planning: price/demand shift simulations and side-by-side comparisons."""

from __future__ import annotations

from typing import Any

from .._http import AsyncHttpClient, SyncHttpClient


class ScenariosResource:
    def __init__(self, http: SyncHttpClient) -> None:
        self._http = http

    def create(
        self,
        store_id: str,
        *,
        name: str,
        description: str | None = None,
        price_change_pct: float = 0.0,
        demand_shift_pct: float = 0.0,
    ) -> dict[str, Any]:
        return self._http.request(
            "POST",
            f"/stores/{store_id}/scenarios",
            json={
                "name": name,
                "description": description,
                "price_change_pct": price_change_pct,
                "demand_shift_pct": demand_shift_pct,
            },
        )

    def list(self, store_id: str) -> list[dict[str, Any]]:
        return self._http.request("GET", f"/stores/{store_id}/scenarios")

    def compare(self, store_id: str, scenario_a_id: str, scenario_b_id: str) -> dict[str, Any]:
        return self._http.request(
            "GET",
            f"/stores/{store_id}/scenarios/compare",
            params={"scenario_a_id": scenario_a_id, "scenario_b_id": scenario_b_id},
        )

    def get(self, store_id: str, scenario_id: str) -> dict[str, Any]:
        return self._http.request("GET", f"/stores/{store_id}/scenarios/{scenario_id}")

    def update(self, scenario_id: str, **fields: Any) -> dict[str, Any]:
        """fields may include name, description, price_change_pct, demand_shift_pct."""
        return self._http.request("PATCH", f"/scenarios/{scenario_id}", json=fields)

    def delete(self, scenario_id: str) -> None:
        self._http.request("DELETE", f"/scenarios/{scenario_id}")

    def execute(self, scenario_id: str) -> dict[str, Any]:
        return self._http.request("POST", f"/scenarios/{scenario_id}/execute")

    def clone(self, scenario_id: str, *, name: str | None = None) -> dict[str, Any]:
        return self._http.request("POST", f"/scenarios/{scenario_id}/clone", json={"name": name})


class AsyncScenariosResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def create(
        self,
        store_id: str,
        *,
        name: str,
        description: str | None = None,
        price_change_pct: float = 0.0,
        demand_shift_pct: float = 0.0,
    ) -> dict[str, Any]:
        return await self._http.request(
            "POST",
            f"/stores/{store_id}/scenarios",
            json={
                "name": name,
                "description": description,
                "price_change_pct": price_change_pct,
                "demand_shift_pct": demand_shift_pct,
            },
        )

    async def list(self, store_id: str) -> list[dict[str, Any]]:
        return await self._http.request("GET", f"/stores/{store_id}/scenarios")

    async def compare(self, store_id: str, scenario_a_id: str, scenario_b_id: str) -> dict[str, Any]:
        return await self._http.request(
            "GET",
            f"/stores/{store_id}/scenarios/compare",
            params={"scenario_a_id": scenario_a_id, "scenario_b_id": scenario_b_id},
        )

    async def get(self, store_id: str, scenario_id: str) -> dict[str, Any]:
        return await self._http.request("GET", f"/stores/{store_id}/scenarios/{scenario_id}")

    async def update(self, scenario_id: str, **fields: Any) -> dict[str, Any]:
        return await self._http.request("PATCH", f"/scenarios/{scenario_id}", json=fields)

    async def delete(self, scenario_id: str) -> None:
        await self._http.request("DELETE", f"/scenarios/{scenario_id}")

    async def execute(self, scenario_id: str) -> dict[str, Any]:
        return await self._http.request("POST", f"/scenarios/{scenario_id}/execute")

    async def clone(self, scenario_id: str, *, name: str | None = None) -> dict[str, Any]:
        return await self._http.request("POST", f"/scenarios/{scenario_id}/clone", json={"name": name})
