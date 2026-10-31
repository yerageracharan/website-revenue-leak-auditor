<a id="website-revenue-leak-auditor"></a>

<div align="center">

# WEBSITE REVENUE LEAK AUDITOR

### Agent 04 / 200 · Build in Public Series

**Find the friction between a website visit and the next customer action.**

[![Tests](https://github.com/yerageracharan/website-revenue-leak-auditor/actions/workflows/tests.yml/badge.svg)](https://github.com/yerageracharan/website-revenue-leak-auditor/actions/workflows/tests.yml)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-7c3bd1.svg)](LICENSE)
[![Build in Public](https://img.shields.io/badge/200%20Agents-04%2F200-17131d)](https://github.com/yerageracharan)

**A practical, evidence-first website audit CLI.**

[Start here](#start-here) · [Feature guide](#what-the-auditor-checks) · [Architecture](#how-the-audit-works) · [Examples](#understanding-the-report) · [Security](#security-and-responsible-use)

</div>

---

# 0. Read this first

A website can receive visitors and still make it unnecessarily difficult for them to take the next step.

A page may have no meaningful title. An internal page may return an error. A page may lack the viewport configuration that helps browsers render it at mobile widths. A visitor may struggle to identify a contact or booking action.

**Website Revenue Leak Auditor** is a Python command-line tool that inspects a limited number of pages on a public website, checks observable HTML and HTTP signals, and produces a prioritised report with evidence and practical recommendations.

It is **Agent #4 in a series of 200 practical AI-agent and automation builds**.

> **Important product status**
>
> This repository currently contains a working static-HTML CLI MVP. It is not yet a hosted SaaS product, browser dashboard, autonomous AI consultant, Lighthouse replacement, or revenue-attribution system. The current findings are produced by deterministic Python checks; no LLM API is required.

## The product in one diagram

~~~mermaid
flowchart LR
    A["Website URL"] --> B["Inspect a small set of pages"]
    B --> C["Check actual HTML and HTTP responses"]
    C --> D["Record evidence"]
    D --> E["Prioritise observations"]
    E --> F["Recommend next steps"]
    F --> G["Markdown"]
    F --> H["JSON"]
    F --> I["HTML report"]
~~~

## What you get

| You provide | The auditor does | You receive |
|---|---|---|
| A public website URL | Validates the URL and applies crawl limits | A record of pages inspected |
| Permission to inspect the site | Fetches same-host HTML pages | Observable issues and supporting evidence |
| Optional output preferences | Runs deterministic checks | Priority and confidence labels |
| — | Builds reports from collected findings | Markdown, JSON, and/or HTML |

The goal is not to produce a dramatic score. The goal is to give a developer or business owner a useful answer to a more concrete question:

**“What did the tool actually observe, where did it observe it, and what should a person check next?”**

---

<a id="start-here"></a>

# 1. Start here

## Who should use this project?

| User | Practical use |
|---|---|
| Freelancers | Prepare a first-pass technical checklist before discussing a redesign |
| Web-development agencies | Identify visible issues that deserve a human review |
| Small business owners | Understand basic website markup and availability observations |
| Developers | Run repeatable checks and export structured findings |
| Students | Learn how crawling, parsing, deterministic checks, and reporting fit together |

## What you need before starting

| Requirement | Minimum |
|---|---|
| Python | 3.10 or newer |
| Git | Installed and available in your terminal |
| Terminal | PowerShell, Windows Terminal, macOS Terminal, or Linux shell |
| Website access | A public site you own or have permission to assess |
| API key | Not required for the current MVP |

## Your first audit: the shortest path

~~~text
┌─────────────────────┐
│ 1. CLONE            │
│ Get the source code │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 2. ENVIRONMENT      │
│ Create a virtualenv │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 3. INSTALL          │
│ Install the package │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 4. AUDIT            │
│ Pass a public URL   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 5. REVIEW           │
│ Open the report     │
└─────────────────────┘
~~~

If you are new to Python, follow every step below in order. You do not need to understand the code before running the first audit.

---

# 2. Installation guide

<a id="installation"></a>

## Step 1 — Clone the repository

Open a terminal and run:

~~~bash
git clone https://github.com/yerageracharan/website-revenue-leak-auditor.git
cd website-revenue-leak-auditor
~~~

This downloads the source code and moves your terminal into the project folder.

## Step 2 — Create a virtual environment

A virtual environment keeps this project's Python packages separate from other Python projects on your computer.

**Windows PowerShell**

~~~powershell
python -m venv .venv
~~~

**macOS or Linux**

~~~bash
python3 -m venv .venv
~~~

## Step 3 — Activate the environment

You need to activate the virtual environment in the terminal where you will install and run the project.

**Windows PowerShell**

~~~powershell
.\.venv\Scripts\Activate.ps1
~~~

If PowerShell blocks the activation script, you can use Command Prompt instead:

~~~bat
.venv\Scripts\activate.bat
~~~

**macOS or Linux**

~~~bash
source .venv/bin/activate
~~~

When activation works, your terminal usually shows the environment name, such as (.venv), at the beginning of the prompt.

## Step 4 — Install the dependencies

Run these commands with the virtual environment activated:

~~~bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
~~~

The installation includes:

| Package | Why it is installed |
|---|---|
| HTTPX | Makes bounded HTTP requests and handles response streaming |
| BeautifulSoup 4 | Parses HTML documents |
| pytest | Runs the automated test suite |
| pytest-cov | Provides optional test-coverage reporting |
| setuptools | Installs the Python package and command-line entry point |

The project is installed in editable mode. This means changes you make to the source code are available to the installed command without reinstalling after every edit.

## Step 5 — Confirm that installation worked

~~~bash
revenue-auditor --help
~~~

You should see the command's usage information, including the URL argument and the supported options.

You can also check the package version:

~~~bash
revenue-auditor --version
~~~

## Step 6 — Run your first audit

Replace the example URL with a public website you own or have permission to inspect.

~~~bash
revenue-auditor https://your-domain.com
~~~

The default settings are:

| Setting | Default |
|---|---:|
| Pages inspected | 5 maximum |
| Request timeout | 10 seconds |
| Markdown output | audit-report.md |
| JSON output | Not created unless requested |
| HTML output | Not created unless requested |

The default run writes a Markdown report named audit-report.md in the folder where you ran the command.

## Step 7 — Export all report formats

The auditor can generate Markdown, JSON, and HTML from the same audit result.

**macOS, Linux, and Git Bash**

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

The tool creates the reports folder automatically if it does not exist.

## Step 8 — Open the HTML report

**Windows PowerShell**

~~~powershell
Start-Process .\reports\audit.html
~~~

**macOS**

~~~bash
open reports/audit.html
~~~

**Linux**

~~~bash
xdg-open reports/audit.html
~~~

You now have a complete first-pass static HTML audit.

---

<a id="what-it-checks"></a>

# 3. What the auditor checks

The current implementation focuses on observable page markup and HTTP responses. The checks are deliberately small and deterministic so that the evidence can be inspected and tested.

## Feature matrix

| Category | Check | Trigger | Confidence in current implementation |
|---|---|---|---|
| SEO | Missing page title | No title element in the inspected HTML | High |
| SEO | Unusually long title | Title is longer than 65 characters | High |
| SEO | Missing meta description | No non-empty description meta tag is found | High |
| SEO | Missing canonical link | No canonical link with a non-empty href is found | Medium |
| Structure | Missing H1 | No H1 element is found | High |
| Structure | Multiple H1 elements | More than one H1 is found | Medium |
| Mobile signal | Missing viewport meta tag | No viewport meta tag is found | High |
| Accessibility signal | Missing image alt attribute | One or more img elements do not have an alt attribute | High |
| Conversion heuristic | No common CTA wording detected | Link and button text does not contain the configured common action terms | Low |
| Availability | HTTP error response | A crawled page returns HTTP 4xx or 5xx | High |

Confidence describes how directly the finding follows from the observed evidence. It does not describe the financial impact of the issue.

## 3.1 SEO and metadata

The auditor inspects:

- Whether a title element exists.
- Whether the title is unusually long.
- Whether a non-empty meta description exists.
- Whether a canonical link with an href is present.

These are markup checks. They do not predict ranking positions, search impressions, click-through rates, or whether a search engine will choose to display a specific description.

## 3.2 Heading structure

The auditor checks the number of H1 elements in each inspected HTML page.

~~~text
EXAMPLE A — NO H1

<body>
  <header>...</header>
  <main>
    <h2>Our Services</h2>
  </main>
</body>

OBSERVATION
No H1 element was detected.
~~~

~~~text
EXAMPLE B — MORE THAN ONE H1

<body>
  <main>
    <h1>Our Services</h1>
    <section>
      <h1>Contact the Team</h1>
    </section>
  </main>
</body>

OBSERVATION
Two H1 elements were detected.
~~~

The check does not determine whether a heading is visually prominent, meaningful, or correctly styled.

## 3.3 Mobile viewport signal

The auditor checks for a meta viewport tag.

A common responsive declaration looks like this:

~~~html
<meta name="viewport" content="width=device-width, initial-scale=1">
~~~

The presence of this tag does not prove that a website is mobile-friendly. It only confirms that the inspected HTML contains the viewport metadata. A real mobile usability review must still inspect layout, text size, navigation, overflow, tap targets, and forms at phone widths.

## 3.4 Image alternative-text attributes

The auditor counts img elements without an alt attribute and records a few example source values.

There is an important distinction:

| Markup | Meaning |
|---|---|
| alt is missing | The attribute is absent; the current check reports this |
| alt="" | The attribute exists and is empty; it may be appropriate for decorative images |
| alt="A person using a laptop" | The attribute exists; the auditor does not judge whether the description is accurate |

This is an attribute-presence check, not a complete accessibility audit.

## 3.5 Conversion and CTA wording heuristic

The auditor searches the visible text of anchor and button elements for common action terms such as:

~~~text
contact
book
booking
reserve
reservation
call
quote
get started
buy
order
schedule
enquire
inquire
appointment
~~~

If none of these terms is detected, the tool reports a low-confidence observation.

This can miss:

- Icon-only buttons.
- Custom calls to action, such as "Let's talk".
- Controls rendered after JavaScript executes.
- Actions implemented in custom components outside ordinary anchor or button elements.

Treat this check as a prompt for human review, not proof that the website has no primary action.

## 3.6 HTTP availability observations

The crawler records HTTP responses for pages it actually visits.

A response such as 404 or 500 becomes an availability finding.

~~~mermaid
flowchart TD
    A["Discovered same-host link"] --> B["Validate target URL"]
    B --> C["Request page"]
    C --> D{"HTTP status"}
    D -->|"Below 400"| E["Continue HTML inspection when content is HTML"]
    D -->|"400–499"| F["Record client-side HTTP error"]
    D -->|"500–599"| G["Record server-side HTTP error"]
    E --> H["Save page result"]
    F --> H
    G --> H
~~~

The tool does not perform a separate, exhaustive crawl of every possible website URL. It only processes a bounded set of same-host links discovered from the pages it inspects.

---

# 4. Understanding the findings

A finding is a structured observation. It is not just an AI-generated sentence.

## Anatomy of a finding

| Field | What it tells you |
|---|---|
| Title | The issue or observation |
| Category | SEO, content structure, mobile usability, accessibility, conversion, or availability |
| URL | The exact page where it was observed |
| Evidence | The value or condition detected by the check |
| Impact | A High, Medium, or Low review priority |
| Confidence | How directly the evidence supports the observation |
| Business rationale | Why the observation may matter to visitors |
| Recommendation | A suggested improvement |
| Verification | A manual way to check whether the change worked |

## Impact and confidence are different

Do not confuse priority with certainty.

| | High confidence | Medium confidence | Low confidence |
|---|---|---|---|
| High impact | Directly observed high-priority issue | Important issue with some ambiguity | Needs human verification before escalation |
| Medium impact | Directly observed issue | Useful heuristic | Weak signal; treat as a question |
| Low impact | Directly observed polish issue | Context-dependent improvement | Optional review |

The current tool assigns impact and confidence separately. It does not combine them into a single website-health score.

## Illustrative example

The following is synthetic documentation data. It is not a scan of a real business.

~~~text
[Medium impact] Viewport configuration is missing

Category:
Mobile usability

Page:
https://example.test/

Confidence:
High

Evidence:
No meta viewport tag was found in the inspected HTML.

Why it may matter:
Mobile visitors may see a poorly scaled or less usable layout.

Recommended action:
Add a responsive viewport declaration and test the page at mobile widths.

How to verify:
Inspect the page at common phone viewport widths.
~~~

The repository includes a longer [sample audit finding](examples/sample-audit-report.md).

---

<a id="understanding-the-report"></a>

# 5. Understanding the report

The auditor can write three different report formats.

~~~mermaid
flowchart LR
    A["AuditResult"] --> B["Markdown renderer"]
    A --> C["JSON serializer"]
    A --> D["HTML renderer"]
    B --> E["audit.md"]
    C --> F["audit.json"]
    D --> G["audit.html"]
~~~

## 5.1 Markdown report

Use Markdown when you want to:

- Read the findings in a text editor.
- Add the findings to a GitHub issue.
- Keep an audit record in a repository.
- Edit or annotate recommendations.

## 5.2 JSON report

Use JSON when you want to:

- Process findings with another Python script.
- Build a future dashboard.
- Store structured audit records.
- Integrate the output with another system.

The JSON report contains the target URL, audit timestamp, page results, findings, priority summary, and audit notes.

## 5.3 HTML report

Use HTML when you want a standalone document that can be opened in a browser or printed.

The current HTML report includes:

- The inspected target and audit timestamp.
- Counts of High, Medium, and Low priority findings.
- Individual finding cards.
- Evidence and recommendations.
- The list of pages inspected.
- Audit notes and limitations.

The report is self-contained and does not rely on an external JavaScript or CSS file.

## Report privacy

The report writer redacts query values for common sensitive parameter names, including token, key, secret, password, auth, session, signature, credential, and csrf.

This is a best-effort safeguard. It does not guarantee the detection of every secret. Do not include credentials or private tokens in URLs.

---

<a id="how-the-audit-works"></a>

# 6. How the audit works

## System overview

~~~mermaid
flowchart TD
    U["User enters a URL"] --> S["safety.py"]
    S -->|"Allowed URL"| A["auditor.py"]
    S -->|"Rejected target"| X["Stop with a clear error"]
    A --> N["Bounded page queue"]
    N --> H["HTTPX request"]
    H --> P["PageResult"]
    H -->|HTML response| C["checks.py"]
    C --> F["Finding objects"]
    P --> R["AuditResult"]
    F --> R
    R --> M["report.py"]
    M --> MD["Markdown"]
    M --> JS["JSON"]
    M --> HT["HTML"]
~~~

## Audit lifecycle

~~~mermaid
sequenceDiagram
    actor User
    participant CLI
    participant Safety
    participant Crawler
    participant Checks
    participant Reports

    User->>CLI: Provide website URL and options
    CLI->>Safety: Validate URL
    Safety-->>CLI: Normalised allowed URL
    CLI->>Crawler: Start bounded audit
    loop Until page limit is reached
        Crawler->>Safety: Validate discovered URL
        Safety-->>Crawler: Allowed URL or rejection
        Crawler->>Crawler: Fetch HTML response
        Crawler->>Checks: Inspect HTML
        Checks-->>Crawler: Title, findings, links
    end
    Crawler-->>CLI: Structured audit result
    CLI->>Reports: Write requested report formats
    Reports-->>CLI: Report files saved
    CLI-->>User: Print summary and output paths
~~~

## Crawl boundaries

The current implementation has conservative limits:

| Boundary | Current behavior |
|---|---|
| Protocol | HTTP and HTTPS only |
| Port | Standard HTTP/HTTPS ports only |
| Host scope | Original hostname only |
| Maximum pages | 15 |
| Default pages | 5 |
| Redirect handling | Manual, maximum of 4 redirect hops |
| Response size | 2 MB per HTML response |
| Default timeout | 10 seconds per request |
| Allowed timeout range | 2–30 seconds |
| Page methods | GET requests |
| Environment proxies | Not inherited by the HTTPX client |

The exact settings are enforced in the Python implementation. They are not merely README recommendations.

---

# 7. CLI reference

## Basic usage

~~~text
revenue-auditor URL [OPTIONS]
~~~

## All supported options

| Argument | Required? | Default | Allowed values / meaning |
|---|---|---:|---|
| URL | Yes | — | Public HTTP or HTTPS URL |
| --max-pages | No | 5 | Integer from 1 to 15 |
| --timeout | No | 10 | Number of seconds from 2 to 30 |
| --output | No | audit-report.md | Markdown output path |
| --json | No | — | Optional JSON output path |
| --html | No | — | Optional HTML output path |
| --help | No | — | Display command help |
| --version | No | — | Display installed version |

## Command examples

**Default audit**

~~~bash
revenue-auditor https://your-domain.com
~~~

**Inspect no more than three pages**

~~~bash
revenue-auditor https://your-domain.com --max-pages 3
~~~

**Use a shorter timeout**

~~~bash
revenue-auditor https://your-domain.com --timeout 5
~~~

**Write Markdown to a custom location**

~~~bash
revenue-auditor https://your-domain.com --output audits/homepage-review.md
~~~

**Write JSON as well**

~~~bash
revenue-auditor https://your-domain.com --json audits/review.json
~~~

**Create all three reports**

~~~bash
revenue-auditor https://your-domain.com --output audits/review.md --json audits/review.json --html audits/review.html
~~~

**Display help**

~~~bash
revenue-auditor --help
~~~

## What the terminal summary means

A typical successful run prints:

1. The target URL and configured page limit.
2. How many pages were inspected.
3. How many findings were created.
4. High, Medium, and Low priority counts.
5. The path to each requested report.

The actual page and finding counts depend on the inspected website. The README does not publish a fixed audit score or promise that every website will produce the same output.

---

<a id="project-structure"></a>

# 8. Project structure and code map

~~~text
website-revenue-leak-auditor/
│
├── .claude/
│   └── skills/
│       └── website-revenue-leak-auditor/
│           └── SKILL.md
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── docs/
│   ├── assets/
│   │   └── panels/
│   │       ├── hero-character.jpg
│   │       ├── desk-character.jpg
│   │       └── ink-eye.jpg
│   └── SECURITY.md
│
├── examples/
│   └── sample-audit-report.md
│
├── src/
│   └── revenue_leak_auditor/
│       ├── __init__.py
│       ├── auditor.py
│       ├── checks.py
│       ├── cli.py
│       ├── models.py
│       ├── report.py
│       └── safety.py
│
├── tests/
│   └── test_mvp.py
│
├── CLAUDE.md
├── LICENSE
├── pyproject.toml
└── README.md
~~~

## Module responsibilities

| File | Responsibility | What to look for |
|---|---|---|
| auditor.py | Orchestrates the crawl | Page queue, HTTP requests, response handling, crawl limits |
| checks.py | Inspects HTML | Title, description, canonical, H1, viewport, alt attributes, CTA text |
| cli.py | Defines the terminal command | Arguments, defaults, command output, report paths |
| models.py | Defines structured data | AuditResult, PageResult, Finding |
| report.py | Creates reports | Markdown, JSON, HTML, URL redaction |
| safety.py | Validates target URLs | Protocol, host, port, DNS and public-address checks |
| test_mvp.py | Tests behavior | URL validation, static checks, crawling, reports, redaction |
| pyproject.toml | Package configuration | Dependencies, Python version, CLI entry point |
| tests.yml | Continuous integration | Test matrix across supported Python versions |
| CLAUDE.md | Project-wide coding rules | Engineering workflow and product boundaries |
| SKILL.md | Claude Code skill | How Claude should work on this project |

## Core data model

~~~mermaid
classDiagram
    class AuditResult {
      +target_url
      +started_at
      +pages[]
      +findings[]
      +notes[]
      +summary
      +to_dict()
    }
    class PageResult {
      +url
      +status_code
      +content_type
      +title
      +error
      +to_dict()
    }
    class Finding {
      +title
      +category
      +url
      +evidence
      +impact
      +confidence
      +recommendation
      +verification
      +business_rationale
      +to_dict()
    }
    AuditResult "1" --> "many" PageResult
    AuditResult "1" --> "many" Finding
~~~

## Why the code is split this way

The crawler should not decide how reports are formatted. The report generator should not make network requests. The HTML checks should not be responsible for command-line argument parsing.

This separation makes it possible to:

- Test the HTML checks without a network connection.
- Test report output using synthetic data.
- Change the CLI without rewriting the crawler.
- Add new checks without coupling them to report formatting.
- Add another output format without changing the audit process.

---

# 9. Run the test suite

Tests are designed to run offline. They use mocked DNS and HTTP behavior instead of relying on a live website.

## Install test dependencies

~~~bash
python -m pip install -e ".[dev]"
~~~

## Run all tests

~~~bash
pytest
~~~

## Run tests with more detail

~~~bash
pytest -v
~~~

## Run one test file

~~~bash
pytest tests/test_mvp.py
~~~

## Continuous integration

The GitHub Actions workflow runs the test suite on the following Python versions:

~~~text
       PUSH / PULL REQUEST
                │
                ▼
         GitHub Actions
                │
       ┌────────┼────────┐
       ▼        ▼        ▼
    Python   Python   Python
     3.10     3.11     3.12
                         │
                         ▼
                      Python
                       3.13
                │
                ▼
          Install package
                │
                ▼
            Run pytest
                │
                ▼
          CLI --help check
~~~

Workflow file: .github/workflows/tests.yml.

[View workflow runs](https://github.com/yerageracharan/website-revenue-leak-auditor/actions).

---

<a id="security"></a>

# 10. Security and responsible use

The auditor makes network requests based on a user-supplied URL. This is an SSRF-sensitive design area and should be treated carefully.

## Current protections

| Protection | Current behavior |
|---|---|
| URL schemes | Only HTTP and HTTPS |
| Embedded credentials | Rejected |
| Non-standard ports | Rejected |
| Local hostnames | Rejected |
| Private/non-global IP answers | Rejected during DNS validation |
| Redirects | Followed manually and revalidated |
| Host scope | Same original hostname |
| Page count | Maximum 15 |
| Response size | Maximum 2 MB per HTML response |
| Request method | GET only |
| Proxy environment | Not inherited |
| Form submissions | Not performed |
| Authentication | Not attempted |
| Arbitrary file downloads | Not performed |
| JavaScript execution | Not performed |

## Important DNS-rebinding limitation

The current program resolves a hostname and checks that the returned IP addresses are public. HTTPX then performs its own hostname resolution when it opens the connection.

Those two resolutions are not pinned to the same address. This leaves a DNS-rebinding or time-of-check-to-time-of-use gap.

**Do not deploy this version as a public, multi-tenant URL-scanning service.**

A hosted deployment would need, at minimum:

- Connection-level DNS pinning to the validated destination.
- TLS SNI and Host handling that remain correct when pinning the connection.
- Redirect validation at the transport boundary.
- Isolated outbound network access.
- Abuse prevention and tenant-level request limits.
- Monitoring and operational controls.

## Safe-use checklist

- [ ] You own the website or have permission to inspect it.
- [ ] You are using a public, non-authenticated URL.
- [ ] The URL does not contain credentials or private tokens.
- [ ] You are keeping the crawl limit conservative.
- [ ] You will review findings manually before making claims to a client.
- [ ] You understand that the tool does not measure revenue loss.

Read [docs/SECURITY.md](docs/SECURITY.md) before changing network behavior or adapting the project for hosted use.

---

# 11. Troubleshooting

## The revenue-auditor command is not recognised

**Possible cause:** the package was not installed in the active environment, or the virtual environment is not active.

Try:

~~~bash
python -m pip install -e ".[dev]"
~~~

Then confirm:

~~~bash
revenue-auditor --help
~~~

## Python is not recognised

Check your Python installation:

~~~bash
python --version
~~~

On macOS or Linux, try:

~~~bash
python3 --version
~~~

Install Python 3.10 or newer if necessary, then reopen your terminal.

## PowerShell blocks virtual environment activation

Use the Command Prompt activation script instead:

~~~bat
.venv\Scripts\activate.bat
~~~

You can also run Python through the virtual environment directly without activation:

~~~powershell
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
~~~

## The URL is rejected

Check that:

- The URL starts with http:// or https://.
- The URL does not include a username or password.
- The host is public and resolves to public IP addresses.
- You are not using localhost or a private IP address.
- You are using the standard port for HTTP or HTTPS.

The validator intentionally rejects many local and unusual destinations.

## The audit finds fewer pages than expected

The current crawler is bounded. It only follows same-host links discovered in inspected pages, and it stops when it reaches the configured maximum page count.

A page may not be discovered if:

- It is not linked from an inspected page.
- Its link is generated by JavaScript.
- It belongs to another hostname.
- It is outside the crawl limit.
- Its URL fails safety validation.

The tool is not a full sitemap crawler.

## A JavaScript-heavy site appears incomplete

The current version reads static HTML. It does not launch a browser or execute JavaScript. Content inserted after page load may therefore not be visible to the checks.

Browser automation is a future roadmap item.

## The HTML report does not open automatically

The CLI creates the file but does not launch a browser. Open the generated HTML file using your operating system's file manager or the platform commands in the installation guide.

## A finding looks incorrect

Check the evidence field and inspect the exact page. Some checks are deliberately heuristic, especially the CTA wording check.

Before reporting a bug, include:

- The check name.
- The observed finding.
- The relevant HTML snippet, if safe to share.
- The expected behavior.
- A reproducible test case.

Do not include credentials, private URLs, customer data, or session tokens in an issue.

---

# 12. Current scope versus future scope

The table below separates implemented functionality from planned functionality.

| Capability | Status | Notes |
|---|---|---|
| Installable Python CLI | <span>Implemented</span> | revenue-auditor command |
| Bounded same-host crawler | <span>Implemented</span> | Static HTML only |
| URL safety checks | <span>Implemented</span> | DNS-rebinding limitation remains |
| SEO metadata checks | <span>Implemented</span> | Title, description, canonical |
| Heading checks | <span>Implemented</span> | H1 presence and count |
| Viewport check | <span>Implemented</span> | Metadata signal only |
| Image alt-attribute check | <span>Implemented</span> | Attribute presence only |
| CTA wording heuristic | <span>Implemented</span> | Low-confidence |
| HTTP error observations | <span>Implemented</span> | For pages actually crawled |
| Markdown report | <span>Implemented</span> | Default output |
| JSON report | <span>Implemented</span> | Optional output |
| HTML report | <span>Implemented</span> | Self-contained output |
| Browser-rendered auditing | <span>Planned</span> | Not in current release |
| Lighthouse/PageSpeed metrics | <span>Planned</span> | Not measured today |
| AI explanations | <span>Planned</span> | No LLM in current findings |
| Revenue attribution | <span>Not implemented</span> | Requires business analytics and causal measurement |
| Public multi-tenant scanning | <span>Not safe yet</span> | Requires network isolation and DNS pinning |

---

# 13. Roadmap

~~~mermaid
flowchart TD
    A["v0.1 · Static audit CLI"] --> B["v0.2 · Better link and asset checks"]
    B --> C["v0.3 · Browser-rendered inspection"]
    C --> D["v0.4 · Lighthouse / PageSpeed integration"]
    D --> E["v0.5 · Optional AI explanation layer"]
    E --> F["v0.6 · Web dashboard and saved audits"]
    F --> G["Future · Hosted service after security hardening"]
~~~

## Current milestone

- [x] Python package and CLI.
- [x] Bounded same-host HTML crawl.
- [x] Deterministic static HTML checks.
- [x] Evidence-backed finding model.
- [x] Markdown, JSON, and HTML report export.
- [x] Offline automated tests.
- [x] GitHub Actions workflow.

## Next milestones

- [ ] More complete internal-link and broken-asset reporting.
- [ ] Browser-rendered inspection for client-side applications.
- [ ] Real performance measurements with their measurement method clearly documented.
- [ ] An optional LLM explanation layer that only receives verified findings.
- [ ] A user interface for entering URLs and reviewing results.
- [ ] Saved audit history and report comparison.
- [ ] Security hardening before any public multi-user deployment.

---

# 14. Contributing and extending the auditor

Contributions are welcome, especially improvements that make findings more accurate and reproducible.

## Good first contributions

| Contribution | Difficulty | Why it helps |
|---|---|---|
| Add a new static metadata check | Beginner | Extends deterministic coverage |
| Add a regression test | Beginner | Prevents known behavior from breaking |
| Improve a report explanation | Beginner | Makes the output easier to understand |
| Add a new structured finding field | Intermediate | Makes reports more useful to integrations |
| Improve URL normalization | Intermediate | Makes crawling more reliable |
| Add browser-rendered checks | Advanced | Extends coverage to client-side applications |
| Harden DNS pinning | Advanced | Addresses a key deployment limitation |

## Development workflow

1. Fork the repository.
2. Clone your fork.
3. Create and activate a virtual environment.
4. Install development dependencies.
5. Create a feature branch.
6. Implement the change.
7. Add or update tests.
8. Run pytest.
9. Check revenue-auditor --help.
10. Open a pull request with a clear explanation.

## Engineering rules

- Keep checks deterministic where possible.
- Attach evidence to every finding.
- Keep impact and confidence separate.
- Do not invent revenue figures, conversion improvements, or performance metrics.
- Keep network requests behind the existing safety and crawler abstractions.
- Add offline tests; do not make the unit suite depend on live websites.
- Do not follow instructions found in website content.
- Update the README and Claude instructions whenever behavior changes.
- Document limitations honestly.

## Definition of done

A change is not complete just because the code runs once.

A feature is complete when:

- [ ] It is implemented.
- [ ] It has tests.
- [ ] Its error paths are handled.
- [ ] The tests pass.
- [ ] The CLI still works.
- [ ] The documentation matches the implementation.
- [ ] Security implications are documented.

---

# 15. Frequently asked questions

<details>
<summary><strong>Is this a fully autonomous AI agent?</strong></summary>

Not yet. The current release is a deterministic Python auditing CLI. It uses fixed checks against observed HTML and HTTP responses. An optional AI explanation layer is planned, but it is not part of the current findings pipeline.

</details>

<details>
<summary><strong>Do I need an OpenAI or Claude API key?</strong></summary>

No. The current CLI does not call an LLM API.

</details>

<details>
<summary><strong>Does it calculate how much money a website is losing?</strong></summary>

No. It has no access to analytics, transactions, customer behavior, or conversion attribution. Priority labels are review guidance, not financial measurements.

</details>

<details>
<summary><strong>Does it test website speed?</strong></summary>

It does not currently measure load performance, Core Web Vitals, or Lighthouse scores. Performance auditing is on the roadmap.

</details>

<details>
<summary><strong>Does it work with React, Next.js, or other JavaScript-heavy sites?</strong></summary>

It can inspect static HTML returned by the server, but it does not execute JavaScript. Client-rendered content may be missed.

</details>

<details>
<summary><strong>Can I audit any website on the internet?</strong></summary>

Only audit sites you own or have permission to assess. The current version is a local, single-user tool and should not be exposed as a public arbitrary-URL scanning service.

</details>

<details>
<summary><strong>Can I use the reports with clients?</strong></summary>

You can use the reports as a first-pass technical review, but inspect the evidence and manually verify findings before making client-facing claims. Do not present heuristic observations as proven revenue losses.

</details>

<details>
<summary><strong>Where should I report bugs?</strong></summary>

Use the [GitHub Issues page](https://github.com/yerageracharan/website-revenue-leak-auditor/issues). Include a reproducible example and remove private data from your report.

</details>

---

# 16. Build in public — Agent #4 of 200

This project is part of a larger challenge: build 200 practical agents and automation projects, document the process, and improve them by shipping real working versions.

**The rule for this series:**

~~~text
BUILD
  ↓
TEST
  ↓
DOCUMENT
  ↓
SHIP
  ↓
LEARN
  ↓
REPEAT — 200 TIMES
~~~

If you find this useful:

- [Star the repository](https://github.com/yerageracharan/website-revenue-leak-auditor)
- [Fork it](https://github.com/yerageracharan/website-revenue-leak-auditor/fork)
- [Open an issue](https://github.com/yerageracharan/website-revenue-leak-auditor/issues)

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for the full text.

<div align="center">

---

### END OF CHAPTER 04

**Better evidence. Clearer fixes. Fewer blind spots.**

[Back to the top](#website-revenue-leak-auditor)

</div>
