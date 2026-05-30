#!/usr/bin/env python3
"""Validate the G04 follow-through trigger tracker.

This validates readiness to execute a future G04 refresh. It does not validate
or clear a completed refresh; use validate_follow_through_refresh.py for that.
"""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass
from pathlib import Path


REQUIRED_COLUMNS = {
    "case_id",
    "ticker",
    "current_action_label",
    "next_event_needed",
    "trigger_metric_or_evidence",
    "expected_source",
    "refresh_priority",
    "current_status",
    "why_it_matters",
    "owner_next_step",
}

ALLOWED_PRIORITIES = {"highest", "high", "medium", "low"}
ALLOWED_STATUSES = {
    "waiting_for_later_event",
    "waiting_for_material_disclosure",
    "ready_to_refresh",
    "refresh_completed",
    "retired",
}

REQUIRED_CASES = {"CRM_2026", "ETN_2026", "VRT_2026", "LLY_2026"}
REQUIRED_CRM_TRIGGER_MARKERS = {"Agentforce", "Data 360", "ARR", "AWUs"}


@dataclass
class Issue:
    severity: str
    subject: str
    message: str

    def render(self) -> str:
        return f"{self.severity}: {self.subject}: {self.message}"


def read_rows(path: Path) -> tuple[list[dict[str, str]], list[Issue]]:
    try:
        with path.open(newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f)), []
    except Exception as exc:
        return [], [Issue("ERROR", str(path), f"could not parse CSV: {exc}")]


def validate_tracker(path: Path) -> list[Issue]:
    issues: list[Issue] = []
    rows, csv_issues = read_rows(path)
    issues.extend(csv_issues)
    if not rows:
        issues.append(Issue("ERROR", str(path), "trigger tracker has no rows"))
        return issues

    header = set(rows[0].keys())
    missing_columns = sorted(REQUIRED_COLUMNS - header)
    if missing_columns:
        issues.append(Issue("ERROR", str(path), f"missing columns: {missing_columns}"))
        return issues

    seen_cases = {row.get("case_id", "").strip() for row in rows}
    missing_cases = sorted(REQUIRED_CASES - seen_cases)
    if missing_cases:
        issues.append(Issue("ERROR", str(path), f"missing required cases: {missing_cases}"))

    crm_rows = [row for row in rows if row.get("case_id", "").strip() == "CRM_2026"]
    if not crm_rows:
        issues.append(Issue("ERROR", str(path), "CRM_2026 preferred G04 candidate missing"))
    else:
        crm = crm_rows[0]
        priority = crm.get("refresh_priority", "").strip()
        trigger = crm.get("trigger_metric_or_evidence", "")
        if priority != "highest":
            issues.append(Issue("ERROR", str(path), "CRM_2026 must be highest priority"))
        missing_markers = sorted(
            marker for marker in REQUIRED_CRM_TRIGGER_MARKERS if marker not in trigger
        )
        if missing_markers:
            issues.append(
                Issue("ERROR", str(path), f"CRM_2026 trigger missing markers: {missing_markers}")
            )

    for i, row in enumerate(rows, start=2):
        case_id = row.get("case_id", "").strip()
        priority = row.get("refresh_priority", "").strip()
        status = row.get("current_status", "").strip()
        trigger = row.get("trigger_metric_or_evidence", "").strip()
        source = row.get("expected_source", "").strip()
        why = row.get("why_it_matters", "").strip()
        next_step = row.get("owner_next_step", "").strip()
        action_label = row.get("current_action_label", "").strip()
        event_needed = row.get("next_event_needed", "").strip()

        if not case_id:
            issues.append(Issue("ERROR", str(path), f"row {i} missing case_id"))
        if priority not in ALLOWED_PRIORITIES:
            issues.append(Issue("ERROR", str(path), f"row {i} invalid refresh_priority `{priority}`"))
        if status not in ALLOWED_STATUSES:
            issues.append(Issue("ERROR", str(path), f"row {i} invalid current_status `{status}`"))
        if status == "refresh_completed":
            issues.append(
                Issue(
                    "ERROR",
                    str(path),
                    f"row {i} is marked refresh_completed; use completed G04 validator instead",
                )
            )
        for field_name, value in {
            "current_action_label": action_label,
            "next_event_needed": event_needed,
            "trigger_metric_or_evidence": trigger,
            "expected_source": source,
            "why_it_matters": why,
            "owner_next_step": next_step,
        }.items():
            if not value:
                issues.append(Issue("ERROR", str(path), f"row {i} missing {field_name}"))
        if case_id != "HUMANOID_2026" and "earnings" not in event_needed.lower() and "guidance" not in event_needed.lower() and "update" not in event_needed.lower():
            issues.append(
                Issue(
                    "WARN",
                    str(path),
                    f"row {i} event trigger may be too vague: `{event_needed}`",
                )
            )
        if "+" not in source and "," not in source and " + " not in source:
            issues.append(
                Issue(
                    "WARN",
                    str(path),
                    f"row {i} expected_source may need multiple source types: `{source}`",
                )
            )
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--tracker",
        default="cases/long-term-workflow-validation-2026-05-30/follow-through-trigger-tracker.csv",
        help="follow-through-trigger-tracker.csv path",
    )
    args = parser.parse_args()

    issues = validate_tracker(Path(args.tracker))
    errors = [issue for issue in issues if issue.severity == "ERROR"]
    warnings = [issue for issue in issues if issue.severity == "WARN"]
    for issue in issues:
        print(issue.render())
    print("follow_through_trigger_tracker_validation:")
    print(f"  tracker_ready: {str(not errors).lower()}")
    print(f"  errors: {len(errors)}")
    print(f"  warnings: {len(warnings)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
