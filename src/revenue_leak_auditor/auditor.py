from __future__ import annotations

from collections import deque
from urllib.parse import urljoin, urlsplit

import httpx

from .checks import inspect_html
from .models import AuditResult, Finding, PageResult
from .safety import UnsafeTarget, validate_public_url

USER_AGENT = "RevenueLeakAuditor/0.1 (+https://github.com/yerageracharan/website-revenue-leak-auditor)"
REDIRECT_CODES = {301, 302, 303, 307, 308}
MAX_RESPONSE_BYTES = 2_000_000


def _same_host(url: str, host: str) -> bool:
    return (urlsplit(url).hostname or "").lower().rstrip(".") == host.lower().rstrip(".")


def _fetch_html(client: httpx.Client, start_url: str, host: str) -> tuple[int, str, str, str]:
    """Fetch one page, manually validating every redirect and capping bytes."""
    current = start_url
    for _ in range(4):
        if not _same_host(current, host):
            raise UnsafeTarget("Cross-host redirects are outside the configured audit scope")
        current = validate_public_url(current)
        with client.stream("GET", current, headers={"User-Agent": USER_AGENT, "Accept": "text/html"}) as response:
            if response.status_code in REDIRECT_CODES:
                location = response.headers.get("location")
                if not location:
                    return response.status_code, response.headers.get("content-type", ""), current, "Redirect response did not include a Location header"
                current = urljoin(current, location)
                continue
            content_type = response.headers.get("content-type", "")
            if "text/html" not in content_type.lower() and "application/xhtml+xml" not in content_type.lower():
                return response.status_code, content_type, current, "Response is not HTML; content inspection skipped"
            data = bytearray()
            for chunk in response.iter_bytes():
                data.extend(chunk)
                if len(data) > MAX_RESPONSE_BYTES:
                    return response.status_code, content_type, current, "HTML response exceeded the 2 MB safety limit"
            encoding = response.encoding or "utf-8"
            return response.status_code, content_type, current, bytes(data).decode(encoding, errors="replace")
    raise RuntimeError("Too many redirects (maximum 4)")


def audit_website(target_url: str, max_pages: int = 5, timeout: float = 10.0) -> AuditResult:
    if not 1 <= max_pages <= 15:
        raise ValueError("max_pages must be between 1 and 15")
    if not 2 <= timeout <= 30:
        raise ValueError("timeout must be between 2 and 30 seconds")

    start_url = validate_public_url(target_url)
    host = urlsplit(start_url).hostname or ""
    result = AuditResult(target_url=start_url)
    queue: deque[str] = deque([start_url])
    visited: set[str] = set()

    limits = httpx.Limits(max_connections=2, max_keepalive_connections=1)
    with httpx.Client(timeout=timeout, follow_redirects=False, trust_env=False,
                      limits=limits, headers={"User-Agent": USER_AGENT}) as client:
        while queue and len(visited) < max_pages:
            page_url = queue.popleft()
            if page_url in visited:
                continue
            visited.add(page_url)
            try:
                status, content_type, final_url, body = _fetch_html(client, page_url, host)
                page = PageResult(url=final_url, status_code=status, content_type=content_type)
                result.pages.append(page)
                if status >= 400:
                    result.findings.append(Finding(
                        title=f"Page returned HTTP {status}", category="Availability", url=final_url,
                        evidence=f"The server returned HTTP status {status}.", impact="High" if status >= 500 else "Medium",
                        confidence="High", recommendation="Restore the page or correct the link that points to it.",
                        verification="Retry the exact URL and confirm it returns the intended page successfully.",
                        business_rationale="Visitors following this URL may be unable to reach the expected content."))
                    continue
                if body and body not in {"Response is not HTML; content inspection skipped", "HTML response exceeded the 2 MB safety limit"}:
                    title, findings, links = inspect_html(final_url, body)
                    page.title = title
                    result.findings.extend(findings)
                    for href in links:
                        candidate = urljoin(final_url, href)
                        if not _same_host(candidate, host):
                            continue
                        try:
                            safe_candidate = validate_public_url(candidate)
                        except UnsafeTarget:
                            result.notes.append("Skipped a same-host link that failed URL safety validation.")
                            continue
                        if safe_candidate not in visited and safe_candidate not in queue and len(visited) + len(queue) < max_pages:
                            queue.append(safe_candidate)
                elif body:
                    page.error = body
                    result.notes.append(f"{final_url}: {body}")
            except (httpx.HTTPError, UnsafeTarget, RuntimeError, UnicodeError) as exc:
                result.pages.append(PageResult(url=page_url, status_code=None, content_type="", error=str(exc)))
                result.notes.append(f"Could not inspect {page_url}: {exc}")

    if queue:
        result.notes.append(f"Crawl limit reached; {len(queue)} discovered page(s) were not inspected.")
    result.notes.append("This is a bounded static-HTML review, not a full browser, accessibility, or performance audit.")
    result.notes.append("Impact labels are prioritisation heuristics, not measured revenue loss or guaranteed conversion outcomes.")
    result.notes.append("Run only against sites you own or are authorised to assess. The local CLI has DNS-rebinding limitations and is not a safe multi-tenant scanning service.")
    return result
