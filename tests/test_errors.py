from predictflow._errors import (
    AuthenticationError,
    InternalServerError,
    NotFoundError,
    RateLimitError,
    ValidationError,
    error_from_response,
)


def test_maps_401_to_authentication_error():
    err = error_from_response(401, {"detail": "Invalid or expired API key"})
    assert isinstance(err, AuthenticationError)
    assert err.message == "Invalid or expired API key"
    assert err.status == 401


def test_maps_404_to_not_found_error():
    err = error_from_response(404, {"detail": "Store not found"})
    assert isinstance(err, NotFoundError)


def test_unwraps_pydantic_array_detail_into_readable_message():
    """422s return `detail` as a list of {msg, loc, type} objects, not a
    string - this is the exact bug pattern that has bitten the main
    PredictFlow frontend before; the fix must hold here too.
    """
    detail = [
        {"loc": ["body", "horizon_days"], "msg": "Value error, horizon_days must be positive", "type": "value_error"}
    ]
    err = error_from_response(422, {"detail": detail})
    assert isinstance(err, ValidationError)
    assert err.message == "horizon_days must be positive"
    assert err.details == detail


def test_joins_multiple_validation_messages():
    err = error_from_response(
        422,
        {"detail": [{"msg": "field a is required"}, {"msg": "field b must be positive"}]},
    )
    assert err.message == "field a is required field b must be positive"


def test_falls_back_to_generic_message_when_body_has_no_detail():
    err = error_from_response(500, {})
    assert isinstance(err, InternalServerError)
    assert err.message == "API request failed with status 500"


def test_rate_limit_error_carries_retry_after_seconds():
    err = error_from_response(429, {"detail": "Rate limit exceeded"}, retry_after_header="30")
    assert isinstance(err, RateLimitError)
    assert err.retry_after_seconds == 30.0


def test_unparseable_retry_after_is_ignored_not_raised():
    err = error_from_response(429, {"detail": "Rate limit exceeded"}, retry_after_header="not-a-number")
    assert isinstance(err, RateLimitError)
    assert err.retry_after_seconds is None
