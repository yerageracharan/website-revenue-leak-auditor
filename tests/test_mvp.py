import pytest

from revenue_leak_auditor.auditor import audit_website
from revenue_leak_auditor.checks import inspect_html
from revenue_leak_auditor.models import AuditResult, Finding, PageResult
from revenue_leak_auditor.report import render_markdown
from revenue_leak_auditor.safety import UnsafeTarget, validate_public_url


def test_rejects_unsupported_scheme():
    with pytest.raises(UnsafeTarget, match="Only http"):
        validate_public_url("file:///etc/passwd")


def test_rejects_embedded_credentials():
    with pytest.raises(UnsafeTarget, match="credentials"):
        validate_public_url("https://user:pass@example.com")


def test_rejects_localhost_before_dns():
    with pytest.raises(UnsafeTarget, match="Local hostnames"):
        validate_public_url("http://localhost:8080")


def test_rejects_nonstandard_port():
    with pytest.raises(UnsafeTarget, match="standard port"):
        validate_public_url("https://example.com:444")


def test_rejects_private_ip_literal():
    with pytest.raises(UnsafeTarget, match="non-public"):
        validate_public_url("http://127.0.0.1")


def test_rejects_hostname_with_private_dns_answer(monkeypatch):
    monkeypatch.setattr("revenue_leak_auditor.safety._resolve_addresses", lambda _host: {"8.8.8.8", "10.0.0.2"})
    with pytest.raises(UnsafeTarget, match="non-public"):
        validate_public_url("https://example.com")


def test_normalises_public_url_and_strips_fragment(monkeypatch):
    monkeypatch.setattr("revenue_leak_auditor.safety._resolve_addresses", lambda _host: {"8.8.8.8"})
    assert validate_public_url("HTTPS://Example.COM/path#section") == "https://example.com/path"


def test_finds_static_html_issues_and_links():
    html = "<html><head></head><body><h1>Welcome</h1><img src='/hero.png'><a href='/contact'>Contact us</a></body></html>"
    title, findings, links = inspect_html("https://example.com", html)
    names = {finding.title for finding in findings}
    assert title == ""
    assert {"Page title is missing", "Meta description is missing", "Viewport configuration is missing", "Images are missing alt attributes"} <= names
    assert "/contact" in links


def test_good_page_avoids_basic_metadata_findings():
    html = """<html><head><title>Example Service</title><meta name='description' content='A clear summary'><meta name='viewport' content='width=device-width, initial-scale=1'><link rel='canonical' href='https://example.com'></head><body><h1>Welcome</h1><a href='/contact'>Contact</a><img src='/hero.png' alt='Team'></body></html>"""
    _, findings, _ = inspect_html("https://example.com", html)
    names = {finding.title for finding in findings}
    assert "Page title is missing" not in names
    assert "Meta description is missing" not in names
    assert "Viewport configuration is missing" not in names
    assert "Images are missing alt attributes" not in names


def test_cta_check_is_low_confidence():
    _, findings, _ = inspect_html("https://example.com", "<html><head><title>Page</title></head><body><h1>Hello</h1></body></html>")
    item = next(f for f in findings if f.title == "No obvious primary action was detected")
    assert item.confidence == "Low"


def test_crawler_is_same_host_bounded_and_flags_http_errors(monkeypatch):
    monkeypatch.setattr("revenue_leak_auditor.auditor.validate_public_url", lambda url: url)

    def fake_fetch(_client, url, _host):
        if url.endswith("/missing"):
            return 404, "text/html", url, "<html><title>Not found</title></html>"
        return 200, "text/html", url, "<html><head><title>Home</title><meta name='description' content='Home'><meta name='viewport' content='width=device-width'></head><body><h1>Home</h1><a href='/missing'>Missing</a><a href='https://other.example/path'>External</a><a href='/about'>About</a></body></html>"

    monkeypatch.setattr("revenue_leak_auditor.auditor._fetch_html", fake_fetch)
    result = audit_website("https://example.com", max_pages=3)
    assert len(result.pages) == 3
    assert any(f.title == "Page returned HTTP 404" for f in result.findings)
    assert not any("other.example" in page.url for page in result.pages)


def test_report_includes_evidence_and_limits():
    result = AuditResult(target_url="https://example.com")
    result.pages.append(PageResult("https://example.com", 200, "text/html", "Example"))
    result.findings.append(Finding(
        title="Missing title", category="SEO", url="https://example.com", evidence="No title element.",
        impact="Medium", confidence="High", recommendation="Add a title.", verification="Inspect source.",
        business_rationale="Search visitors may have less context.",
    ))
    report = render_markdown(result)
    assert "Missing title" in report
    assert "No title element." in report
    assert "does not estimate revenue loss" in report
    assert "Pages inspected" in report


def test_page_limit_validation():
    with pytest.raises(ValueError, match="max_pages"):
        audit_website("https://example.com", max_pages=0)

 
 
def test_unsafe_discovered_link_is_skipped_without_duplicate_page(monkeypatch):
    from revenue_leak_auditor.safety import UnsafeTarget

    def validate(url):
        if ":8080" in url:
            raise UnsafeTarget("non-standard port")
        return url

    monkeypatch.setattr("revenue_leak_auditor.auditor.validate_public_url", validate)
    html = "<html><head><title>Home</title></head><body><h1>Home</h1><a href='http://example.com:8080/private'>Private port</a></body></html>"
    monkeypatch.setattr(
        "revenue_leak_auditor.auditor._fetch_html",
        lambda _client, url, _host: (200, "text/html", url, html),
    )
    result = audit_website("https://example.com", max_pages=3)
    assert len(result.pages) == 1
    assert any("Skipped a same-host link" in note for note in result.notes)


def test_rejects_malformed_port():
    with pytest.raises(UnsafeTarget, match="invalid port"):
        validate_public_url("https://example.com:not-a-port")


def test_same_host_redirect_is_followed_and_external_redirect_is_blocked(monkeypatch):
    import httpx
    from revenue_leak_auditor.auditor import _fetch_html

    monkeypatch.setattr("revenue_leak_auditor.auditor.validate_public_url", lambda url: url)
    seen = []

    def handler(request):
        seen.append(str(request.url))
        if request.url.path == "/start":
            return httpx.Response(302, headers={"Location": "/final"})
        return httpx.Response(200, headers={"Content-Type": "text/html; charset=utf-8"}, text="<title>Final</title>")

    with httpx.Client(transport=httpx.MockTransport(handler), follow_redirects=False) as client:
        status, content_type, final_url, html = _fetch_html(client, "https://example.com/start", "example.com")
    assert status == 200
    assert "text/html" in content_type
    assert final_url == "https://example.com/final"
    assert "Final" in html
    assert seen == ["https://example.com/start", "https://example.com/final"]

    def external_redirect(_request):
        return httpx.Response(302, headers={"Location": "https://other.example/"})

    with httpx.Client(transport=httpx.MockTransport(external_redirect), follow_redirects=False) as client:
        with pytest.raises(UnsafeTarget, match="Cross-host"):
            _fetch_html(client, "https://example.com/start", "example.com")


def test_report_redacts_sensitive_query_values_and_creates_folders(tmp_path):
    import json
    from revenue_leak_auditor.report import write_reports

    result = AuditResult(target_url="https://example.com/?access_token=secret-value&q=hello")
    result.notes.append("Could not inspect https://example.com/?session_id=note-secret: request failed")
    result.pages.append(PageResult("https://example.com/page?api_key=hidden", 200, "text/html", "Page"))
    md_path = tmp_path / "nested" / "audit.md"
    json_path = tmp_path / "nested" / "audit.json"
    write_reports(result, str(md_path), str(json_path))
    assert "secret-value" not in md_path.read_text(encoding="utf-8")
    assert "hidden" not in json_path.read_text(encoding="utf-8")
    assert "note-secret" not in json_path.read_text(encoding="utf-8")
    assert "note-secret" not in md_path.read_text(encoding="utf-8")
    assert "%5BREDACTED%5D" in json.loads(json_path.read_text(encoding="utf-8"))["target_url"]


def test_html_report_is_escaped_redacted_and_self_contained(tmp_path):
    from revenue_leak_auditor.report import render_html, write_reports

    result = AuditResult(target_url="https://example.com/?api_key=top-secret")
    result.findings.append(Finding(
        title="<script>alert('x')</script>", category="SEO", url="https://example.com/?token=secret",
        evidence="Observed <title> content.", impact="High", confidence="High",
        recommendation="Fix the title.", verification="Inspect the page.",
        business_rationale="A visitor may be confused.",
    ))
    rendered = render_html(result)
    assert "<script>alert('x')</script>" not in rendered
    assert "&lt;script&gt;" in rendered
    assert "top-secret" not in rendered and "secret</div>" not in rendered
    html_path = tmp_path / "client" / "audit.html"
    write_reports(result, str(tmp_path / "client" / "audit.md"), html_path=str(html_path))
    assert html_path.exists()


@pytest.mark.parametrize("url", ["http://[::1", "https://[2001:db8::1", "http://example.com:99999"])
def test_rejects_malformed_authority_and_invalid_port(url):
    with pytest.raises(UnsafeTarget):
        validate_public_url(url)


@pytest.mark.parametrize("max_pages", [True, 1.5, "5"])
def test_page_limit_requires_an_integer(max_pages):
    with pytest.raises(ValueError, match="integer between 1 and 15"):
        audit_website("https://example.com", max_pages=max_pages)


@pytest.mark.parametrize("timeout", [True, float("nan"), float("inf"), "10", 1, 31])
def test_timeout_requires_a_finite_number_in_range(timeout):
    with pytest.raises(ValueError, match="finite number between 2 and 30"):
        audit_website("https://example.com", timeout=timeout)
