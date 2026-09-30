"""Forecast demand for a product, check stockout risk, and get a reorder recommendation."""

import os

from predictflow import PredictFlow


def main() -> None:
    client = PredictFlow(api_key=os.environ["PREDICTFLOW_API_KEY"])

    product_id = os.environ["PREDICTFLOW_EXAMPLE_PRODUCT_ID"]

    prediction = client.products.forecast(product_id, horizon_days=30, model="prophet")
    print(f"Prediction {prediction['id']} generated at {prediction['generated_at']}")

    stockout = client.predictions.stockout(prediction["id"], current_stock=40)
    probability = stockout["total_stockout_probability"]
    print(f"Probability of stockout within {stockout['horizon_days']} days: {probability:.1%}")
    if stockout["expected_days_until_stockout"] is not None:
        print(f"Expected days until stockout: {stockout['expected_days_until_stockout']:.1f}")

    recommendation = client.predictions.inventory_recommendation(prediction["id"], current_stock=40, lead_time_days=7)
    detail = recommendation["recommendation"]
    action = recommendation["action"]
    print(f"Reorder point: {detail['reorder_point']} units")
    print(f"Recommended order quantity: {detail['reorder_quantity']} units")
    print(f"Should reorder now: {action['should_reorder_now']} (urgency: {action['urgency']})")

    client.close()


if __name__ == "__main__":
    main()
