"""Conservative URL validation for the local, single-user CLI.

This is a defence-in-depth guard, not a hardened network sandbox. A hosted,
multi-tenant deployment must pin DNS resolution to the validated address at the
connection layer to eliminate DNS-rebinding/TOCTOU risks.
"""

from __future__ import annotations

import ipaddress
import socket
from urllib.parse import urlsplit, urlunsplit


class UnsafeTarget(ValueError):
    """Raised when a URL is outside the auditor's permitted network scope."""


def _resolve_addresses(hostname: str) -> set[str]:
    try:
        rows = socket.getaddrinfo(hostname, None, type=socket.SOCK_STREAM)
    except socket.gaierror as exc:
        raise UnsafeTarget(f"Could not resolve host: {hostname}") from exc
    return {row[4][0].split("%", 1)[0] for row in rows}


def validate_public_url(raw_url: str) -> str:
    """Validate and normalise an HTTP(S) URL whose resolved IPs are public."""
    if not raw_url or len(raw_url) > 2048:
        raise UnsafeTarget("URL is empty or exceeds 2,048 characters")

    parts = urlsplit(raw_url.strip())
    scheme = parts.scheme.lower()
    if scheme not in {"http", "https"}:
        raise UnsafeTarget("Only http:// and https:// URLs are allowed")
    if not parts.hostname:
        raise UnsafeTarget("URL must include a hostname")
    if parts.username is not None or parts.password is not None:
        raise UnsafeTarget("URLs containing embedded credentials are not allowed")

    hostname = parts.hostname.rstrip(".").lower()
    if hostname == "localhost" or hostname.endswith(".localhost") or hostname.endswith(".local"):
        raise UnsafeTarget("Local hostnames are not allowed")
    allowed_port = 80 if scheme == "http" else 443
    try:
        port = parts.port
    except ValueError as exc:
        raise UnsafeTarget("URL contains an invalid port") from exc
    if port not in (None, allowed_port):
        raise UnsafeTarget("Only the standard port for the selected HTTP scheme is allowed")

    try:
        literal = ipaddress.ip_address(hostname)
        addresses = {str(literal)}
    except ValueError:
        addresses = _resolve_addresses(hostname)

    if not addresses:
        raise UnsafeTarget("Host did not resolve to an IP address")
    for address in addresses:
        ip = ipaddress.ip_address(address)
        if not ip.is_global:
            raise UnsafeTarget(f"Host resolves to a non-public address ({address})")

    netloc = f"[{hostname}]" if ":" in hostname else hostname
    if port:
        netloc = f"{netloc}:{port}"
    return urlunsplit((scheme, netloc, parts.path or "/", parts.query, ""))
