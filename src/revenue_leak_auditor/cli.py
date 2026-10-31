from __future__ import annotations

import argparse
import sys

from . import __version__
from .auditor import audit_website
from .report import write_reports
from .safety import UnsafeTarget


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="revenue-auditor",
        description="Run a bounded, evidence-first static website audit and save a Markdown report.",
        epilog="Only audit websites you own or are authorised to assess.",
    )
    parser.add_argument("url", help="Public website URL, for example https://example.com")
    parser.add_argument("--max-pages", type=int, default=5, help="Maximum pages to inspect (1-15; default: 5)")
    parser.add_argument("--timeout", type=float, default=10, help="Per-request timeout in seconds (2-30; default: 10)")
    parser.add_argument("--output", default="audit-report.md", help="Markdown report path (default: audit-report.md)")
    parser.add_argument("--json", dest="json_path", help="Optional JSON report path")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        print(f"Auditing {args.url} (up to {args.max_pages} pages)...")
        result = audit_website(args.url, max_pages=args.max_pages, timeout=args.timeout)
        write_reports(result, args.output, args.json_path)
    except (UnsafeTarget, ValueError) as exc:
        parser.error(str(exc))
    except KeyboardInterrupt:
        print("Audit cancelled.", file=sys.stderr)
        raise SystemExit(130)
    counts = result.summary
    print(f"Done: {len(result.pages)} page(s) inspected; {len(result.findings)} finding(s).")
    print(f"Priority: {counts['high']} high / {counts['medium']} medium / {counts['low']} low")
    print(f"Markdown report: {args.output}")
    if args.json_path:
        print(f"JSON report: {args.json_path}")


if __name__ == "__main__":
    main()
