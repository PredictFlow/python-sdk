# PredictFlow Python SDK

[![PyPI version](https://img.shields.io/pypi/v/predictflow.svg)](https://pypi.org/project/predictflow/)
[![Python versions](https://img.shields.io/pypi/pyversions/predictflow.svg)](https://pypi.org/project/predictflow/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

The official Python SDK for [PredictFlow](https://predictflow.co) — demand forecasting, inventory intelligence, and pricing optimization for Shopify and WooCommerce stores.

---

## Features

- **Sync and async** — `PredictFlow` and `AsyncPredictFlow` share the same method names and shapes; pick whichever fits your codebase.
- **One dependency** — [`httpx`](https://www.python-httpx.org/), for both sync and async HTTP in a single library. Nothing else.
- **Typed** — full type hints on every method signature, `py.typed` marker included for `mypy`/`pyright`. Response *bodies* are typed as `dict`/`list` rather than full schemas for now — see [Typing](#typing) below for why.
- **Automatic retries** — safe by default: `GET`/`PUT`/`DELETE` retry on `429`/5xx with backoff, `POST`/`PATCH` don't (they aren't guaranteed idempotent) unless you explicitly opt a call in.
- **Typed errors** — every non-2xx response raises a specific `PredictFlowError` subclass, never a bare `httpx` exception.

## Installation

```bash
pip install predictflow
```

## Quickstart

```python
from predictflow import PredictFlow

client = PredictFlow(api_key="pk_live_...")  # or set PREDICTFLOW_API_KEY

stores = client.stores.list()
forecast = client.products.forecast(product_id="prod_123", horizon_days=30)
print(forecast["forecast_data"])

client.close()
```

Or as a context manager, which closes the connection pool for you:

```python
with PredictFlow(api_key="pk_live_...") as client:
    stores = client.stores.list()
```

### Async

```python
import asyncio
from predictflow import AsyncPredictFlow

async def main():
    async with AsyncPredictFlow(api_key="pk_live_...") as client:
        forecast = await client.products.forecast("prod_123", horizon_days=30)
        print(forecast["forecast_data"])

asyncio.run(main())
```

## Resources

| Resource | Covers |
|---|---|
| `client.stores` | Connect/manage stores, trigger syncs, import CSV catalogs and orders |
| `client.products` | Catalog, inventory health, ABC analysis, forecasting, cost/margin, competitor prices |
| `client.predictions` | Simulation, stockout risk, and inventory policy for an existing forecast |
| `client.analytics` | KPIs, revenue trends, day-of-week seasonality, product growth, projections |
| `client.pricing` | Elasticity, optimization, simulation, cross-elasticity, batch repricing |
| `client.scenarios` | What-if scenario planning and side-by-side comparisons |
| `client.alerts` | Alert rules, templates, and evaluation history |
| `client.exports` | CSV/XLSX/PDF exports — returns a `FileDownload` (raw bytes + filename), not JSON |

See [`examples/`](examples/) for runnable scripts covering each of these.

## Error handling

```python
from predictflow import (
    PredictFlow,
    AuthenticationError,
    NotFoundError,
    ValidationError,
    RateLimitError,
    PredictFlowError,
)

client = PredictFlow(api_key="pk_live_...")

try:
    forecast = client.products.forecast("prod_missing")
except AuthenticationError:
    print("Check your API key")
except NotFoundError:
    print("Product not found")
except RateLimitError as exc:
    print(f"Rate limited, retry after {exc.retry_after_seconds}s")
except ValidationError as exc:
    print(f"Invalid request: {exc.message}")
except PredictFlowError as exc:
    print(f"API error [{exc.status}]: {exc.message}")
```

## Client options

```python
client = PredictFlow(
    api_key="pk_live_...",       # or PREDICTFLOW_API_KEY env var
    base_url="https://predictflow.co/api/v1",  # default
    timeout_seconds=30.0,
    max_retries=2,               # applies to GET/PUT/DELETE by default
    default_headers={"X-Custom-App": "my-integration/1.0"},
)
```

Per-call overrides work the same way on every resource method via the underlying client - e.g. pass `max_retries=1` to opt a specific `POST` call into retries if you know that particular endpoint is safe to retry.

## Typing

Every method's *parameters* are fully typed and checked by `mypy --strict`. Response *bodies* are typed as plain `dict[str, Any]` / `list[dict[str, Any]]` rather than full per-endpoint schemas, on purpose: adding a dependency like `pydantic` (or hand-written `TypedDict`s for ~70 endpoints) to validate responses is a real drift risk of its own - a schema that's wrong is worse than no schema, since it fails silently instead of just being untyped. This may be layered in incrementally in a future minor version without breaking anything, since it would only add stricter typing, not change runtime behavior.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Security

See [SECURITY.md](SECURITY.md) — please don't open a public issue for a vulnerability.

## License

MIT © [PredictFlow](https://predictflow.co)
