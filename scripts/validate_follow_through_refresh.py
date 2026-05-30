#!/usr/bin/env python3
"""Validate a completed G04 follow-through refresh.

This script validates the refresh artifact itself. It is intentionally stricter
than the template and should fail against an unfilled template.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path


DATE_RE = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")
FIELD_RE = re.compile(r"^\s*-\s*([^:]+):\s*(.*?)\s*$", re.MULTILINE)

ALLOWED_REFRESH_RESULT_LABELS = {
    "thesis_strengthened_action_unchanged",
    "thesis_strengthened_action_upgraded",
    "thesis_weakened_action_unchanged",
    "thesis_weakened_action_downgraded",
    "source_gap_closed_action_unchanged",
    "refresh_trigger_failed_too_vague",
    "refresh_trigger_failed_wrong_variable",
}

PLACEHOLDERS = {"", "yes/no", "replace", "TBD", "YYYY-MM-DD"}
G04_CLEAR_STATUSES = {"pass_external", "pass_public_grade", "completed", "accepted"}

REQUIRED_G04_INTAKE_REQUIREMENTS = {
    "later_event",
    "material_variable",
    "new_source_evidence",
    "before_after_action_label",
    "trigger_quality_evaluated",
    "result_label_valid",
    "public_grade_impact",
    "downstream_logs_updated",
}


@dataclass
class Issue:
    severity: str
    subject: str
    message: str

    def render(self) -> str:
        return f"{self.severity}: {self.subject}: {self.message}"


def parse_date(value: str) -> date | None:
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def read_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for match in FIELD_RE.finditer(text):
        key = match.group(1).strip()
        value = match.group(2).strip()
        fields[key] = value
    return fields


def scalar_field(text: str, key: str) -> str:
    pattern = re.compile(rf"^[ \t]*-[ \t]*{re.escape(key)}:[ \t]*(.*)[ \t]*$", re.MULTILINE)
    match = pattern.search(text)
    if not match:
        return ""
    return match.group(1).strip()


def section_text(text: str, heading: str) -> str:
    start = text.find(heading)
    if start == -1:
        return ""
    rest = text[start + len(heading) :]
    next_heading = rest.find("\n## ")
    if next_heading == -1:
        return rest
    return rest[:next_heading]


def table_data_rows(section: str) -> list[str]:
    rows: list[str] = []
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        if "---" in stripped:
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if cells and cells[0].lower() in {"requirement", "source_id", "thesis_variable"}:
            continue
        if any(cell for cell in cells):
            rows.append(stripped)
    return rows


def table_cells(row: str) -> list[str]:
    return [cell.strip() for cell in row.strip().strip("|").split("|")]


def has_non_placeholder_row(rows: list[str]) -> bool:
    for row in rows:
        cells = [cell.strip() for cell in row.strip("|").split("|")]
        if any(cell and cell not in PLACEHOLDERS for cell in cells):
            return True
    return False


def selected_refresh_result_labels(section: str) -> set[str]:
    selected: set[str] = set()
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped.startswith("-"):
            continue
        for label in ALLOWED_REFRESH_RESULT_LABELS:
            if label in stripped:
                selected.add(label)
    return selected


def evidence_log_later_source_ids(path: Path, cutoff: date) -> tuple[set[str], list[Issue]]:
    issues: list[Issue] = []
    source_ids: set[str] = set()
    try:
        with path.open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    except Exception as exc:
        return set(), [Issue("ERROR", str(path), f"could not parse evidence log: {exc}")]
    for i, row in enumerate(rows, start=2):
        raw_date = (row.get("source_date") or "").strip()
        source_id = (row.get("source_id") or "").strip()
        source_date = parse_date(raw_date)
        if source_date and source_date > cutoff:
            if source_id and source_id not in PLACEHOLDERS:
                source_ids.add(source_id)
        if raw_date and not source_date:
            issues.append(Issue("WARN", str(path), f"row {i} has non-ISO source_date `{raw_date}`"))
    return source_ids, issues


def read_csv_rows(path: Path) -> tuple[list[dict[str, str]], list[Issue]]:
    try:
        with path.open(newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f)), []
    except Exception as exc:
        return [], [Issue("ERROR", str(path), f"could not parse CSV: {exc}")]


def validate_intake(path: Path) -> list[Issue]:
    issues: list[Issue] = []
    try:
        with path.open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    except Exception as exc:
        return [Issue("ERROR", str(path), f"could not parse intake checklist: {exc}")]
    if not rows:
        return [Issue("ERROR", str(path), "intake checklist has no rows")]
    required_columns = {"check_id", "requirement", "pass_condition", "status", "notes"}
    missing = sorted(required_columns - set(rows[0].keys()))
    if missing:
        issues.append(Issue("ERROR", str(path), f"missing columns: {missing}"))
        return issues
    requirements = {row.get("requirement", "").strip() for row in rows}
    missing_requirements = sorted(REQUIRED_G04_INTAKE_REQUIREMENTS - requirements)
    if missing_requirements:
        issues.append(Issue("ERROR", str(path), f"missing requirements: {missing_requirements}"))
    for i, row in enumerate(rows, start=2):
        status = (row.get("status") or "").strip()
        if status not in {"pass", "accepted"}:
            issues.append(Issue("ERROR", str(path), f"row {i} not pass/accepted: {status}"))
    return issues


def validate_gate_tracker(path: Path, refresh_path: Path) -> list[Issue]:
    issues: list[Issue] = []
    rows, row_issues = read_csv_rows(path)
    issues.extend(row_issues)
    if row_issues:
        return issues
    g04_rows = [row for row in rows if row.get("gate_id", "").strip() == "G04"]
    if len(g04_rows) != 1:
        return [Issue("ERROR", str(path), f"expected exactly one G04 row, got {len(g04_rows)}")]
    row = g04_rows[0]
    status = row.get("current_status", "").strip()
    evidence_path = row.get("evidence_path", "").strip()
    if status not in G04_CLEAR_STATUSES:
        issues.append(Issue("ERROR", str(path), f"G04 current_status is not externally clear: {status}"))
    if not evidence_path or evidence_path in PLACEHOLDERS:
        issues.append(Issue("ERROR", str(path), "G04 evidence_path missing completed refresh"))
    elif Path(evidence_path).name != refresh_path.name and str(refresh_path) not in evidence_path:
        issues.append(
            Issue(
                "ERROR",
                str(path),
                f"G04 evidence_path must point to completed refresh `{refresh_path.name}`",
            )
        )
    return issues


def validate_public_readiness_audit(
    path: Path,
    case_id: str,
    refresh_path: Path,
    selected_labels: set[str],
) -> list[Issue]:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as exc:
        return [Issue("ERROR", str(path), f"could not read public readiness audit: {exc}")]
    issues: list[Issue] = []
    for marker in (case_id, refresh_path.name, "follow_through_gate_status: pass"):
        if marker and marker not in text:
            issues.append(Issue("ERROR", str(path), f"public readiness audit missing `{marker}`"))
    for label in selected_labels:
        if label not in text:
            issues.append(Issue("ERROR", str(path), f"public readiness audit missing refresh result `{label}`"))
    return issues


def validate_methodology_review_log(
    path: Path,
    case_id: str,
    refresh_path: Path,
    selected_labels: set[str],
) -> list[Issue]:
    rows, row_issues = read_csv_rows(path)
    if row_issues:
        return row_issues
    if not rows:
        return [Issue("ERROR", str(path), "methodology review log has no rows")]
    matching_rows = []
    for row in rows:
        row_text = " ".join(value.strip() for value in row.values())
        normalized = row_text.lower().replace("-", "_")
        has_case = case_id in row_text
        has_follow_through = "follow_through" in normalized
        has_refresh_ref = refresh_path.name in row_text or any(label in row_text for label in selected_labels)
        has_g04_boundary = "G04" in row_text or "true follow-through" in row_text
        if has_case and has_follow_through and has_refresh_ref and has_g04_boundary:
            matching_rows.append(row)
    if not matching_rows:
        return [
            Issue(
                "ERROR",
                str(path),
                f"methodology review log missing G04 follow-through row for `{case_id}` and `{refresh_path.name}`",
            )
        ]
    return []


def validate_refresh(
    path: Path,
    cutoff: date,
    evidence_log: Path | None,
    intake: Path | None,
    gate_tracker: Path | None,
    public_readiness_audit: Path | None,
    review_log: Path | None,
) -> tuple[list[Issue], int]:
    issues: list[Issue] = []
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as exc:
        return [Issue("ERROR", str(path), f"could not read refresh file: {exc}")], 0

    fields = read_fields(text)
    case_id = (fields.get("case_id", "") or scalar_field(text, "case_id")).strip()
    required_fields = [
        "case_id",
        "refresh_date",
        "original_memo_date",
        "original_action_label",
        "refreshed_action_label",
        "qualifies_as_true_follow_through",
        "follow_through_gate_status",
        "stale_after",
        "must_refresh_if",
    ]
    for field in required_fields:
        value = (fields.get(field, "") or scalar_field(text, field)).strip()
        if value in PLACEHOLDERS:
            issues.append(Issue("ERROR", str(path), f"missing or placeholder field `{field}`"))

    refresh_date = parse_date(fields.get("refresh_date", "") or scalar_field(text, "refresh_date"))
    if not refresh_date:
        issues.append(Issue("ERROR", str(path), "refresh_date must be YYYY-MM-DD"))
    elif refresh_date <= cutoff:
        issues.append(Issue("ERROR", str(path), f"refresh_date {refresh_date} is not after cutoff {cutoff}"))

    original_memo_date = parse_date(fields.get("original_memo_date", "") or scalar_field(text, "original_memo_date"))
    if not original_memo_date:
        issues.append(Issue("ERROR", str(path), "original_memo_date must be YYYY-MM-DD"))
    elif original_memo_date != cutoff:
        issues.append(
            Issue(
                "ERROR",
                str(path),
                f"original_memo_date {original_memo_date} does not match cutoff {cutoff}",
            )
        )

    stale_after = parse_date(fields.get("stale_after", "") or scalar_field(text, "stale_after"))
    if not stale_after:
        issues.append(Issue("ERROR", str(path), "stale_after must be YYYY-MM-DD"))
    elif refresh_date and stale_after <= refresh_date:
        issues.append(Issue("ERROR", str(path), f"stale_after {stale_after} is not after refresh_date {refresh_date}"))

    qualifies = (fields.get("qualifies_as_true_follow_through", "") or scalar_field(text, "qualifies_as_true_follow_through")).strip().lower()
    if qualifies != "yes":
        issues.append(Issue("ERROR", str(path), "qualifies_as_true_follow_through must be yes"))
    gate_status = (fields.get("follow_through_gate_status", "") or scalar_field(text, "follow_through_gate_status")).strip()
    if gate_status != "pass":
        issues.append(Issue("ERROR", str(path), "follow_through_gate_status must be pass"))

    required_markers = [
        "Event occurred after original memo cutoff",
        "Event is material to named thesis variable",
        "New source evidence added",
        "Before / After",
        "Refresh Trigger Quality",
        "Public-Grade Impact",
    ]
    for marker in required_markers:
        if marker not in text:
            issues.append(Issue("ERROR", str(path), f"missing marker `{marker}`"))

    qualification_rows = table_data_rows(section_text(text, "## Qualification Check"))
    if len(qualification_rows) < 5:
        issues.append(Issue("ERROR", str(path), "qualification table is incomplete"))
    expected_qualification_rows = {
        "Event occurred after original memo cutoff",
        "Event is material to named thesis variable",
        "New source evidence added",
        "Before/after action label stated",
        "Original refresh trigger evaluated",
    }
    seen_qualification_rows: set[str] = set()
    for row in qualification_rows:
        cells = table_cells(row)
        if len(cells) < 3:
            issues.append(Issue("ERROR", str(path), f"malformed qualification row: {row}"))
            continue
        requirement, answer, evidence = cells[0], cells[1].lower(), cells[2]
        seen_qualification_rows.add(requirement)
        if requirement in expected_qualification_rows and answer != "yes":
            issues.append(Issue("ERROR", str(path), f"qualification `{requirement}` must answer yes"))
        if requirement in expected_qualification_rows and evidence in PLACEHOLDERS:
            issues.append(Issue("ERROR", str(path), f"qualification `{requirement}` lacks evidence"))
    missing_qualification_rows = sorted(expected_qualification_rows - seen_qualification_rows)
    if missing_qualification_rows:
        issues.append(Issue("ERROR", str(path), f"missing qualification rows: {missing_qualification_rows}"))

    evidence_rows = table_data_rows(section_text(text, "## New Event Evidence"))
    if not has_non_placeholder_row(evidence_rows):
        issues.append(Issue("ERROR", str(path), "new event evidence table has no completed source rows"))
    refresh_source_ids: set[str] = set()
    later_refresh_source_ids: set[str] = set()
    for row in evidence_rows:
        cells = table_cells(row)
        if len(cells) < 6:
            issues.append(Issue("ERROR", str(path), f"malformed new event evidence row: {row}"))
            continue
        source_id, source_type, raw_source_date, claim, link_or_path, confidence = cells[:6]
        if source_id in PLACEHOLDERS:
            issues.append(Issue("ERROR", str(path), "new event evidence row missing source_id"))
            continue
        refresh_source_ids.add(source_id)
        source_date = parse_date(raw_source_date)
        if not source_date:
            issues.append(Issue("ERROR", str(path), f"new event evidence `{source_id}` has invalid source_date `{raw_source_date}`"))
        elif source_date <= cutoff:
            issues.append(Issue("ERROR", str(path), f"new event evidence `{source_id}` is not after cutoff {cutoff}"))
        else:
            later_refresh_source_ids.add(source_id)
        for column_name, value in (
            ("source_type", source_type),
            ("claim_supported", claim),
            ("link_or_path", link_or_path),
            ("confidence", confidence),
        ):
            if value in PLACEHOLDERS:
                issues.append(Issue("ERROR", str(path), f"new event evidence `{source_id}` missing {column_name}"))
    if evidence_rows and not later_refresh_source_ids:
        issues.append(Issue("ERROR", str(path), "new event evidence table has no source row after original cutoff"))

    before_after_rows = table_data_rows(section_text(text, "## Before / After"))
    if not has_non_placeholder_row(before_after_rows):
        issues.append(Issue("ERROR", str(path), "before/after table has no completed thesis-variable rows"))

    decision_section = section_text(text, "## Decision")
    selected_labels = selected_refresh_result_labels(decision_section)
    if not selected_labels:
        issues.append(Issue("ERROR", str(path), "decision section lacks an approved refresh result label"))
    elif len(selected_labels) != 1:
        issues.append(
            Issue(
                "ERROR",
                str(path),
                f"decision section must select exactly one approved refresh result label, got {sorted(selected_labels)}",
            )
        )

    if evidence_log:
        later_log_source_ids, log_issues = evidence_log_later_source_ids(evidence_log, cutoff)
        issues.extend(log_issues)
        if not later_log_source_ids:
            issues.append(Issue("ERROR", str(evidence_log), f"evidence log has no source_date after cutoff {cutoff}"))
        missing_from_log = sorted(later_refresh_source_ids - later_log_source_ids)
        if missing_from_log:
            issues.append(
                Issue(
                    "ERROR",
                    str(evidence_log),
                    f"refresh source_ids missing from evidence log later-event rows: {missing_from_log}",
                )
            )
    if intake:
        issues.extend(validate_intake(intake))
    downstream_updates_checked = 0
    if gate_tracker:
        issues.extend(validate_gate_tracker(gate_tracker, path))
        downstream_updates_checked += 1
    if public_readiness_audit:
        issues.extend(validate_public_readiness_audit(public_readiness_audit, case_id, path, selected_labels))
        downstream_updates_checked += 1
    if review_log:
        issues.extend(validate_methodology_review_log(review_log, case_id, path, selected_labels))
        downstream_updates_checked += 1
    return issues, downstream_updates_checked


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh", required=True, help="completed follow-through-refresh-YYYY-MM-DD.md")
    parser.add_argument("--original-cutoff", required=True, help="original memo cutoff date, YYYY-MM-DD")
    parser.add_argument("--evidence-log", help="updated evidence-log.csv")
    parser.add_argument("--intake", help="completed g04-follow-through-intake-checklist.csv")
    parser.add_argument("--gate-tracker", help="updated public-release-gate-tracker.csv")
    parser.add_argument("--public-readiness-audit", help="updated public-readiness-audit.md")
    parser.add_argument("--review-log", help="updated methodology review-log.csv")
    args = parser.parse_args()

    cutoff = parse_date(args.original_cutoff)
    if not cutoff:
        print(f"ERROR: --original-cutoff: invalid date `{args.original_cutoff}`")
        return 1

    issues, downstream_updates_checked = validate_refresh(
        Path(args.refresh),
        cutoff,
        Path(args.evidence_log) if args.evidence_log else None,
        Path(args.intake) if args.intake else None,
        Path(args.gate_tracker) if args.gate_tracker else None,
        Path(args.public_readiness_audit) if args.public_readiness_audit else None,
        Path(args.review_log) if args.review_log else None,
    )
    for issue in issues:
        print(issue.render())
    errors = [issue for issue in issues if issue.severity == "ERROR"]
    print("follow_through_refresh_validation:")
    print(f"  g04_clearable: {str(not errors).lower()}")
    print(f"  downstream_updates_checked: {downstream_updates_checked}")
    print(f"  errors: {len(errors)}")
    print(f"  warnings: {len([issue for issue in issues if issue.severity == 'WARN'])}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
