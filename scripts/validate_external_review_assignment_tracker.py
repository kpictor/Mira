#!/usr/bin/env python3
"""Validate the G06 external reviewer assignment tracker.

This validates assignment logistics and release-state honesty. It does not
validate a completed reviewer return and does not clear G06.
"""

from __future__ import annotations

import csv
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRACKER = Path("cases/long-term-workflow-validation-2026-05-30/g06-reviewer-assignment-tracker.csv")
INDEPENDENCE_SCREEN = Path("cases/long-term-workflow-validation-2026-05-30/g06-reviewer-independence-screen.csv")
CANDIDATE_SCREEN = Path("cases/long-term-workflow-validation-2026-05-30/g06-reviewer-candidate-screen.csv")

REQUIRED_COLUMNS = {
    "assignment_id",
    "gate_id",
    "packet_status",
    "reviewer_status",
    "independence_required",
    "assigned_reviewer",
    "assigned_date",
    "due_date",
    "packet_command",
    "return_validator_command",
    "current_status",
    "release_impact",
    "evidence_path",
    "next_action",
}

PACKET_STATUSES = {"packet_export_ready", "packet_sent", "packet_needs_update"}
REVIEWER_STATUSES = {"not_assigned", "assigned", "returned", "validated", "rejected"}
CURRENT_STATUSES = {
    "ready_to_assign_not_completed",
    "assigned_not_returned",
    "returned_not_validated",
    "validated_completed",
    "rejected_or_needs_revision",
}
REQUIRED_SCREEN_ROWS = {"screen_05", "screen_06"}
REQUIRED_CANDIDATE_COLUMNS = {
    "candidate_id",
    "candidate_status",
    "reviewer_name",
    "assigned_in_tracker",
    "release_impact",
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
        with (ROOT / TRACKER).open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    except Exception as exc:
        return [], [Issue("ERROR", str(TRACKER), f"could not parse CSV: {exc}")]
    if not rows:
        return [], [Issue("ERROR", str(TRACKER), "assignment tracker has no rows")]
    missing = sorted(REQUIRED_COLUMNS - set(rows[0].keys()))
    if missing:
        return rows, [Issue("ERROR", str(TRACKER), f"missing columns: {missing}")]
    return rows, []


def read_screen_rows() -> tuple[dict[str, dict[str, str]], list[Issue]]:
    try:
        with (ROOT / INDEPENDENCE_SCREEN).open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    except Exception as exc:
        return {}, [Issue("ERROR", str(INDEPENDENCE_SCREEN), f"could not parse CSV: {exc}")]
    if not rows:
        return {}, [Issue("ERROR", str(INDEPENDENCE_SCREEN), "independence screen has no rows")]
    required_columns = {"check_id", "status", "release_impact", "validator"}
    missing = sorted(required_columns - set(rows[0].keys()))
    if missing:
        return {}, [Issue("ERROR", str(INDEPENDENCE_SCREEN), f"missing columns: {missing}")]
    return {row.get("check_id", "").strip(): row for row in rows if row.get("check_id", "").strip()}, []


def read_candidate_rows() -> tuple[list[dict[str, str]], list[Issue]]:
    try:
        with (ROOT / CANDIDATE_SCREEN).open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    except Exception as exc:
        return [], [Issue("ERROR", str(CANDIDATE_SCREEN), f"could not parse CSV: {exc}")]
    if not rows:
        return [], [Issue("ERROR", str(CANDIDATE_SCREEN), "candidate screen has no rows")]
    missing = sorted(REQUIRED_CANDIDATE_COLUMNS - set(rows[0].keys()))
    if missing:
        return rows, [Issue("ERROR", str(CANDIDATE_SCREEN), f"missing columns: {missing}")]
    return rows, []


def validate_tracker() -> tuple[list[Issue], dict[str, int | bool]]:
    issues: list[Issue] = []
    rows, read_issues = read_rows()
    issues.extend(read_issues)
    screen_rows, screen_issues = read_screen_rows()
    issues.extend(screen_issues)
    candidate_rows, candidate_issues = read_candidate_rows()
    issues.extend(candidate_issues)
    stats: dict[str, int | bool] = {
        "assignments": len(rows),
        "ready_to_assign": 0,
        "assigned": 0,
        "validated_completed": 0,
        "screen_rows_checked": 0,
        "candidate_rows_checked": 0,
        "tracker_ready": False,
    }
    if read_issues or screen_issues or candidate_issues:
        return issues, stats

    missing_screen_rows = sorted(REQUIRED_SCREEN_ROWS - set(screen_rows))
    if missing_screen_rows:
        issues.append(Issue("ERROR", str(INDEPENDENCE_SCREEN), f"missing required screen rows: {missing_screen_rows}"))

    selected_candidates = [
        row
        for row in candidate_rows
        if row.get("candidate_status", "").strip() == "selected_assigned"
        or row.get("assigned_in_tracker", "").strip().lower() == "yes"
    ]
    pending_or_eligible_candidates = [
        row
        for row in candidate_rows
        if row.get("candidate_status", "").strip() in {"pending_candidate_selection", "eligible_for_assignment"}
    ]
    for i, candidate in enumerate(candidate_rows, start=2):
        stats["candidate_rows_checked"] = int(stats["candidate_rows_checked"]) + 1
        if candidate.get("release_impact", "").strip() != "blocks_external_release":
            issues.append(Issue("ERROR", str(CANDIDATE_SCREEN), f"row {i} must block external release"))

    for i, row in enumerate(rows, start=2):
        assignment_id = row.get("assignment_id", "").strip()
        gate_id = row.get("gate_id", "").strip()
        packet_status = row.get("packet_status", "").strip()
        reviewer_status = row.get("reviewer_status", "").strip()
        independence_required = row.get("independence_required", "").strip().lower()
        current_status = row.get("current_status", "").strip()
        release_impact = row.get("release_impact", "").strip()
        evidence_path = row.get("evidence_path", "").strip()
        packet_command = row.get("packet_command", "").strip()
        return_command = row.get("return_validator_command", "").strip()
        next_action = row.get("next_action", "").strip()

        if not assignment_id:
            issues.append(Issue("ERROR", str(TRACKER), f"row {i} missing assignment_id"))
        if gate_id != "G06":
            issues.append(Issue("ERROR", str(TRACKER), f"row {i} gate_id must be G06"))
        if packet_status not in PACKET_STATUSES:
            issues.append(Issue("ERROR", str(TRACKER), f"row {i} invalid packet_status `{packet_status}`"))
        if reviewer_status not in REVIEWER_STATUSES:
            issues.append(Issue("ERROR", str(TRACKER), f"row {i} invalid reviewer_status `{reviewer_status}`"))
        if independence_required != "yes":
            issues.append(Issue("ERROR", str(TRACKER), f"row {i} independence_required must be yes"))
        if current_status not in CURRENT_STATUSES:
            issues.append(Issue("ERROR", str(TRACKER), f"row {i} invalid current_status `{current_status}`"))
        if "build_external_review_packet.py --output" not in packet_command:
            issues.append(Issue("ERROR", str(TRACKER), f"row {i} missing packet builder command"))
        if "validate_external_review_return.py" not in return_command:
            issues.append(Issue("ERROR", str(TRACKER), f"row {i} missing return validator command"))
        for marker in ("--scorecard", "--results", "--intake", "--assignment-tracker", "--independence-screen"):
            if marker not in return_command:
                issues.append(Issue("ERROR", str(TRACKER), f"row {i} return validator command missing `{marker}`"))
        for marker in (
            "G01 method-source decision",
            "G04 readiness/false-completion results",
            "G05 source decision",
            "historical consensus exception decision",
        ):
            if marker not in next_action:
                issues.append(Issue("ERROR", str(TRACKER), f"row {i} next_action missing `{marker}`"))
        if evidence_path and not (ROOT / evidence_path).exists():
            issues.append(Issue("ERROR", str(TRACKER), f"row {i} evidence_path missing: {evidence_path}"))

        if REQUIRED_SCREEN_ROWS <= set(screen_rows):
            stats["screen_rows_checked"] = int(stats["screen_rows_checked"]) + len(REQUIRED_SCREEN_ROWS)
            for check_id in REQUIRED_SCREEN_ROWS:
                screen = screen_rows[check_id]
                if screen.get("release_impact", "").strip() != "blocks_external_release":
                    issues.append(Issue("ERROR", str(TRACKER), f"{check_id} must block external release"))

        if current_status == "ready_to_assign_not_completed":
            stats["ready_to_assign"] = int(stats["ready_to_assign"]) + 1
            if release_impact != "blocks_external_release":
                issues.append(Issue("ERROR", str(TRACKER), f"row {i} ready state must block external release"))
            if row.get("assigned_reviewer", "").strip() or row.get("assigned_date", "").strip() or row.get("due_date", "").strip():
                issues.append(Issue("ERROR", str(TRACKER), f"row {i} ready state cannot have reviewer/date/due_date"))
            if selected_candidates:
                issues.append(Issue("ERROR", str(TRACKER), f"row {i} ready state cannot have selected reviewer candidate"))
            if not pending_or_eligible_candidates:
                issues.append(Issue("ERROR", str(TRACKER), f"row {i} ready state requires pending or eligible reviewer candidate screen row"))
            for check_id in REQUIRED_SCREEN_ROWS:
                screen = screen_rows.get(check_id)
                if screen and screen.get("status", "").strip() != "pending_external":
                    issues.append(
                        Issue(
                            "ERROR",
                            str(TRACKER),
                            f"row {i} ready assignment requires {check_id} pending_external, got {screen.get('status', '').strip()}",
                        )
                    )
        if current_status in {"assigned_not_returned", "returned_not_validated"}:
            stats["assigned"] = int(stats["assigned"]) + 1
            if not row.get("assigned_reviewer", "").strip() or not row.get("assigned_date", "").strip() or not row.get("due_date", "").strip():
                issues.append(Issue("ERROR", str(TRACKER), f"row {i} assigned state requires reviewer, assigned_date and due_date"))
            if release_impact != "blocks_external_release":
                issues.append(Issue("ERROR", str(TRACKER), f"row {i} incomplete assigned state must block external release"))
            screen_05 = screen_rows.get("screen_05")
            if screen_05 and screen_05.get("status", "").strip() not in {"pass", "accepted"}:
                issues.append(Issue("ERROR", str(TRACKER), f"row {i} assigned state requires screen_05 pass/accepted"))
            screen_06 = screen_rows.get("screen_06")
            if current_status == "assigned_not_returned" and screen_06 and screen_06.get("status", "").strip() != "pending_external":
                issues.append(Issue("ERROR", str(TRACKER), f"row {i} assigned_not_returned requires screen_06 pending_external"))
            if len(selected_candidates) != 1:
                issues.append(Issue("ERROR", str(TRACKER), f"row {i} assigned state requires exactly one selected reviewer candidate"))
            elif selected_candidates[0].get("reviewer_name", "").strip() != row.get("assigned_reviewer", "").strip():
                issues.append(Issue("ERROR", str(TRACKER), f"row {i} assigned reviewer must match selected reviewer candidate"))
        if current_status == "validated_completed":
            stats["validated_completed"] = int(stats["validated_completed"]) + 1
            if packet_status != "packet_sent":
                issues.append(Issue("ERROR", str(TRACKER), f"row {i} completed state requires packet_status packet_sent"))
            if reviewer_status != "validated":
                issues.append(Issue("ERROR", str(TRACKER), f"row {i} completed state requires reviewer_status validated"))
            if not row.get("assigned_reviewer", "").strip() or not row.get("assigned_date", "").strip() or not row.get("due_date", "").strip():
                issues.append(Issue("ERROR", str(TRACKER), f"row {i} completed state requires reviewer, assigned_date and due_date"))
            if release_impact not in {"can_clear_g06_if_return_validator_passed", "supports_external_release"}:
                issues.append(Issue("ERROR", str(TRACKER), f"row {i} completed state has invalid release_impact"))
            if "external-review-results" not in evidence_path or not evidence_path.endswith(".md"):
                issues.append(Issue("ERROR", str(TRACKER), f"row {i} completed state must point to external review results memo"))
            for check_id in REQUIRED_SCREEN_ROWS:
                screen = screen_rows.get(check_id)
                if screen and screen.get("status", "").strip() not in {"pass", "accepted"}:
                    issues.append(Issue("ERROR", str(TRACKER), f"row {i} completed state requires {check_id} pass/accepted"))
            if len(selected_candidates) != 1:
                issues.append(Issue("ERROR", str(TRACKER), f"row {i} completed state requires exactly one selected reviewer candidate"))
            elif selected_candidates[0].get("reviewer_name", "").strip() != row.get("assigned_reviewer", "").strip():
                issues.append(Issue("ERROR", str(TRACKER), f"row {i} completed reviewer must match selected reviewer candidate"))

    stats["tracker_ready"] = not [issue for issue in issues if issue.severity == "ERROR"]
    return issues, stats


def main() -> int:
    issues, stats = validate_tracker()
    errors = [issue for issue in issues if issue.severity == "ERROR"]
    for issue in issues:
        print(issue.render())
    print("external_review_assignment_tracker_validation:")
    print(f"  tracker_ready: {str(bool(stats['tracker_ready'])).lower()}")
    print(f"  assignments: {int(stats['assignments'])}")
    print(f"  ready_to_assign: {int(stats['ready_to_assign'])}")
    print(f"  assigned: {int(stats['assigned'])}")
    print(f"  validated_completed: {int(stats['validated_completed'])}")
    print(f"  screen_rows_checked: {int(stats['screen_rows_checked'])}")
    print(f"  candidate_rows_checked: {int(stats['candidate_rows_checked'])}")
    print(f"  errors: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
