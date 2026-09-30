"""Get a price optimization suggestion, simulate a specific price, and
save a dead-stock report to disk.
"""

import os

from predictflow import PredictFlow


def main() -> None:
    client = PredictFlow(api_key=os.environ["PREDICTFLOW_API_KEY"])

    product_id = os.environ["PREDICTFLOW_EXAMPLE_PRODUCT_ID"]
    store_id = os.environ["PREDICTFLOW_EXAMPLE_STORE_ID"]

    optimized = client.pricing.optimize(product_id, strategy="maximize_profit")
    print(f"Current price: ${optimized['current_price']}")
    print(f"Recommended price: ${optimized['recommended_price']} ({optimized['price_change_pct']:+.1f}%)")
    print(f"Expected profit change: {optimized['expected_profit_change_pct']}%")

    simulated = client.pricing.simulate(product_id, new_price=optimized["recommended_price"] - 1)
    print(f"If priced at ${simulated['new_price']} instead: {simulated['expected_revenue_change_pct']:+.1f}% revenue")

    dead_stock = client.exports.dead_stock(store_id, format="csv")
    out_path = dead_stock.filename or "dead-stock-export.csv"
    with open(out_path, "wb") as f:
        f.write(dead_stock.content)
    print(f"Saved {out_path} ({len(dead_stock.content)} bytes)")

    client.close()


if __name__ == "__main__":
    main()
