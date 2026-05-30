#!/usr/bin/env python3
"""Validate G06 dispatch readiness controls.

This checks the pre-assignment dispatch checklist and related source files.
It proves the reviewer packet is ready to assign under controlled conditions.
It does not assign a reviewer, validate a reviewer return, or clear G06.
"""

from __future__ import annotations

import csv
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKLIST = Path("cases/long-term-workflow-validation-2026-05-30/g06-dispatch-readiness-checklist.csv")
REQUEST = Path("cases/long-term-workflow-validation-2026-05-30/public-workflow-pack/external-review-request.md")
BLIND_ASSIGNMENT = Path("cases/long-term-workflow-validation-2026-05-30/public-workflow-pack/blind-review-assignment.md")
ASSIGNMENT_TRACKER = Path("cases/long-term-workflow-validation-2026-05-30/g06-reviewer-assignment-tracker.csv")
INDEPENDENCE_SCREEN = Path("cases/long-term-workflow-validation-2026-05-30/g06-reviewer-independence-screen.csv")
CANDIDATE_SCREEN = Path("cases/long-term-workflow-validation-2026-05-30/g06-reviewer-candidate-screen.csv")

REQUIRED_COLUMNS = {
    "check_id",
    "control",
    "pass_condition",
    "status",
    "evidence_path",
    "validator",
    "release_impact",
    "notes",
}

REQUIRED_CHECKS = {
    "dispatch_01",
    "dispatch_02",
    "dispatch_03",
    "dispatch_04",
    "dispatch_05",
    "dispatch_06",
    "dispatch_07",
    "dispatch_08",
    "dispatch_09",
    "dispatch_10",
    "dispatch_11",
}

PRE_ASSIGNMENT_PASS_CHECKS = {
    "dispatch_01",
    "dispatch_02",
    "dispatch_03",
    "dispatch_04",
    "dispatch_05",
    "dispatch_06",
    "dispatch_07",
    "dispatch_08",
    "dispatch_09",
}

PENDING_EXTERNAL_CHECKS = {"dispatch_10", "dispatch_11"}
ALLOWED_STATUSES = {"pass", "accepted", "pending_external"}


@dataclass
class Issue:
    severity: str
    subject: str
    message: str

    def render(self) -> str:
        return f"{self.severity}: {self.subject}: {self.message}"


def read_rows(path: Path) -> tuple[list[dict[str, str]], list[Issue]]:
    try:
        with (ROOT / path).open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    except Exception as exc:
        return [], [Issue("ERROR", str(path), f"could not parse CSV: {exc}")]
    if not rows:
        return [], [Issue("ERROR", str(path), "checklist has no rows")]
    missing = sorted(REQUIRED_COLUMNS - set(rows[0].keys()))
    if missing:
        return rows, [Issue("ERROR", str(path), f"missing columns: {missing}")]
    return rows, []


def read_text(path: Path) -> tuple[str, list[Issue]]:
    try:
        return (ROOT / path).read_text(encoding="utf-8"), []
    except Exception as exc:
        return "", [Issue("ERROR", str(path), f"could not read file: {exc}")]


def validate_assignment_tracker() -> list[Issue]:
    issues: list[Issue] = []
    try:
        with (ROOT / ASSIGNMENT_TRACKER).open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    except Exception as exc:
        return [Issue("ERROR", str(ASSIGNMENT_TRACKER), f"could not parse CSV: {exc}")]
    ready_rows = [
        row
        for row in rows
        if row.get("gate_id", "").strip() == "G06"
        and row.get("current_status", "").strip() == "ready_to_assign_not_completed"
    ]
    if len(ready_rows) != 1:
        issues.append(Issue("ERROR", str(ASSIGNMENT_TRACKER), f"expected 1 ready-to-assign row, got {len(ready_rows)}"))
        return issues
    row = ready_rows[0]
    if row.get("reviewer_status", "").strip() != "not_assigned":
        issues.append(Issue("ERROR", str(ASSIGNMENT_TRACKER), "ready dispatch row must not be assigned"))
    if row.get("assigned_reviewer", "").strip() or row.get("assigned_date", "").strip() or row.get("due_date", "").strip():
        issues.append(Issue("ERROR", str(ASSIGNMENT_TRACKER), "ready dispatch row must not contain reviewer/date/due_date"))
    if row.get("release_impact", "").strip() != "blocks_external_release":
        issues.append(Issue("ERROR", str(ASSIGNMENT_TRACKER), "ready dispatch row must block external release"))
    return issues


def validate_text_controls() -> list[Issue]:
    issues: list[Issue] = []
    request_text, request_issues = read_text(REQUEST)
    issues.extend(request_issues)
    if "requested_return_by: replace" in request_text:
        issues.append(Issue("ERROR", str(REQUEST), "requested_return_by still uses placeholder `replace`"))
    if "requested_return_by: set_on_assignment" not in request_text:
        issues.append(Issue("ERROR", str(REQUEST), "requested_return_by must be set_on_assignment before reviewer assignment"))

    blind_text, blind_issues = read_text(BLIND_ASSIGNMENT)
    issues.extend(blind_issues)
    for marker in (
        "Do not send:",
        "chat transcript",
        "methodology development notes",
        "review-log history",
        "answers from the original analyst",
    ):
        if marker not in blind_text:
            issues.append(Issue("ERROR", str(BLIND_ASSIGNMENT), f"missing independence/internal boundary marker `{marker}`"))
    return issues


def validate_independence_screen() -> list[Issue]:
    issues: list[Issue] = []
    try:
        with (ROOT / INDEPENDENCE_SCREEN).open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    except Exception as exc:
        return [Issue("ERROR", str(INDEPENDENCE_SCREEN), f"could not parse CSV: {exc}")]
    required = {"screen_01", "screen_02", "screen_03", "screen_04", "screen_05", "screen_06"}
    seen = {row.get("check_id", "").strip(): row for row in rows}
    missing = sorted(required - set(seen))
    if missing:
        issues.append(Issue("ERROR", str(INDEPENDENCE_SCREEN), f"missing checks: {missing}"))
    for check_id in ("screen_01", "screen_02", "screen_03", "screen_04"):
        row = seen.get(check_id, {})
        if row.get("status", "").strip() not in {"pass", "accepted"}:
            issues.append(Issue("ERROR", str(INDEPENDENCE_SCREEN), f"{check_id} must pass before dispatch"))
    for check_id in ("screen_05", "screen_06"):
        row = seen.get(check_id, {})
        if row.get("status", "").strip() != "pending_external":
            issues.append(Issue("ERROR", str(INDEPENDENCE_SCREEN), f"{check_id} must stay pending_external"))
        if row.get("release_impact", "").strip() != "blocks_external_release":
            issues.append(Issue("ERROR", str(INDEPENDENCE_SCREEN), f"{check_id} must block external release"))
    return issues


def validate_candidate_screen() -> list[Issue]:
    issues: list[Issue] = []
    try:
        with (ROOT / CANDIDATE_SCREEN).open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    except Exception as exc:
        return [Issue("ERROR", str(CANDIDATE_SCREEN), f"could not parse CSV: {exc}")]
    pending_rows = [
        row
        for row in rows
        if row.get("candidate_status", "").strip() in {"pending_candidate_selection", "eligible_for_assignment"}
    ]
    selected_rows = [
        row
        for row in rows
        if row.get("candidate_status", "").strip() == "selected_assigned"
        or row.get("assigned_in_tracker", "").strip().lower() == "yes"
    ]
    if not pending_rows:
        issues.append(Issue("ERROR", str(CANDIDATE_SCREEN), "dispatch readiness requires a pending or eligible reviewer candidate row"))
    if selected_rows:
        issues.append(Issue("ERROR", str(CANDIDATE_SCREEN), "dispatch readiness cannot have a selected reviewer candidate before assignment"))
    for i, row in enumerate(rows, start=2):
        if row.get("internal_material_access", "").strip().lower() != "no":
            issues.append(Issue("ERROR", str(CANDIDATE_SCREEN), f"row {i} reviewer candidate cannot have internal material access"))
    return issues


def validate_checklist() -> tuple[list[Issue], dict[str, int | bool]]:
    issues: list[Issue] = []
    rows, row_issues = read_rows(CHECKLIST)
    issues.extend(row_issues)
    stats: dict[str, int | bool] = {
        "checks": len(rows),
        "pre_assignment_passed": 0,
        "pending_external": 0,
        "dispatch_ready": False,
    }
    if row_issues:
        return issues, stats

    seen = {row.get("check_id", "").strip(): row for row in rows}
    missing_checks = sorted(REQUIRED_CHECKS - set(seen))
    if missing_checks:
        issues.append(Issue("ERROR", str(CHECKLIST), f"missing checks: {missing_checks}"))

    for check_id, row in seen.items():
        status = row.get("status", "").strip()
        release_impact = row.get("release_impact", "").strip()
        evidence_path = row.get("evidence_path", "").strip()
        validator = row.get("validator", "").strip()
        if status not in ALLOWED_STATUSES:
            issues.append(Issue("ERROR", str(CHECKLIST), f"{check_id} invalid status `{status}`"))
        if evidence_path and not (ROOT / evidence_path).exists():
            issues.append(Issue("ERROR", str(CHECKLIST), f"{check_id} evidence_path missing: {evidence_path}"))
        if validator and not (ROOT / validator).exists():
            issues.append(Issue("ERROR", str(CHECKLIST), f"{check_id} validator missing: {validator}"))
        if check_id in PRE_ASSIGNMENT_PASS_CHECKS:
            if status not in {"pass", "accepted"}:
                issues.append(Issue("ERROR", str(CHECKLIST), f"{check_id} must pass before dispatch readiness"))
            else:
                stats["pre_assignment_passed"] = int(stats["pre_assignment_passed"]) + 1
            if release_impact != "supports_dispatch_ready":
                issues.append(Issue("ERROR", str(CHECKLIST), f"{check_id} must support dispatch readiness"))
        if check_id in PENDING_EXTERNAL_CHECKS:
            if status != "pending_external":
                issues.append(Issue("ERROR", str(CHECKLIST), f"{check_id} must remain pending_external before real reviewer work"))
            else:
                stats["pending_external"] = int(stats["pending_external"]) + 1
            if release_impact != "blocks_external_release":
                issues.append(Issue("ERROR", str(CHECKLIST), f"{check_id} must block external release"))

    stats["dispatch_ready"] = not [issue for issue in issues if issue.severity == "ERROR"]
    return issues, stats


def main() -> int:
    issues, stats = validate_checklist()
    issues.extend(validate_text_controls())
    issues.extend(validate_assignment_tracker())
    issues.extend(validate_independence_screen())
    issues.extend(validate_candidate_screen())
    errors = [issue for issue in issues if issue.severity == "ERROR"]
    for issue in issues:
        print(issue.render())
    print("g06_dispatch_readiness_validation:")
    print(f"  dispatch_ready: {str(not errors).lower()}")
    print(f"  checks: {int(stats['checks'])}")
    print(f"  pre_assignment_passed: {int(stats['pre_assignment_passed'])}")
    print(f"  pending_external: {int(stats['pending_external'])}")
    print("  reviewer_assigned: false")
    print("  clears_g06: false")
    print(f"  errors: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
