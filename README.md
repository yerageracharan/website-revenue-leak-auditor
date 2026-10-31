# Website Revenue Leak Auditor

**Agent #4 in the 200 AI agents build-in-public series.** A small, evidence-first tool that inspects a public website and turns observable technical and UX issues into a prioritised audit report.

> **Current status:** working Python CLI MVP. It crawls a bounded number of same-host HTML pages, runs deterministic static checks, and exports Markdown (plus optional JSON). It does not yet run Lighthouse, render JavaScript-heavy pages, or estimate actual lost revenue.

<p align="center">
  <strong>Inspect → Verify → Prioritise → Recommend</strong><br/>
  <sub>No fabricated scores. No invented revenue numbers. Evidence attached to every finding.</sub>
</p>

## What it does today

| Area | Checks in the current MVP | What the result means |
|---|---|---|
| SEO | Missing/long title, missing meta description, missing canonical | A static HTML observation, not a ranking prediction |
| Content structure | Missing or multiple H1 headings | A page-structure heuristic |
| Mobile usability | Missing viewport meta tag | A signal to test the page at real mobile widths |
| Accessibility | Images without an `alt` attribute | An attribute-level check, not a full accessibility audit |
| Conversion | No common CTA wording found in links/buttons | A low-confidence text heuristic; custom/icon controls can be missed |
| Availability | Crawled pages returning HTTP 4xx/5xx | The observed response for the requested URL at audit time |

Every finding includes the affected URL, observed evidence, impact heuristic, confidence, recommendation, and a way to verify the fix. If a check cannot run, it is reported as not inspected or noted as a limitation rather than guessed.

## Quick start

Requires Python 3.10 or newer.

```bash
git clone https://github.com/yerageracharan/website-revenue-leak-auditor.git
cd website-revenue-leak-auditor
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

python -m pip install -e ".[dev]"
revenue-auditor https://example.com
```

The command writes `audit-report.md` in the current directory. To also save machine-readable output:

```bash
revenue-auditor https://example.com --max-pages 8 --output reports/example-audit.md --json reports/example-audit.json
```

Options:

```text
revenue-auditor URL [--max-pages 1..15] [--timeout 2..30]
                   [--output report.md] [--json report.json]
```

## Example finding

```text
[Medium impact] Viewport configuration is missing
Page: https://example.com/services
Confidence: High
Evidence: No meta name="viewport" tag was found in the inspected HTML.
Why it may matter: The mobile page may render at an unexpected scale.
Recommended action: Add a responsive viewport declaration and test mobile widths.
How to verify: Inspect the page at common phone viewport widths.
```

This is an illustrative shape only, not a claim about `example.com`. A synthetic example report lives in [`examples/sample-audit-report.md`](examples/sample-audit-report.md).

## Architecture

```text
URL
 │
 ▼
URL + public-address validation
 │
 ▼
Bounded same-host crawler ───► HTML response (2 MB cap)
 │                                      │
 ▼                                      ▼
Page queue + status records       BeautifulSoup parser
                                        │
                                        ▼
                              Deterministic check functions
                                        │
                                        ▼
                          Structured findings + evidence
                                        │
                                        ▼
                             Markdown / JSON report
```

The current release has no LLM dependency. Deterministic checks establish what was observed; a future optional AI layer may explain or group those facts but must never invent findings, metrics, or business outcomes.

## Run the tests

```bash
python -m pip install -e ".[dev]"
pytest
```

Tests use mocked DNS and HTTP responses. They do not crawl live websites and do not require API keys.

## Repository map

```text
.
├── .claude/skills/website-revenue-leak-auditor/SKILL.md  # Claude Code workflow
├── .github/workflows/tests.yml                           # Python CI
├── docs/SECURITY.md                                      # Threat model and limits
├── examples/                                             # Synthetic report example
├── src/revenue_leak_auditor/                             # CLI, crawler, checks, models, reports
├── tests/                                                # Unit and mocked integration tests
├── CLAUDE.md                                             # Project instructions for Claude Code
├── pyproject.toml                                        # Package and CLI configuration
└── README.md
```

## Safety boundary — read before running

- Only audit websites you own or are authorised to assess. The tool makes HTTP requests to the supplied host.
- The crawler is read-only: it does not log in, submit forms, purchase, book, send messages, or change site state.
- It accepts HTTP(S), limits ports to their standard defaults, rejects embedded credentials and non-public DNS/IP answers, manually validates redirects, restricts crawl scope to the original hostname, limits crawl depth/page count, and caps HTML bodies at 2 MB.
- The DNS check and the HTTP client's later hostname resolution are separate operations. **DNS-rebinding/TOCTOU is not fully eliminated.** This CLI is intended for a trusted, local, single-user workflow. Do not expose it as a public or multi-tenant URL-scanning service without connection-level DNS pinning, network egress isolation, and additional abuse controls.
- Static HTML checks do not execute JavaScript. A site that renders content client-side may be only partially inspected.
- Likely sensitive query parameters (such as token, key, password, auth, and session values) are redacted in generated Markdown and JSON reports. Avoid supplying secrets in URLs regardless.
- Impact is a prioritisation heuristic, not measured revenue loss. The auditor has no access to analytics, transactions, or conversion attribution.
- The crawler is intentionally small and bounded. It is not a substitute for Lighthouse, WCAG conformance testing, penetration testing, or a human UX review.

See [`docs/SECURITY.md`](docs/SECURITY.md) for the threat model and known limitations.

## Roadmap

- [x] Python package and installable `revenue-auditor` CLI.
- [x] Bounded same-host HTML crawl and structured page records.
- [x] Evidence-backed static SEO, structure, mobile-signal, accessibility-attribute, CTA-heuristic, and HTTP status checks.
- [x] Markdown and JSON reports.
- [x] Unit tests and GitHub Actions CI.
- [ ] Browser-rendered checks for JavaScript-heavy sites.
- [ ] Lighthouse/PageSpeed integration with explicit lab-vs-field labels.
- [ ] Broken asset checks and richer internal-link reporting.
- [ ] Optional LLM narrative layer grounded strictly in verified findings.
- [ ] Connection-level DNS pinning and isolated worker before any hosted scanning mode.

## Build in public

This is **Agent #4/200**. The aim is to ship small, useful agents, document what actually works, and improve them through real tests—not to label a mockup as an autonomous product.

Repository: https://github.com/yerageracharan/website-revenue-leak-auditor

## License

MIT. See [`LICENSE`](LICENSE).
