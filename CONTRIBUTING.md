# Contributing

Thanks for improving Website Revenue Leak Auditor. The project is an evidence-first, read-only local auditor—not a revenue attribution engine or public scanning service.

## Before changing code

- Search existing issues and commits for related work.
- Open an issue before a new audit capability, network behavior change, or report-schema change. Describe the user problem, scope, alternatives, and validation plan.
- For defects, provide a reproducible public test page or synthetic HTML fixture, exact command, expected result, actual result, and redacted logs.
- Keep changes focused. Separate network safety changes from detector tuning and documentation-only changes.

## Development setup

Python 3.10 or newer.

```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Validation

```bash
python -m pytest -q
revenue-auditor --help
python -m compileall -q src tests
```

For URL/network changes, add tests for public/private IPs, malformed authorities, redirects, DNS answers, ports, timeout boundaries, response limits, and same-host enforcement. Prefer mocked transport tests over uncontrolled external requests.

## Engineering expectations

- Network safety checks are product behavior; do not weaken them to simplify a test.
- Explain detector confidence and evidence. Do not claim revenue impact without analytics.
- Keep the tool GET-only; do not add form submission, login, checkout, booking, or messaging behavior without a separate design review.
- Update [docs/SECURITY.md](docs/SECURITY.md) whenever the network threat model or safety limits change.
- Update README/docs when options, report fields, or supported use changes.

## Pull requests

Use the repository PR template. Include problem, scope, exact validation commands/results, and any remaining security limitation. Link an issue for non-trivial work.

## Security disclosure

Do not publish exploitable details, target URLs containing secrets, or unredacted reports. Follow [SECURITY.md](SECURITY.md) for private disclosure.
