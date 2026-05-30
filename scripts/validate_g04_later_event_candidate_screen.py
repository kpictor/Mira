#!/usr/bin/env python3
"""Validate G04 later-event candidate screening.

This sits between the watch calendar and a completed follow-through refresh.
It prevents scheduled events, non-official updates, or non-material updates from
being treated as a G04-ready refresh trigger.
"""

from __future__ import annotations

import csv
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCREEN = Path("cases/long-term-workflow-validation-2026-05-30/g04-later-event-candidate-screen.csv")
EVENT_WATCH_CALENDAR = Path("cases/long-term-workflow-validation-2026-05-30/g04-follow-through-event-watch-calendar.csv")
EXECUTION_TRACKER = Path("cases/long-term-workflow-validation-2026-05-30/g04-follow-through-execution-tracker.csv")

REQUIRED_CASES = {"ETN_2026", "VRT_2026", "CRM_2026", "LLY_2026"}
REQUIRED_COLUMNS = {
    "case_id",
    "ticker",
    "original_cutoff",
    "candidate_event",
    "candidate_event_date",
    "candidate_event_status",
    "after_original_cutoff",
    "official_source_status",
    "materiality_status",
    "selected_for_refresh",
    "refresh_allowed",
    "execution_status_required",
    "evidence_path",
    "release_impact",
    "next_action",
    "notes",
}

CANDIDATE_STATUSES = {
    "no_later_event_identified",
    "scheduled_future_event",
    "later_event_available",
    "event_not_qualifying",
}
OFFICIAL_SOURCE_STATUSES = {
    "not_available",
    "scheduled_official_ir",
    "official_materials_available",
    "non_official_only",
}
MATERIALITY_STATUSES = {"pending_external", "pending_event_materials", "pass", "fail"}
YES_NO = {"yes", "no"}


@dataclass
class Issue:
    severity: str
    subject: str
    message: str

    def render(self) -> str:
        return f"{self.severity}: {self.subject}: {self.message}"


def read_rows(path: Path, required_columns: set[str]) -> tuple[list[dict[str, str]], list[Issue]]:
    try:
        with (ROOT / path).open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    except Exception as exc:
        return [], [Issue("ERROR", str(path), f"could not parse CSV: {exc}")]
    if not rows:
        return [], [Issue("ERROR", str(path), "CSV has no rows")]
    missing = sorted(required_columns - set(rows[0].keys()))
    if missing:
        return rows, [Issue("ERROR", str(path), f"missing columns: {missing}")]
    return rows, []


def by_case(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row.get("case_id", "").strip(): row for row in rows if row.get("case_id", "").strip()}


def parse_date(value: str) -> date | None:
    if value.strip() == "n/a":
        return None
    try:
        return date.fromisoformat(value.strip())
    except ValueError:
        return None


def validate_screen() -> tuple[list[Issue], dict[str, int | bool]]:
    issues: list[Issue] = []
    rows, row_issues = read_rows(SCREEN, REQUIRED_COLUMNS)
    calendar_rows, calendar_issues = read_rows(
        EVENT_WATCH_CALENDAR,
        {"case_id", "original_cutoff", "latest_event_qualifies", "next_expected_event_date", "event_status", "release_impact"},
    )
    execution_rows, execution_issues = read_rows(
        EXECUTION_TRACKER,
        {"case_id", "current_status", "event_status", "release_impact"},
    )
    issues.extend(row_issues + calendar_issues + execution_issues)
    stats: dict[str, int | bool] = {
        "candidate_rows": len(rows),
        "scheduled_future_events": 0,
        "later_event_available": 0,
        "selected_for_refresh": 0,
        "support_rows_checked": 0,
        "clears_g04": False,
    }
    if row_issues or calendar_issues or execution_issues:
        return issues, stats

    calendar_by_case = by_case(calendar_rows)
    execution_by_case = by_case(execution_rows)
    seen_cases = {row.get("case_id", "").strip() for row in rows}
    missing_cases = sorted(REQUIRED_CASES - seen_cases)
    if missing_cases:
        issues.append(Issue("ERROR", str(SCREEN), f"missing required candidate cases: {missing_cases}"))

    for i, row in enumerate(rows, start=2):
        case_id = row.get("case_id", "").strip()
        original_cutoff = row.get("original_cutoff", "").strip()
        candidate_event = row.get("candidate_event", "").strip()
        candidate_event_date = row.get("candidate_event_date", "").strip()
        candidate_status = row.get("candidate_event_status", "").strip()
        after_cutoff = row.get("after_original_cutoff", "").strip()
        official_status = row.get("official_source_status", "").strip()
        materiality_status = row.get("materiality_status", "").strip()
        selected = row.get("selected_for_refresh", "").strip()
        refresh_allowed = row.get("refresh_allowed", "").strip()
        execution_required = row.get("execution_status_required", "").strip()
        release_impact = row.get("release_impact", "").strip()
        evidence_path = row.get("evidence_path", "").strip()
        calendar = calendar_by_case.get(case_id)
        execution = execution_by_case.get(case_id)

        if case_id not in REQUIRED_CASES:
            issues.append(Issue("ERROR", str(SCREEN), f"row {i} unsupported case_id `{case_id}`"))
        if not candidate_event:
            issues.append(Issue("ERROR", str(SCREEN), f"row {i} missing candidate_event"))
        if original_cutoff != "2026-05-30":
            issues.append(Issue("ERROR", str(SCREEN), f"row {i} original_cutoff must be 2026-05-30"))
        if candidate_status not in CANDIDATE_STATUSES:
            issues.append(Issue("ERROR", str(SCREEN), f"row {i} invalid candidate_event_status `{candidate_status}`"))
        if after_cutoff not in YES_NO:
            issues.append(Issue("ERROR", str(SCREEN), f"row {i} after_original_cutoff must be yes or no"))
        if official_status not in OFFICIAL_SOURCE_STATUSES:
            issues.append(Issue("ERROR", str(SCREEN), f"row {i} invalid official_source_status `{official_status}`"))
        if materiality_status not in MATERIALITY_STATUSES:
            issues.append(Issue("ERROR", str(SCREEN), f"row {i} invalid materiality_status `{materiality_status}`"))
        if selected not in YES_NO:
            issues.append(Issue("ERROR", str(SCREEN), f"row {i} selected_for_refresh must be yes or no"))
        if refresh_allowed not in YES_NO:
            issues.append(Issue("ERROR", str(SCREEN), f"row {i} refresh_allowed must be yes or no"))
        if release_impact != "blocks_external_release":
            issues.append(Issue("ERROR", str(SCREEN), f"row {i} candidate screen must block external release until refresh validates"))
        if evidence_path and not (ROOT / evidence_path).exists():
            issues.append(Issue("ERROR", str(SCREEN), f"row {i} evidence_path missing: {evidence_path}"))
        if not calendar:
            issues.append(Issue("ERROR", str(SCREEN), f"row {i} missing calendar support row"))
        if not execution:
            issues.append(Issue("ERROR", str(SCREEN), f"row {i} missing execution support row"))
        if calendar and execution:
            stats["support_rows_checked"] = int(stats["support_rows_checked"]) + 1

        event_date = parse_date(candidate_event_date)
        cutoff = parse_date(original_cutoff)
        if candidate_event_date != "n/a" and event_date is None:
            issues.append(Issue("ERROR", str(SCREEN), f"row {i} candidate_event_date must be ISO date or n/a"))
        if event_date and cutoff and event_date <= cutoff:
            issues.append(Issue("ERROR", str(SCREEN), f"row {i} candidate_event_date must be after original_cutoff"))
        if event_date and after_cutoff != "yes":
            issues.append(Issue("ERROR", str(SCREEN), f"row {i} dated candidate after cutoff must mark after_original_cutoff yes"))

        if candidate_status == "no_later_event_identified":
            if after_cutoff != "no" or official_status != "not_available":
                issues.append(Issue("ERROR", str(SCREEN), f"row {i} no later event must have no cutoff and no official source"))
            if selected != "no" or refresh_allowed != "no":
                issues.append(Issue("ERROR", str(SCREEN), f"row {i} no later event cannot be selected for refresh"))

        if candidate_status == "scheduled_future_event":
            stats["scheduled_future_events"] = int(stats["scheduled_future_events"]) + 1
            if candidate_event_date == "n/a" or after_cutoff != "yes":
                issues.append(Issue("ERROR", str(SCREEN), f"row {i} scheduled future event requires dated post-cutoff event"))
            if official_status != "scheduled_official_ir":
                issues.append(Issue("ERROR", str(SCREEN), f"row {i} scheduled future event requires scheduled_official_ir"))
            if materiality_status != "pending_event_materials":
                issues.append(Issue("ERROR", str(SCREEN), f"row {i} scheduled future event materiality must be pending_event_materials"))
            if selected != "no" or refresh_allowed != "no":
                issues.append(Issue("ERROR", str(SCREEN), f"row {i} scheduled future event cannot be selected before materials publish"))
            if calendar and calendar.get("event_status", "").strip() != "scheduled_future_event":
                issues.append(Issue("ERROR", str(SCREEN), f"row {i} calendar must also show scheduled_future_event"))

        if candidate_status == "later_event_available":
            stats["later_event_available"] = int(stats["later_event_available"]) + 1
            if after_cutoff != "yes":
                issues.append(Issue("ERROR", str(SCREEN), f"row {i} later event must be after original cutoff"))
            if official_status != "official_materials_available":
                issues.append(Issue("ERROR", str(SCREEN), f"row {i} later event requires official materials"))
            if materiality_status != "pass":
                issues.append(Issue("ERROR", str(SCREEN), f"row {i} later event requires materiality pass"))
            if selected != "yes" or refresh_allowed != "yes":
                issues.append(Issue("ERROR", str(SCREEN), f"row {i} later event must be selected and refresh_allowed"))
            if execution_required != "ready_to_refresh":
                issues.append(Issue("ERROR", str(SCREEN), f"row {i} later event requires execution_status_required ready_to_refresh"))

        if selected == "yes" or refresh_allowed == "yes":
            stats["selected_for_refresh"] = int(stats["selected_for_refresh"]) + 1
            if candidate_status != "later_event_available":
                issues.append(Issue("ERROR", str(SCREEN), f"row {i} refresh selection requires later_event_available"))
            if calendar and calendar.get("latest_event_qualifies", "").strip() != "yes":
                issues.append(Issue("ERROR", str(SCREEN), f"row {i} selected refresh requires calendar latest_event_qualifies yes"))
            if execution and execution.get("current_status", "").strip() != "ready_to_refresh":
                issues.append(Issue("ERROR", str(SCREEN), f"row {i} selected refresh requires execution tracker ready_to_refresh"))
        else:
            if execution and execution.get("current_status", "").strip() != execution_required:
                issues.append(Issue("ERROR", str(SCREEN), f"row {i} execution tracker status does not match screen requirement"))

    stats["clears_g04"] = False
    return issues, stats


def main() -> int:
    issues, stats = validate_screen()
    errors = [issue for issue in issues if issue.severity == "ERROR"]
    for issue in issues:
        print(issue.render())
    print("g04_later_event_candidate_screen_validation:")
    print(f"  candidate_rows: {int(stats['candidate_rows'])}")
    print(f"  scheduled_future_events: {int(stats['scheduled_future_events'])}")
    print(f"  later_event_available: {int(stats['later_event_available'])}")
    print(f"  selected_for_refresh: {int(stats['selected_for_refresh'])}")
    print(f"  support_rows_checked: {int(stats['support_rows_checked'])}")
    print(f"  clears_g04: {str(bool(stats['clears_g04'])).lower()}")
    print(f"  errors: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
