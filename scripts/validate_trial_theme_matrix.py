#!/usr/bin/env python3
"""Validate recent-theme selection evidence for the long-term workflow trials."""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
THEME_MATRIX = Path("cases/long-term-workflow-validation-2026-05-30/trial-theme-matrix.csv")
CROSS_CASE_MATRIX = Path("cases/long-term-workflow-validation-2026-05-30/cross-case-validation-matrix.csv")
DEFAULT_AS_OF = date(2026, 5, 30)

REQUIRED_COLUMNS = {
    "theme",
    "selection_date",
    "market_scope",
    "hotness_basis",
    "public_expressions",
    "main_lenses_to_stress",
    "expected_weak_lens",
    "why_good_test",
    "initial_source_quality",
    "next_step",
    "linked_case_ids",
    "evidence_log_paths",
    "source_ids",
}

REQUIRED_THEMES = {
    "ai_power_and_data_center_infrastructure",
    "enterprise_ai_agents_and_software_monetization",
    "glp1_metabolic_health_and_consumer_readthrough",
    "humanoid_robotics_and_physical_ai",
    "nuclear_smr_and_ai_power_contracts",
    "stablecoin_payments_and_tokenized_cash",
    "defense_autonomy_drones_and_counter_uas",
}

REQUIRED_LENS_MARKERS = {
    "consumer_demand",
    "product_reality",
    "industry_structure",
    "company_execution",
    "valuation_expectations",
}


@dataclass
class Issue:
    severity: str
    subject: str
    message: str

    def render(self) -> str:
        return f"{self.severity}: {self.subject}: {self.message}"


def read_csv(path: Path) -> tuple[list[dict[str, str]], list[Issue]]:
    try:
        with path.open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    except Exception as exc:
        return [], [Issue("ERROR", str(path), f"could not parse CSV: {exc}")]
    if not rows:
        return [], [Issue("ERROR", str(path), "CSV has no rows")]
    return rows, []


def parse_date(value: str) -> date | None:
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def split_multi(value: str) -> list[str]:
    return [item.strip() for item in value.replace(";", "|").split("|") if item.strip()]


def case_ids_by_theme() -> tuple[set[str], dict[str, str], list[Issue]]:
    rows, issues = read_csv(ROOT / CROSS_CASE_MATRIX)
    if issues:
        return set(), {}, issues
    case_ids = {row.get("case_id", "").strip() for row in rows if row.get("case_id", "").strip()}
    decisions = {
        row.get("case_id", "").strip(): row.get("workflow_decision", "").strip()
        for row in rows
        if row.get("case_id", "").strip()
    }
    return case_ids, decisions, []


def evidence_log_source_ids(path: Path) -> tuple[set[str], list[Issue]]:
    rows, issues = read_csv(path)
    if issues:
        return set(), issues
    if "source_id" not in (rows[0].keys() if rows else set()):
        return set(), [Issue("ERROR", str(path), "evidence log missing source_id column")]
    return {row.get("source_id", "").strip() for row in rows if row.get("source_id", "").strip()}, []


def validate_theme_matrix(as_of: date) -> tuple[list[Issue], dict[str, int]]:
    issues: list[Issue] = []
    rows, row_issues = read_csv(ROOT / THEME_MATRIX)
    issues.extend(row_issues)
    stats = {
        "themes": len(rows),
        "linked_cases": 0,
        "source_ids_checked": 0,
    }
    if row_issues:
        return issues, stats

    header = set(rows[0].keys())
    missing_columns = sorted(REQUIRED_COLUMNS - header)
    if missing_columns:
        issues.append(Issue("ERROR", str(THEME_MATRIX), f"missing columns: {missing_columns}"))
        return issues, stats

    seen_themes = {row.get("theme", "").strip() for row in rows}
    missing_themes = sorted(REQUIRED_THEMES - seen_themes)
    if missing_themes:
        issues.append(Issue("ERROR", str(THEME_MATRIX), f"missing required themes: {missing_themes}"))
    if len(rows) < len(REQUIRED_THEMES):
        issues.append(Issue("ERROR", str(THEME_MATRIX), "too few recent hot themes"))

    known_cases, case_decisions, case_issues = case_ids_by_theme()
    issues.extend(case_issues)
    covered_lenses: set[str] = set()
    industry_map_first_cases = 0
    linked_cases_seen: set[str] = set()

    for i, row in enumerate(rows, start=2):
        theme = row.get("theme", "").strip()
        for field in REQUIRED_COLUMNS:
            if not row.get(field, "").strip():
                issues.append(Issue("ERROR", str(THEME_MATRIX), f"row {i} `{theme}` missing {field}"))

        selected = parse_date(row.get("selection_date", "").strip())
        if selected is None:
            issues.append(Issue("ERROR", str(THEME_MATRIX), f"row {i} invalid selection_date"))
        elif selected > as_of:
            issues.append(Issue("ERROR", str(THEME_MATRIX), f"row {i} selection_date after as_of"))
        elif (as_of - selected).days > 180:
            issues.append(Issue("ERROR", str(THEME_MATRIX), f"row {i} selection_date is stale for recent-theme claim"))

        expressions = split_multi(row.get("public_expressions", ""))
        if len(expressions) < 3:
            issues.append(Issue("ERROR", str(THEME_MATRIX), f"row {i} `{theme}` needs at least three public expressions"))

        lenses = set(split_multi(row.get("main_lenses_to_stress", "")))
        covered_lenses.update(lenses)

        linked_case_ids = split_multi(row.get("linked_case_ids", ""))
        if not linked_case_ids:
            issues.append(Issue("ERROR", str(THEME_MATRIX), f"row {i} `{theme}` has no linked cases"))
        for case_id in linked_case_ids:
            if case_id not in known_cases:
                issues.append(Issue("ERROR", str(THEME_MATRIX), f"row {i} unknown linked case `{case_id}`"))
            else:
                linked_cases_seen.add(case_id)
                if "industry_map_first" in case_decisions.get(case_id, ""):
                    industry_map_first_cases += 1

        evidence_log_paths = split_multi(row.get("evidence_log_paths", ""))
        source_ids = split_multi(row.get("source_ids", ""))
        available_source_ids: set[str] = set()
        for evidence_path in evidence_log_paths:
            source_set, source_issues = evidence_log_source_ids(ROOT / evidence_path)
            available_source_ids.update(source_set)
            issues.extend(source_issues)
        for source_id in source_ids:
            stats["source_ids_checked"] += 1
            if source_id not in available_source_ids:
                issues.append(Issue("ERROR", str(THEME_MATRIX), f"row {i} source_id not found in evidence logs: {source_id}"))

    missing_lenses = sorted(REQUIRED_LENS_MARKERS - covered_lenses)
    if missing_lenses:
        issues.append(Issue("ERROR", str(THEME_MATRIX), f"missing required lens coverage: {missing_lenses}"))
    if industry_map_first_cases < 3:
        issues.append(Issue("ERROR", str(THEME_MATRIX), "needs at least three industry_map_first theme-screen cases"))

    stats["linked_cases"] = len(linked_cases_seen)
    return issues, stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--as-of", default=DEFAULT_AS_OF.isoformat(), help="as-of date YYYY-MM-DD")
    args = parser.parse_args()
    as_of = parse_date(args.as_of)
    if as_of is None:
        print(f"ERROR: --as-of: invalid date `{args.as_of}`")
        return 1

    issues, stats = validate_theme_matrix(as_of)
    errors = [issue for issue in issues if issue.severity == "ERROR"]
    for issue in issues:
        print(issue.render())
    print("trial_theme_matrix_validation:")
    print(f"  themes: {stats['themes']}")
    print(f"  linked_cases: {stats['linked_cases']}")
    print(f"  source_ids_checked: {stats['source_ids_checked']}")
    print(f"  errors: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
