import pytest

from predictflow._config import resolve_config
from predictflow._errors import NotFoundError, RateLimitError, ValidationError
from predictflow._http import AsyncHttpClient, SyncHttpClient

BASE_URL = "https://predictflow.test/api/v1"


def _config(**overrides):
    overrides.setdefault("max_retries", 2)
    return resolve_config(api_key="pk_live_test", base_url=BASE_URL, **overrides)


def test_authorization_and_accept_headers_are_sent(httpx_mock):
    httpx_mock.add_response(json={"id": "store_1"})
    client = SyncHttpClient(_config())

    client.request("GET", "/stores/store_1")

    request = httpx_mock.get_requests()[0]
    assert request.headers["authorization"] == "Bearer pk_live_test"
    assert request.headers["accept"] == "application/json"
    client.close()


def test_get_retries_on_500_and_succeeds(httpx_mock):
    httpx_mock.add_response(status_code=500, json={"detail": "Temporary failure"})
    httpx_mock.add_response(json={"recovered": True})
    client = SyncHttpClient(_config())

    result = client.request("GET", "/health")

    assert result == {"recovered": True}
    assert len(httpx_mock.get_requests()) == 2
    client.close()


def test_post_does_not_auto_retry_on_500(httpx_mock):
    """POST isn't guaranteed idempotent - retrying one whose response was
    lost after the server already processed it risks duplicate side
    effects, so it must not retry unless the caller opts in per-call.
    """
    httpx_mock.add_response(status_code=500, json={"detail": "Temporary failure"})
    client = SyncHttpClient(_config())

    with pytest.raises(Exception):
        client.request("POST", "/predictions/pred_1/evaluate")

    assert len(httpx_mock.get_requests()) == 1
    client.close()


def test_post_retries_when_max_retries_explicitly_passed(httpx_mock):
    httpx_mock.add_response(status_code=500, json={"detail": "Temporary failure"})
    httpx_mock.add_response(json={"recovered": True})
    client = SyncHttpClient(_config())

    result = client.request("POST", "/predictions/pred_1/evaluate", max_retries=1)

    assert result == {"recovered": True}
    assert len(httpx_mock.get_requests()) == 2
    client.close()


def test_404_raises_not_found_error(httpx_mock):
    httpx_mock.add_response(status_code=404, json={"detail": "Store not found"})
    client = SyncHttpClient(_config())

    with pytest.raises(NotFoundError, match="Store not found"):
        client.request("GET", "/stores/missing")
    client.close()


def test_422_with_pydantic_array_detail_raises_readable_validation_error(httpx_mock):
    httpx_mock.add_response(
        status_code=422,
        json={"detail": [{"msg": "Value error, horizon_days must be positive"}]},
    )
    client = SyncHttpClient(_config())

    with pytest.raises(ValidationError, match="horizon_days must be positive"):
        client.request("POST", "/products/prod_1/forecast", max_retries=0)
    client.close()


def test_429_carries_retry_after_and_is_retried(httpx_mock):
    httpx_mock.add_response(status_code=429, headers={"retry-after": "0"}, json={"detail": "Rate limited"})
    httpx_mock.add_response(json={"ok": True})
    client = SyncHttpClient(_config())

    result = client.request("GET", "/products")

    assert result == {"ok": True}
    client.close()


def test_max_retries_exhausted_raises_rate_limit_error(httpx_mock):
    httpx_mock.add_response(
        status_code=429, headers={"retry-after": "0"}, json={"detail": "Rate limited"}, is_reusable=True
    )
    client = SyncHttpClient(_config(max_retries=1))

    with pytest.raises(RateLimitError):
        client.request("GET", "/products")

    assert len(httpx_mock.get_requests()) == 2  # 1 original + 1 retry
    client.close()


def test_delete_returns_none_on_204(httpx_mock):
    httpx_mock.add_response(status_code=204)
    client = SyncHttpClient(_config())

    result = client.request("DELETE", "/stores/store_1")

    assert result is None
    client.close()


async def test_async_client_get_retries_on_502(httpx_mock):
    httpx_mock.add_response(status_code=502, json={"detail": "Bad gateway"})
    httpx_mock.add_response(json={"recovered": True})
    client = AsyncHttpClient(_config())

    result = await client.request("GET", "/health")

    assert result == {"recovered": True}
    await client.aclose()


async def test_async_client_post_does_not_auto_retry(httpx_mock):
    httpx_mock.add_response(status_code=503, json={"detail": "Unavailable"})
    client = AsyncHttpClient(_config())

    with pytest.raises(Exception):
        await client.request("POST", "/predictions/pred_1/evaluate")

    assert len(httpx_mock.get_requests()) == 1
    await client.aclose()


def test_query_params_with_none_values_are_dropped(httpx_mock):
    httpx_mock.add_response(json={"ok": True})
    client = SyncHttpClient(_config())

    client.request("GET", "/analytics/kpis", params={"days": 30, "store_id": None})

    request = httpx_mock.get_requests()[0]
    assert "store_id" not in str(request.url)
    assert "days=30" in str(request.url)
    client.close()
