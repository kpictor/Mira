#!/usr/bin/env python3
"""Validate a completed institutional colleague acceptance return.

This validates the future colleague pilot memo and completed checklist. It is
not a substitute for validate_long_term_release.py --require-external-ready.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path


REQUIRED_CHECKS = {f"acceptance_{i:02d}" for i in range(1, 10)}
REQUIRED_COLUMNS = {"check_id", "requirement", "pass_condition", "status", "evidence_path", "notes"}
PASSING_STATUSES = {"pass", "accepted"}
PLACEHOLDERS = {"", "replace", "tbd", "todo", "n/a", "YYYY-MM-DD"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

CLEAR_RESULTS = {"pass", "accepted_with_caveats"}
CLEAR_RECOMMENDATIONS = {"release_to_institutional_colleagues", "release_with_caveats"}

REQUIRED_MEMO_FIELDS = {
    "acceptance_date",
    "colleague_id",
    "colleague_role",
    "used_live_author_context",
    "packet_version_date",
    "reproduced_case_id",
    "reproduced_action_label",
    "new_or_refresh_case_id",
    "source_gap_visibility",
    "action_label_stop_rule_understood",
    "practice_falsification_understood",
    "methodology_iteration_traceability",
    "release_recommendation",
    "stale_after",
    "must_refresh_if",
}


@dataclass
class Issue:
    severity: str
    subject: str
    message: str

    def render(self) -> str:
        return f"{self.severity}: {self.subject}: {self.message}"


def read_csv(path: Path) -> tuple[list[dict[str, str]], list[Issue]]:
    try:
        with path.open(newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f)), []
    except Exception as exc:
        return [], [Issue("ERROR", str(path), f"could not parse CSV: {exc}")]


def scalar_from_memo(text: str, key: str) -> str:
    pattern = re.compile(rf"^[ \t]*-[ \t]*{re.escape(key)}:[ \t]*(.*)[ \t]*$", re.MULTILINE)
    match = pattern.search(text)
    if not match:
        return ""
    return match.group(1).strip().strip("`")


def parse_date(value: str) -> date | None:
    if not DATE_RE.match(value):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def is_placeholder(value: str) -> bool:
    return value.strip().lower() in PLACEHOLDERS


def validate_checklist(path: Path) -> tuple[list[Issue], int, int]:
    issues: list[Issue] = []
    rows, row_issues = read_csv(path)
    issues.extend(row_issues)
    if row_issues:
        return issues, 0, 0
    if not rows:
        return [Issue("ERROR", str(path), "checklist has no rows")], 0, 0

    missing_columns = sorted(REQUIRED_COLUMNS - set(rows[0].keys()))
    if missing_columns:
        issues.append(Issue("ERROR", str(path), f"missing columns: {missing_columns}"))
        return issues, len(rows), 0

    seen = {row.get("check_id", "").strip() for row in rows}
    missing_checks = sorted(REQUIRED_CHECKS - seen)
    if missing_checks:
        issues.append(Issue("ERROR", str(path), f"missing checks: {missing_checks}"))

    passed = 0
    for i, row in enumerate(rows, start=2):
        check_id = row.get("check_id", "").strip()
        status = row.get("status", "").strip()
        if status not in PASSING_STATUSES:
            issues.append(Issue("ERROR", str(path), f"row {i} `{check_id}` not pass/accepted: {status}"))
        else:
            passed += 1
        for field in ("requirement", "pass_condition", "notes"):
            if is_placeholder(row.get(field, "")):
                issues.append(Issue("ERROR", str(path), f"row {i} `{check_id}` has placeholder {field}"))
    return issues, len(rows), passed


def validate_memo(path: Path) -> tuple[list[Issue], dict[str, str]]:
    issues: list[Issue] = []
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as exc:
        return [Issue("ERROR", str(path), f"could not read memo: {exc}")], {}

    values = {field: scalar_from_memo(text, field) for field in REQUIRED_MEMO_FIELDS}
    for field, value in values.items():
        if is_placeholder(value):
            issues.append(Issue("ERROR", str(path), f"{field} is placeholder or missing"))

    acceptance_date = parse_date(values.get("acceptance_date", ""))
    if acceptance_date is None:
        issues.append(Issue("ERROR", str(path), "acceptance_date must be YYYY-MM-DD"))

    stale_after = parse_date(values.get("stale_after", ""))
    if stale_after is None:
        issues.append(Issue("ERROR", str(path), "stale_after must be YYYY-MM-DD"))
    elif acceptance_date is not None and stale_after <= acceptance_date:
        issues.append(Issue("ERROR", str(path), "stale_after must be after acceptance_date"))

    if values.get("used_live_author_context", "").lower() != "false":
        issues.append(Issue("ERROR", str(path), "used_live_author_context must be false"))

    if values.get("source_gap_visibility") not in CLEAR_RESULTS:
        issues.append(Issue("ERROR", str(path), "source_gap_visibility does not clear acceptance"))
    if values.get("action_label_stop_rule_understood") not in CLEAR_RESULTS:
        issues.append(Issue("ERROR", str(path), "action_label_stop_rule_understood does not clear acceptance"))
    if values.get("practice_falsification_understood") not in CLEAR_RESULTS:
        issues.append(Issue("ERROR", str(path), "practice_falsification_understood does not clear acceptance"))
    if values.get("methodology_iteration_traceability") not in CLEAR_RESULTS:
        issues.append(Issue("ERROR", str(path), "methodology_iteration_traceability does not clear acceptance"))
    if values.get("release_recommendation") not in CLEAR_RECOMMENDATIONS:
        issues.append(Issue("ERROR", str(path), "release_recommendation does not clear acceptance"))

    for marker in ("Residual Caveats", "Required Fixes", "Refresh Conditions", "owner:", "fix:"):
        if marker not in text:
            issues.append(Issue("ERROR", str(path), f"missing marker `{marker}`"))
    return issues, values


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checklist", required=True, help="completed institutional-colleague-acceptance-checklist.csv")
    parser.add_argument("--memo", required=True, help="completed institutional-colleague-acceptance-YYYY-MM-DD.md")
    args = parser.parse_args()

    issues: list[Issue] = []
    checklist_issues, checks, passed = validate_checklist(Path(args.checklist))
    memo_issues, memo_values = validate_memo(Path(args.memo))
    issues.extend(checklist_issues)
    issues.extend(memo_issues)

    errors = [issue for issue in issues if issue.severity == "ERROR"]
    for issue in issues:
        print(issue.render())
    print("institutional_colleague_acceptance_return_validation:")
    print(f"  acceptance_return_clearable: {str(not errors).lower()}")
    print(f"  checks: {checks}")
    print(f"  passed_or_accepted: {passed}")
    print(f"  colleague_id: {memo_values.get('colleague_id') or 'missing'}")
    print(f"  release_recommendation: {memo_values.get('release_recommendation') or 'missing'}")
    print(f"  methodology_iteration_traceability: {memo_values.get('methodology_iteration_traceability') or 'missing'}")
    print(f"  errors: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
