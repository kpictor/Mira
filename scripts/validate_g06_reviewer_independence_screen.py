#!/usr/bin/env python3
"""Validate G06 reviewer independence screening controls.

This proves the reviewer-selection standard is explicit before assignment.
It does not name a reviewer, validate a reviewer return, or clear G06.
"""

from __future__ import annotations

import csv
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCREEN = Path("cases/long-term-workflow-validation-2026-05-30/g06-reviewer-independence-screen.csv")
ASSIGNMENT_TRACKER = Path("cases/long-term-workflow-validation-2026-05-30/g06-reviewer-assignment-tracker.csv")
BLIND_ASSIGNMENT = Path("cases/long-term-workflow-validation-2026-05-30/public-workflow-pack/blind-review-assignment.md")
REVIEWER_BRIEF = Path("cases/long-term-workflow-validation-2026-05-30/public-workflow-pack/external-reviewer-brief.md")
G06_HANDOFF = Path("cases/long-term-workflow-validation-2026-05-30/g06-external-review-handoff-2026-05-30.md")

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
    "screen_01",
    "screen_02",
    "screen_03",
    "screen_04",
    "screen_05",
    "screen_06",
}

PRE_ASSIGNMENT_PASS_CHECKS = {
    "screen_01",
    "screen_02",
    "screen_03",
    "screen_04",
}

PENDING_EXTERNAL_CHECKS = {"screen_05", "screen_06"}
ALLOWED_STATUSES = {"pass", "accepted", "pending_external"}


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
    missing = sorted(REQUIRED_COLUMNS - set(rows[0].keys()))
    if missing:
        return rows, [Issue("ERROR", str(path), f"missing columns: {missing}")]
    return rows, []


def read_text(path: Path) -> tuple[str, list[Issue]]:
    try:
        return (ROOT / path).read_text(encoding="utf-8"), []
    except Exception as exc:
        return "", [Issue("ERROR", str(path), f"could not read file: {exc}")]


def validate_screen_rows() -> tuple[list[Issue], dict[str, int | bool]]:
    issues: list[Issue] = []
    rows, row_issues = read_csv(SCREEN)
    issues.extend(row_issues)
    stats: dict[str, int | bool] = {
        "checks": len(rows),
        "pre_assignment_passed": 0,
        "pending_external": 0,
        "screen_ready": False,
    }
    if row_issues:
        return issues, stats

    seen = {row.get("check_id", "").strip(): row for row in rows}
    missing = sorted(REQUIRED_CHECKS - set(seen))
    if missing:
        issues.append(Issue("ERROR", str(SCREEN), f"missing checks: {missing}"))

    for check_id, row in seen.items():
        status = row.get("status", "").strip()
        release_impact = row.get("release_impact", "").strip()
        evidence_path = row.get("evidence_path", "").strip()
        validator = row.get("validator", "").strip()
        pass_condition = row.get("pass_condition", "").strip()

        if status not in ALLOWED_STATUSES:
            issues.append(Issue("ERROR", str(SCREEN), f"{check_id} invalid status `{status}`"))
        if evidence_path and not (ROOT / evidence_path).exists():
            issues.append(Issue("ERROR", str(SCREEN), f"{check_id} evidence_path missing: {evidence_path}"))
        if validator and not (ROOT / validator).exists():
            issues.append(Issue("ERROR", str(SCREEN), f"{check_id} validator missing: {validator}"))
        if check_id in PRE_ASSIGNMENT_PASS_CHECKS:
            if status not in {"pass", "accepted"}:
                issues.append(Issue("ERROR", str(SCREEN), f"{check_id} must pass before reviewer assignment"))
            else:
                stats["pre_assignment_passed"] = int(stats["pre_assignment_passed"]) + 1
            if release_impact != "supports_assignment_ready":
                issues.append(Issue("ERROR", str(SCREEN), f"{check_id} must support assignment readiness"))
        if check_id in PENDING_EXTERNAL_CHECKS:
            if status != "pending_external":
                issues.append(Issue("ERROR", str(SCREEN), f"{check_id} must remain pending_external before real reviewer work"))
            else:
                stats["pending_external"] = int(stats["pending_external"]) + 1
            if release_impact != "blocks_external_release":
                issues.append(Issue("ERROR", str(SCREEN), f"{check_id} must block external release"))

        for marker in ("independent", "Reviewer"):
            if check_id in {"screen_01", "screen_05", "screen_06"} and marker not in pass_condition:
                issues.append(Issue("ERROR", str(SCREEN), f"{check_id} pass_condition missing `{marker}`"))

    stats["screen_ready"] = not [issue for issue in issues if issue.severity == "ERROR"]
    return issues, stats


def validate_text_controls() -> list[Issue]:
    issues: list[Issue] = []
    blind_text, blind_issues = read_text(BLIND_ASSIGNMENT)
    issues.extend(blind_issues)
    for marker in (
        "Do not send:",
        "chat transcript",
        "methodology development notes",
        "review-log history",
        "answers from the original analyst",
        "Reviewer 5: G04 Follow-Through Readiness",
    ):
        if marker not in blind_text:
            issues.append(Issue("ERROR", str(BLIND_ASSIGNMENT), f"missing boundary marker `{marker}`"))

    brief_text, brief_issues = read_text(REVIEWER_BRIEF)
    issues.extend(brief_issues)
    for marker in (
        "Reviewer Independence Rule",
        "internal chat history",
        "unpublished reasoning notes",
        "public sources",
        "assigned case artifacts",
        "G04 Follow-Through Readiness Challenge",
    ):
        if marker not in brief_text:
            issues.append(Issue("ERROR", str(REVIEWER_BRIEF), f"missing reviewer brief marker `{marker}`"))

    handoff_text, handoff_issues = read_text(G06_HANDOFF)
    issues.extend(handoff_issues)
    for marker in ("reviewer independence is confirmed", "G06 Clearing Rule"):
        if marker not in handoff_text:
            issues.append(Issue("ERROR", str(G06_HANDOFF), f"missing handoff marker `{marker}`"))
    return issues


def validate_assignment_tracker_boundary() -> list[Issue]:
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
        issues.append(Issue("ERROR", str(ASSIGNMENT_TRACKER), f"expected 1 ready G06 row, got {len(ready_rows)}"))
        return issues

    row = ready_rows[0]
    if row.get("independence_required", "").strip().lower() != "yes":
        issues.append(Issue("ERROR", str(ASSIGNMENT_TRACKER), "independence_required must be yes"))
    if row.get("assigned_reviewer", "").strip() or row.get("assigned_date", "").strip() or row.get("due_date", "").strip():
        issues.append(Issue("ERROR", str(ASSIGNMENT_TRACKER), "ready screen state cannot contain reviewer/date/due_date"))
    if row.get("release_impact", "").strip() != "blocks_external_release":
        issues.append(Issue("ERROR", str(ASSIGNMENT_TRACKER), "ready state must block external release"))
    return issues


def main() -> int:
    issues, stats = validate_screen_rows()
    issues.extend(validate_text_controls())
    issues.extend(validate_assignment_tracker_boundary())

    errors = [issue for issue in issues if issue.severity == "ERROR"]
    for issue in issues:
        print(issue.render())
    print("g06_reviewer_independence_screen_validation:")
    print(f"  screen_ready: {str(not errors).lower()}")
    print(f"  checks: {int(stats['checks'])}")
    print(f"  pre_assignment_passed: {int(stats['pre_assignment_passed'])}")
    print(f"  pending_external: {int(stats['pending_external'])}")
    print("  reviewer_selected: false")
    print("  clears_g06: false")
    print(f"  errors: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
