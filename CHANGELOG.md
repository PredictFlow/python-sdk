# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); this project follows
[Semantic Versioning](https://semver.org/) once it reaches 1.0.0 - see
[CONTRIBUTING.md](CONTRIBUTING.md#versioning--breaking-changes) for what that
means before then.

## [0.1.0] - 2026-09-30

Initial release.

### Added

- `PredictFlow` (sync) and `AsyncPredictFlow` clients, sharing the same
  8-resource surface: stores, products, predictions, analytics, pricing,
  scenarios, alerts, exports.
- Typed error hierarchy (`PredictFlowError` and subclasses), including
  unwrapping FastAPI/Pydantic's array-shaped `detail` on 422s into a
  readable message.
- Automatic retries with backoff on `GET`/`PUT`/`DELETE` for `429`/5xx
  responses; `POST`/`PATCH` don't retry by default since they aren't
  guaranteed idempotent (a caller can opt a specific call in via
  `max_retries`).
- One runtime dependency (`httpx`), for both sync and async HTTP.
- `FileDownload` for the exports resource - raw bytes + filename, not a
  failed JSON decode of a spreadsheet.
- Full type hints, `py.typed` marker, `mypy --strict` clean.

Every endpoint this SDK calls was verified against the real backend before
release (see [CONTRIBUTING.md](CONTRIBUTING.md)) - including a live smoke
test against a running PredictFlow instance, not just against the OpenAPI
schema.
