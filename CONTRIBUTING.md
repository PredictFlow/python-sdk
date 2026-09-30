# Contributing to predictflow (Python)

This is a thin, typed client over the real PredictFlow API. The most valuable thing you can bring to a PR is confidence that what you wrote actually matches what the backend does.

## Ground rule: verify against the real API

Every method in this SDK should correspond to a real, working PredictFlow endpoint - method, path, and whether its parameters are query params or a JSON body (FastAPI endpoints mix both, inconsistently, depending on the specific route - don't assume). Check it against the backend's OpenAPI schema or the actual endpoint source before opening a PR, not against what seems plausible. The PR template has a checkbox for this because it's already prevented a real bug during this SDK's own development (several default values and one query-vs-body assumption were wrong on the first pass and only caught by checking the backend source directly).

If you're proposing a resource or method for a capability you *think* PredictFlow should have but haven't confirmed exists, open an issue first rather than a PR.

## Getting set up

```bash
git clone https://github.com/PredictFlow/python-sdk.git
cd python-sdk
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

```bash
pytest                    # run tests
mypy src/predictflow       # strict type check
ruff check .               # lint
ruff format .              # format
```

All three should be clean before you open a PR - CI runs them on Python 3.9 through 3.13 and it's a required check.

## Making a change

1. Branch from `main`.
2. Keep the diff focused - one logical change per PR.
3. If you're adding or changing a resource method:
   - Match the existing pattern in `src/predictflow/resources/*.py` - a sync class and an `Async`-prefixed class in the same file, both thin wrappers around `SyncHttpClient`/`AsyncHttpClient`, co-located so they can't silently drift apart from each other.
   - Add a test in `tests/` using the `httpx_mock` fixture (`pytest-httpx`) - assert the actual method/path/params sent, not just that the call doesn't raise.
   - Update the README's resource table if it's a new resource, or an example if it's a good illustration of something not yet covered.
4. This package has exactly one runtime dependency (`httpx`) on purpose. Don't add another without opening an issue first.
5. Watch for the `list` name collision: if a resource class defines a method literally named `list` (several do, matching the API's own naming), any *later* method in that same class that needs to reference the builtin `list[...]` type will have it shadowed by the method - `mypy` will report this as `"X.list" is not valid as a type`, not as an obvious "name shadowing" error. Use `typing.List[...]` (capital L) with a `# noqa: UP006` comment for those specific annotations - see `stores.py`/`products.py` for the existing pattern.
6. Commit messages: a plain, present-tense description of what changed and why is enough. No enforced format.
7. Open the PR against `main` and fill in the template.

## Versioning & breaking changes

This package follows [Semantic Versioning](https://semver.org/), with the usual pre-1.0 caveat: anything in a `0.x` release can technically break between minor versions, but we still treat it like a real breaking-change bump (`0.1.x` → `0.2.0`), not a patch, once it's past initial development. Concretely, a **breaking change** is any of:

- Removing or renaming a public export (a class, a resource method, an error class).
- Changing a method's required parameters, or changing what an existing parameter means.
- Changing a response's shape in a way that breaks a reasonable consumer (removing a key, changing a value's type) - adding a new key is not breaking.
- Changing default behavior a consumer could reasonably have been relying on (e.g. which HTTP methods retry by default).

Not breaking: internal refactors, dependency bumps, new resource methods, new optional parameters, README/example changes, adding a new exception subclass (as long as it still extends `PredictFlowError`, existing `except` blocks keep working).

Every release gets a [CHANGELOG.md](CHANGELOG.md) entry - see existing entries for the format. If your PR is user-facing, mention what changed under `## [Unreleased]` (add that heading at the top of the file if it doesn't exist yet) rather than leaving the changelog for the maintainer to reconstruct from commit messages at release time.

## Review & merge

PRs require passing CI and a code owner review before merging - `main` is protected, so nobody merges without going through this, maintainers included.

## Reporting a bug vs. a vulnerability

Regular bugs (wrong types, a broken example, a method that doesn't match the API) → open a GitHub issue.

Anything security-related → see [SECURITY.md](SECURITY.md) instead of a public issue.

## Code of conduct

Be respectful, assume good faith, keep disagreements about the code and not the person.
