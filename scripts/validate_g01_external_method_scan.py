#!/usr/bin/env python3
"""Validate G01 external method-source upgrade.

This checks that the methodology scan now includes public Chinese/practitioner
and institutional sources while preserving the limitation that G01 is improved,
not externally cleared.
"""

from __future__ import annotations

import csv
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATION_DIR = Path("cases/long-term-workflow-validation-2026-05-30")
AUDIT = VALIDATION_DIR / "g01-external-method-source-audit.csv"
UPGRADE = VALIDATION_DIR / "g01-external-method-source-upgrade-2026-05-30.md"

REQUIRED_COLUMNS = {
    "source_id",
    "source_name",
    "source_date",
    "language_or_circle",
    "source_bucket",
    "url",
    "method_claim",
    "workflow_use",
    "coverage_contribution",
    "remaining_limit",
    "release_impact",
}

REQUIRED_SOURCES = {
    "hillhouse_long_term_2015",
    "hillhouse_approach_current",
    "pingan_asset_equity_research",
    "jpm_ltcma_2026",
}


@dataclass
class Issue:
    severity: str
    subject: str
    message: str

    def render(self) -> str:
        return f"{self.severity}: {self.subject}: {self.message}"


def read_rows() -> tuple[list[dict[str, str]], list[Issue]]:
    try:
        with (ROOT / AUDIT).open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    except Exception as exc:
        return [], [Issue("ERROR", str(AUDIT), f"could not parse CSV: {exc}")]
    if not rows:
        return [], [Issue("ERROR", str(AUDIT), "source audit has no rows")]
    missing = sorted(REQUIRED_COLUMNS - set(rows[0].keys()))
    if missing:
        return rows, [Issue("ERROR", str(AUDIT), f"missing columns: {missing}")]
    return rows, []


def validate_scan() -> tuple[list[Issue], dict[str, int | bool]]:
    issues: list[Issue] = []
    rows, row_issues = read_rows()
    issues.extend(row_issues)
    stats: dict[str, int | bool] = {
        "sources": len(rows),
        "zh_sources": 0,
        "practitioner_sources": 0,
        "institutional_sources": 0,
        "supports_improvement": 0,
        "scan_improved": False,
    }
    if row_issues:
        return issues, stats

    seen = {row.get("source_id", "").strip() for row in rows}
    missing_sources = sorted(REQUIRED_SOURCES - seen)
    if missing_sources:
        issues.append(Issue("ERROR", str(AUDIT), f"missing required sources: {missing_sources}"))

    for i, row in enumerate(rows, start=2):
        source_id = row.get("source_id", "").strip()
        language = row.get("language_or_circle", "").strip()
        bucket = row.get("source_bucket", "").strip()
        release_impact = row.get("release_impact", "").strip()
        for field in ("url", "method_claim", "workflow_use", "coverage_contribution", "remaining_limit"):
            if not row.get(field, "").strip():
                issues.append(Issue("ERROR", str(AUDIT), f"row {i} {source_id} missing {field}"))
        if language.startswith("zh"):
            stats["zh_sources"] = int(stats["zh_sources"]) + 1
        if "practitioner" in bucket:
            stats["practitioner_sources"] = int(stats["practitioner_sources"]) + 1
        if "institutional" in bucket:
            stats["institutional_sources"] = int(stats["institutional_sources"]) + 1
        if release_impact == "supports_g01_improvement":
            stats["supports_improvement"] = int(stats["supports_improvement"]) + 1

    if int(stats["zh_sources"]) < 1:
        issues.append(Issue("ERROR", str(AUDIT), "must include at least one Chinese-language practitioner/institutional source"))
    if int(stats["practitioner_sources"]) < 2:
        issues.append(Issue("ERROR", str(AUDIT), "must include at least two practitioner/buyside public sources"))
    if int(stats["institutional_sources"]) < 2:
        issues.append(Issue("ERROR", str(AUDIT), "must include at least two institutional sources"))
    if int(stats["supports_improvement"]) < 4:
        issues.append(Issue("ERROR", str(AUDIT), "too few sources support G01 improvement"))

    try:
        text = (ROOT / UPGRADE).read_text(encoding="utf-8")
    except Exception as exc:
        issues.append(Issue("ERROR", str(UPGRADE), f"could not read upgrade memo: {exc}"))
        text = ""
    for marker in (
        "partial_pass_improved",
        "`pass_external`",
        "External reviewer challenge remains necessary",
        "Private buyside process detail remains undercovered",
        "stale_after:",
        "must_refresh_if:",
    ):
        if marker not in text:
            issues.append(Issue("ERROR", str(UPGRADE), f"missing marker `{marker}`"))

    stats["scan_improved"] = not [issue for issue in issues if issue.severity == "ERROR"]
    return issues, stats


def main() -> int:
    issues, stats = validate_scan()
    errors = [issue for issue in issues if issue.severity == "ERROR"]
    for issue in issues:
        print(issue.render())
    print("g01_external_method_scan_validation:")
    print(f"  scan_improved: {str(bool(stats['scan_improved'])).lower()}")
    print(f"  sources: {int(stats['sources'])}")
    print(f"  zh_sources: {int(stats['zh_sources'])}")
    print(f"  practitioner_sources: {int(stats['practitioner_sources'])}")
    print(f"  institutional_sources: {int(stats['institutional_sources'])}")
    print(f"  errors: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
