"""Sync and async HTTP clients: retries, timeouts, and typed error mapping.

POST/PATCH aren't guaranteed idempotent - retrying one whose response was
lost after the server already processed it (a sync trigger, a CSV import,
a forecast run) risks duplicate side effects, with no idempotency-key
mechanism to protect against it. GET/PUT/DELETE are safe to retry by
default; a caller who knows a specific POST/PATCH call is safe can still
opt in by passing max_retries explicitly on that call.
"""

from __future__ import annotations

import asyncio
import random
import re
import time
from dataclasses import dataclass
from typing import Any

import httpx

from ._config import ClientConfig
from ._errors import ConnectionError_, PredictFlowError, TimeoutError_, error_from_response

_IDEMPOTENT_METHODS = {"GET", "PUT", "DELETE"}
_RETRYABLE_STATUSES = {429, 500, 502, 503, 504}
_SDK_USER_AGENT = "predictflow-python"


def _build_headers(config: ClientConfig, extra: dict[str, str] | None) -> dict[str, str]:
    headers = {
        "Accept": "application/json",
        "User-Agent": _SDK_USER_AGENT,
        **config.default_headers,
        **(extra or {}),
    }
    if config.api_key:
        headers["Authorization"] = f"Bearer {config.api_key}"
    return headers


def _default_max_retries(config: ClientConfig, method: str, max_retries: int | None) -> int:
    if max_retries is not None:
        return max_retries
    return config.max_retries if method in _IDEMPOTENT_METHODS else 0


def _backoff_seconds(attempt: int, retry_after_header: str | None) -> float:
    if retry_after_header:
        try:
            parsed = float(retry_after_header)
            if parsed > 0:
                return parsed
        except ValueError:
            pass
    base_delay = min(0.2 * (2 ** (attempt - 1)), 4.0)
    return base_delay + random.uniform(0, 0.1)


@dataclass(frozen=True)
class FileDownload:
    """A binary export response - content plus the filename/content-type
    the server suggested, so callers can write it to disk without having
    to parse Content-Disposition themselves.
    """

    content: bytes
    content_type: str
    filename: str | None


def _filename_from_content_disposition(header: str | None) -> str | None:
    if not header:
        return None
    match = re.search(r'filename="?([^";]+)"?', header)
    return match.group(1) if match else None


def _finish_download(response: httpx.Response) -> FileDownload:
    if response.status_code >= 400:
        body = _parse_body(response)
        raise error_from_response(
            response.status_code,
            body,
            request_id=response.headers.get("x-request-id"),
            retry_after_header=response.headers.get("retry-after"),
        )
    return FileDownload(
        content=response.content,
        content_type=response.headers.get("content-type", "application/octet-stream"),
        filename=_filename_from_content_disposition(response.headers.get("content-disposition")),
    )


def _parse_body(response: httpx.Response) -> Any:
    if response.status_code == 204 or not response.content:
        return None
    content_type = response.headers.get("content-type", "")
    if "application/json" in content_type:
        try:
            return response.json()
        except ValueError:
            return None
    try:
        return response.text
    except Exception:
        return None


class SyncHttpClient:
    def __init__(self, config: ClientConfig) -> None:
        self._config = config
        self._client = httpx.Client(timeout=config.timeout_seconds)

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> SyncHttpClient:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: Any = None,
        files: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        max_retries: int | None = None,
        timeout_seconds: float | None = None,
    ) -> Any:
        url = f"{self._config.base_url}{path}"
        retries = _default_max_retries(self._config, method, max_retries)
        request_headers = _build_headers(self._config, headers)
        timeout = timeout_seconds if timeout_seconds is not None else self._config.timeout_seconds

        attempt = 0
        while True:
            attempt += 1
            try:
                response = self._client.request(
                    method,
                    url,
                    params=_clean_params(params),
                    json=json,
                    files=files,
                    headers=request_headers,
                    timeout=timeout,
                )
            except httpx.TimeoutException as exc:
                if attempt <= retries:
                    time.sleep(_backoff_seconds(attempt, None))
                    continue
                raise TimeoutError_(f"Request timed out after {timeout}s") from exc
            except httpx.HTTPError as exc:
                if attempt <= retries:
                    time.sleep(_backoff_seconds(attempt, None))
                    continue
                raise ConnectionError_(str(exc)) from exc

            if response.status_code in _RETRYABLE_STATUSES and attempt <= retries:
                time.sleep(_backoff_seconds(attempt, response.headers.get("retry-after")))
                continue

            return _finish(response)

    def request_file(self, method: str, path: str, *, params: dict[str, Any] | None = None) -> FileDownload:
        """Like request(), but for binary export endpoints - returns the raw
        bytes and suggested filename instead of trying to JSON-decode them.
        """
        url = f"{self._config.base_url}{path}"
        response = self._client.request(
            method, url, params=_clean_params(params), headers=_build_headers(self._config, None)
        )
        return _finish_download(response)

    def request_absolute(self, method: str, url: str) -> Any:
        """Like request(), but against an absolute URL instead of one
        joined to config.base_url - only needed for /health, which lives
        at the bare origin rather than under the /api/v1 prefix.
        """
        response = self._client.request(method, url, headers=_build_headers(self._config, None))
        return _finish(response)


class AsyncHttpClient:
    def __init__(self, config: ClientConfig) -> None:
        self._config = config
        self._client = httpx.AsyncClient(timeout=config.timeout_seconds)

    async def aclose(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> AsyncHttpClient:
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        await self.aclose()

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: Any = None,
        files: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        max_retries: int | None = None,
        timeout_seconds: float | None = None,
    ) -> Any:
        url = f"{self._config.base_url}{path}"
        retries = _default_max_retries(self._config, method, max_retries)
        request_headers = _build_headers(self._config, headers)
        timeout = timeout_seconds if timeout_seconds is not None else self._config.timeout_seconds

        attempt = 0
        while True:
            attempt += 1
            try:
                response = await self._client.request(
                    method,
                    url,
                    params=_clean_params(params),
                    json=json,
                    files=files,
                    headers=request_headers,
                    timeout=timeout,
                )
            except httpx.TimeoutException as exc:
                if attempt <= retries:
                    await asyncio.sleep(_backoff_seconds(attempt, None))
                    continue
                raise TimeoutError_(f"Request timed out after {timeout}s") from exc
            except httpx.HTTPError as exc:
                if attempt <= retries:
                    await asyncio.sleep(_backoff_seconds(attempt, None))
                    continue
                raise ConnectionError_(str(exc)) from exc

            if response.status_code in _RETRYABLE_STATUSES and attempt <= retries:
                await asyncio.sleep(_backoff_seconds(attempt, response.headers.get("retry-after")))
                continue

            return _finish(response)

    async def request_file(self, method: str, path: str, *, params: dict[str, Any] | None = None) -> FileDownload:
        url = f"{self._config.base_url}{path}"
        response = await self._client.request(
            method, url, params=_clean_params(params), headers=_build_headers(self._config, None)
        )
        return _finish_download(response)

    async def request_absolute(self, method: str, url: str) -> Any:
        response = await self._client.request(method, url, headers=_build_headers(self._config, None))
        return _finish(response)


def _clean_params(params: dict[str, Any] | None) -> dict[str, Any] | None:
    """Drops None values and leaves everything else (including lists,
    which httpx already serializes as repeated query params) untouched.
    """
    if not params:
        return None
    return {k: v for k, v in params.items() if v is not None}


def _finish(response: httpx.Response) -> Any:
    body = _parse_body(response)
    if response.status_code >= 400:
        raise error_from_response(
            response.status_code,
            body,
            request_id=response.headers.get("x-request-id"),
            retry_after_header=response.headers.get("retry-after"),
        )
    return body


__all__ = ["SyncHttpClient", "AsyncHttpClient", "FileDownload", "PredictFlowError"]
