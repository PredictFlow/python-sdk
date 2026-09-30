"""Inventory alert rules, templates, and evaluation history."""

from __future__ import annotations

from typing import Any

from .._http import AsyncHttpClient, SyncHttpClient


class AlertsResource:
    def __init__(self, http: SyncHttpClient) -> None:
        self._http = http

    def list_templates(self) -> list[dict[str, Any]]:
        return self._http.request("GET", "/alert-templates")

    def create_rule(
        self,
        store_id: str,
        *,
        metric_type: str,
        name: str | None = None,
        threshold: float | None = None,
        product_ids: list[str] | None = None,
        is_active: bool = True,
    ) -> dict[str, Any]:
        return self._http.request(
            "POST",
            f"/stores/{store_id}/alert-rules",
            json={
                "metric_type": metric_type,
                "name": name,
                "threshold": threshold,
                "product_ids": product_ids or [],
                "is_active": is_active,
            },
        )

    def list_rules(self, store_id: str) -> list[dict[str, Any]]:
        return self._http.request("GET", f"/stores/{store_id}/alert-rules")

    def get_rule(self, rule_id: str) -> dict[str, Any]:
        return self._http.request("GET", f"/alert-rules/{rule_id}")

    def update_rule(self, rule_id: str, **fields: Any) -> dict[str, Any]:
        """fields may include name, threshold, is_active."""
        return self._http.request("PATCH", f"/alert-rules/{rule_id}", json=fields)

    def delete_rule(self, rule_id: str) -> None:
        self._http.request("DELETE", f"/alert-rules/{rule_id}")

    def rule_history(self, rule_id: str) -> list[dict[str, Any]]:
        return self._http.request("GET", f"/alert-rules/{rule_id}/history")


class AsyncAlertsResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def list_templates(self) -> list[dict[str, Any]]:
        return await self._http.request("GET", "/alert-templates")

    async def create_rule(
        self,
        store_id: str,
        *,
        metric_type: str,
        name: str | None = None,
        threshold: float | None = None,
        product_ids: list[str] | None = None,
        is_active: bool = True,
    ) -> dict[str, Any]:
        return await self._http.request(
            "POST",
            f"/stores/{store_id}/alert-rules",
            json={
                "metric_type": metric_type,
                "name": name,
                "threshold": threshold,
                "product_ids": product_ids or [],
                "is_active": is_active,
            },
        )

    async def list_rules(self, store_id: str) -> list[dict[str, Any]]:
        return await self._http.request("GET", f"/stores/{store_id}/alert-rules")

    async def get_rule(self, rule_id: str) -> dict[str, Any]:
        return await self._http.request("GET", f"/alert-rules/{rule_id}")

    async def update_rule(self, rule_id: str, **fields: Any) -> dict[str, Any]:
        return await self._http.request("PATCH", f"/alert-rules/{rule_id}", json=fields)

    async def delete_rule(self, rule_id: str) -> None:
        await self._http.request("DELETE", f"/alert-rules/{rule_id}")

    async def rule_history(self, rule_id: str) -> list[dict[str, Any]]:
        return await self._http.request("GET", f"/alert-rules/{rule_id}/history")
