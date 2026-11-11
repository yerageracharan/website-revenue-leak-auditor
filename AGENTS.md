# Agent Instructions

These instructions apply across Website Revenue Leak Auditor.

## Product and safety invariants

- Audits are read-only and intended for sites the operator owns or is authorized to assess.
- Preserve URL validation, DNS checks, redirect restrictions, request timeouts, page-count limits, response-size limits, and same-host scope.
- Never turn static HTML heuristics into claims about actual lost revenue, conversion lift, or user behavior without analytics evidence.
- Do not present a 404/5xx observation as permanent; describe it as an observation at audit time.
- Respect the documented DNS-rebinding limitation: this version is not a hosted arbitrary-URL scanning service.

## Repository map

- `src/revenue_leak_auditor/`: URL safety, HTTP fetching, HTML checks, scoring, report rendering, and CLI.
- `tests/`: mocked network and detector regression tests.
- `docs/SECURITY.md`: canonical security model and operational limitations.
- `docs/visuals/`: explanatory diagrams; implementation and tests remain authoritative.

## Working rules

- Read the canonical security model before changing URL fetching or redirects.
- Validate user-controlled URLs before any network request.
- Do not inherit environment proxy settings or follow redirects without revalidating policy.
- Keep crawl/page/response/time limits explicit and bounded.
- Avoid tests that scan arbitrary real targets. Use mocks or sites explicitly intended for testing.
- Distinguish observed facts from detector interpretation and business impact.
- Never state that the auditor measured conversion, sales, or lost revenue unless such data is explicitly ingested and validated.

## Validation

```bash
python -m pytest -q
revenue-auditor --help
python -m compileall -q src tests
```
