#!/usr/bin/env python3
"""Validate that methodology claims are grounded in practice evidence."""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATION_DIR = Path("cases/long-term-workflow-validation-2026-05-30")
AUDIT = VALIDATION_DIR / "practice-falsification-audit.csv"
CROSS_CASE_MATRIX = VALIDATION_DIR / "cross-case-validation-matrix.csv"
OVERLAY_AUDIT = VALIDATION_DIR / "overlay-coverage-audit.csv"
G04_CANDIDATE_SCREEN = VALIDATION_DIR / "g04-later-event-candidate-screen.csv"
DEFAULT_AS_OF = date(2026, 5, 30)

REQUIRED_COLUMNS = {
    "claim_id",
    "methodology_claim",
    "required_practice_evidence",
    "case_ids",
    "evidence_artifact",
    "falsification_test",
    "actionability_delta",
    "status",
    "public_release_boundary",
    "stale_after",
    "must_refresh_if",
}

REQUIRED_CLAIMS = {
    "PFA01": "multi_lens_workflow_must_change_decisions",
    "PFA02": "theme_to_stock_requires_value_capture_evidence",
    "PFA03": "valuation_expectations_can_override_business_quality",
    "PFA04": "product_traction_is_not_company_monetization",
    "PFA05": "pull_forward_demand_must_be_separated_from_structural_demand",
    "PFA06": "overlays_are_promoted_only_from_case_failures",
    "PFA07": "follow_through_claims_require_post_cutoff_events",
    "PFA08": "source_gaps_must_change_release_status_or_actionability",
}

ALLOWED_STATUSES = {"pass_internal", "blocked_external"}
PLACEHOLDERS = {"", "tbd", "todo", "replace", "n/a", "none"}


@dataclass
class Issue:
    severity: str
    subject: str
    message: str

    def render(self) -> str:
        return f"{self.severity}: {self.subject}: {self.message}"


def read_csv(path: Path) -> tuple[list[dict[str, str]], list[Issue]]:
    try:
        with (ROOT / path).open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    except Exception as exc:
        return [], [Issue("ERROR", str(path), f"could not parse CSV: {exc}")]
    if not rows:
        return [], [Issue("ERROR", str(path), "CSV has no rows")]
    return rows, []


def parse_date(value: str) -> date | None:
    try:
        return date.fromisoformat(value.strip())
    except ValueError:
        return None


def split_multi(value: str) -> list[str]:
    return [item.strip() for item in value.replace("|", ";").split(";") if item.strip()]


def has_placeholder(value: str) -> bool:
    return value.strip().lower() in PLACEHOLDERS


def case_index() -> tuple[dict[str, dict[str, str]], list[Issue]]:
    rows, issues = read_csv(CROSS_CASE_MATRIX)
    if issues:
        return {}, issues
    index: dict[str, dict[str, str]] = {}
    for row in rows:
        case_id = row.get("case_id", "").strip()
        if not case_id:
            issues.append(Issue("ERROR", str(CROSS_CASE_MATRIX), "blank case_id"))
            continue
        index[case_id] = row
    return index, issues


def validate_audit(as_of: date) -> tuple[list[Issue], dict[str, int]]:
    issues: list[Issue] = []
    rows, row_issues = read_csv(AUDIT)
    issues.extend(row_issues)
    stats = {
        "claims": len(rows),
        "case_links_checked": 0,
        "falsification_tests_checked": 0,
        "blocked_external_claims": 0,
    }
    if row_issues:
        return issues, stats

    header = set(rows[0].keys())
    missing_columns = sorted(REQUIRED_COLUMNS - header)
    if missing_columns:
        issues.append(Issue("ERROR", str(AUDIT), f"missing columns: {missing_columns}"))
        return issues, stats

    cases, case_issues = case_index()
    issues.extend(case_issues)

    seen = {row.get("claim_id", "").strip(): row for row in rows}
    for claim_id, claim_name in REQUIRED_CLAIMS.items():
        row = seen.get(claim_id)
        if not row:
            issues.append(Issue("ERROR", claim_id, f"missing methodology claim `{claim_name}`"))
            continue
        if row.get("methodology_claim", "").strip() != claim_name:
            issues.append(
                Issue(
                    "ERROR",
                    claim_id,
                    "methodology_claim mismatch: "
                    f"{row.get('methodology_claim', '').strip()} != {claim_name}",
                )
            )

    for i, row in enumerate(rows, start=2):
        claim_id = row.get("claim_id", "").strip()
        claim_name = row.get("methodology_claim", "").strip()
        for field in REQUIRED_COLUMNS:
            if has_placeholder(row.get(field, "")):
                issues.append(Issue("ERROR", str(AUDIT), f"row {i} `{claim_id}` has placeholder {field}"))

        evidence_path = row.get("evidence_artifact", "").strip()
        if evidence_path and not (ROOT / evidence_path).exists():
            issues.append(Issue("ERROR", str(AUDIT), f"row {i} evidence_artifact missing: {evidence_path}"))
        if evidence_path and not evidence_path.startswith(str(VALIDATION_DIR)):
            issues.append(Issue("ERROR", str(AUDIT), f"row {i} evidence_artifact outside validation package"))

        case_ids = split_multi(row.get("case_ids", ""))
        if not case_ids:
            issues.append(Issue("ERROR", str(AUDIT), f"row {i} `{claim_id}` has no case_ids"))
        for case_id in case_ids:
            stats["case_links_checked"] += 1
            if case_id not in cases:
                issues.append(Issue("ERROR", str(AUDIT), f"row {i} unknown case_id `{case_id}`"))

        if claim_id == "PFA01" and len(set(case_ids)) < 8:
            issues.append(Issue("ERROR", claim_id, "multi-lens practice claim needs at least eight case links"))
        if claim_id == "PFA02":
            expected_theme_cases = {
                "HUMANOID_ROBOTICS_2026",
                "NUCLEAR_AI_POWER_2026",
                "STABLECOIN_PAYMENTS_2026",
                "DEFENSE_AUTONOMY_2026",
            }
            if not expected_theme_cases.issubset(set(case_ids)):
                issues.append(Issue("ERROR", claim_id, "theme-to-stock claim missing hot-theme screens"))
        if claim_id == "PFA07" and row.get("status", "").strip() != "blocked_external":
            issues.append(Issue("ERROR", claim_id, "follow-through practice claim must remain blocked_external before G04 clears"))

        for case_id in case_ids:
            case = cases.get(case_id)
            if not case:
                continue
            actionability_change = case.get("actionability_change", "").strip()
            if not actionability_change:
                issues.append(Issue("ERROR", str(AUDIT), f"row {i} case `{case_id}` lacks actionability_change"))
            if claim_id == "PFA08" and not case.get("source_gap_exposed", "").strip():
                issues.append(Issue("ERROR", str(AUDIT), f"row {i} case `{case_id}` lacks source_gap_exposed"))

        falsification_test = row.get("falsification_test", "").strip().lower()
        if "reject" not in falsification_test:
            issues.append(Issue("ERROR", str(AUDIT), f"row {i} falsification_test must state a rejection condition"))
        else:
            stats["falsification_tests_checked"] += 1

        if row.get("status", "").strip() not in ALLOWED_STATUSES:
            issues.append(Issue("ERROR", str(AUDIT), f"row {i} invalid status `{row.get('status', '').strip()}`"))
        if row.get("status", "").strip() == "blocked_external":
            stats["blocked_external_claims"] += 1

        boundary = row.get("public_release_boundary", "").strip()
        if row.get("status", "").strip() == "blocked_external" and "G04" not in boundary:
            issues.append(Issue("ERROR", str(AUDIT), f"row {i} blocked_external claim missing G04 boundary"))
        if claim_id in {"PFA01", "PFA02", "PFA03", "PFA05", "PFA08"} and "G06" not in boundary:
            issues.append(Issue("ERROR", claim_id, "practice claim must preserve G06 reviewer boundary"))

        stale_after = parse_date(row.get("stale_after", ""))
        if stale_after is None:
            issues.append(Issue("ERROR", str(AUDIT), f"row {i} invalid stale_after"))
        elif stale_after <= as_of:
            issues.append(Issue("ERROR", str(AUDIT), f"row {i} stale_after must be after as_of"))
        elif (stale_after - as_of).days > 45:
            issues.append(Issue("ERROR", str(AUDIT), f"row {i} stale_after is too far away for practice validation"))

        if claim_name.endswith("theory") or "theory_only" in row.get("status", "").lower():
            issues.append(Issue("ERROR", str(AUDIT), f"row {i} appears to preserve a theory-only claim"))

    if (ROOT / OVERLAY_AUDIT).exists() and not any(row.get("claim_id", "").strip() == "PFA06" for row in rows):
        issues.append(Issue("ERROR", str(AUDIT), "overlay practice claim missing despite overlay audit"))
    if (ROOT / G04_CANDIDATE_SCREEN).exists() and not any(row.get("claim_id", "").strip() == "PFA07" for row in rows):
        issues.append(Issue("ERROR", str(AUDIT), "follow-through practice claim missing despite G04 candidate screen"))

    return issues, stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--as-of", default=DEFAULT_AS_OF.isoformat(), help="as-of date YYYY-MM-DD")
    args = parser.parse_args()
    as_of = parse_date(args.as_of)
    if as_of is None:
        print(f"ERROR: --as-of: invalid date `{args.as_of}`")
        return 1

    issues, stats = validate_audit(as_of)
    errors = [issue for issue in issues if issue.severity == "ERROR"]
    for issue in issues:
        print(issue.render())
    print("practice_falsification_audit_validation:")
    print(f"  claims: {stats['claims']}")
    print(f"  case_links_checked: {stats['case_links_checked']}")
    print(f"  falsification_tests_checked: {stats['falsification_tests_checked']}")
    print(f"  blocked_external_claims: {stats['blocked_external_claims']}")
    print(f"  errors: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
