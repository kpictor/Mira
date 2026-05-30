#!/usr/bin/env python3
"""Validate the G04 follow-through event watch calendar.

This checks that future follow-through work has observable event watches
without treating a scheduled or monitored event as completed G04 evidence.
"""

from __future__ import annotations

import csv
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CALENDAR = Path("cases/long-term-workflow-validation-2026-05-30/g04-follow-through-event-watch-calendar.csv")
ORIGINAL_CUTOFF = date.fromisoformat("2026-05-30")
REQUIRED_CASES = {"ETN_2026", "VRT_2026", "CRM_2026", "LLY_2026"}
ALLOWED_EVENT_STATUSES = {"monitor_official_ir", "scheduled_future_event", "later_event_available"}
ALLOWED_QUALIFY_FLAGS = {"no", "future_pending", "yes_after_refresh_validated"}
OFFICIAL_SOURCE_MARKERS = {
    "ETN_2026": "eaton.com",
    "VRT_2026": "investors.vertiv.com",
    "CRM_2026": "salesforce.com",
    "LLY_2026": "investor.lilly.com",
}

REQUIRED_COLUMNS = {
    "case_id",
    "ticker",
    "as_of_date",
    "original_cutoff",
    "latest_verified_event",
    "latest_verified_event_date",
    "latest_event_qualifies",
    "watch_event",
    "next_expected_event_date",
    "event_status",
    "official_source_url",
    "next_check_after",
    "trigger_requirements",
    "owner_next_step",
    "release_impact",
    "source_note",
}


@dataclass
class Issue:
    severity: str
    subject: str
    message: str

    def render(self) -> str:
        return f"{self.severity}: {self.subject}: {self.message}"


def parse_date(value: str, *, allow_not_announced: bool = False) -> date | None:
    value = value.strip()
    if allow_not_announced and value == "not_announced":
        return None
    return date.fromisoformat(value)


def read_rows() -> tuple[list[dict[str, str]], list[Issue]]:
    try:
        with (ROOT / CALENDAR).open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    except Exception as exc:
        return [], [Issue("ERROR", str(CALENDAR), f"could not parse CSV: {exc}")]
    if not rows:
        return [], [Issue("ERROR", str(CALENDAR), "event watch calendar has no rows")]
    missing = sorted(REQUIRED_COLUMNS - set(rows[0].keys()))
    if missing:
        return rows, [Issue("ERROR", str(CALENDAR), f"missing columns: {missing}")]
    return rows, []


def validate_calendar() -> tuple[list[Issue], dict[str, int | bool]]:
    issues: list[Issue] = []
    rows, row_issues = read_rows()
    issues.extend(row_issues)
    stats: dict[str, int | bool] = {
        "watch_rows": len(rows),
        "scheduled_future_events": 0,
        "monitor_rows": 0,
        "later_event_available": 0,
        "calendar_ready": False,
    }
    if row_issues:
        return issues, stats

    seen = {row.get("case_id", "").strip() for row in rows}
    missing_cases = sorted(REQUIRED_CASES - seen)
    if missing_cases:
        issues.append(Issue("ERROR", str(CALENDAR), f"missing required cases: {missing_cases}"))

    for i, row in enumerate(rows, start=2):
        case_id = row.get("case_id", "").strip()
        latest_qualifies = row.get("latest_event_qualifies", "").strip()
        event_status = row.get("event_status", "").strip()
        source_url = row.get("official_source_url", "").strip()
        release_impact = row.get("release_impact", "").strip()
        next_expected = row.get("next_expected_event_date", "").strip()
        trigger_requirements = row.get("trigger_requirements", "").strip()
        owner_next_step = row.get("owner_next_step", "").strip()
        source_note = row.get("source_note", "").strip()

        if case_id not in REQUIRED_CASES:
            issues.append(Issue("ERROR", str(CALENDAR), f"row {i} unsupported case `{case_id}`"))
            continue
        if event_status not in ALLOWED_EVENT_STATUSES:
            issues.append(Issue("ERROR", str(CALENDAR), f"row {i} invalid event_status `{event_status}`"))
        if latest_qualifies not in ALLOWED_QUALIFY_FLAGS:
            issues.append(Issue("ERROR", str(CALENDAR), f"row {i} invalid latest_event_qualifies `{latest_qualifies}`"))
        if latest_qualifies != "no":
            issues.append(Issue("ERROR", str(CALENDAR), f"row {i} cannot mark G04 event qualifying before validated refresh"))
        if release_impact != "blocks_external_release":
            issues.append(Issue("ERROR", str(CALENDAR), f"row {i} must block external release until refresh validates"))
        if OFFICIAL_SOURCE_MARKERS[case_id] not in source_url:
            issues.append(Issue("ERROR", str(CALENDAR), f"row {i} official source is not expected IR domain: {source_url}"))
        if not trigger_requirements or ";" not in trigger_requirements:
            issues.append(Issue("ERROR", str(CALENDAR), f"row {i} trigger_requirements must list multiple checks"))
        if "2026-05-30" not in owner_next_step and "after" not in owner_next_step.lower():
            issues.append(Issue("ERROR", str(CALENDAR), f"row {i} next step must preserve post-cutoff boundary"))
        if not source_note:
            issues.append(Issue("ERROR", str(CALENDAR), f"row {i} missing source_note"))

        try:
            as_of = parse_date(row.get("as_of_date", ""))
            cutoff = parse_date(row.get("original_cutoff", ""))
            latest_event = parse_date(row.get("latest_verified_event_date", ""))
            next_check = parse_date(row.get("next_check_after", ""))
            next_event_date = parse_date(next_expected, allow_not_announced=True)
        except ValueError as exc:
            issues.append(Issue("ERROR", str(CALENDAR), f"row {i} invalid date: {exc}"))
            continue

        if cutoff != ORIGINAL_CUTOFF:
            issues.append(Issue("ERROR", str(CALENDAR), f"row {i} original_cutoff must be 2026-05-30"))
        if as_of != ORIGINAL_CUTOFF:
            issues.append(Issue("ERROR", str(CALENDAR), f"row {i} as_of_date must be 2026-05-30"))
        if latest_event and latest_event > ORIGINAL_CUTOFF and latest_qualifies == "no":
            issues.append(Issue("ERROR", str(CALENDAR), f"row {i} later event cannot be marked non-qualifying without rationale"))
        if next_check <= ORIGINAL_CUTOFF:
            issues.append(Issue("ERROR", str(CALENDAR), f"row {i} next_check_after must be after original cutoff"))
        if event_status == "scheduled_future_event":
            stats["scheduled_future_events"] = int(stats["scheduled_future_events"]) + 1
            if not next_event_date or next_event_date <= ORIGINAL_CUTOFF:
                issues.append(Issue("ERROR", str(CALENDAR), f"row {i} scheduled future event must have post-cutoff date"))
        if event_status == "monitor_official_ir":
            stats["monitor_rows"] = int(stats["monitor_rows"]) + 1
            if next_expected != "not_announced":
                issues.append(Issue("ERROR", str(CALENDAR), f"row {i} monitor row should use not_announced next_expected_event_date"))
        if event_status == "later_event_available":
            stats["later_event_available"] = int(stats["later_event_available"]) + 1
            issues.append(Issue("ERROR", str(CALENDAR), f"row {i} later event available must move execution tracker to ready_to_refresh"))

    stats["calendar_ready"] = not [issue for issue in issues if issue.severity == "ERROR"]
    return issues, stats


def main() -> int:
    issues, stats = validate_calendar()
    errors = [issue for issue in issues if issue.severity == "ERROR"]
    for issue in issues:
        print(issue.render())
    print("g04_event_watch_calendar_validation:")
    print(f"  calendar_ready: {str(bool(stats['calendar_ready'])).lower()}")
    print(f"  watch_rows: {int(stats['watch_rows'])}")
    print(f"  scheduled_future_events: {int(stats['scheduled_future_events'])}")
    print(f"  monitor_rows: {int(stats['monitor_rows'])}")
    print(f"  later_event_available: {int(stats['later_event_available'])}")
    print("  clears_g04: false")
    print(f"  errors: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
