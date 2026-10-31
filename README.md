<div align="center">

<img src="docs/assets/manga-hero.svg" alt="Website Revenue Leak Auditor — Agent 4 of 200" width="100%"/>

[![Tests](https://github.com/yerageracharan/website-revenue-leak-auditor/actions/workflows/tests.yml/badge.svg)](https://github.com/yerageracharan/website-revenue-leak-auditor/actions/workflows/tests.yml)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![MIT License](https://img.shields.io/badge/License-MIT-7c3bd1.svg)](LICENSE)
[![Agent 4 of 200](https://img.shields.io/badge/Build%20in%20Public-Agent%2004%2F200-17131d)](https://github.com/yerageracharan)

### 200 agents. 200 practical builds. One project at a time.

**Find the friction between a website visit and the next customer action.**

[Get started](#get-started) · [What it checks](#what-it-checks) · [Reports](#reports) · [Project structure](#project-structure) · [Security](#security)

</div>

---

## The idea

A business can attract visitors and still make it difficult for them to take the next step.

A page title may be missing. A contact link may lead to a 404. A mobile viewport may not be configured. The primary action may be hard to identify.

**Website Revenue Leak Auditor** is a small Python command-line tool that inspects a limited number of pages on a public website, records issues it can verify in the HTML or HTTP response, and creates a report with evidence and recommended next steps.

It is **Agent #4 in my 200-agent build-in-public series**.

<div align="center">
<table>
  <tr>
    <td align="center" width="33%">
      <img src="docs/assets/panels/hero-character.jpg" alt="Manga-style character artwork" width="125"/>
      <br/><strong>Investigate</strong>
      <br/><sub>Inspect the pages</sub>
    </td>
    <td align="center" width="33%">
      <img src="docs/assets/panels/desk-character.jpg" alt="Manga-style character studying at a desk" width="125"/>
      <br/><strong>Find evidence</strong>
      <br/><sub>Verify what is observable</sub>
    </td>
    <td align="center" width="33%">
      <img src="docs/assets/panels/ink-eye.jpg" alt="Black-and-white manga eye detail" width="125"/>
      <br/><strong>Prioritise</strong>
      <br/><sub>Explain what to fix next</sub>
    </td>
  </tr>
</table>
</div>

> **Current status:** working static-HTML CLI MVP. This repository does not yet contain a web dashboard, a browser-rendering engine, Lighthouse integration, or an AI model that autonomously evaluates business performance.

## What it checks

The current version uses deterministic Python checks. It does not need an AI API key.

| Area | Current check | What the finding means |
|---|---|---|
| Page metadata | Missing or unusually long page title; missing meta description; missing canonical link | A metadata observation—not a search-ranking prediction |
| Content structure | Missing H1 or multiple H1 elements | A page-structure signal |
| Mobile setup | Missing viewport meta tag | A reason to test the page at real mobile widths |
| Image markup | Images without an alt attribute | An accessibility-related observation—not an assessment of alt-text quality |
| Conversion wording | No common CTA wording found in links or buttons | A low-confidence text heuristic; custom and icon-only controls may be missed |
| Availability | Crawled pages returning HTTP 4xx or 5xx | The response observed at the time of the audit |

Each finding includes the page where it was observed, the evidence collected by the check, an impact priority, a separate confidence level, a practical recommendation, and a manual way to verify the fix.

### What it does not claim

The current release does not measure revenue loss, conversion rates, search rankings, Core Web Vitals, or Lighthouse scores. It does not execute JavaScript, test every accessibility requirement, or understand all custom user interfaces.

An impact label is a way to organise a review. It is **not** a financial estimate.

## Get started

### Requirements

- Python 3.10 or newer.
- Git.
- Permission to inspect the website you provide.

### 1. Clone the repository

~~~bash
git clone https://github.com/yerageracharan/website-revenue-leak-auditor.git
cd website-revenue-leak-auditor
~~~

### 2. Create a virtual environment

**Windows PowerShell**

~~~powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
~~~

**macOS or Linux**

~~~bash
python3 -m venv .venv
source .venv/bin/activate
~~~

### 3. Install the project

~~~bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
~~~

This installs the command-line tool and the development dependencies used by the test suite.

### 4. Run your first audit

Replace the example URL with a public website you own or are authorised to assess.

~~~bash
revenue-auditor https://your-domain.com
~~~

By default, the tool inspects up to **5 pages**, uses a **10-second timeout per request**, and writes **audit-report.md** in the current directory.

### 5. Export Markdown, JSON, and HTML reports

**macOS, Linux, or Git Bash**

~~~bash
revenue-auditor https://your-domain.com \
  --max-pages 8 \
  --timeout 10 \
  --output reports/audit.md \
  --json reports/audit.json \
  --html reports/audit.html
~~~

**Windows PowerShell**

~~~powershell
revenue-auditor https://your-domain.com --max-pages 8 --timeout 10 --output reports/audit.md --json reports/audit.json --html reports/audit.html
~~~

The reports directory is created automatically when it does not already exist.

### 6. Open the HTML report

**Windows PowerShell**

~~~powershell
Start-Process .\\reports\\audit.html
~~~

**macOS**

~~~bash
open reports/audit.html
~~~

**Linux**

~~~bash
xdg-open reports/audit.html
~~~

### 7. Run the tests

~~~bash
pytest
~~~

The tests use mocked HTTP and DNS responses. They do not need API keys or a live website.

<div align="center">
<img src="docs/assets/terminal-walkthrough.svg" alt="Command-line setup and audit walkthrough" width="100%"/>
<sub>Command-line walkthrough. This is a documentation illustration, not a screenshot of a live scan.</sub>
</div>

## Command reference

| Option | Default | Description |
|---|---:|---|
| URL | Required | Public HTTP or HTTPS website to inspect |
| --max-pages | 5 | Maximum pages to inspect; allowed range is 1–15 |
| --timeout | 10 | Per-request timeout in seconds; allowed range is 2–30 |
| --output | audit-report.md | Markdown report destination |
| --json | Off | Optional JSON report destination |
| --html | Off | Optional self-contained HTML report destination |
| --help | — | Show all CLI options |
| --version | — | Show the installed version |

~~~bash
revenue-auditor --help
revenue-auditor --version
~~~

## Reports

The same audit result can be exported in three formats.

| Output | Best for |
|---|---|
| Markdown | Reading, editing, sharing in GitHub issues, or keeping notes |
| JSON | Scripts, structured data, and future integrations |
| HTML | A self-contained report that opens in a browser and can be printed |

<div align="center">
<img src="docs/assets/report-preview.svg" alt="Illustrative report layout with evidence, findings, and priority labels" width="100%"/>
<br/>
<sub><strong>Illustrative report layout.</strong> The example values are synthetic and are not from a real website scan. The current tool does not calculate an overall website score.</sub>
</div>

A sample finding is available in [examples/sample-audit-report.md](examples/sample-audit-report.md).

Reports redact query values for common sensitive parameter names such as token, key, password, auth, and session. This is best-effort protection, not secret detection. Avoid putting credentials or private tokens in URLs.

## How it works

~~~mermaid
flowchart TD
    A["Website URL"] --> B["Validate URL and public address"]
    B --> C["Bounded same-host crawler"]
    C --> D["Fetch HTML response"]
    D --> E["Parse HTML with BeautifulSoup"]
    E --> F["Run deterministic checks"]
    F --> G["Create evidence-backed findings"]
    G --> H["Prioritise and recommend"]
    H --> I["Markdown"]
    H --> J["JSON"]
    H --> K["HTML"]
~~~

### Technology

| Technology | Purpose |
|---|---|
| Python 3.10+ | Core application and CLI |
| HTTPX | HTTP requests, timeouts, and redirect handling |
| BeautifulSoup 4 | HTML parsing |
| pytest | Unit and mocked integration tests |
| GitHub Actions | Continuous integration across Python 3.10–3.13 |
| Claude Code skill | Project-specific development instructions |

There is no LLM dependency in the current MVP. A future AI layer should explain or group verified findings, not invent observations.

## Project structure

~~~text
website-revenue-leak-auditor/
├── .claude/
│   └── skills/
│       └── website-revenue-leak-auditor/
│           └── SKILL.md       # Claude Code skill
├── .github/
│   └── workflows/
│       └── tests.yml          # CI workflow
├── docs/
│   ├── assets/
│   │   ├── panels/            # Cropped manga artwork
│   │   ├── manga-hero.svg
│   │   ├── terminal-walkthrough.svg
│   │   └── report-preview.svg
│   └── SECURITY.md            # Security model and limitations
├── examples/
│   └── sample-audit-report.md
├── src/
│   └── revenue_leak_auditor/
│       ├── auditor.py         # Crawl and audit orchestration
│       ├── checks.py          # Deterministic HTML checks
│       ├── cli.py             # Command-line interface
│       ├── models.py          # Audit, page, and finding models
│       ├── report.py          # Markdown, JSON, and HTML exports
│       └── safety.py          # URL validation
├── tests/
│   └── test_mvp.py            # Offline tests
├── CLAUDE.md                 # Project-wide Claude Code guidance
├── pyproject.toml            # Package configuration
├── LICENSE
└── README.md
~~~

## Security and limitations

This tool makes network requests to a URL supplied by the user. Treat it as an SSRF-sensitive application.

- Only HTTP and HTTPS URLs are accepted.
- Embedded URL credentials and non-standard ports are rejected.
- DNS answers are checked for public IP addresses before a request.
- Redirects are followed manually and must remain on the original hostname.
- The crawler is limited to the original hostname, a maximum of 15 pages, and 2 MB per HTML response.
- Requests are read-only GET requests. The tool does not log in, submit forms, purchase, book, send messages, or modify a website.
- Website JavaScript is not executed and arbitrary files are not downloaded.

**Important DNS limitation:** DNS is checked before HTTPX connects, but HTTPX performs its own hostname resolution when opening the connection. This leaves a DNS-rebinding / time-of-check-to-time-of-use gap. This version is intended for trusted, local, single-user use. Do not expose it as a public multi-tenant URL scanner without connection-level DNS pinning, network isolation, transport-level redirect controls, and abuse protection.

Read the full [security model](docs/SECURITY.md) before adapting the crawler for hosted use.

## Roadmap

- [x] Installable Python CLI.
- [x] Bounded same-host HTML crawl.
- [x] Static metadata, H1, viewport, image-alt, CTA-heuristic, and HTTP status checks.
- [x] Findings with evidence, impact, confidence, and recommendations.
- [x] Markdown, JSON, and HTML report exports.
- [x] Offline tests and GitHub Actions CI.
- [ ] Richer internal-link and broken-asset checks.
- [ ] Browser-rendered checks for JavaScript-heavy pages.
- [ ] Lighthouse or PageSpeed integration with clearly labelled lab and field metrics.
- [ ] Optional AI explanations grounded only in verified findings.
- [ ] Connection-level DNS pinning and isolated workers before hosted scanning.

## Who is it for?

- **Freelancers and web studios:** prepare a first-pass review before a redesign conversation.
- **Small businesses:** understand visible website issues and what to investigate next.
- **Developers:** run repeatable static checks and export structured findings.
- **Students and builders:** learn how crawling, parsing, deterministic checks, and reporting fit together.

Treat an audit as a starting point for human review—not proof of lost customers or guaranteed growth.

## Build in public — Agent #4 of 200

This repository is part of a public challenge to build **200 practical AI agents and automation projects**.

**Build something real. Show the evidence. Document the limitations. Ship the next version.**

- [Star the repository](https://github.com/yerageracharan/website-revenue-leak-auditor)
- [Report an issue](https://github.com/yerageracharan/website-revenue-leak-auditor/issues)
- [Fork the project](https://github.com/yerageracharan/website-revenue-leak-auditor/fork)

When reporting an issue, include the expected behavior and a reproducible example. Do not post private URLs, credentials, or customer data.

## License

MIT. See [LICENSE](LICENSE).

---

<div align="center">

**END OF CHAPTER 04**

*Better evidence. Clearer fixes. Fewer blind spots.*

[Back to top](#website-revenue-leak-auditor)

</div>
