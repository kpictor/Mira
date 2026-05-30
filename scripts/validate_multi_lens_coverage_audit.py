#!/usr/bin/env python3
"""Validate multi-lens case coverage for the long-term workflow."""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATION_DIR = Path("cases/long-term-workflow-validation-2026-05-30")
AUDIT = VALIDATION_DIR / "multi-lens-coverage-audit.csv"
CROSS_CASE_MATRIX = VALIDATION_DIR / "cross-case-validation-matrix.csv"
DEFAULT_AS_OF = date(2026, 5, 30)

REQUIRED_COLUMNS = {
    "lens_id",
    "lens_name",
    "required_case_evidence",
    "case_ids",
    "evidence_artifact",
    "coverage_standard",
    "decision_delta",
    "status",
    "remaining_gap",
    "stale_after",
    "must_refresh_if",
}

REQUIRED_LENSES = {
    "LENS01": "consumer_demand",
    "LENS02": "product_reality",
    "LENS03": "economy_macro",
    "LENS04": "industry_structure",
    "LENS05": "company_execution",
    "LENS06": "valuation_expectations",
}

LENS_MARKERS = {
    "consumer_demand": {"consumer_demand", "pull_forward_vs_structural_demand", "hardware_subscription_mix", "payer_access_net_price"},
    "product_reality": {"product_reality", "product_monetization", "theme_to_company_handoff", "stablecoin_reserve_regulatory_quality"},
    "economy_macro": {"macro_demand", "macro_rates", "budget", "power_contract_regulatory_quality", "government_procurement_program_quality"},
    "industry_structure": {"industry_structure", "public_company_value_capture", "theme_to_company_handoff", "contract_quality"},
    "company_execution": {"company_execution", "capital_allocation", "acquisition_value_capture", "project_execution", "delivery"},
    "valuation_expectations": {"valuation_expectations"},
}

ALLOWED_STATUSES = {"pass_internal", "blocked_external"}
PLACEHOLDERS = {"", "tbd", "todo", "replace", "n/a"}


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
            return list(csv.DictReader(f)), []
    except Exception as exc:
        return [], [Issue("ERROR", str(path), f"could not parse CSV: {exc}")]


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
    if not rows:
        return {}, [Issue("ERROR", str(CROSS_CASE_MATRIX), "matrix has no rows")]
    index: dict[str, dict[str, str]] = {}
    for row in rows:
        case_id = row.get("case_id", "").strip()
        if not case_id:
            issues.append(Issue("ERROR", str(CROSS_CASE_MATRIX), "blank case_id"))
            continue
        index[case_id] = row
    return index, issues


def lens_blob(case: dict[str, str]) -> str:
    return ";".join(
        [
            case.get("primary_lens_tested", ""),
            case.get("secondary_lenses_tested", ""),
            case.get("overlay_or_patch_created", ""),
        ]
    ).lower()


def validate_audit(as_of: date) -> tuple[list[Issue], dict[str, int]]:
    issues: list[Issue] = []
    rows, row_issues = read_csv(AUDIT)
    issues.extend(row_issues)
    stats = {
        "lenses": len(rows),
        "case_links_checked": 0,
        "lens_markers_checked": 0,
        "decision_deltas_checked": 0,
    }
    if row_issues:
        return issues, stats
    if not rows:
        return [Issue("ERROR", str(AUDIT), "audit has no rows")], stats

    missing_columns = sorted(REQUIRED_COLUMNS - set(rows[0].keys()))
    if missing_columns:
        issues.append(Issue("ERROR", str(AUDIT), f"missing columns: {missing_columns}"))
        return issues, stats

    cases, case_issues = case_index()
    issues.extend(case_issues)

    seen = {row.get("lens_id", "").strip(): row for row in rows}
    for lens_id, lens_name in REQUIRED_LENSES.items():
        row = seen.get(lens_id)
        if not row:
            issues.append(Issue("ERROR", lens_id, f"missing required lens `{lens_name}`"))
            continue
        if row.get("lens_name", "").strip() != lens_name:
            issues.append(
                Issue(
                    "ERROR",
                    lens_id,
                    "lens_name mismatch: "
                    f"{row.get('lens_name', '').strip()} != {lens_name}",
                )
            )

    for i, row in enumerate(rows, start=2):
        lens_id = row.get("lens_id", "").strip()
        lens_name = row.get("lens_name", "").strip()
        for field in REQUIRED_COLUMNS:
            if has_placeholder(row.get(field, "")):
                issues.append(Issue("ERROR", str(AUDIT), f"row {i} `{lens_id}` has placeholder {field}"))

        evidence_path = row.get("evidence_artifact", "").strip()
        if evidence_path and not (ROOT / evidence_path).exists():
            issues.append(Issue("ERROR", str(AUDIT), f"row {i} evidence_artifact missing: {evidence_path}"))

        case_ids = split_multi(row.get("case_ids", ""))
        minimum_cases = 4 if lens_name in {"industry_structure", "valuation_expectations"} else 2
        if len(set(case_ids)) < minimum_cases:
            issues.append(Issue("ERROR", lens_id, f"needs at least {minimum_cases} linked cases"))

        markers = LENS_MARKERS.get(lens_name, set())
        matched_cases = 0
        for case_id in case_ids:
            stats["case_links_checked"] += 1
            case = cases.get(case_id)
            if not case:
                issues.append(Issue("ERROR", str(AUDIT), f"row {i} unknown case_id `{case_id}`"))
                continue
            blob = lens_blob(case)
            if any(marker.lower() in blob for marker in markers):
                matched_cases += 1
            if not case.get("actionability_change", "").strip():
                issues.append(Issue("ERROR", str(AUDIT), f"row {i} case `{case_id}` lacks actionability_change"))
        if matched_cases < minimum_cases:
            issues.append(Issue("ERROR", lens_id, f"only {matched_cases} linked cases show matching lens markers"))
        else:
            stats["lens_markers_checked"] += matched_cases

        if row.get("status", "").strip() not in ALLOWED_STATUSES:
            issues.append(Issue("ERROR", str(AUDIT), f"row {i} invalid status `{row.get('status', '').strip()}`"))

        decision_delta = row.get("decision_delta", "").strip().lower()
        if not any(marker in decision_delta for marker in ("downgraded", "blocked", "changed", "stop")):
            issues.append(Issue("ERROR", str(AUDIT), f"row {i} decision_delta must show actionability or stop-rule change"))
        else:
            stats["decision_deltas_checked"] += 1

        stale_after = parse_date(row.get("stale_after", ""))
        if stale_after is None:
            issues.append(Issue("ERROR", str(AUDIT), f"row {i} invalid stale_after"))
        elif stale_after <= as_of:
            issues.append(Issue("ERROR", str(AUDIT), f"row {i} stale_after must be after as_of"))
        elif (stale_after - as_of).days > 45:
            issues.append(Issue("ERROR", str(AUDIT), f"row {i} stale_after is too far away for lens coverage"))

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
    print("multi_lens_coverage_audit_validation:")
    print(f"  lenses: {stats['lenses']}")
    print(f"  case_links_checked: {stats['case_links_checked']}")
    print(f"  lens_markers_checked: {stats['lens_markers_checked']}")
    print(f"  decision_deltas_checked: {stats['decision_deltas_checked']}")
    print(f"  errors: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
