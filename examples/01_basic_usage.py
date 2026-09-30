"""Connect a store, list products, and check inventory health."""

import os

from predictflow import PredictFlow


def main() -> None:
    client = PredictFlow(api_key=os.environ["PREDICTFLOW_API_KEY"])

    stores = client.stores.list()
    print(f"Connected stores: {len(stores)}")
    if not stores:
        return

    store = stores[0]
    print(f"Using store: {store['name']} ({store['id']})")

    health = client.products.inventory_health(store["id"])
    print(f"Healthy: {health['healthy']} ({health['healthy_pct']:.1f}%)")
    print(f"Low stock: {health['low_stock']} ({health['low_stock_pct']:.1f}%)")
    print(f"Out of stock: {health['out_of_stock']} ({health['out_of_stock_pct']:.1f}%)")

    low_stock = client.products.low_stock(store["id"])
    print(f"Products below the low-stock threshold ({low_stock['threshold']}): {len(low_stock['items'])}")

    client.close()


if __name__ == "__main__":
    main()
