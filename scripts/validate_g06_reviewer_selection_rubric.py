#!/usr/bin/env python3
"""Validate the G06 reviewer selection rubric.

The rubric maps required external-release decisions to reviewer profiles and
scorecard dimensions. It keeps reviewer assignment from becoming an ad hoc
choice while still leaving G06 blocked until an independent reviewer returns.
"""

from __future__ import annotations

import csv
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUBRIC = Path("cases/long-term-workflow-validation-2026-05-30/g06-reviewer-selection-rubric.csv")
CANDIDATE_SCREEN = Path("cases/long-term-workflow-validation-2026-05-30/g06-reviewer-candidate-screen.csv")
SCORECARD = Path("cases/long-term-workflow-validation-2026-05-30/public-workflow-pack/external-reviewer-scorecard.csv")

REQUIRED_COLUMNS = {
    "rubric_id",
    "required_decision",
    "primary_reviewer_profile",
    "secondary_profile_allowed",
    "scorecard_dimension",
    "minimum_release_score",
    "required_return_artifact",
    "evidence_path",
    "assignment_gate",
    "release_impact",
    "notes",
}

REQUIRED_DECISIONS = {
    "g01_method_source_decision",
    "theme_selection_freshness",
    "practice_falsification",
    "methodology_iteration_traceability",
    "g04_follow_through_readiness",
    "g04_false_completion_control",
    "g05_source_decision",
    "historical_consensus_exception_decision",
    "live_case_action_label_reproducibility",
    "ordinary_vs_workflow_delta",
    "release_recommendation",
}

REQUIRED_PROFILES = {
    "integrated_methodology_reviewer",
    "live_case_reproducibility_reviewer",
    "source_quality_valuation_reviewer",
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
            rows = list(csv.DictReader(f))
    except Exception as exc:
        return [], [Issue("ERROR", str(path), f"could not parse CSV: {exc}")]
    if not rows:
        return [], [Issue("ERROR", str(path), "CSV has no rows")]
    return rows, []


def validate_rubric() -> tuple[list[Issue], dict[str, int | bool]]:
    issues: list[Issue] = []
    rows, row_issues = read_csv(RUBRIC)
    candidate_rows, candidate_issues = read_csv(CANDIDATE_SCREEN)
    scorecard_rows, scorecard_issues = read_csv(SCORECARD)
    issues.extend(row_issues + candidate_issues + scorecard_issues)
    stats: dict[str, int | bool] = {
        "rubric_rows": len(rows),
        "decisions_checked": 0,
        "profiles_checked": 0,
        "scorecard_dimensions_checked": 0,
        "evidence_paths_checked": 0,
        "clears_g06": False,
    }
    if row_issues or candidate_issues or scorecard_issues:
        return issues, stats

    missing_columns = sorted(REQUIRED_COLUMNS - set(rows[0].keys()))
    if missing_columns:
        issues.append(Issue("ERROR", str(RUBRIC), f"missing columns: {missing_columns}"))
        return issues, stats

    candidate_profiles = {row.get("candidate_profile", "").strip() for row in candidate_rows}
    missing_profiles = sorted(REQUIRED_PROFILES - candidate_profiles)
    if missing_profiles:
        issues.append(Issue("ERROR", str(CANDIDATE_SCREEN), f"candidate screen missing profiles: {missing_profiles}"))
    scorecard_dimensions = {row.get("dimension", "").strip() for row in scorecard_rows}

    decisions = {row.get("required_decision", "").strip() for row in rows}
    missing_decisions = sorted(REQUIRED_DECISIONS - decisions)
    extra_decisions = sorted(decisions - REQUIRED_DECISIONS)
    if missing_decisions:
        issues.append(Issue("ERROR", str(RUBRIC), f"missing required decisions: {missing_decisions}"))
    if extra_decisions:
        issues.append(Issue("ERROR", str(RUBRIC), f"unexpected decisions: {extra_decisions}"))

    primary_profiles_used: set[str] = set()
    for i, row in enumerate(rows, start=2):
        rubric_id = row.get("rubric_id", "").strip()
        decision = row.get("required_decision", "").strip()
        primary_profile = row.get("primary_reviewer_profile", "").strip()
        secondary_profile = row.get("secondary_profile_allowed", "").strip()
        scorecard_dimension = row.get("scorecard_dimension", "").strip()
        evidence_path = row.get("evidence_path", "").strip()
        assignment_gate = row.get("assignment_gate", "").strip()
        release_impact = row.get("release_impact", "").strip()
        return_artifact = row.get("required_return_artifact", "").strip()
        notes = row.get("notes", "").strip()

        if not rubric_id:
            issues.append(Issue("ERROR", str(RUBRIC), f"row {i} missing rubric_id"))
        if decision in REQUIRED_DECISIONS:
            stats["decisions_checked"] = int(stats["decisions_checked"]) + 1
        if primary_profile not in REQUIRED_PROFILES:
            issues.append(Issue("ERROR", str(RUBRIC), f"row {i} invalid primary_reviewer_profile `{primary_profile}`"))
        else:
            primary_profiles_used.add(primary_profile)
            stats["profiles_checked"] = int(stats["profiles_checked"]) + 1
        if secondary_profile not in REQUIRED_PROFILES:
            issues.append(Issue("ERROR", str(RUBRIC), f"row {i} invalid secondary_profile_allowed `{secondary_profile}`"))
        if scorecard_dimension not in scorecard_dimensions:
            issues.append(Issue("ERROR", str(RUBRIC), f"row {i} scorecard_dimension missing from scorecard: {scorecard_dimension}"))
        else:
            stats["scorecard_dimensions_checked"] = int(stats["scorecard_dimensions_checked"]) + 1
        try:
            minimum_score = int(row.get("minimum_release_score", "").strip())
        except ValueError:
            issues.append(Issue("ERROR", str(RUBRIC), f"row {i} invalid minimum_release_score"))
        else:
            if minimum_score < 4:
                issues.append(Issue("ERROR", str(RUBRIC), f"row {i} minimum_release_score must be at least 4"))
        if return_artifact != "completed_scorecard_and_results_memo":
            issues.append(Issue("ERROR", str(RUBRIC), f"row {i} return artifact must require completed scorecard and results memo"))
        if evidence_path and not (ROOT / evidence_path).exists():
            issues.append(Issue("ERROR", str(RUBRIC), f"row {i} evidence_path missing: {evidence_path}"))
        else:
            stats["evidence_paths_checked"] = int(stats["evidence_paths_checked"]) + 1
        if assignment_gate != "must_cover_before_assignment":
            issues.append(Issue("ERROR", str(RUBRIC), f"row {i} assignment_gate must be must_cover_before_assignment"))
        if release_impact != "blocks_external_release":
            issues.append(Issue("ERROR", str(RUBRIC), f"row {i} release_impact must block external release"))
        for marker in ("Reviewer", "must"):
            if marker not in notes:
                issues.append(Issue("ERROR", str(RUBRIC), f"row {i} notes missing `{marker}`"))

    missing_primary_profile_use = sorted(REQUIRED_PROFILES - primary_profiles_used)
    if missing_primary_profile_use:
        issues.append(Issue("ERROR", str(RUBRIC), f"required profiles not used as primary: {missing_primary_profile_use}"))
    stats["clears_g06"] = False
    return issues, stats


def main() -> int:
    issues, stats = validate_rubric()
    errors = [issue for issue in issues if issue.severity == "ERROR"]
    for issue in issues:
        print(issue.render())
    print("g06_reviewer_selection_rubric_validation:")
    print(f"  rubric_rows: {int(stats['rubric_rows'])}")
    print(f"  decisions_checked: {int(stats['decisions_checked'])}")
    print(f"  profiles_checked: {int(stats['profiles_checked'])}")
    print(f"  scorecard_dimensions_checked: {int(stats['scorecard_dimensions_checked'])}")
    print(f"  evidence_paths_checked: {int(stats['evidence_paths_checked'])}")
    print(f"  clears_g06: {str(bool(stats['clears_g06'])).lower()}")
    print(f"  errors: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
