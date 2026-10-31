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
