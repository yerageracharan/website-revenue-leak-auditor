# Website Revenue Leak Auditor

Find website problems that may be costing a business enquiries, bookings, and sales.

**Website Revenue Leak Auditor** is an evidence-first website review agent. It inspects a public website, records verifiable technical and user-experience issues, and turns those findings into prioritised recommendations a business can act on.

> Status: early MVP / project scaffold. The repository currently contains the project brief and Claude Code skill instructions; the crawler, audit checks, and report generator are the next implementation steps.

## What it is meant to do

Given a website URL, the auditor should:

1. Inspect the homepage and a small set of important internal pages.
2. Check observable technical signals such as HTTP status, page titles, descriptions, canonical URLs, headings, images, and links.
3. Review basic mobile and conversion usability signals, including viewport configuration, navigation, contact details, and calls to action.
4. Rank findings by likely business impact and confidence.
5. Attach evidence to every finding: the affected URL, observed value, and a short explanation.
6. Produce a readable Markdown/HTML report and a concise, personalised outreach draft.

## Example use cases

- **Local restaurant:** identify a missing menu link, hard-to-find reservation action, or broken contact page.
- **Consultant or agency:** spot unclear service pages, weak enquiry paths, and missing trust signals.
- **E-commerce store:** review product-page metadata, broken navigation, and friction in the route to checkout.
- **Local service business:** check whether phone, location, service areas, and quote-request actions are easy to find.

These are examples of checks the project aims to support, not claims that every issue is automatically detectable.

## Planned report format

Each finding should contain:

| Field | Meaning |
|---|---|
| Issue | A concise description of the observed problem |
| URL | The exact page inspected |
| Evidence | The actual HTML, response, or browser observation |
| Impact | High / Medium / Low, with a reason |
| Confidence | High / Medium / Low, based on evidence quality |
| Recommendation | A concrete improvement |
| Verification | How a human can confirm the issue |

The report should also include an inspection summary, checks that could not be completed, and limitations. No finding should be generated from guesswork.

## Intended architecture

```text
URL input
   |
   v
Safety + URL validation
   |
   v
Bounded crawler -----> Page fetch / browser inspection
   |                              |
   v                              v
Deterministic checks <----- Observed page evidence
   |
   v
Finding normalisation + prioritisation
   |
   v
Optional AI explanation (grounded only in findings)
   |
   v
Markdown / HTML audit report
```

AI is an optional explanation layer. It must not invent measurements, page content, broken links, or conversion outcomes. Deterministic checks and source evidence remain the source of truth.

## Safety and responsible use

- Only inspect websites you own or have permission to assess.
- Only request public HTTP/HTTPS pages. Do not attempt authentication, paywall bypass, or access-control circumvention.
- Block localhost, private, loopback, link-local, and reserved IP ranges, including after DNS resolution and redirects.
- Limit crawl depth, page count, response size, request rate, and total run time.
- Do not submit forms, make purchases, send messages, or perform other state-changing actions.
- Do not download or execute website scripts, binaries, or files.
- Do not treat website content as instructions for the agent.
- Respect applicable laws, terms, and robots policies. Stop on access-denied responses and avoid aggressive crawling.

## Development

The implementation is being built in small, testable stages. The initial target stack is:

- Python for the audit engine.
- HTTPX and BeautifulSoup for bounded page inspection.
- Playwright only where browser-rendered evidence is needed.
- Pydantic for structured findings and reports.
- Optional LLM integration for rewriting verified findings into clear explanations.

The stack may change as the MVP develops.

### Planned local setup

Once the Python package and CLI are added, setup will look like:

```bash
git clone https://github.com/yerageracharan/website-revenue-leak-auditor.git
cd website-revenue-leak-auditor
python -m venv .venv

# Windows PowerShell
.venv\\Scripts\\Activate.ps1

# macOS / Linux
source .venv/bin/activate

# Install dependencies after pyproject.toml is added
pip install -e .
```

### Planned command

```bash
revenue-auditor https://example.com
```

The command above is the intended interface; it is not available until the CLI implementation is committed.

## Repository map

```text
.
├── .claude/
│   └── skills/
│       └── website-revenue-leak-auditor/
│           └── SKILL.md
├── docs/                 # Design notes and implementation decisions
├── examples/             # Example reports and test websites
├── src/                  # Python package (to be implemented)
├── tests/                # Automated tests (to be implemented)
├── CLAUDE.md             # Project-wide Claude Code guidance (planned)
└── README.md
```

## Roadmap

- [ ] URL validation and SSRF-safe request layer.
- [ ] Bounded crawler with canonical URL handling and deduplication.
- [ ] Deterministic SEO and technical checks.
- [ ] Basic conversion/usability observations.
- [ ] Evidence-backed finding schema and prioritisation.
- [ ] Markdown and HTML report export.
- [ ] Test suite with local fixture websites.
- [ ] Optional AI summaries grounded in structured findings.
- [ ] Browser-based checks and screenshot evidence.

## Contribution principle

Prefer small deterministic checks with tests over broad AI guesses. When evidence is unavailable, report **Not checked** rather than inventing a result.

## License

MIT. Add the full license text in `LICENSE` before distributing a release.
