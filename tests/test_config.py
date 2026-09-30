from predictflow._config import DEFAULT_BASE_URL, DEFAULT_MAX_RETRIES, DEFAULT_TIMEOUT_SECONDS, resolve_config


def test_defaults():
    config = resolve_config()
    assert config.base_url == DEFAULT_BASE_URL
    assert config.timeout_seconds == DEFAULT_TIMEOUT_SECONDS
    assert config.max_retries == DEFAULT_MAX_RETRIES
    assert config.api_key == ""


def test_explicit_api_key_wins_over_env(monkeypatch):
    monkeypatch.setenv("PREDICTFLOW_API_KEY", "pk_live_from_env")
    config = resolve_config("pk_live_explicit")
    assert config.api_key == "pk_live_explicit"


def test_falls_back_to_env_var(monkeypatch):
    monkeypatch.setenv("PREDICTFLOW_API_KEY", "pk_live_from_env")
    config = resolve_config()
    assert config.api_key == "pk_live_from_env"


def test_trailing_slash_stripped_from_base_url():
    config = resolve_config(base_url="https://predictflow.co/api/v1/")
    assert config.base_url == "https://predictflow.co/api/v1"


def test_custom_headers_are_copied_not_aliased():
    headers = {"X-Custom": "1"}
    config = resolve_config(default_headers=headers)
    headers["X-Custom"] = "mutated"
    assert config.default_headers == {"X-Custom": "1"}
