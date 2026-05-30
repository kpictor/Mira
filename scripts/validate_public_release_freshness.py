#!/usr/bin/env python3
"""Validate freshness controls for public-release workflow materials.

The release package should not become an institutional workflow through
document inertia. Public-facing materials need concrete stale_after dates and
observable refresh triggers; templates need explicit refresh fields so a future
signed artifact cannot omit them.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATION_DIR = Path("cases/long-term-workflow-validation-2026-05-30")
PUBLIC_PACK = VALIDATION_DIR / "public-workflow-pack"
DEFAULT_AS_OF = "2026-05-30"
MAX_STALE_WINDOW_DAYS = 45

CONCRETE_PUBLIC_DOCS = [
    PUBLIC_PACK / "README.md",
    PUBLIC_PACK / "operator-runbook.md",
    PUBLIC_PACK / "source-appendix.md",
    PUBLIC_PACK / "external-review-request.md",
    PUBLIC_PACK / "external-reviewer-brief.md",
    PUBLIC_PACK / "institutional-use-boundaries.md",
    PUBLIC_PACK / "institutional-adoption-faq.md",
    PUBLIC_PACK / "reviewer-dry-run-2026-05-30.md",
    VALIDATION_DIR / "public-readiness-audit.md",
    VALIDATION_DIR / "public-release-decision.md",
    VALIDATION_DIR / "public-handoff-manifest.md",
    VALIDATION_DIR / "release-qa-report-2026-05-30.md",
    VALIDATION_DIR / "g06-external-review-handoff-2026-05-30.md",
    VALIDATION_DIR / "g04-follow-through-handoff-2026-05-30.md",
    VALIDATION_DIR / "follow-through-refresh-playbook.md",
]

TEMPLATE_DOCS = [
    VALIDATION_DIR / "external-release-go-no-go-template.md",
    PUBLIC_PACK / "external-review-results-template.md",
    PUBLIC_PACK / "institutional-colleague-release-notes-template.md",
    PUBLIC_PACK / "institutional-colleague-acceptance-memo-template.md",
]

PLACEHOLDERS = {"", "replace", "tbd", "todo", "n/a"}
REFRESH_TRIGGER_MARKERS = {
    "G04",
    "G06",
    "reviewer",
    "case",
    "event",
    "source",
    "gate",
    "release",
    "material",
    "changes",
    "findings",
}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


@dataclass
class Issue:
    severity: str
    subject: str
    message: str

    def render(self) -> str:
        return f"{self.severity}: {self.subject}: {self.message}"


def parse_date(value: str) -> date | None:
    token = value.strip().split()[0] if value.strip() else ""
    if not DATE_RE.match(token):
        return None
    try:
        return date.fromisoformat(token)
    except ValueError:
        return None


def scalar_from_text(text: str, key: str) -> str:
    match = re.search(rf"^[ \t]*-[ \t]*{re.escape(key)}:[ \t]*(.*)[ \t]*$", text, re.MULTILINE)
    if not match:
        return ""
    return match.group(1).strip().strip("`")


def validate_concrete_doc(path: Path, as_of: date) -> list[Issue]:
    issues: list[Issue] = []
    full_path = ROOT / path
    try:
        text = full_path.read_text(encoding="utf-8")
    except Exception as exc:
        return [Issue("ERROR", str(path), f"could not read file: {exc}")]

    stale_raw = scalar_from_text(text, "stale_after")
    stale_after = parse_date(stale_raw)
    if stale_after is None:
        issues.append(Issue("ERROR", str(path), f"stale_after must be concrete YYYY-MM-DD, got `{stale_raw}`"))
    else:
        if stale_after <= as_of:
            issues.append(Issue("ERROR", str(path), f"stale_after must be after as_of {as_of.isoformat()}"))
        if (stale_after - as_of).days > MAX_STALE_WINDOW_DAYS:
            issues.append(Issue("ERROR", str(path), f"stale_after is more than {MAX_STALE_WINDOW_DAYS} days after as_of"))

    refresh = scalar_from_text(text, "must_refresh_if")
    if refresh.strip().lower() in PLACEHOLDERS:
        issues.append(Issue("ERROR", str(path), "must_refresh_if is missing or placeholder"))
    if len(refresh) < 20:
        issues.append(Issue("ERROR", str(path), "must_refresh_if is too vague"))
    if not any(marker.lower() in refresh.lower() for marker in REFRESH_TRIGGER_MARKERS):
        issues.append(Issue("ERROR", str(path), "must_refresh_if lacks observable refresh trigger markers"))

    return issues


def validate_template_doc(path: Path) -> list[Issue]:
    try:
        text = (ROOT / path).read_text(encoding="utf-8")
    except Exception as exc:
        return [Issue("ERROR", str(path), f"could not read file: {exc}")]

    issues: list[Issue] = []
    if "stale_after:" not in text:
        issues.append(Issue("ERROR", str(path), "template missing stale_after field"))
    if "must_refresh_if:" not in text:
        issues.append(Issue("ERROR", str(path), "template missing must_refresh_if field"))
    return issues


def validate_freshness(as_of: date) -> tuple[list[Issue], dict[str, int | str]]:
    issues: list[Issue] = []
    for path in CONCRETE_PUBLIC_DOCS:
        issues.extend(validate_concrete_doc(path, as_of))
    for path in TEMPLATE_DOCS:
        issues.extend(validate_template_doc(path))

    stats: dict[str, int | str] = {
        "concrete_documents_checked": len(CONCRETE_PUBLIC_DOCS),
        "template_documents_checked": len(TEMPLATE_DOCS),
        "stale_after_window_days": MAX_STALE_WINDOW_DAYS,
        "as_of": as_of.isoformat(),
    }
    return issues, stats


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--as-of", default=DEFAULT_AS_OF)
    args = parser.parse_args()

    as_of = parse_date(args.as_of)
    if as_of is None:
        print(f"ERROR: --as-of must be YYYY-MM-DD, got `{args.as_of}`")
        return 1

    issues, stats = validate_freshness(as_of)
    errors = [issue for issue in issues if issue.severity == "ERROR"]
    for issue in issues:
        print(issue.render())
    print("public_release_freshness_validation:")
    print(f"  as_of: {stats['as_of']}")
    print(f"  concrete_documents_checked: {stats['concrete_documents_checked']}")
    print(f"  template_documents_checked: {stats['template_documents_checked']}")
    print(f"  stale_after_window_days: {stats['stale_after_window_days']}")
    print(f"  errors: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
