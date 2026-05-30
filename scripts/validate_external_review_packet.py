#!/usr/bin/env python3
"""Validate the blank G06 external reviewer packet before assignment.

This checks packet completeness and consistency with
validate_external_review_return.py. It does not validate a completed reviewer
return and does not clear G06.
"""

from __future__ import annotations

import csv
import sys
from dataclasses import dataclass
from pathlib import Path

import validate_external_review_return as return_validator


ROOT = Path(__file__).resolve().parents[1]
VALIDATION_DIR = Path("cases/long-term-workflow-validation-2026-05-30")
PUBLIC_PACK = VALIDATION_DIR / "public-workflow-pack"

SCORECARD = PUBLIC_PACK / "external-reviewer-scorecard.csv"
RESULTS_TEMPLATE = PUBLIC_PACK / "external-review-results-template.md"
INTAKE = PUBLIC_PACK / "external-review-intake-checklist.csv"
BUNDLE_MANIFEST = VALIDATION_DIR / "external-reviewer-bundle-manifest.csv"
G06_HANDOFF = VALIDATION_DIR / "g06-external-review-handoff-2026-05-30.md"
G06_STANDARD = VALIDATION_DIR / "g06-external-review-return-validation-standard.md"
REVIEWER_BRIEF = PUBLIC_PACK / "external-reviewer-brief.md"
REVIEW_REQUEST = PUBLIC_PACK / "external-review-request.md"
G06_SELECTION_RUBRIC = VALIDATION_DIR / "g06-reviewer-selection-rubric.csv"

REQUIRED_MANIFEST_PATHS = {
    "public-workflow-pack/external-reviewer-scorecard.csv",
    "public-workflow-pack/external-review-results-template.md",
    "public-workflow-pack/external-review-intake-checklist.csv",
    "g01-external-method-source-audit.csv",
    "g01-external-method-source-upgrade-2026-05-30.md",
    "trial-theme-matrix.csv",
    "theme-selection-refresh-audit.csv",
    "g06-reviewer-selection-rubric.csv",
    "practice-falsification-audit.csv",
    "methodology-iteration-trace-audit.csv",
    "multi-lens-coverage-audit.csv",
    "../../scripts/validate_recent_theme_selection.py",
    "follow-through-trigger-tracker.csv",
    "g04-follow-through-event-watch-calendar.csv",
    "g04-later-event-candidate-screen.csv",
    "../../scripts/validate_g04_later_event_candidate_screen.py",
    "g04-follow-through-execution-tracker.csv",
    "g04-follow-through-handoff-2026-05-30.md",
    "historical-consensus-source-attempts.csv",
    "historical-consensus-unavailable-data-exception-2026-05-30.md",
    "../tdoc-2020-2022-failure-backtest/",
    "../pton-2020-2022-failure-backtest/",
}

REQUIRED_INTAKE_REQUIREMENTS = {
    "independence_confirmed",
    "scorecard_completed",
    "no_p0_findings",
    "p1_fix_plan",
    "g01_method_source_decision",
    "theme_selection_freshness",
    "practice_falsification",
    "methodology_iteration_traceability",
    "g04_follow_through_results",
    "g05_source_decision",
    "historical_consensus_exception_decision",
    "action_label_reproducibility",
    "release_recommendation",
    "results_memo_complete",
}

REQUIRED_TEMPLATE_MARKERS = {
    "g05_source_decision:",
    "g01_method_source_decision:",
    "g04_follow_through_readiness:",
    "g04_false_completion_control:",
    "theme_selection_freshness:",
    "practice_falsification:",
    "methodology_iteration_traceability:",
    "historical_consensus_exception_decision:",
    "accept_basis",
    "accepted_with_caveats",
    "accept_exception",
    "accept_with_caveats",
    "require_private_material",
    "reject_basis",
    "require_export",
    "reject_exception",
    "release_recommendation:",
    "must_refresh_if:",
}

REQUIRED_TEXT_MARKERS = {
    "historical_consensus_exception_decision",
    "g01_method_source_decision",
    "accept_basis",
    "require_private_material",
    "accept_exception",
    "accept_with_caveats",
    "require_export",
    "reject_exception",
    "g04_follow_through_readiness",
    "g04_false_completion_control",
    "theme_selection_freshness",
    "practice_falsification",
    "methodology_iteration_traceability",
    "validate_recent_theme_selection.py",
    "theme-selection-refresh-audit.csv",
    "practice-falsification-audit.csv",
    "methodology-iteration-trace-audit.csv",
    "multi-lens-coverage-audit.csv",
    "g04-later-event-candidate-screen.csv",
    "g06-reviewer-selection-rubric.csv",
    "validate_g04_later_event_candidate_screen.py",
    "refresh_allowed: yes",
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
        with (ROOT / path).open(newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f)), []
    except Exception as exc:
        return [], [Issue("ERROR", str(path), f"could not parse CSV: {exc}")]


def read_text(path: Path) -> tuple[str, list[Issue]]:
    try:
        return (ROOT / path).read_text(encoding="utf-8"), []
    except Exception as exc:
        return "", [Issue("ERROR", str(path), f"could not read file: {exc}")]


def validate_scorecard() -> list[Issue]:
    issues: list[Issue] = []
    rows, csv_issues = read_csv(SCORECARD)
    issues.extend(csv_issues)
    if not rows:
        issues.append(Issue("ERROR", str(SCORECARD), "scorecard template has no rows"))
        return issues

    header = set(rows[0].keys())
    missing_columns = sorted(return_validator.REQUIRED_SCORECARD_COLUMNS - header)
    if missing_columns:
        issues.append(Issue("ERROR", str(SCORECARD), f"missing columns: {missing_columns}"))

    dimensions = {row.get("dimension", "").strip() for row in rows}
    missing_dimensions = sorted(return_validator.REQUIRED_DIMENSIONS - dimensions)
    if missing_dimensions:
        issues.append(Issue("ERROR", str(SCORECARD), f"missing dimensions: {missing_dimensions}"))

    extra_dimensions = sorted(dim for dim in dimensions if not dim)
    if extra_dimensions:
        issues.append(Issue("ERROR", str(SCORECARD), "blank dimension rows present"))
    return issues


def validate_results_template() -> list[Issue]:
    text, issues = read_text(RESULTS_TEMPLATE)
    for marker in REQUIRED_TEMPLATE_MARKERS:
        if marker not in text:
            issues.append(Issue("ERROR", str(RESULTS_TEMPLATE), f"missing marker `{marker}`"))
    return issues


def validate_intake() -> list[Issue]:
    issues: list[Issue] = []
    rows, csv_issues = read_csv(INTAKE)
    issues.extend(csv_issues)
    if not rows:
        issues.append(Issue("ERROR", str(INTAKE), "intake checklist has no rows"))
        return issues
    requirements = {row.get("requirement", "").strip() for row in rows}
    missing = sorted(REQUIRED_INTAKE_REQUIREMENTS - requirements)
    if missing:
        issues.append(Issue("ERROR", str(INTAKE), f"missing requirements: {missing}"))
    return issues


def validate_manifest() -> list[Issue]:
    issues: list[Issue] = []
    rows, csv_issues = read_csv(BUNDLE_MANIFEST)
    issues.extend(csv_issues)
    if not rows:
        issues.append(Issue("ERROR", str(BUNDLE_MANIFEST), "bundle manifest has no rows"))
        return issues
    send_paths = {
        row.get("path", "").strip()
        for row in rows
        if row.get("send_to_reviewer", "").strip() == "yes"
    }
    missing = sorted(REQUIRED_MANIFEST_PATHS - send_paths)
    if missing:
        issues.append(Issue("ERROR", str(BUNDLE_MANIFEST), f"missing send paths: {missing}"))
    for path in send_paths:
        candidate = ROOT / VALIDATION_DIR / path
        if not candidate.exists():
            issues.append(Issue("ERROR", str(BUNDLE_MANIFEST), f"send path does not exist: {path}"))
    return issues


def validate_selection_rubric() -> list[Issue]:
    issues: list[Issue] = []
    rows, csv_issues = read_csv(G06_SELECTION_RUBRIC)
    issues.extend(csv_issues)
    if not rows:
        issues.append(Issue("ERROR", str(G06_SELECTION_RUBRIC), "selection rubric has no rows"))
        return issues
    decisions = {row.get("required_decision", "").strip() for row in rows}
    for marker in (
        "g01_method_source_decision",
        "theme_selection_freshness",
        "practice_falsification",
        "methodology_iteration_traceability",
        "g04_follow_through_readiness",
        "g04_false_completion_control",
        "g05_source_decision",
        "historical_consensus_exception_decision",
        "release_recommendation",
    ):
        if marker not in decisions:
            issues.append(Issue("ERROR", str(G06_SELECTION_RUBRIC), f"selection rubric missing `{marker}`"))
    return issues


def validate_text_markers() -> list[Issue]:
    issues: list[Issue] = []
    for path in (G06_HANDOFF, G06_STANDARD, REVIEWER_BRIEF, REVIEW_REQUEST):
        text, read_issues = read_text(path)
        issues.extend(read_issues)
        for marker in REQUIRED_TEXT_MARKERS:
            if marker not in text:
                issues.append(Issue("ERROR", str(path), f"missing marker `{marker}`"))
    return issues


def main() -> int:
    issues: list[Issue] = []
    issues.extend(validate_scorecard())
    issues.extend(validate_results_template())
    issues.extend(validate_intake())
    issues.extend(validate_manifest())
    issues.extend(validate_selection_rubric())
    issues.extend(validate_text_markers())

    errors = [issue for issue in issues if issue.severity == "ERROR"]
    for issue in issues:
        print(issue.render())
    print("external_review_packet_validation:")
    print(f"  packet_assignable: {str(not errors).lower()}")
    print(f"  required_dimensions: {len(return_validator.REQUIRED_DIMENSIONS)}")
    print(f"  errors: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
