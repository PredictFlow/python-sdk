## Summary

<!-- What does this PR change, and why? -->

## Type of change

- [ ] Bug fix
- [ ] New feature / new resource or method
- [ ] Breaking change (anything that changes an existing public method's signature or behavior)
- [ ] Docs only

## Verified against the real API

<!--
This SDK wraps the real PredictFlow API - every endpoint it calls should
correspond to a real one, including whether its parameters are query
params or a JSON body (this has already been wrong once during initial
development and only caught by checking the backend source directly).
-->

- [ ] Every new/changed HTTP call matches a real backend endpoint (method, path, query-vs-body, and response shape)
- [ ] No new runtime dependency was introduced without a prior issue discussing it

## Test plan

- [ ] `ruff check .` passes
- [ ] `mypy src/predictflow` passes
- [ ] `pytest` passes, and I added/updated tests covering this change

## Linked issue

Closes #
