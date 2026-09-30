"""Spot-checks that resource methods build the right method/path/params -
one per resource module, not exhaustive coverage of every method (that's
what the endpoint-vs-openapi.json verification during development was
for; these guard against regressions in that verified mapping).
"""

from predictflow import PredictFlow


def _client(httpx_mock):
    httpx_mock.add_response(json={})
    return PredictFlow(api_key="pk_live_test", base_url="https://predictflow.test/api/v1")


def test_stores_sync_sends_full_as_query_param(httpx_mock):
    client = _client(httpx_mock)
    client.stores.sync("store_1", full=True)
    request = httpx_mock.get_requests()[0]
    assert request.method == "POST"
    assert str(request.url) == "https://predictflow.test/api/v1/stores/store_1/sync?full=true"
    client.close()


def test_products_forecast_sends_options_as_query_not_body(httpx_mock):
    """These POST endpoints take FastAPI Query() params, not a JSON body -
    verified against the real backend endpoint signature, not assumed.
    """
    client = _client(httpx_mock)
    client.products.forecast("prod_1", horizon_days=14, model="xgboost")
    request = httpx_mock.get_requests()[0]
    assert request.method == "POST"
    assert "horizon_days=14" in str(request.url)
    assert "model=xgboost" in str(request.url)
    assert request.content == b""
    client.close()


def test_products_update_cost_sends_body_not_query(httpx_mock):
    client = _client(httpx_mock)
    client.products.update_cost("prod_1", cogs=5.5)
    request = httpx_mock.get_requests()[0]
    assert request.method == "PATCH"
    assert "cogs" not in str(request.url)
    assert b'"cogs":5.5' in request.content
    client.close()


def test_predictions_stockout_path_and_params(httpx_mock):
    client = _client(httpx_mock)
    client.predictions.stockout("pred_1", current_stock=42)
    request = httpx_mock.get_requests()[0]
    assert str(request.url) == "https://predictflow.test/api/v1/predictions/pred_1/stockout?current_stock=42"
    client.close()


def test_pricing_cross_elasticity_path(httpx_mock):
    client = _client(httpx_mock)
    client.pricing.cross_elasticity("prod_1", "prod_2", lookback_days=60)
    request = httpx_mock.get_requests()[0]
    assert request.method == "GET"
    assert "/pricing/product/prod_1/cross-elasticity/prod_2" in str(request.url)
    assert "lookback_days=60" in str(request.url)
    client.close()


def test_scenarios_create_sends_json_body(httpx_mock):
    client = _client(httpx_mock)
    client.scenarios.create("store_1", name="Holiday markdown", price_change_pct=-10.0)
    request = httpx_mock.get_requests()[0]
    assert request.method == "POST"
    assert str(request.url) == "https://predictflow.test/api/v1/stores/store_1/scenarios"
    assert b'"name":"Holiday markdown"' in request.content
    client.close()


def test_scenarios_compare_sends_ids_as_query_params(httpx_mock):
    client = _client(httpx_mock)
    client.scenarios.compare("store_1", "scen_a", "scen_b")
    request = httpx_mock.get_requests()[0]
    assert "scenario_a_id=scen_a" in str(request.url)
    assert "scenario_b_id=scen_b" in str(request.url)
    client.close()


def test_alerts_create_rule_body(httpx_mock):
    client = _client(httpx_mock)
    client.alerts.create_rule("store_1", metric_type="low_stock", threshold=10)
    request = httpx_mock.get_requests()[0]
    assert str(request.url) == "https://predictflow.test/api/v1/stores/store_1/alert-rules"
    assert b'"metric_type":"low_stock"' in request.content
    client.close()


def test_exports_returns_file_download_not_json(httpx_mock):
    httpx_mock.add_response(
        content=b"sku,name\nSKU-1,Widget\n",
        headers={
            "content-type": "text/csv",
            "content-disposition": 'attachment; filename="products.csv"',
        },
    )
    client = PredictFlow(api_key="pk_live_test", base_url="https://predictflow.test/api/v1")

    result = client.exports.products("store_1", format="csv")

    assert result.content == b"sku,name\nSKU-1,Widget\n"
    assert result.filename == "products.csv"
    assert result.content_type == "text/csv"
    client.close()


def test_stores_import_products_csv_sends_multipart_file(httpx_mock):
    client = _client(httpx_mock)
    client.stores.import_products_csv("store_1", "sku,name\nSKU-1,Widget\n", filename="my-products.csv")
    request = httpx_mock.get_requests()[0]
    assert b'filename="my-products.csv"' in request.content
    assert b"SKU-1,Widget" in request.content
    client.close()
