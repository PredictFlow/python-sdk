"""Typed error hierarchy for predictable error handling.

Mirrors the same shape as the JavaScript SDK's error hierarchy so the two
feel consistent to anyone using both, but this is its own implementation -
not a port of the TypeScript code.
"""

from __future__ import annotations

from typing import Any


class PredictFlowError(Exception):
    """Base class for all errors originating from the PredictFlow SDK."""

    def __init__(
        self,
        message: str,
        *,
        status: int | None = None,
        code: str | None = None,
        request_id: str | None = None,
        details: Any = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status = status
        self.code = code
        self.request_id = request_id
        self.details = details

    def __repr__(self) -> str:
        return f"{type(self).__name__}(message={self.message!r}, status={self.status!r})"


class AuthenticationError(PredictFlowError):
    """401 Unauthorized or 403 Forbidden."""


class NotFoundError(PredictFlowError):
    """404 Not Found."""


class ValidationError(PredictFlowError):
    """400 Bad Request or 422 Unprocessable Entity."""


class RateLimitError(PredictFlowError):
    """429 Too Many Requests."""

    def __init__(self, *args: Any, retry_after_seconds: float | None = None, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.retry_after_seconds = retry_after_seconds


class InternalServerError(PredictFlowError):
    """500, 502, 503, or 504."""


class TimeoutError_(PredictFlowError):
    """A request timed out. Named with a trailing underscore to avoid
    shadowing the builtin TimeoutError while keeping the same name every
    other PredictFlow error uses.
    """


class ConnectionError_(PredictFlowError):
    """A connection could not be established, or the network is unreachable."""


def _unwrap_detail(detail: Any) -> str | None:
    """FastAPI/Pydantic validation failures (422s) return `detail` as a
    list of {msg, loc, type} objects, not a string - unwrapping it here
    means a ValidationError's .message is always the real field-level
    reason instead of a generic "request failed with status 422".
    Pydantic prefixes a model-level ValueError's message with
    "Value error, " - stripped here as an implementation detail.
    """
    if isinstance(detail, str):
        return detail
    if isinstance(detail, list):
        messages = []
        for item in detail:
            if isinstance(item, dict) and isinstance(item.get("msg"), str):
                msg = item["msg"]
                if msg.startswith("Value error, "):
                    msg = msg[len("Value error, ") :]
                messages.append(msg)
        if messages:
            return " ".join(messages)
    return None


_STATUS_TO_ERROR: dict[int, type[PredictFlowError]] = {
    401: AuthenticationError,
    403: AuthenticationError,
    404: NotFoundError,
    400: ValidationError,
    422: ValidationError,
    429: RateLimitError,
    500: InternalServerError,
    502: InternalServerError,
    503: InternalServerError,
    504: InternalServerError,
}


def error_from_response(
    status: int,
    body: Any,
    *,
    request_id: str | None = None,
    retry_after_header: str | None = None,
) -> PredictFlowError:
    """Maps an HTTP status code and response payload to the appropriate
    PredictFlowError subclass.
    """
    message = f"API request failed with status {status}"
    code: str | None = None
    details: Any = None

    if isinstance(body, dict):
        unwrapped = _unwrap_detail(body.get("detail"))
        if unwrapped:
            message = unwrapped
        elif isinstance(body.get("message"), str):
            message = body["message"]
        if "detail" in body:
            details = body["detail"]
        if isinstance(body.get("code"), str):
            code = body["code"]

    error_cls = _STATUS_TO_ERROR.get(status, PredictFlowError)

    if error_cls is RateLimitError:
        retry_after_seconds: float | None = None
        if retry_after_header:
            try:
                retry_after_seconds = float(retry_after_header)
            except ValueError:
                retry_after_seconds = None
        return RateLimitError(
            message,
            status=status,
            code=code,
            request_id=request_id,
            details=details,
            retry_after_seconds=retry_after_seconds,
        )

    return error_cls(message, status=status, code=code, request_id=request_id, details=details)
