#!/usr/bin/env python3
"""Validate the G04 follow-through execution tracker.

This checks readiness and release-state honesty for future follow-through
execution. It does not validate a completed refresh and does not clear G04.
"""

from __future__ import annotations

import csv
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRACKER = Path("cases/long-term-workflow-validation-2026-05-30/g04-follow-through-execution-tracker.csv")
EVENT_WATCH_CALENDAR = Path("cases/long-term-workflow-validation-2026-05-30/g04-follow-through-event-watch-calendar.csv")
TRIGGER_TRACKER = Path("cases/long-term-workflow-validation-2026-05-30/follow-through-trigger-tracker.csv")
LATER_EVENT_CANDIDATE_SCREEN = Path("cases/long-term-workflow-validation-2026-05-30/g04-later-event-candidate-screen.csv")

REQUIRED_COLUMNS = {
    "execution_id",
    "gate_id",
    "case_id",
    "packet_status",
    "event_status",
    "refresh_status",
    "original_cutoff",
    "packet_command",
    "refresh_validator_command",
    "current_status",
    "release_impact",
    "evidence_path",
    "next_action",
}

PACKET_STATUSES = {"packet_export_ready", "packet_exported", "packet_needs_update"}
EVENT_STATUSES = {"waiting_for_later_event", "later_event_available", "event_not_qualifying"}
REFRESH_STATUSES = {"not_started", "drafted_not_validated", "validated_completed", "rejected_or_needs_revision"}
CURRENT_STATUSES = {
    "ready_to_execute_waiting_event",
    "ready_to_refresh",
    "refresh_drafted_not_validated",
    "validated_completed",
    "rejected_or_needs_revision",
}
REQUIRED_CASES = {"ETN_2026", "VRT_2026", "CRM_2026", "LLY_2026"}
WAITING_TRIGGER_STATUSES = {"waiting_for_later_event", "waiting_for_material_disclosure"}


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
        return [], [Issue("ERROR", str(TRACKER), "execution tracker has no rows")]
    missing = sorted(REQUIRED_COLUMNS - set(rows[0].keys()))
    if missing:
        return rows, [Issue("ERROR", str(TRACKER), f"missing columns: {missing}")]
    return rows, []


def read_support_rows(path: Path, required_columns: set[str]) -> tuple[dict[str, dict[str, str]], list[Issue]]:
    try:
        with (ROOT / path).open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    except Exception as exc:
        return {}, [Issue("ERROR", str(path), f"could not parse CSV: {exc}")]
    if not rows:
        return {}, [Issue("ERROR", str(path), "supporting tracker has no rows")]
    missing = sorted(required_columns - set(rows[0].keys()))
    if missing:
        return {}, [Issue("ERROR", str(path), f"missing columns: {missing}")]
    return {row.get("case_id", "").strip(): row for row in rows if row.get("case_id", "").strip()}, []


def validate_tracker() -> tuple[list[Issue], dict[str, int | bool]]:
    issues: list[Issue] = []
    rows, read_issues = read_rows()
    issues.extend(read_issues)
    calendar_rows, calendar_issues = read_support_rows(
        EVENT_WATCH_CALENDAR,
        {"case_id", "latest_event_qualifies", "event_status", "release_impact"},
    )
    trigger_rows, trigger_issues = read_support_rows(
        TRIGGER_TRACKER,
        {"case_id", "current_status", "next_event_needed"},
    )
    candidate_rows, candidate_issues = read_support_rows(
        LATER_EVENT_CANDIDATE_SCREEN,
        {"case_id", "candidate_event_status", "selected_for_refresh", "refresh_allowed", "release_impact"},
    )
    issues.extend(calendar_issues)
    issues.extend(trigger_issues)
    issues.extend(candidate_issues)
    stats: dict[str, int | bool] = {
        "executions": len(rows),
        "ready_waiting_event": 0,
        "ready_to_refresh": 0,
        "validated_completed": 0,
        "support_rows_checked": 0,
        "candidate_rows_checked": 0,
        "tracker_ready": False,
    }
    if read_issues or calendar_issues or trigger_issues or candidate_issues:
        return issues, stats

    seen_cases = {row.get("case_id", "").strip() for row in rows}
    missing_cases = sorted(REQUIRED_CASES - seen_cases)
    if missing_cases:
        issues.append(Issue("ERROR", str(TRACKER), f"missing required execution cases: {missing_cases}"))

    for i, row in enumerate(rows, start=2):
        gate_id = row.get("gate_id", "").strip()
        case_id = row.get("case_id", "").strip()
        packet_status = row.get("packet_status", "").strip()
        event_status = row.get("event_status", "").strip()
        refresh_status = row.get("refresh_status", "").strip()
        original_cutoff = row.get("original_cutoff", "").strip()
        packet_command = row.get("packet_command", "").strip()
        validator_command = row.get("refresh_validator_command", "").strip()
        current_status = row.get("current_status", "").strip()
        release_impact = row.get("release_impact", "").strip()
        evidence_path = row.get("evidence_path", "").strip()
        calendar = calendar_rows.get(case_id)
        trigger = trigger_rows.get(case_id)
        candidate = candidate_rows.get(case_id)

        if gate_id != "G04":
            issues.append(Issue("ERROR", str(TRACKER), f"row {i} gate_id must be G04"))
        if case_id not in REQUIRED_CASES:
            issues.append(Issue("ERROR", str(TRACKER), f"row {i} unsupported execution case `{case_id}`"))
        if case_id in REQUIRED_CASES:
            if not calendar:
                issues.append(Issue("ERROR", str(TRACKER), f"row {i} missing event calendar row for {case_id}"))
            if not trigger:
                issues.append(Issue("ERROR", str(TRACKER), f"row {i} missing trigger tracker row for {case_id}"))
            if not candidate:
                issues.append(Issue("ERROR", str(TRACKER), f"row {i} missing later-event candidate screen row for {case_id}"))
            if calendar and trigger:
                stats["support_rows_checked"] = int(stats["support_rows_checked"]) + 1
            if candidate:
                stats["candidate_rows_checked"] = int(stats["candidate_rows_checked"]) + 1
        if packet_status not in PACKET_STATUSES:
            issues.append(Issue("ERROR", str(TRACKER), f"row {i} invalid packet_status `{packet_status}`"))
        if event_status not in EVENT_STATUSES:
            issues.append(Issue("ERROR", str(TRACKER), f"row {i} invalid event_status `{event_status}`"))
        if refresh_status not in REFRESH_STATUSES:
            issues.append(Issue("ERROR", str(TRACKER), f"row {i} invalid refresh_status `{refresh_status}`"))
        if current_status not in CURRENT_STATUSES:
            issues.append(Issue("ERROR", str(TRACKER), f"row {i} invalid current_status `{current_status}`"))
        if original_cutoff != "2026-05-30":
            issues.append(Issue("ERROR", str(TRACKER), f"row {i} original_cutoff must be 2026-05-30"))
        if "build_follow_through_packet.py" not in packet_command or "--output" not in packet_command:
            issues.append(Issue("ERROR", str(TRACKER), f"row {i} missing packet builder command"))
        if case_id != "CRM_2026" and f"--case-id {case_id}" not in packet_command:
            issues.append(Issue("ERROR", str(TRACKER), f"row {i} non-default case missing explicit --case-id"))
        if "validate_follow_through_refresh.py" not in validator_command:
            issues.append(Issue("ERROR", str(TRACKER), f"row {i} missing refresh validator command"))
        for marker in (
            "--original-cutoff 2026-05-30",
            "--evidence-log",
            "--intake",
            "--gate-tracker",
            "--public-readiness-audit",
            "--review-log",
        ):
            if marker not in validator_command:
                issues.append(Issue("ERROR", str(TRACKER), f"row {i} validator command missing `{marker}`"))
        if evidence_path and not (ROOT / evidence_path).exists():
            issues.append(Issue("ERROR", str(TRACKER), f"row {i} evidence_path missing: {evidence_path}"))

        if current_status == "ready_to_execute_waiting_event":
            stats["ready_waiting_event"] = int(stats["ready_waiting_event"]) + 1
            if event_status != "waiting_for_later_event" or refresh_status != "not_started":
                issues.append(Issue("ERROR", str(TRACKER), f"row {i} ready waiting state must have waiting event and not_started refresh"))
            if release_impact != "blocks_external_release":
                issues.append(Issue("ERROR", str(TRACKER), f"row {i} waiting state must block external release"))
            if calendar:
                if calendar.get("latest_event_qualifies", "").strip() != "no":
                    issues.append(Issue("ERROR", str(TRACKER), f"row {i} event calendar must not mark latest event qualifying"))
                if calendar.get("event_status", "").strip() == "later_event_available":
                    issues.append(Issue("ERROR", str(TRACKER), f"row {i} event calendar says later event available but execution is waiting"))
                if calendar.get("release_impact", "").strip() != "blocks_external_release":
                    issues.append(Issue("ERROR", str(TRACKER), f"row {i} event calendar must block external release"))
            if trigger and trigger.get("current_status", "").strip() not in WAITING_TRIGGER_STATUSES:
                issues.append(
                    Issue(
                        "ERROR",
                        str(TRACKER),
                        f"row {i} trigger tracker status conflicts with waiting execution: "
                        f"{trigger.get('current_status', '').strip()}",
                    )
                )
            if candidate:
                if candidate.get("selected_for_refresh", "").strip() != "no" or candidate.get("refresh_allowed", "").strip() != "no":
                    issues.append(Issue("ERROR", str(TRACKER), f"row {i} waiting execution cannot have selected later-event candidate"))
                if candidate.get("release_impact", "").strip() != "blocks_external_release":
                    issues.append(Issue("ERROR", str(TRACKER), f"row {i} candidate screen must block external release"))
        if current_status in {"ready_to_refresh", "refresh_drafted_not_validated"}:
            stats["ready_to_refresh"] = int(stats["ready_to_refresh"]) + 1
            if release_impact != "blocks_external_release":
                issues.append(Issue("ERROR", str(TRACKER), f"row {i} incomplete refresh state must block external release"))
            if trigger and trigger.get("current_status", "").strip() == "refresh_completed":
                issues.append(Issue("ERROR", str(TRACKER), f"row {i} trigger tracker cannot mark refresh_completed before validation"))
            if candidate:
                if candidate.get("candidate_event_status", "").strip() != "later_event_available":
                    issues.append(Issue("ERROR", str(TRACKER), f"row {i} ready refresh requires later_event_available candidate"))
                if candidate.get("selected_for_refresh", "").strip() != "yes" or candidate.get("refresh_allowed", "").strip() != "yes":
                    issues.append(Issue("ERROR", str(TRACKER), f"row {i} ready refresh requires selected refresh candidate"))
        if current_status == "validated_completed":
            stats["validated_completed"] = int(stats["validated_completed"]) + 1
            if refresh_status != "validated_completed":
                issues.append(Issue("ERROR", str(TRACKER), f"row {i} completed state must have validated_completed refresh_status"))
            if release_impact not in {"can_clear_g04_if_gate_tracker_updated", "supports_external_release"}:
                issues.append(Issue("ERROR", str(TRACKER), f"row {i} completed state has invalid release_impact"))

    stats["tracker_ready"] = not [issue for issue in issues if issue.severity == "ERROR"]
    return issues, stats


def main() -> int:
    issues, stats = validate_tracker()
    errors = [issue for issue in issues if issue.severity == "ERROR"]
    for issue in issues:
        print(issue.render())
    print("follow_through_execution_tracker_validation:")
    print(f"  tracker_ready: {str(bool(stats['tracker_ready'])).lower()}")
    print(f"  executions: {int(stats['executions'])}")
    print(f"  ready_waiting_event: {int(stats['ready_waiting_event'])}")
    print(f"  ready_to_refresh: {int(stats['ready_to_refresh'])}")
    print(f"  validated_completed: {int(stats['validated_completed'])}")
    print(f"  support_rows_checked: {int(stats['support_rows_checked'])}")
    print(f"  candidate_rows_checked: {int(stats['candidate_rows_checked'])}")
    print(f"  errors: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
