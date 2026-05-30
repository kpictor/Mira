#!/usr/bin/env python3
"""Validate the external release action queue.

The queue is an execution control for unresolved external blockers. It should
make G04/G06 next actions concrete without letting internal preparation masquerade
as completed external evidence.
"""

from __future__ import annotations

import csv
import shlex
import subprocess
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUEUE = Path("cases/long-term-workflow-validation-2026-05-30/external-release-action-queue.csv")

REQUIRED_COLUMNS = {
    "action_id",
    "gate_id",
    "blocking_requirement",
    "action_type",
    "current_status",
    "earliest_action_date",
    "owner_role",
    "external_dependency",
    "evidence_path",
    "verification_command",
    "expected_exit_current",
    "completion_validator_command",
    "clearance_condition",
    "internal_completion_allowed",
    "release_impact",
    "next_check_after",
    "notes",
}

REQUIRED_ACTION_IDS = {
    "G04_ETN_MONITOR",
    "G04_VRT_MONITOR",
    "G04_CRM_MONITOR",
    "G04_LLY_SCHEDULED_REFRESH",
    "G06_ASSIGN_REVIEWER",
    "G06_VALIDATE_RETURN",
}

ALLOWED_GATES = {"G04", "G06"}
ALLOWED_ACTION_TYPES = {
    "event_monitor",
    "follow_through_refresh",
    "reviewer_assignment",
    "reviewer_return",
}
ALLOWED_STATUSES = {
    "waiting_for_event",
    "scheduled_future_event",
    "ready_to_assign",
    "waiting_reviewer_return",
    "completed_external",
}
BLOCKING_RELEASE_IMPACT = "blocks_external_release"
RECURSIVE_SCRIPTS = {
    "scripts/run_long_term_release_checks.py",
    "scripts/test_long_term_release_validators.py",
    "scripts/validate_external_release_action_queue.py",
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
        with (ROOT / QUEUE).open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    except Exception as exc:
        return [], [Issue("ERROR", str(QUEUE), f"could not parse CSV: {exc}")]
    if not rows:
        return [], [Issue("ERROR", str(QUEUE), "action queue has no rows")]
    missing = sorted(REQUIRED_COLUMNS - set(rows[0].keys()))
    if missing:
        return rows, [Issue("ERROR", str(QUEUE), f"missing columns: {missing}")]
    return rows, []


def parse_iso_or_assignment(value: str, row_number: int, column: str) -> Issue | None:
    if value == "set_on_assignment":
        return None
    try:
        date.fromisoformat(value)
    except ValueError:
        return Issue("ERROR", str(QUEUE), f"row {row_number} {column} must be ISO date or set_on_assignment")
    return None


def parse_expected_exit(value: str, row_number: int) -> tuple[int | None, Issue | None]:
    try:
        expected = int(value.strip())
    except ValueError:
        return None, Issue("ERROR", str(QUEUE), f"row {row_number} invalid expected_exit_current `{value}`")
    if expected < 0 or expected > 255:
        return None, Issue("ERROR", str(QUEUE), f"row {row_number} expected_exit_current out of range")
    return expected, None


def run_verification(row_number: int, action_id: str, command: str, expected_exit: int) -> tuple[Issue | None, bool]:
    try:
        parts = shlex.split(command)
    except ValueError as exc:
        return Issue("ERROR", str(QUEUE), f"row {row_number} invalid verification_command: {exc}"), False
    if len(parts) < 2 or parts[0] != "python3" or not parts[1].startswith("scripts/"):
        return Issue("ERROR", str(QUEUE), f"row {row_number} command must start with `python3 scripts/...`"), False
    if parts[1] in RECURSIVE_SCRIPTS:
        return Issue("ERROR", str(QUEUE), f"row {row_number} recursive command is not allowed: {parts[1]}"), False
    if not (ROOT / parts[1]).exists():
        return Issue("ERROR", str(QUEUE), f"row {row_number} command script missing: {parts[1]}"), False

    result = subprocess.run([sys.executable, *parts[1:]], cwd=ROOT, text=True, capture_output=True, timeout=180)
    if result.returncode != expected_exit:
        detail = "\n".join(part for part in (result.stdout, result.stderr) if part).strip()
        return (
            Issue(
                "ERROR",
                str(QUEUE),
                f"{action_id} exited {result.returncode}, expected {expected_exit}: {detail}",
            ),
            True,
        )
    return None, True


def parse_completion_command(row_number: int, command: str) -> tuple[list[str], Issue | None]:
    try:
        parts = shlex.split(command)
    except ValueError as exc:
        return [], Issue("ERROR", str(QUEUE), f"row {row_number} invalid completion_validator_command: {exc}")
    if len(parts) < 2 or parts[0] != "python3" or not parts[1].startswith("scripts/"):
        return [], Issue("ERROR", str(QUEUE), f"row {row_number} completion command must start with `python3 scripts/...`")
    if parts[1] in RECURSIVE_SCRIPTS:
        return [], Issue("ERROR", str(QUEUE), f"row {row_number} recursive completion command is not allowed: {parts[1]}")
    if not (ROOT / parts[1]).exists():
        return [], Issue("ERROR", str(QUEUE), f"row {row_number} completion command script missing: {parts[1]}")
    return parts, None


def external_ready() -> bool:
    result = subprocess.run(
        [sys.executable, "scripts/validate_long_term_release.py", "--require-external-ready"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=180,
    )
    return result.returncode == 0


def validate_queue() -> tuple[list[Issue], dict[str, int | bool]]:
    issues: list[Issue] = []
    rows, row_issues = read_rows()
    issues.extend(row_issues)
    stats: dict[str, int | bool] = {
        "actions": len(rows),
        "g04_actions": 0,
        "g06_actions": 0,
        "blocking_actions": 0,
        "external_dependencies": 0,
        "commands_executed": 0,
        "completion_commands_checked": 0,
        "external_ready": external_ready(),
    }
    if row_issues:
        return issues, stats

    seen = {row.get("action_id", "").strip() for row in rows}
    missing_ids = sorted(REQUIRED_ACTION_IDS - seen)
    extra_ids = sorted(seen - REQUIRED_ACTION_IDS)
    if missing_ids:
        issues.append(Issue("ERROR", str(QUEUE), f"missing action ids: {missing_ids}"))
    if extra_ids:
        issues.append(Issue("ERROR", str(QUEUE), f"unexpected action ids: {extra_ids}"))

    for i, row in enumerate(rows, start=2):
        action_id = row.get("action_id", "").strip()
        gate_id = row.get("gate_id", "").strip()
        action_type = row.get("action_type", "").strip()
        status = row.get("current_status", "").strip()
        evidence_path = row.get("evidence_path", "").strip()
        command = row.get("verification_command", "").strip()
        completion_command = row.get("completion_validator_command", "").strip()
        internal_allowed = row.get("internal_completion_allowed", "").strip().lower()
        release_impact = row.get("release_impact", "").strip()
        external_dependency = row.get("external_dependency", "").strip()

        for field in REQUIRED_COLUMNS:
            if not row.get(field, "").strip():
                issues.append(Issue("ERROR", str(QUEUE), f"row {i} missing {field}"))
        if gate_id not in ALLOWED_GATES:
            issues.append(Issue("ERROR", str(QUEUE), f"row {i} invalid gate_id `{gate_id}`"))
        if action_type not in ALLOWED_ACTION_TYPES:
            issues.append(Issue("ERROR", str(QUEUE), f"row {i} invalid action_type `{action_type}`"))
        if status not in ALLOWED_STATUSES:
            issues.append(Issue("ERROR", str(QUEUE), f"row {i} invalid current_status `{status}`"))
        if internal_allowed not in {"yes", "no"}:
            issues.append(Issue("ERROR", str(QUEUE), f"row {i} internal_completion_allowed must be yes or no"))
        if internal_allowed != "no":
            issues.append(Issue("ERROR", str(QUEUE), f"row {i} external blocker cannot be internally completed"))
        if release_impact != BLOCKING_RELEASE_IMPACT and not bool(stats["external_ready"]):
            issues.append(Issue("ERROR", str(QUEUE), f"row {i} must block external release while external_ready is false"))
        if evidence_path and not (ROOT / evidence_path).exists():
            issues.append(Issue("ERROR", str(QUEUE), f"row {i} evidence_path missing: {evidence_path}"))
        for column in ("earliest_action_date", "next_check_after"):
            date_issue = parse_iso_or_assignment(row.get(column, "").strip(), i, column)
            if date_issue:
                issues.append(date_issue)
        expected_exit, exit_issue = parse_expected_exit(row.get("expected_exit_current", ""), i)
        if exit_issue:
            issues.append(exit_issue)
            continue
        assert expected_exit is not None

        if gate_id == "G04":
            stats["g04_actions"] = int(stats["g04_actions"]) + 1
            if action_type not in {"event_monitor", "follow_through_refresh"}:
                issues.append(Issue("ERROR", str(QUEUE), f"row {i} G04 action must be event_monitor or follow_through_refresh"))
            completion_parts, completion_issue = parse_completion_command(i, completion_command)
            if completion_issue:
                issues.append(completion_issue)
            else:
                stats["completion_commands_checked"] = int(stats["completion_commands_checked"]) + 1
                if completion_parts[1] != "scripts/validate_follow_through_refresh.py":
                    issues.append(Issue("ERROR", str(QUEUE), f"row {i} G04 completion must use validate_follow_through_refresh.py"))
                for marker in (
                    "--refresh",
                    "--original-cutoff",
                    "--evidence-log",
                    "--intake",
                    "--gate-tracker",
                    "--public-readiness-audit",
                    "--review-log",
                ):
                    if marker not in completion_parts:
                        issues.append(Issue("ERROR", str(QUEUE), f"row {i} G04 completion command missing `{marker}`"))
            for marker in ("post-2026-05-30", "refresh"):
                if marker not in row.get("clearance_condition", ""):
                    issues.append(Issue("ERROR", str(QUEUE), f"row {i} G04 clearance_condition missing `{marker}`"))
        if gate_id == "G06":
            stats["g06_actions"] = int(stats["g06_actions"]) + 1
            if action_type not in {"reviewer_assignment", "reviewer_return"}:
                issues.append(Issue("ERROR", str(QUEUE), f"row {i} G06 action must be reviewer_assignment or reviewer_return"))
            completion_parts, completion_issue = parse_completion_command(i, completion_command)
            if completion_issue:
                issues.append(completion_issue)
            else:
                stats["completion_commands_checked"] = int(stats["completion_commands_checked"]) + 1
                if action_type == "reviewer_assignment" and completion_parts[1] != "scripts/validate_external_review_assignment_tracker.py":
                    issues.append(
                        Issue("ERROR", str(QUEUE), f"row {i} reviewer assignment must use validate_external_review_assignment_tracker.py")
                    )
                if action_type == "reviewer_return":
                    if completion_parts[1] != "scripts/validate_external_review_return.py":
                        issues.append(Issue("ERROR", str(QUEUE), f"row {i} reviewer return must use validate_external_review_return.py"))
                    for marker in ("--scorecard", "--results", "--intake", "--assignment-tracker", "--independence-screen"):
                        if marker not in completion_parts:
                            issues.append(Issue("ERROR", str(QUEUE), f"row {i} reviewer return command missing `{marker}`"))
            for marker in ("independent", "reviewer"):
                if marker not in row.get("clearance_condition", "").lower():
                    issues.append(Issue("ERROR", str(QUEUE), f"row {i} G06 clearance_condition missing `{marker}`"))
        if release_impact == BLOCKING_RELEASE_IMPACT:
            stats["blocking_actions"] = int(stats["blocking_actions"]) + 1
        if external_dependency:
            stats["external_dependencies"] = int(stats["external_dependencies"]) + 1

        command_issue, executed = run_verification(i, action_id, command, expected_exit)
        if executed:
            stats["commands_executed"] = int(stats["commands_executed"]) + 1
        if command_issue:
            issues.append(command_issue)

    if int(stats["g04_actions"]) < 4:
        issues.append(Issue("ERROR", str(QUEUE), "action queue must include all four G04 monitored live cases"))
    if int(stats["g06_actions"]) < 2:
        issues.append(Issue("ERROR", str(QUEUE), "action queue must include G06 assignment and return actions"))
    if not bool(stats["external_ready"]) and int(stats["blocking_actions"]) != len(rows):
        issues.append(Issue("ERROR", str(QUEUE), "all current action rows must block external release while external_ready is false"))
    if not bool(stats["external_ready"]) and int(stats["external_dependencies"]) != len(rows):
        issues.append(Issue("ERROR", str(QUEUE), "all current action rows must identify external dependency"))
    if int(stats["completion_commands_checked"]) != len(rows):
        issues.append(Issue("ERROR", str(QUEUE), "all action rows must have checked completion validator commands"))
    return issues, stats


def main() -> int:
    issues, stats = validate_queue()
    errors = [issue for issue in issues if issue.severity == "ERROR"]
    for issue in issues:
        print(issue.render())
    print("external_release_action_queue_validation:")
    print(f"  external_ready: {str(bool(stats['external_ready'])).lower()}")
    print(f"  actions: {int(stats['actions'])}")
    print(f"  g04_actions: {int(stats['g04_actions'])}")
    print(f"  g06_actions: {int(stats['g06_actions'])}")
    print(f"  blocking_actions: {int(stats['blocking_actions'])}")
    print(f"  external_dependencies: {int(stats['external_dependencies'])}")
    print(f"  commands_executed: {int(stats['commands_executed'])}")
    print(f"  completion_commands_checked: {int(stats['completion_commands_checked'])}")
    print(f"  errors: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
