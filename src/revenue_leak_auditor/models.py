from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(slots=True)
class Finding:
    title: str
    category: str
    url: str
    evidence: str
    impact: str
    confidence: str
    recommendation: str
    verification: str
    business_rationale: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class PageResult:
    url: str
    status_code: int | None
    content_type: str
    title: str = ""
    error: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class AuditResult:
    target_url: str
    started_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    pages: list[PageResult] = field(default_factory=list)
    findings: list[Finding] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @property
    def summary(self) -> dict[str, int]:
        return {
            "high": sum(f.impact == "High" for f in self.findings),
            "medium": sum(f.impact == "Medium" for f in self.findings),
            "low": sum(f.impact == "Low" for f in self.findings),
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "target_url": self.target_url,
            "started_at": self.started_at,
            "pages": [p.to_dict() for p in self.pages],
            "findings": [f.to_dict() for f in self.findings],
            "summary": self.summary,
            "notes": self.notes,
        }
