#!/usr/bin/env python3
"""Validate Mira repository research discipline.

Default mode is strict and exits non-zero on errors. Use --report-only to
surface current legacy drift without failing the run.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from dataclasses import dataclass
from pathlib import Path


CANONICAL_EVIDENCE_COLUMNS = [
    "source_id",
    "claim_area",
    "claim_type",
    "claim_text",
    "source_speaker",
    "verification_status",
    "authority_level",
    "source_date",
    "as_of_date",
    "url_or_path",
    "used_by_agent",
    "used_by_skill",
    "confidence",
    "upstream_sources",
    "notes",
]

CLAIM_TYPES = {
    "fact",
    "reported_metric",
    "company_claim",
    "guidance",
    "target",
    "commitment",
    "forecast",
    "assumption",
    "interpretation",
    "opinion",
    "market_pricing",
    "sentiment",
    "rumor_signal",
    "derived_calculation",
}

VERIFICATION_STATUSES = {
    "verified",
    "disclosed",
    "claimed",
    "estimated",
    "modeled",
    "unverified",
    "contradicted",
}

AUTHORITY_LEVELS = {"L1", "L2", "L3", "L4", "L5", "L6"}
CONFIDENCE_LEVELS = {"high", "medium", "low"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

SOURCE_RECORD_COLUMNS = {
    "source_name",
    "source_type",
    "source_group",
    "content_mode",
    "credibility_level",
    "content_type",
    "research_role",
    "market_scope",
    "access_method",
    "acquisition_mode",
    "update_frequency",
    "latency_class",
    "as_of_date_required",
    "usable_for",
    "last_checked_date",
}


@dataclass
class Issue:
    severity: str
    path: Path
    line: int
    message: str

    def render(self) -> str:
        loc = f"{self.path}:{self.line}" if self.line else str(self.path)
        return f"{self.severity}: {loc}: {self.message}"


def is_template(path: Path) -> bool:
    return "templates" in path.parts


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]], list[Issue]]:
    issues: list[Issue] = []
    try:
        with path.open(newline="") as f:
            reader = csv.DictReader(f)
            header = reader.fieldnames or []
            rows = [dict(row) for row in reader]
    except Exception as exc:  # pragma: no cover - defensive for repo checks
        issues.append(Issue("ERROR", path, 0, f"could not read CSV: {exc}"))
        return [], [], issues

    if not header:
        issues.append(Issue("ERROR", path, 1, "missing CSV header"))
    return header, rows, issues


def validate_evidence_log(path: Path) -> list[Issue]:
    header, rows, issues = read_csv(path)
    if not header:
        return issues

    header_set = set(header)
    if header != CANONICAL_EVIDENCE_COLUMNS:
        missing = [c for c in CANONICAL_EVIDENCE_COLUMNS if c not in header_set]
        extra = [c for c in header if c not in CANONICAL_EVIDENCE_COLUMNS]
        if SOURCE_RECORD_COLUMNS & header_set:
            issues.append(
                Issue(
                    "ERROR",
                    path,
                    1,
                    "evidence-log.csv appears to use source-record schema; use claim-level canonical evidence schema",
                )
            )
        issues.append(
            Issue(
                "ERROR",
                path,
                1,
                f"non-canonical evidence-log header; missing={missing}; extra={extra}",
            )
        )
        return issues

    if is_template(path):
        return issues

    for i, row in enumerate(rows, start=2):
        for field in CANONICAL_EVIDENCE_COLUMNS:
            if not (row.get(field) or "").strip():
                issues.append(Issue("ERROR", path, i, f"missing required field `{field}`"))

        claim_type = row.get("claim_type", "").strip()
        if claim_type and claim_type not in CLAIM_TYPES:
            issues.append(Issue("ERROR", path, i, f"invalid claim_type `{claim_type}`"))

        verification_status = row.get("verification_status", "").strip()
        if verification_status and verification_status not in VERIFICATION_STATUSES:
            issues.append(
                Issue("ERROR", path, i, f"invalid verification_status `{verification_status}`")
            )

        authority_level = row.get("authority_level", "").strip()
        if authority_level and authority_level not in AUTHORITY_LEVELS:
            issues.append(Issue("ERROR", path, i, f"invalid authority_level `{authority_level}`"))

        confidence = row.get("confidence", "").strip()
        if confidence and confidence not in CONFIDENCE_LEVELS:
            issues.append(Issue("ERROR", path, i, f"invalid confidence `{confidence}`"))

        for field in ("source_date", "as_of_date"):
            value = row.get(field, "").strip()
            if value and not DATE_RE.match(value):
                issues.append(Issue("ERROR", path, i, f"`{field}` must be YYYY-MM-DD"))

        upstream = row.get("upstream_sources", "").strip()
        if (claim_type == "derived_calculation" or authority_level == "L6") and upstream in {
            "",
            "not_applicable",
            "na",
            "n/a",
        }:
            issues.append(
                Issue(
                    "ERROR",
                    path,
                    i,
                    "derived_calculation or L6 claim requires upstream_sources",
                )
            )

        if claim_type == "rumor_signal" and confidence == "high":
            issues.append(Issue("ERROR", path, i, "rumor_signal cannot have high confidence"))

        if claim_type in {"sentiment", "opinion", "rumor_signal"} and verification_status == "verified":
            issues.append(
                Issue(
                    "WARN",
                    path,
                    i,
                    f"{claim_type} with verification_status=verified is usually a classification smell",
                )
            )

    if not rows:
        issues.append(Issue("ERROR", path, 1, "evidence-log.csv has no claim rows"))

    return issues


def validate_methodology_adoption(root: Path) -> list[Issue]:
    path = root / "memory" / "methodologies" / "adopted.md"
    if not path.exists():
        return []

    issues: list[Issue] = []
    lines = path.read_text().splitlines()
    current_method = None
    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("- `") and stripped.endswith("`"):
            current_method = stripped.strip("- `")
        if stripped.startswith("based_on_cases:") and current_method:
            value = stripped.split(":", 1)[1].strip().lower()
            weak_markers = {"design iteration", "sample", "routed design iteration"}
            if any(marker in value for marker in weak_markers):
                issues.append(
                    Issue(
                        "WARN",
                        path,
                        i,
                        f"`{current_method}` adoption is based on design/sample rather than outcome-reviewed cases",
                    )
                )
    return issues


def validate_repo(root: Path) -> list[Issue]:
    issues: list[Issue] = []
    for path in sorted(root.glob("**/evidence-log.csv")):
        if ".git" in path.parts:
            continue
        issues.extend(validate_evidence_log(path))
    issues.extend(validate_methodology_adoption(root))
    return issues


def validate_paths(paths: list[Path]) -> list[Issue]:
    issues: list[Issue] = []
    for path in paths:
        if path.is_dir():
            evidence = path / "evidence-log.csv"
            if evidence.exists():
                issues.extend(validate_evidence_log(evidence))
            else:
                issues.append(Issue("ERROR", path, 0, "directory has no evidence-log.csv"))
        elif path.name == "evidence-log.csv":
            issues.extend(validate_evidence_log(path))
        else:
            issues.append(Issue("ERROR", path, 0, "expected evidence-log.csv or case directory"))
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="repository root")
    parser.add_argument(
        "paths",
        nargs="*",
        help="optional evidence-log.csv files or case directories to validate instead of full repo",
    )
    parser.add_argument(
        "--report-only",
        action="store_true",
        help="print issues but exit 0; useful while migrating legacy cases",
    )
    args = parser.parse_args()

    root = Path(args.root)
    if args.paths:
        issues = validate_paths([root / path for path in args.paths])
    else:
        issues = validate_repo(root)
    errors = [issue for issue in issues if issue.severity == "ERROR"]
    warnings = [issue for issue in issues if issue.severity == "WARN"]

    for issue in issues:
        print(issue.render())

    print(f"summary: {len(errors)} errors, {len(warnings)} warnings")

    if args.report_only:
        return 0
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
