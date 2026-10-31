# Security model and limitations

## Intended use
This release is a local, single-user command-line tool for a person auditing a site they own or are authorised to assess. It is not a public URL-scanning service.

## Controls currently implemented
- HTTP and HTTPS only.
- Rejects URL-embedded credentials and non-standard ports.
- Resolves hostnames and rejects any non-global IP answer; rejects localhost and local-name suffixes.
- Manually follows a maximum of four redirects and requires the redirect hostname to remain the original hostname.
- Disables automatic redirect following and environment proxy inheritance in HTTPX.
- Restricts discovered pages to the original hostname.
- Defaults to five pages, allows at most 15, applies request timeouts, caps each HTML response at 2 MB, and limits HTTP connection concurrency.
- Performs GET requests only; does not submit forms or interact with checkout, login, booking, or messaging workflows.
- Does not execute page JavaScript or download non-HTML assets.

## Important DNS-rebinding limitation
The code checks DNS answers before making a request, but HTTPX performs its own hostname resolution when it opens the connection. Those two resolutions are not pinned to the same address. A hostile DNS configuration could therefore change its answer between validation and connection (a DNS-rebinding / time-of-check-to-use gap).

Do not deploy this version as a hosted service that accepts arbitrary URLs from untrusted users. A production service must pin the connection to the validated public IP while preserving the correct Host header and TLS SNI, revalidate every redirect at the transport boundary, isolate outbound network access, and enforce tenant-level quotas and abuse controls.

## Other limitations
- Static HTML parsing misses content that appears only after JavaScript runs.
- The CTA check is a low-confidence text heuristic and may miss icon-only controls or non-standard wording.
- An image with an empty alt attribute may be intentionally decorative; the current check reports only missing attributes, not semantic quality.
- A 404/5xx result is an observation at the time of the audit; transient failures are possible.
- Impact labels are triage guidance, not financial estimates. The tool has no analytics or sales data.

## Report privacy

Markdown, JSON, and HTML reports redact query values for common sensitive parameter names such as `token`, `key`, `secret`, `password`, `auth`, `session`, and `csrf`. This is a best-effort safeguard, not secret detection: custom parameter names and secrets embedded in paths or page content may not be recognised. Avoid putting secrets in audit URLs.

## Safe operation checklist
1. Obtain permission before running an audit.
2. Keep crawl size conservative; do not raise limits to overwhelm a site.
3. Avoid authenticated or sensitive URLs.
4. Do not use this build for broad internet scanning.
5. Review findings manually before contacting a business or making claims about its revenue.
