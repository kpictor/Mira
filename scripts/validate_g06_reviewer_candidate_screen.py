#!/usr/bin/env python3
"""Validate the G06 reviewer candidate screen.

This is a candidate-level pre-assignment control. It does not clear G06; it
keeps reviewer selection auditable before a named independent reviewer is added
to the assignment tracker.
"""

from __future__ import annotations

import csv
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCREEN = Path("cases/long-term-workflow-validation-2026-05-30/g06-reviewer-candidate-screen.csv")

REQUIRED_COLUMNS = {
    "candidate_id",
    "candidate_profile",
    "target_review_scope",
    "selection_priority",
    "candidate_status",
    "reviewer_name",
    "reviewer_org_or_role",
    "conflict_check",
    "authorship_check",
    "incentive_check",
    "capability_check",
    "source_boundary_ack",
    "internal_material_access",
    "assigned_in_tracker",
    "evidence_path",
    "release_impact",
    "notes",
}

REQUIRED_PROFILES = {
    "integrated_methodology_reviewer",
    "live_case_reproducibility_reviewer",
    "source_quality_valuation_reviewer",
}
REQUIRED_PRIORITIES = {"primary", "alternate_1", "alternate_2"}

CANDIDATE_STATUSES = {
    "pending_candidate_selection",
    "screened_not_assigned",
    "eligible_for_assignment",
    "selected_assigned",
    "rejected",
}
CHECK_COLUMNS = {
    "conflict_check",
    "authorship_check",
    "incentive_check",
    "capability_check",
    "source_boundary_ack",
}
CHECK_STATUSES = {"pending_external", "pass", "accepted", "fail", "not_applicable"}


@dataclass
class Issue:
    severity: str
    subject: str
    message: str

    def render(self) -> str:
        return f"{self.severity}: {self.subject}: {self.message}"


def read_rows() -> tuple[list[dict[str, str]], list[Issue]]:
    try:
        with (ROOT / SCREEN).open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    except Exception as exc:
        return [], [Issue("ERROR", str(SCREEN), f"could not parse CSV: {exc}")]
    if not rows:
        return [], [Issue("ERROR", str(SCREEN), "candidate screen has no rows")]
    missing = sorted(REQUIRED_COLUMNS - set(rows[0].keys()))
    if missing:
        return rows, [Issue("ERROR", str(SCREEN), f"missing columns: {missing}")]
    return rows, []


def passed(value: str) -> bool:
    return value.strip() in {"pass", "accepted"}


def placeholder(value: str) -> bool:
    return value.strip() in {"", "set_on_assignment", "pending_candidate_selection"}


def validate_screen() -> tuple[list[Issue], dict[str, int | bool]]:
    issues: list[Issue] = []
    rows, read_issues = read_rows()
    issues.extend(read_issues)
    stats: dict[str, int | bool] = {
        "candidates": len(rows),
        "pending_candidate_selection": 0,
        "eligible_for_assignment": 0,
        "selected_assigned": 0,
        "candidate_profiles_checked": 0,
        "control_rows_checked": 0,
        "clears_g06": False,
    }
    if read_issues:
        return issues, stats

    profiles = {row.get("candidate_profile", "").strip() for row in rows}
    missing_profiles = sorted(REQUIRED_PROFILES - profiles)
    if missing_profiles:
        issues.append(Issue("ERROR", str(SCREEN), f"missing required candidate profiles: {missing_profiles}"))
    priorities = {row.get("selection_priority", "").strip() for row in rows}
    missing_priorities = sorted(REQUIRED_PRIORITIES - priorities)
    if missing_priorities:
        issues.append(Issue("ERROR", str(SCREEN), f"missing required selection priorities: {missing_priorities}"))

    for i, row in enumerate(rows, start=2):
        candidate_id = row.get("candidate_id", "").strip()
        candidate_profile = row.get("candidate_profile", "").strip()
        target_scope = row.get("target_review_scope", "").strip()
        selection_priority = row.get("selection_priority", "").strip()
        candidate_status = row.get("candidate_status", "").strip()
        reviewer_name = row.get("reviewer_name", "").strip()
        reviewer_role = row.get("reviewer_org_or_role", "").strip()
        internal_access = row.get("internal_material_access", "").strip().lower()
        assigned = row.get("assigned_in_tracker", "").strip().lower()
        release_impact = row.get("release_impact", "").strip()
        evidence_path = row.get("evidence_path", "").strip()

        if not candidate_id:
            issues.append(Issue("ERROR", str(SCREEN), f"row {i} missing candidate_id"))
        if candidate_profile not in REQUIRED_PROFILES:
            issues.append(Issue("ERROR", str(SCREEN), f"row {i} unsupported candidate_profile `{candidate_profile}`"))
        else:
            stats["candidate_profiles_checked"] = int(stats["candidate_profiles_checked"]) + 1
        if selection_priority not in REQUIRED_PRIORITIES:
            issues.append(Issue("ERROR", str(SCREEN), f"row {i} unsupported selection_priority `{selection_priority}`"))
        if len(target_scope) < 40:
            issues.append(Issue("ERROR", str(SCREEN), f"row {i} target_review_scope too vague"))
        for marker in ("G04", "source", "workflow"):
            if marker not in target_scope:
                issues.append(Issue("ERROR", str(SCREEN), f"row {i} target_review_scope missing `{marker}`"))
        if candidate_status not in CANDIDATE_STATUSES:
            issues.append(Issue("ERROR", str(SCREEN), f"row {i} invalid candidate_status `{candidate_status}`"))
        if internal_access not in {"yes", "no"}:
            issues.append(Issue("ERROR", str(SCREEN), f"row {i} internal_material_access must be yes or no"))
        if assigned not in {"yes", "no"}:
            issues.append(Issue("ERROR", str(SCREEN), f"row {i} assigned_in_tracker must be yes or no"))
        if internal_access != "no":
            issues.append(Issue("ERROR", str(SCREEN), f"row {i} reviewer candidate cannot have internal material access"))
        if release_impact != "blocks_external_release":
            issues.append(Issue("ERROR", str(SCREEN), f"row {i} candidate screen must block external release until G06 return passes"))
        if evidence_path and not (ROOT / evidence_path).exists():
            issues.append(Issue("ERROR", str(SCREEN), f"row {i} evidence_path missing: {evidence_path}"))

        for column in CHECK_COLUMNS:
            value = row.get(column, "").strip()
            if value not in CHECK_STATUSES:
                issues.append(Issue("ERROR", str(SCREEN), f"row {i} invalid {column} `{value}`"))
            stats["control_rows_checked"] = int(stats["control_rows_checked"]) + 1

        if candidate_status == "pending_candidate_selection":
            stats["pending_candidate_selection"] = int(stats["pending_candidate_selection"]) + 1
            if reviewer_name != "set_on_assignment" or reviewer_role != "set_on_assignment":
                issues.append(Issue("ERROR", str(SCREEN), f"row {i} pending candidate selection must not name reviewer"))
            for column in CHECK_COLUMNS:
                if row.get(column, "").strip() != "pending_external":
                    issues.append(Issue("ERROR", str(SCREEN), f"row {i} pending candidate selection requires {column} pending_external"))
            if assigned != "no":
                issues.append(Issue("ERROR", str(SCREEN), f"row {i} pending candidate selection cannot be assigned in tracker"))

        if candidate_status in {"screened_not_assigned", "eligible_for_assignment", "selected_assigned"}:
            if placeholder(reviewer_name) or placeholder(reviewer_role):
                issues.append(Issue("ERROR", str(SCREEN), f"row {i} screened candidate requires named reviewer and role"))
            for column in CHECK_COLUMNS:
                if not passed(row.get(column, "")):
                    issues.append(Issue("ERROR", str(SCREEN), f"row {i} screened candidate requires {column} pass/accepted"))

        if candidate_status == "eligible_for_assignment":
            stats["eligible_for_assignment"] = int(stats["eligible_for_assignment"]) + 1
            if assigned != "no":
                issues.append(Issue("ERROR", str(SCREEN), f"row {i} eligible candidate is not yet assigned and must have assigned_in_tracker no"))

        if candidate_status == "selected_assigned":
            stats["selected_assigned"] = int(stats["selected_assigned"]) + 1
            if assigned != "yes":
                issues.append(Issue("ERROR", str(SCREEN), f"row {i} selected_assigned requires assigned_in_tracker yes"))
            if placeholder(reviewer_name):
                issues.append(Issue("ERROR", str(SCREEN), f"row {i} selected_assigned requires named reviewer"))

        if candidate_status == "rejected":
            if assigned != "no":
                issues.append(Issue("ERROR", str(SCREEN), f"row {i} rejected candidate cannot be assigned in tracker"))

    stats["clears_g06"] = False
    return issues, stats


def main() -> int:
    issues, stats = validate_screen()
    errors = [issue for issue in issues if issue.severity == "ERROR"]
    for issue in issues:
        print(issue.render())
    print("g06_reviewer_candidate_screen_validation:")
    print(f"  candidates: {int(stats['candidates'])}")
    print(f"  pending_candidate_selection: {int(stats['pending_candidate_selection'])}")
    print(f"  eligible_for_assignment: {int(stats['eligible_for_assignment'])}")
    print(f"  selected_assigned: {int(stats['selected_assigned'])}")
    print(f"  candidate_profiles_checked: {int(stats['candidate_profiles_checked'])}")
    print(f"  control_rows_checked: {int(stats['control_rows_checked'])}")
    print(f"  clears_g06: {str(bool(stats['clears_g06'])).lower()}")
    print(f"  errors: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
