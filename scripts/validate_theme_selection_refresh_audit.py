#!/usr/bin/env python3
"""Validate recent-theme freshness and replacement controls."""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATION_DIR = Path("cases/long-term-workflow-validation-2026-05-30")
THEME_MATRIX = VALIDATION_DIR / "trial-theme-matrix.csv"
REFRESH_AUDIT = VALIDATION_DIR / "theme-selection-refresh-audit.csv"
DEFAULT_AS_OF = date(2026, 5, 30)

REQUIRED_COLUMNS = {
    "theme",
    "selection_date",
    "stale_after",
    "hotness_source_ids",
    "linked_case_ids",
    "refresh_frequency",
    "refresh_trigger",
    "drop_or_replace_if",
    "monitoring_source",
    "release_impact",
    "notes",
}

ALLOWED_RELEASE_IMPACTS = {"supports_internal_candidate", "blocks_external_release"}
PLACEHOLDERS = {"", "tbd", "todo", "replace", "n/a"}


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
    return rows, []


def parse_date(value: str) -> date | None:
    try:
        return date.fromisoformat(value.strip())
    except ValueError:
        return None


def split_multi(value: str) -> list[str]:
    return [item.strip() for item in value.replace(";", "|").split("|") if item.strip()]


def evidence_log_source_ids(path: Path) -> tuple[set[str], list[Issue]]:
    rows, issues = read_csv(path)
    if issues:
        return set(), issues
    if "source_id" not in (rows[0].keys() if rows else set()):
        return set(), [Issue("ERROR", str(path), "evidence log missing source_id column")]
    return {row.get("source_id", "").strip() for row in rows if row.get("source_id", "").strip()}, []


def theme_matrix_index() -> tuple[dict[str, dict[str, str]], dict[str, set[str]], list[Issue]]:
    rows, issues = read_csv(THEME_MATRIX)
    if issues:
        return {}, {}, issues
    matrix: dict[str, dict[str, str]] = {}
    source_ids_by_theme: dict[str, set[str]] = {}
    for row in rows:
        theme = row.get("theme", "").strip()
        if not theme:
            issues.append(Issue("ERROR", str(THEME_MATRIX), "blank theme in trial matrix"))
            continue
        matrix[theme] = row
        available_source_ids: set[str] = set()
        for evidence_path in split_multi(row.get("evidence_log_paths", "")):
            source_set, source_issues = evidence_log_source_ids(Path(evidence_path))
            available_source_ids.update(source_set)
            issues.extend(source_issues)
        source_ids_by_theme[theme] = available_source_ids
    return matrix, source_ids_by_theme, issues


def has_placeholder(value: str) -> bool:
    return value.strip().lower() in PLACEHOLDERS


def validate_refresh_audit(as_of: date) -> tuple[list[Issue], dict[str, int]]:
    issues: list[Issue] = []
    rows, row_issues = read_csv(REFRESH_AUDIT)
    issues.extend(row_issues)
    stats = {
        "themes": len(rows),
        "source_ids_checked": 0,
        "refresh_triggers_checked": 0,
        "replacement_rules_checked": 0,
    }
    if row_issues:
        return issues, stats

    header = set(rows[0].keys())
    missing_columns = sorted(REQUIRED_COLUMNS - header)
    if missing_columns:
        issues.append(Issue("ERROR", str(REFRESH_AUDIT), f"missing columns: {missing_columns}"))
        return issues, stats

    matrix, source_ids_by_theme, matrix_issues = theme_matrix_index()
    issues.extend(matrix_issues)
    matrix_themes = set(matrix)
    audit_themes = {row.get("theme", "").strip() for row in rows if row.get("theme", "").strip()}

    missing_audit_rows = sorted(matrix_themes - audit_themes)
    extra_audit_rows = sorted(audit_themes - matrix_themes)
    if missing_audit_rows:
        issues.append(Issue("ERROR", str(REFRESH_AUDIT), f"missing theme rows: {missing_audit_rows}"))
    if extra_audit_rows:
        issues.append(Issue("ERROR", str(REFRESH_AUDIT), f"unknown theme rows: {extra_audit_rows}"))

    seen: set[str] = set()
    for i, row in enumerate(rows, start=2):
        theme = row.get("theme", "").strip()
        if not theme:
            issues.append(Issue("ERROR", str(REFRESH_AUDIT), f"row {i} blank theme"))
            continue
        if theme in seen:
            issues.append(Issue("ERROR", str(REFRESH_AUDIT), f"row {i} duplicate theme `{theme}`"))
        seen.add(theme)

        for field in REQUIRED_COLUMNS:
            if has_placeholder(row.get(field, "")):
                issues.append(Issue("ERROR", str(REFRESH_AUDIT), f"row {i} `{theme}` has placeholder {field}"))

        matrix_row = matrix.get(theme)
        if not matrix_row:
            continue

        selection_date = parse_date(row.get("selection_date", ""))
        matrix_selection_date = parse_date(matrix_row.get("selection_date", ""))
        stale_after = parse_date(row.get("stale_after", ""))
        if selection_date is None:
            issues.append(Issue("ERROR", str(REFRESH_AUDIT), f"row {i} invalid selection_date"))
        elif matrix_selection_date != selection_date:
            issues.append(Issue("ERROR", str(REFRESH_AUDIT), f"row {i} selection_date does not match trial matrix"))
        elif selection_date > as_of:
            issues.append(Issue("ERROR", str(REFRESH_AUDIT), f"row {i} selection_date after as_of"))

        if stale_after is None:
            issues.append(Issue("ERROR", str(REFRESH_AUDIT), f"row {i} invalid stale_after"))
        elif selection_date and stale_after <= selection_date:
            issues.append(Issue("ERROR", str(REFRESH_AUDIT), f"row {i} stale_after must be after selection_date"))
        elif (stale_after - as_of).days > 45:
            issues.append(Issue("ERROR", str(REFRESH_AUDIT), f"row {i} stale_after is too far away for recent-theme monitoring"))

        audit_cases = set(split_multi(row.get("linked_case_ids", "")))
        matrix_cases = set(split_multi(matrix_row.get("linked_case_ids", "")))
        if not audit_cases:
            issues.append(Issue("ERROR", str(REFRESH_AUDIT), f"row {i} `{theme}` has no linked cases"))
        elif not audit_cases.issubset(matrix_cases):
            issues.append(Issue("ERROR", str(REFRESH_AUDIT), f"row {i} linked_case_ids not in trial matrix: {sorted(audit_cases - matrix_cases)}"))

        source_ids = split_multi(row.get("hotness_source_ids", ""))
        if len(source_ids) < 2:
            issues.append(Issue("ERROR", str(REFRESH_AUDIT), f"row {i} `{theme}` needs at least two hotness source ids"))
        available_source_ids = source_ids_by_theme.get(theme, set())
        for source_id in source_ids:
            stats["source_ids_checked"] += 1
            if source_id not in available_source_ids:
                issues.append(Issue("ERROR", str(REFRESH_AUDIT), f"row {i} hotness source_id not found in evidence logs: {source_id}"))

        if "material" not in row.get("refresh_trigger", "").lower() and "changes" not in row.get("refresh_trigger", "").lower():
            issues.append(Issue("ERROR", str(REFRESH_AUDIT), f"row {i} refresh_trigger must define observable change"))
        else:
            stats["refresh_triggers_checked"] += 1

        if "no longer" not in row.get("drop_or_replace_if", "").lower() and "weakens" not in row.get("drop_or_replace_if", "").lower():
            issues.append(Issue("ERROR", str(REFRESH_AUDIT), f"row {i} drop_or_replace_if must define a replacement condition"))
        else:
            stats["replacement_rules_checked"] += 1

        if row.get("release_impact", "").strip() not in ALLOWED_RELEASE_IMPACTS:
            issues.append(Issue("ERROR", str(REFRESH_AUDIT), f"row {i} invalid release_impact"))

    return issues, stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--as-of", default=DEFAULT_AS_OF.isoformat(), help="as-of date YYYY-MM-DD")
    args = parser.parse_args()
    as_of = parse_date(args.as_of)
    if as_of is None:
        print(f"ERROR: --as-of: invalid date `{args.as_of}`")
        return 1

    issues, stats = validate_refresh_audit(as_of)
    errors = [issue for issue in issues if issue.severity == "ERROR"]
    for issue in issues:
        print(issue.render())
    print("theme_selection_refresh_audit_validation:")
    print(f"  themes: {stats['themes']}")
    print(f"  source_ids_checked: {stats['source_ids_checked']}")
    print(f"  refresh_triggers_checked: {stats['refresh_triggers_checked']}")
    print(f"  replacement_rules_checked: {stats['replacement_rules_checked']}")
    print(f"  errors: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
