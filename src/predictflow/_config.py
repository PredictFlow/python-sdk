"""Client configuration - mirrors the JavaScript SDK's config.py for a
consistent feel, independently implemented.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field

DEFAULT_BASE_URL = "https://predictflow.co/api/v1"
DEFAULT_TIMEOUT_SECONDS = 30.0
DEFAULT_MAX_RETRIES = 2


@dataclass(frozen=True)
class ClientConfig:
    """Resolved, immutable client configuration - see `resolve_config`."""

    api_key: str
    base_url: str
    timeout_seconds: float
    max_retries: int
    default_headers: dict[str, str] = field(default_factory=dict)


def resolve_config(
    api_key: str | None = None,
    *,
    base_url: str | None = None,
    timeout_seconds: float | None = None,
    max_retries: int | None = None,
    default_headers: dict[str, str] | None = None,
) -> ClientConfig:
    """Resolves user-provided options into a complete configuration.

    api_key falls back to the PREDICTFLOW_API_KEY environment variable if
    not passed explicitly - matches the JS SDK's same fallback so a
    consumer moving between languages doesn't have to relearn this.
    """
    resolved_key = api_key or os.environ.get("PREDICTFLOW_API_KEY", "")
    resolved_base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")

    return ClientConfig(
        api_key=resolved_key,
        base_url=resolved_base_url,
        timeout_seconds=timeout_seconds if timeout_seconds is not None else DEFAULT_TIMEOUT_SECONDS,
        max_retries=max_retries if max_retries is not None else DEFAULT_MAX_RETRIES,
        default_headers=dict(default_headers) if default_headers else {},
    )
