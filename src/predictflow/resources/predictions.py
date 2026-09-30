"""Monte Carlo simulation, stockout risk, and inventory policy for an existing prediction.

Forecast generation itself lives on ProductsResource (forecast/forecast_store)
since that's where the backend puts it - a Prediction is created there, then
these methods operate on its id.
"""

from __future__ import annotations

from typing import Any

from .._http import AsyncHttpClient, SyncHttpClient


class PredictionsResource:
    def __init__(self, http: SyncHttpClient) -> None:
        self._http = http

    def evaluate(self, prediction_id: str) -> dict[str, Any]:
        """Backtests a prediction against real sales that have since happened."""
        return self._http.request("POST", f"/predictions/{prediction_id}/evaluate")

    def simulate(
        self, prediction_id: str, *, n_simulations: int = 5000, distribution: str = "negative_binomial"
    ) -> dict[str, Any]:
        return self._http.request(
            "POST",
            f"/predictions/{prediction_id}/simulate",
            params={"n_simulations": n_simulations, "distribution": distribution},
        )

    def stockout(self, prediction_id: str, *, current_stock: int | None = None) -> dict[str, Any]:
        return self._http.request(
            "POST", f"/predictions/{prediction_id}/stockout", params={"current_stock": current_stock}
        )

    def inventory_recommendation(
        self,
        prediction_id: str,
        *,
        current_stock: int | None = None,
        lead_time_days: int = 7,
        target_service_level: float = 0.95,
    ) -> dict[str, Any]:
        return self._http.request(
            "POST",
            f"/predictions/{prediction_id}/inventory-recommendation",
            params={
                "current_stock": current_stock,
                "lead_time_days": lead_time_days,
                "target_service_level": target_service_level,
            },
        )

    def optimize_policy(
        self,
        prediction_id: str,
        *,
        current_stock: int | None = None,
        lead_time_days: int = 7,
        target_service_level: float = 0.95,
        n_simulations: int = 1000,
    ) -> dict[str, Any]:
        return self._http.request(
            "POST",
            f"/predictions/{prediction_id}/optimize-policy",
            params={
                "current_stock": current_stock,
                "lead_time_days": lead_time_days,
                "target_service_level": target_service_level,
                "n_simulations": n_simulations,
            },
        )


class AsyncPredictionsResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def evaluate(self, prediction_id: str) -> dict[str, Any]:
        return await self._http.request("POST", f"/predictions/{prediction_id}/evaluate")

    async def simulate(
        self, prediction_id: str, *, n_simulations: int = 5000, distribution: str = "negative_binomial"
    ) -> dict[str, Any]:
        return await self._http.request(
            "POST",
            f"/predictions/{prediction_id}/simulate",
            params={"n_simulations": n_simulations, "distribution": distribution},
        )

    async def stockout(self, prediction_id: str, *, current_stock: int | None = None) -> dict[str, Any]:
        return await self._http.request(
            "POST", f"/predictions/{prediction_id}/stockout", params={"current_stock": current_stock}
        )

    async def inventory_recommendation(
        self,
        prediction_id: str,
        *,
        current_stock: int | None = None,
        lead_time_days: int = 7,
        target_service_level: float = 0.95,
    ) -> dict[str, Any]:
        return await self._http.request(
            "POST",
            f"/predictions/{prediction_id}/inventory-recommendation",
            params={
                "current_stock": current_stock,
                "lead_time_days": lead_time_days,
                "target_service_level": target_service_level,
            },
        )

    async def optimize_policy(
        self,
        prediction_id: str,
        *,
        current_stock: int | None = None,
        lead_time_days: int = 7,
        target_service_level: float = 0.95,
        n_simulations: int = 1000,
    ) -> dict[str, Any]:
        return await self._http.request(
            "POST",
            f"/predictions/{prediction_id}/optimize-policy",
            params={
                "current_stock": current_stock,
                "lead_time_days": lead_time_days,
                "target_service_level": target_service_level,
                "n_simulations": n_simulations,
            },
        )
