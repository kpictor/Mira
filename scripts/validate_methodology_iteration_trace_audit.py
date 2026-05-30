#!/usr/bin/env python3
"""Validate that methodology iterations trace back to case failures."""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATION_DIR = Path("cases/long-term-workflow-validation-2026-05-30")
AUDIT = VALIDATION_DIR / "methodology-iteration-trace-audit.csv"
CROSS_CASE_MATRIX = VALIDATION_DIR / "cross-case-validation-matrix.csv"
DEFAULT_AS_OF = date(2026, 5, 30)

REQUIRED_COLUMNS = {
    "iteration_id",
    "case_trigger",
    "failure_mode",
    "methodology_patch",
    "patch_artifact",
    "evidence_artifact",
    "validation_command",
    "decision_effect",
    "release_boundary",
    "stale_after",
    "must_refresh_if",
}

REQUIRED_ITERATIONS = {f"ITER{i:02d}" for i in range(1, 13)}
REQUIRED_CASE_TRIGGERS = {
    "ETN_2026",
    "VRT_2026",
    "CRM_2026",
    "LLY_2026",
    "TDOC_2020_2022",
    "PTON_2020_2022",
    "HUMANOID_ROBOTICS_2026",
    "NUCLEAR_AI_POWER_2026",
    "STABLECOIN_PAYMENTS_2026",
    "DEFENSE_AUTONOMY_2026",
}
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
    if value is None:
        return True
    return value.strip().lower() in PLACEHOLDERS


def case_ids() -> tuple[set[str], list[Issue]]:
    rows, issues = read_csv(CROSS_CASE_MATRIX)
    if issues:
        return set(), issues
    return {row.get("case_id", "").strip() for row in rows if row.get("case_id", "").strip()}, []


def validate_audit(as_of: date) -> tuple[list[Issue], dict[str, int]]:
    issues: list[Issue] = []
    rows, row_issues = read_csv(AUDIT)
    issues.extend(row_issues)
    stats = {
        "iterations": len(rows),
        "case_triggers_checked": 0,
        "patch_artifacts_checked": 0,
        "validation_commands_checked": 0,
    }
    if row_issues:
        return issues, stats
    if not rows:
        return [Issue("ERROR", str(AUDIT), "audit has no rows")], stats

    missing_columns = sorted(REQUIRED_COLUMNS - set(rows[0].keys()))
    if missing_columns:
        issues.append(Issue("ERROR", str(AUDIT), f"missing columns: {missing_columns}"))
        return issues, stats

    available_cases, case_issues = case_ids()
    issues.extend(case_issues)

    seen_iterations = {row.get("iteration_id", "").strip() for row in rows}
    missing_iterations = sorted(REQUIRED_ITERATIONS - seen_iterations)
    if missing_iterations:
        issues.append(Issue("ERROR", str(AUDIT), f"missing iterations: {missing_iterations}"))

    seen_case_triggers: set[str] = set()
    for i, row in enumerate(rows, start=2):
        iteration_id = row.get("iteration_id", "").strip()
        for field in REQUIRED_COLUMNS:
            if has_placeholder(row.get(field, "")):
                issues.append(Issue("ERROR", str(AUDIT), f"row {i} `{iteration_id}` has placeholder {field}"))

        case_trigger = row.get("case_trigger", "").strip()
        if case_trigger != "validation_set":
            stats["case_triggers_checked"] += 1
            seen_case_triggers.add(case_trigger)
            if case_trigger not in available_cases:
                issues.append(Issue("ERROR", str(AUDIT), f"row {i} unknown case_trigger `{case_trigger}`"))

        if not row.get("failure_mode", "").strip():
            issues.append(Issue("ERROR", str(AUDIT), f"row {i} missing failure_mode"))
        if not row.get("methodology_patch", "").strip():
            issues.append(Issue("ERROR", str(AUDIT), f"row {i} missing methodology_patch"))

        for artifact in split_multi(row.get("patch_artifact", "")):
            stats["patch_artifacts_checked"] += 1
            if not (ROOT / artifact).exists():
                issues.append(Issue("ERROR", str(AUDIT), f"row {i} patch_artifact missing: {artifact}"))

        evidence_artifact = row.get("evidence_artifact", "").strip()
        if evidence_artifact and not (ROOT / evidence_artifact).exists():
            issues.append(Issue("ERROR", str(AUDIT), f"row {i} evidence_artifact missing: {evidence_artifact}"))

        validation_command = row.get("validation_command", "").strip()
        if not validation_command.startswith("python3 scripts/"):
            issues.append(Issue("ERROR", str(AUDIT), f"row {i} validation_command must use repo script"))
        else:
            stats["validation_commands_checked"] += 1

        decision_effect = row.get("decision_effect", "").strip().lower()
        if not any(marker in decision_effect for marker in ("downgraded", "blocked", "keeps", "would_have")):
            issues.append(Issue("ERROR", str(AUDIT), f"row {i} decision_effect must show actionability impact"))

        boundary = row.get("release_boundary", "")
        if "G04" not in boundary and "G06" not in boundary:
            issues.append(Issue("ERROR", str(AUDIT), f"row {i} release_boundary must preserve G04 or G06"))

        stale_after = parse_date(row.get("stale_after", ""))
        if stale_after is None:
            issues.append(Issue("ERROR", str(AUDIT), f"row {i} invalid stale_after"))
        elif stale_after <= as_of:
            issues.append(Issue("ERROR", str(AUDIT), f"row {i} stale_after must be after as_of"))
        elif (stale_after - as_of).days > 45:
            issues.append(Issue("ERROR", str(AUDIT), f"row {i} stale_after is too far away for iteration trace"))

    missing_case_triggers = sorted(REQUIRED_CASE_TRIGGERS - seen_case_triggers)
    if missing_case_triggers:
        issues.append(Issue("ERROR", str(AUDIT), f"missing case-trigger coverage: {missing_case_triggers}"))

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
    print("methodology_iteration_trace_audit_validation:")
    print(f"  iterations: {stats['iterations']}")
    print(f"  case_triggers_checked: {stats['case_triggers_checked']}")
    print(f"  patch_artifacts_checked: {stats['patch_artifacts_checked']}")
    print(f"  validation_commands_checked: {stats['validation_commands_checked']}")
    print(f"  errors: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
