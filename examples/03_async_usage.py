"""The async client mirrors the sync one method-for-method - use it inside
an existing asyncio application (a FastAPI/Starlette handler, a worker
task) instead of blocking the event loop with the sync client.
"""

import asyncio
import os

from predictflow import AsyncPredictFlow


async def main() -> None:
    async with AsyncPredictFlow(api_key=os.environ["PREDICTFLOW_API_KEY"]) as client:
        stores = await client.stores.list()
        if not stores:
            print("No connected stores yet.")
            return

        # Fetch KPIs for every store concurrently instead of one at a time.
        kpi_results = await asyncio.gather(*(client.analytics.kpis(store_id=store["id"]) for store in stores))

        for store, kpis in zip(stores, kpi_results):
            current = kpis["current"]
            growth_pct = kpis["growth"]["revenue_growth_pct"]
            growth_label = f"{growth_pct:+.1f}%" if growth_pct is not None else "n/a"
            print(f"{store['name']}: ${current['revenue']} revenue ({growth_label} vs prior period)")


if __name__ == "__main__":
    asyncio.run(main())
