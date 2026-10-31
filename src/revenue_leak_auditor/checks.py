from __future__ import annotations

from bs4 import BeautifulSoup

from .models import Finding

CTA_TERMS = (
    "contact", "book", "booking", "reserve", "reservation", "call", "quote",
    "get started", "buy", "order", "schedule", "enquire", "inquire", "appointment",
)


def inspect_html(url: str, html: str) -> tuple[str, list[Finding], list[str]]:
    """Return page title, evidence-backed findings, and same-site link candidates."""
    soup = BeautifulSoup(html, "html.parser")
    findings: list[Finding] = []
    links: list[str] = []

    def add(title: str, category: str, evidence: str, impact: str, confidence: str,
            recommendation: str, verification: str, rationale: str) -> None:
        findings.append(Finding(title, category, url, evidence, impact, confidence,
                                recommendation, verification, rationale))

    title_tag = soup.find("title")
    title = title_tag.get_text(" ", strip=True) if title_tag else ""
    if not title:
        add("Page title is missing", "SEO", "No <title> element found in the HTML document.",
            "Medium", "High", "Add a concise, page-specific title that describes the page.",
            "Reload the page and confirm the title appears in the document head.",
            "Search results and browser tabs may provide visitors with little context.")
    elif len(title) > 65:
        add("Page title is unusually long", "SEO", f"Observed title length: {len(title)} characters.",
            "Low", "High", "Rewrite the title to communicate the page topic earlier and more concisely.",
            "Check the revised title in the page source and a search preview.",
            "Long titles may be truncated in some search result layouts.")

    description = soup.find("meta", attrs={"name": lambda value: value and value.lower() == "description"})
    description_text = (description.get("content") or "").strip() if description else ""
    if not description_text:
        add("Meta description is missing", "SEO", "No non-empty meta description was found.",
            "Low", "High", "Add a unique summary of the page that accurately sets visitor expectations.",
            "Inspect the rendered document head for a non-empty description meta tag.",
            "A useful description can improve how the page is presented in search results.")

    canonical = soup.find("link", rel=lambda value: value and "canonical" in [v.lower() for v in (value if isinstance(value, list) else value.split())])
    if not canonical or not (canonical.get("href") or "").strip():
        add("Canonical URL was not detected", "SEO", "No canonical link element with an href was found.",
            "Low", "Medium", "Add a canonical URL when the page has a preferred indexable URL.",
            "Check that the canonical href points to the intended canonical page.",
            "Canonical signals can help consolidate duplicate or variant URLs.")

    h1s = soup.find_all("h1")
    if not h1s:
        add("No main H1 heading was detected", "Content structure", "The inspected HTML contains zero H1 elements.",
            "Medium", "High", "Add a clear primary heading that describes the page's main purpose.",
            "Inspect the page and confirm one visible, descriptive H1 is present.",
            "Visitors scanning the page may have difficulty identifying its main topic.")
    elif len(h1s) > 1:
        add("Multiple H1 headings were detected", "Content structure", f"Found {len(h1s)} H1 elements.",
            "Low", "Medium", "Review the heading hierarchy and use headings to reflect the page structure.",
            "Inspect the page outline and confirm headings describe distinct sections.",
            "A clear heading hierarchy can make long pages easier to scan.")

    viewport = soup.find("meta", attrs={"name": lambda value: value and value.lower() == "viewport"})
    if not viewport:
        add("Viewport configuration is missing", "Mobile usability", "No meta viewport tag was found.",
            "Medium", "High", "Add a responsive viewport declaration and test the page at mobile widths.",
            "Use a mobile device or browser emulation to verify layout and scaling.",
            "Mobile visitors may see a poorly scaled or less usable layout.")

    images = soup.find_all("img")
    missing_alt = [img for img in images if img.get("alt") is None]
    if missing_alt:
        sample = ", ".join((img.get("src") or "(image without src)")[:80] for img in missing_alt[:3])
        add("Images are missing alt attributes", "Accessibility",
            f"{len(missing_alt)} of {len(images)} inspected images have no alt attribute. Examples: {sample}",
            "Medium", "High", "Add appropriate alt text for informative images and alt=\"\" for decorative images.",
            "Recheck each image and confirm its alt value reflects its purpose.",
            "People using screen readers may miss information conveyed by images.")

    action_text = " ".join(element.get_text(" ", strip=True).lower() for element in soup.find_all(["a", "button"]))
    if not any(term in action_text for term in CTA_TERMS):
        add("No obvious primary action was detected", "Conversion observation",
            "No link or button text matched the auditor's common contact, booking, quote, or purchase terms.",
            "Medium", "Low", "Review the primary visitor task and make its next step clear and easy to find.",
            "Ask a first-time visitor to locate the intended next step on desktop and mobile.",
            "A hard-to-find next step may create friction, but this text-only heuristic can miss icon-only or custom controls.")

    for anchor in soup.find_all("a", href=True):
        href = anchor.get("href", "").strip()
        if not href or href.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
            continue
        links.append(href)

    return title, findings, links
