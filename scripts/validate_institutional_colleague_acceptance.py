#!/usr/bin/env python3
"""Validate institutional colleague acceptance controls.

This validator keeps the current internal-candidate state honest: the
acceptance checklist may be prepared, but it must not be marked complete before
external-ready gates clear and a real colleague acceptance memo exists.
"""

from __future__ import annotations

import csv
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATION_DIR = Path("cases/long-term-workflow-validation-2026-05-30")
PUBLIC_PACK = VALIDATION_DIR / "public-workflow-pack"
CHECKLIST = VALIDATION_DIR / "institutional-colleague-acceptance-checklist.csv"
MEMO_TEMPLATE = PUBLIC_PACK / "institutional-colleague-acceptance-memo-template.md"
MEMO_RE = re.compile(r"^institutional-colleague-acceptance-\d{4}-\d{2}-\d{2}\.md$")

REQUIRED_CHECKS = {f"acceptance_{i:02d}" for i in range(1, 10)}
ALLOWED_STATUSES = {"pending", "pass", "accepted"}
PLACEHOLDERS = {"", "tbd", "todo", "replace", "n/a"}
REQUIRED_TEMPLATE_MARKERS = {
    "acceptance_date:",
    "colleague_id:",
    "used_live_author_context: false",
    "reproduced_case_id:",
    "new_or_refresh_case_id:",
    "practice_falsification_understood:",
    "methodology_iteration_traceability:",
    "release_recommendation:",
    "stale_after:",
    "must_refresh_if:",
    "owner:",
    "fix:",
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
        with (ROOT / path).open(newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f)), []
    except Exception as exc:
        return [], [Issue("ERROR", str(path), f"could not parse CSV: {exc}")]


def external_ready() -> bool:
    result = subprocess.run(
        [sys.executable, "scripts/validate_long_term_release.py", "--require-external-ready"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    return result.returncode == 0


def validate_return_memo(memo: Path) -> list[Issue]:
    result = subprocess.run(
        [
            sys.executable,
            "scripts/validate_institutional_colleague_acceptance_return.py",
            "--checklist",
            str(ROOT / CHECKLIST),
            "--memo",
            str(memo),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if result.returncode == 0:
        return []

    detail_lines = [
        line.strip()
        for line in (result.stdout + "\n" + result.stderr).splitlines()
        if line.strip() and (line.startswith("ERROR:") or line.startswith("Traceback"))
    ]
    memo_lines = [line for line in detail_lines if str(memo) in line]
    if memo_lines:
        detail_lines = memo_lines + [line for line in detail_lines if line not in memo_lines]
    detail = "; ".join(detail_lines[:6]) if detail_lines else "see return validator output"
    return [Issue("ERROR", str(memo.relative_to(ROOT)), f"acceptance return validator failed: {detail}")]


def has_placeholder(value: str) -> bool:
    return value.strip().lower() in PLACEHOLDERS


def validate_acceptance() -> tuple[list[Issue], dict[str, int | bool]]:
    issues: list[Issue] = []
    rows, row_issues = read_csv(CHECKLIST)
    issues.extend(row_issues)
    stats: dict[str, int | bool] = {
        "checks": len(rows),
        "passed_or_accepted": 0,
        "pending": 0,
        "memo_present": False,
        "return_memos_checked": 0,
        "external_ready": False,
        "acceptance_ready": False,
    }
    if row_issues:
        return issues, stats
    if not rows:
        return [Issue("ERROR", str(CHECKLIST), "checklist has no rows")], stats

    required_columns = {"check_id", "requirement", "pass_condition", "status", "evidence_path", "notes"}
    missing_columns = sorted(required_columns - set(rows[0].keys()))
    if missing_columns:
        issues.append(Issue("ERROR", str(CHECKLIST), f"missing columns: {missing_columns}"))
        return issues, stats

    seen = {row.get("check_id", "").strip() for row in rows}
    missing_checks = sorted(REQUIRED_CHECKS - seen)
    if missing_checks:
        issues.append(Issue("ERROR", str(CHECKLIST), f"missing checks: {missing_checks}"))

    for i, row in enumerate(rows, start=2):
        check_id = row.get("check_id", "").strip()
        status = row.get("status", "").strip()
        if status not in ALLOWED_STATUSES:
            issues.append(Issue("ERROR", str(CHECKLIST), f"row {i} invalid status `{status}`"))
        if status in {"pass", "accepted"}:
            stats["passed_or_accepted"] = int(stats["passed_or_accepted"]) + 1
        if status == "pending":
            stats["pending"] = int(stats["pending"]) + 1
        for field in ("requirement", "pass_condition", "notes"):
            if has_placeholder(row.get(field, "")):
                issues.append(Issue("ERROR", str(CHECKLIST), f"row {i} `{check_id}` has placeholder {field}"))
        evidence_path = row.get("evidence_path", "").strip()
        if evidence_path and not (ROOT / VALIDATION_DIR / evidence_path).exists() and not (ROOT / evidence_path).exists():
            issues.append(Issue("ERROR", str(CHECKLIST), f"row {i} evidence_path missing: {evidence_path}"))
        if status in {"pass", "accepted"} and check_id in {"acceptance_01", "acceptance_09"} and not evidence_path:
            issues.append(Issue("ERROR", str(CHECKLIST), f"row {i} `{check_id}` requires dated acceptance evidence"))

    try:
        template_text = (ROOT / MEMO_TEMPLATE).read_text(encoding="utf-8")
    except Exception as exc:
        issues.append(Issue("ERROR", str(MEMO_TEMPLATE), f"could not read acceptance memo template: {exc}"))
        template_text = ""
    for marker in REQUIRED_TEMPLATE_MARKERS:
        if marker not in template_text:
            issues.append(Issue("ERROR", str(MEMO_TEMPLATE), f"missing marker `{marker}`"))

    memos = sorted(
        path
        for path in (ROOT / VALIDATION_DIR).glob("institutional-colleague-acceptance-*.md")
        if MEMO_RE.match(path.name)
    )
    stats["memo_present"] = bool(memos)
    stats["return_memos_checked"] = len(memos)
    for memo in memos:
        issues.extend(validate_return_memo(memo))
    stats["external_ready"] = external_ready()

    all_checks_passed = int(stats["passed_or_accepted"]) == len(REQUIRED_CHECKS)
    stats["acceptance_ready"] = bool(stats["external_ready"]) and all_checks_passed and bool(memos)

    if not bool(stats["external_ready"]) and all_checks_passed:
        issues.append(Issue("ERROR", str(CHECKLIST), "all acceptance checks pass while external-ready validator fails"))
    if not bool(stats["external_ready"]) and bool(memos):
        issues.append(Issue("ERROR", str(CHECKLIST), "acceptance memo exists before external-ready gates clear"))
    if bool(stats["acceptance_ready"]) and int(stats["pending"]) > 0:
        issues.append(Issue("ERROR", str(CHECKLIST), "acceptance_ready true while pending rows remain"))

    return issues, stats


def main() -> int:
    issues, stats = validate_acceptance()
    errors = [issue for issue in issues if issue.severity == "ERROR"]
    for issue in issues:
        print(issue.render())
    print("institutional_colleague_acceptance_validation:")
    print(f"  acceptance_ready: {str(bool(stats['acceptance_ready'])).lower()}")
    print(f"  external_ready: {str(bool(stats['external_ready'])).lower()}")
    print(f"  checks: {int(stats['checks'])}")
    print(f"  passed_or_accepted: {int(stats['passed_or_accepted'])}")
    print(f"  pending: {int(stats['pending'])}")
    print(f"  memo_present: {str(bool(stats['memo_present'])).lower()}")
    print(f"  return_memos_checked: {int(stats['return_memos_checked'])}")
    print(f"  errors: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
