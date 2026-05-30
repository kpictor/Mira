#!/usr/bin/env python3
"""Validate a returned G06 external reviewer package.

This script is for the future reviewer return, not for the blank template.
It intentionally fails when reviewer fields still contain placeholders.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
G06_SELECTION_RUBRIC = ROOT / "cases/long-term-workflow-validation-2026-05-30/g06-reviewer-selection-rubric.csv"

REQUIRED_SCORECARD_COLUMNS = {
    "review_id",
    "reviewer",
    "review_date",
    "case_or_task",
    "dimension",
    "score_1_to_5",
    "minimum_release_score",
    "finding_severity",
    "evidence",
    "required_fix",
    "release_impact",
}

REQUIRED_DIMENSIONS = {
    "source_quality",
    "lens_routing",
    "action_label_reproducibility",
    "valuation_discipline",
    "refresh_conditions",
    "g04_follow_through_readiness",
    "g04_false_completion_control",
    "theme_selection_freshness",
    "practice_falsification",
    "methodology_iteration_traceability",
    "theme_to_company_handoff",
    "downgrade_timing",
    "workflow_cost_efficiency",
    "reviewer_release_recommendation",
    "g01_method_source_sufficiency",
    "g01_private_buyside_gap_control",
    "g01_method_source_decision",
    "g05_source_sufficiency",
    "g05_false_precision_control",
    "g05_source_decision",
    "historical_consensus_exception_sufficiency",
    "historical_consensus_false_precision_control",
    "historical_consensus_exception_decision",
}

ALLOWED_RELEASE_RECOMMENDATIONS = {
    "release_external",
    "release_with_caveats",
    "release_internal_only",
    "reject",
}
ALLOWED_FINDING_SEVERITIES = {"P0", "P1", "P2", "P3", "none"}

G06_CLEAR_RELEASE_RECOMMENDATIONS = {"release_external", "release_with_caveats"}
G06_CLEAR_G01_DECISIONS = {"accept_basis", "accept_with_caveats"}
G06_CLEAR_G05_DECISIONS = {"accept_source", "accept_with_caveats"}
G06_CLEAR_HISTORICAL_CONSENSUS_DECISIONS = {"accept_exception", "accept_with_caveats"}
G06_CLEAR_G04_RESULTS = {"pass", "accepted_with_caveats"}
G06_CLEAR_THEME_SELECTION_RESULTS = {"pass", "accepted_with_caveats"}
G06_CLEAR_PRACTICE_RESULTS = {"pass", "accepted_with_caveats"}
G06_CLEAR_METHOD_ITERATION_RESULTS = {"pass", "accepted_with_caveats"}
PLACEHOLDERS = {"", "replace", "YYYY-MM-DD", "0"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
G06_RETURN_ASSIGNMENT_STATUSES = {"returned_not_validated", "validated_completed"}
G06_RETURN_REVIEWER_STATUSES = {"returned", "validated"}

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

REQUIRED_FINDINGS_COLUMNS = {
    "severity",
    "case_or_task",
    "finding",
    "evidence",
    "required_fix",
    "release_impact",
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
            return list(csv.DictReader(f)), []
    except Exception as exc:
        return [], [Issue("ERROR", str(path), f"could not parse CSV: {exc}")]


def scalar_from_results(text: str, key: str) -> str:
    pattern = re.compile(rf"^[ \t]*-[ \t]*{re.escape(key)}:[ \t]*(.*)[ \t]*$", re.MULTILINE)
    match = pattern.search(text)
    if not match:
        return ""
    return match.group(1).strip().strip("`")


def scalar_int_from_results(text: str, key: str) -> int | None:
    value = scalar_from_results(text, key)
    try:
        return int(value)
    except ValueError:
        return None


def scalar_float_from_results(text: str, key: str) -> float | None:
    value = scalar_from_results(text, key)
    try:
        return float(value)
    except ValueError:
        return None


def split_markdown_table_row(line: str) -> list[str]:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return []
    return [cell.strip().strip("`") for cell in stripped.strip("|").split("|")]


def is_markdown_separator_row(cells: list[str]) -> bool:
    return bool(cells) and all(cell and set(cell) <= {"-", ":"} for cell in cells)


def parse_findings_table(text: str, path: Path) -> tuple[list[dict[str, str]], list[Issue]]:
    issues: list[Issue] = []
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip().lower() == "## findings":
            start = i + 1
            break
    if start is None:
        return [], [Issue("ERROR", str(path), "missing ## Findings section")]

    header: list[str] = []
    table_rows: list[dict[str, str]] = []
    for i in range(start, len(lines)):
        stripped = lines[i].strip()
        if stripped.startswith("## "):
            break
        cells = split_markdown_table_row(stripped)
        if not cells:
            continue
        normalized = [cell.lower() for cell in cells]
        if "severity" not in normalized or "required_fix" not in normalized:
            continue
        header = normalized
        missing = sorted(REQUIRED_FINDINGS_COLUMNS - set(header))
        if missing:
            issues.append(Issue("ERROR", str(path), f"findings table missing columns: {missing}"))
            return [], issues
        for row_line in lines[i + 1 :]:
            row_stripped = row_line.strip()
            if row_stripped.startswith("## "):
                break
            row_cells = split_markdown_table_row(row_stripped)
            if not row_cells:
                continue
            if is_markdown_separator_row(row_cells):
                continue
            if len(row_cells) != len(header):
                issues.append(Issue("ERROR", str(path), "findings table row width does not match header"))
                continue
            table_rows.append(dict(zip(header, row_cells)))
        break

    if not header:
        issues.append(Issue("ERROR", str(path), "findings table missing"))
    if not table_rows:
        issues.append(Issue("ERROR", str(path), "findings table has no rows"))
    return table_rows, issues


def validate_scorecard(path: Path) -> tuple[list[Issue], dict[str, float | int | str]]:
    issues: list[Issue] = []
    rows, csv_issues = read_csv(path)
    issues.extend(csv_issues)
    stats: dict[str, float | int | str] = {
        "average_score": 0.0,
        "minimum_score": 0,
        "p0_findings_count": 0,
        "p1_findings_count": 0,
        "reviewer": "",
        "review_date": "",
        "g01_method_source_decision": "",
        "g04_follow_through_readiness": "",
        "g04_false_completion_control": "",
        "g04_follow_through_readiness_score": 0,
        "g04_false_completion_control_score": 0,
        "theme_selection_freshness": "",
        "theme_selection_freshness_score": 0,
        "practice_falsification": "",
        "practice_falsification_score": 0,
        "methodology_iteration_traceability": "",
        "methodology_iteration_traceability_score": 0,
        "g05_source_decision": "",
        "historical_consensus_exception_decision": "",
        "release_recommendation": "",
    }
    if not rows:
        issues.append(Issue("ERROR", str(path), "scorecard has no rows"))
        return issues, stats

    header = set(rows[0].keys())
    missing = sorted(REQUIRED_SCORECARD_COLUMNS - header)
    if missing:
        issues.append(Issue("ERROR", str(path), f"missing columns: {missing}"))
        return issues, stats

    dimensions = {row.get("dimension", "").strip() for row in rows}
    missing_dimensions = sorted(REQUIRED_DIMENSIONS - dimensions)
    if missing_dimensions:
        issues.append(Issue("ERROR", str(path), f"missing dimensions: {missing_dimensions}"))

    reviewers: set[str] = set()
    review_dates: set[str] = set()
    scores: list[int] = []
    for i, row in enumerate(rows, start=2):
        reviewer = row.get("reviewer", "").strip()
        review_date = row.get("review_date", "").strip()
        dimension = row.get("dimension", "").strip()
        severity = row.get("finding_severity", "").strip()
        evidence = row.get("evidence", "").strip()
        required_fix = row.get("required_fix", "").strip()
        release_impact = row.get("release_impact", "").strip()

        if reviewer in PLACEHOLDERS:
            issues.append(Issue("ERROR", str(path), f"row {i} reviewer is placeholder"))
        else:
            reviewers.add(reviewer)
        if not DATE_RE.match(review_date):
            issues.append(Issue("ERROR", str(path), f"row {i} invalid review_date `{review_date}`"))
        else:
            review_dates.add(review_date)
        try:
            score = int(row.get("score_1_to_5", "").strip())
            min_score = int(row.get("minimum_release_score", "").strip())
        except ValueError:
            issues.append(Issue("ERROR", str(path), f"row {i} score fields must be integers"))
            continue
        scores.append(score)
        if score < 1 or score > 5:
            issues.append(Issue("ERROR", str(path), f"row {i} score out of range: {score}"))
        if score < min_score:
            issues.append(Issue("ERROR", str(path), f"row {i} score {score} below release minimum {min_score}"))
        if severity in {"replace", ""}:
            issues.append(Issue("ERROR", str(path), f"row {i} finding_severity is placeholder"))
        elif severity not in ALLOWED_FINDING_SEVERITIES:
            issues.append(Issue("ERROR", str(path), f"row {i} invalid finding_severity `{severity}`"))
        if release_impact not in {"blocker", "caveat", "none"}:
            issues.append(Issue("ERROR", str(path), f"row {i} invalid release_impact `{release_impact}`"))
        if evidence in {"replace", ""}:
            issues.append(Issue("ERROR", str(path), f"row {i} evidence is placeholder"))
        if severity in {"P0", "P1"} and required_fix in {"replace", ""}:
            issues.append(Issue("ERROR", str(path), f"row {i} P0/P1 finding lacks required_fix"))
        if severity == "P1":
            required_fix_lower = required_fix.lower()
            if "owner:" not in required_fix_lower:
                issues.append(Issue("ERROR", str(path), f"row {i} P1 finding required_fix missing owner:"))
            if "fix:" not in required_fix_lower:
                issues.append(Issue("ERROR", str(path), f"row {i} P1 finding required_fix missing fix:"))
        if severity == "P0" and release_impact != "blocker":
            issues.append(Issue("ERROR", str(path), f"row {i} P0 finding must have release_impact blocker"))
        if severity == "P1" and release_impact not in {"blocker", "caveat"}:
            issues.append(Issue("ERROR", str(path), f"row {i} P1 finding must have blocker or caveat impact"))
        if severity == "none" and release_impact != "none":
            issues.append(Issue("ERROR", str(path), f"row {i} severity none must have release_impact none"))
        if severity == "P0":
            stats["p0_findings_count"] = int(stats["p0_findings_count"]) + 1
        if severity == "P1":
            stats["p1_findings_count"] = int(stats["p1_findings_count"]) + 1
        if dimension == "g01_method_source_decision":
            allowed = G06_CLEAR_G01_DECISIONS | {"require_private_material", "reject_basis"}
            decision = evidence if evidence in allowed else required_fix
            stats["g01_method_source_decision"] = str(decision).strip()
        if dimension == "g04_follow_through_readiness":
            stats["g04_follow_through_readiness_score"] = score
        if dimension == "g04_false_completion_control":
            stats["g04_false_completion_control_score"] = score
        if dimension == "theme_selection_freshness":
            stats["theme_selection_freshness_score"] = score
        if dimension == "practice_falsification":
            stats["practice_falsification_score"] = score
        if dimension == "methodology_iteration_traceability":
            stats["methodology_iteration_traceability_score"] = score
        if dimension == "g05_source_decision":
            decision = evidence if evidence in G06_CLEAR_G05_DECISIONS | {"reject_source"} else required_fix
            stats["g05_source_decision"] = str(decision).strip()
        if dimension == "historical_consensus_exception_decision":
            allowed = G06_CLEAR_HISTORICAL_CONSENSUS_DECISIONS | {"require_export", "reject_exception"}
            decision = evidence if evidence in allowed else required_fix
            stats["historical_consensus_exception_decision"] = str(decision).strip()
        if dimension == "reviewer_release_recommendation":
            recommendation = evidence if evidence in ALLOWED_RELEASE_RECOMMENDATIONS else required_fix
            stats["release_recommendation"] = str(recommendation).strip()

    if scores:
        stats["average_score"] = sum(scores) / len(scores)
        stats["minimum_score"] = min(scores)
        if stats["average_score"] < 4:
            issues.append(Issue("ERROR", str(path), f"average score below 4: {stats['average_score']:.2f}"))
        if stats["minimum_score"] < 4:
            issues.append(Issue("ERROR", str(path), f"minimum score below 4: {stats['minimum_score']}"))
    if len(reviewers) != 1:
        issues.append(Issue("ERROR", str(path), f"scorecard must have exactly one reviewer, got {sorted(reviewers)}"))
    else:
        stats["reviewer"] = next(iter(reviewers))
    if len(review_dates) != 1:
        issues.append(Issue("ERROR", str(path), f"scorecard must have exactly one review_date, got {sorted(review_dates)}"))
    else:
        stats["review_date"] = next(iter(review_dates))
    return issues, stats


def validate_results(path: Path, scorecard_stats: dict[str, float | int | str]) -> list[Issue]:
    issues: list[Issue] = []
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as exc:
        return [Issue("ERROR", str(path), f"could not read results memo: {exc}")]

    required_markers = [
        "reviewer_independence_confirmed: true",
        "p0_findings_count:",
        "p1_findings_count:",
        "g01_method_source_decision:",
        "g04_follow_through_readiness:",
        "g04_false_completion_control:",
        "theme_selection_freshness:",
        "practice_falsification:",
        "methodology_iteration_traceability:",
        "g05_source_decision:",
        "historical_consensus_exception_decision:",
        "release_recommendation:",
        "must_refresh_if:",
    ]
    for marker in required_markers:
        if marker not in text:
            issues.append(Issue("ERROR", str(path), f"missing `{marker}`"))

    findings_rows, findings_issues = parse_findings_table(text, path)
    issues.extend(findings_issues)
    findings_p0_count = 0
    findings_p1_count = 0
    for i, row in enumerate(findings_rows, start=1):
        severity = row.get("severity", "").strip()
        required_fix = row.get("required_fix", "").strip()
        release_impact = row.get("release_impact", "").strip()
        evidence = row.get("evidence", "").strip()
        finding = row.get("finding", "").strip()

        if severity in {"replace", ""}:
            issues.append(Issue("ERROR", str(path), f"findings row {i} finding_severity is placeholder"))
            continue
        if severity not in ALLOWED_FINDING_SEVERITIES:
            issues.append(Issue("ERROR", str(path), f"findings row {i} invalid finding_severity `{severity}`"))
            continue
        if release_impact not in {"blocker", "caveat", "none"}:
            issues.append(Issue("ERROR", str(path), f"findings row {i} invalid release_impact `{release_impact}`"))
        if severity != "none" and evidence in {"replace", ""}:
            issues.append(Issue("ERROR", str(path), f"findings row {i} evidence is placeholder"))
        if severity != "none" and finding in {"replace", ""}:
            issues.append(Issue("ERROR", str(path), f"findings row {i} finding is placeholder"))
        if severity in {"P0", "P1"} and required_fix in {"replace", ""}:
            issues.append(Issue("ERROR", str(path), f"findings row {i} P0/P1 finding lacks required_fix"))
        if severity == "P1":
            findings_p1_count += 1
            required_fix_lower = required_fix.lower()
            if "owner:" not in required_fix_lower:
                issues.append(Issue("ERROR", str(path), f"findings row {i} P1 required_fix missing owner:"))
            if "fix:" not in required_fix_lower:
                issues.append(Issue("ERROR", str(path), f"findings row {i} P1 required_fix missing fix:"))
            if release_impact not in {"blocker", "caveat"}:
                issues.append(Issue("ERROR", str(path), f"findings row {i} P1 finding must have blocker or caveat impact"))
        if severity == "P0":
            findings_p0_count += 1
            if release_impact != "blocker":
                issues.append(Issue("ERROR", str(path), f"findings row {i} P0 finding must have release_impact blocker"))
        if severity == "none" and release_impact != "none":
            issues.append(Issue("ERROR", str(path), f"findings row {i} severity none must have release_impact none"))

    review_date = scalar_from_results(text, "review_date")
    if not DATE_RE.match(review_date):
        issues.append(Issue("ERROR", str(path), f"invalid review_date `{review_date}`"))
    elif review_date != str(scorecard_stats.get("review_date", "")):
        issues.append(
            Issue(
                "ERROR",
                str(path),
                "review_date does not match scorecard: "
                f"{review_date} vs {scorecard_stats.get('review_date')}",
            )
        )

    reviewer_id = scalar_from_results(text, "reviewer_id")
    if reviewer_id in PLACEHOLDERS:
        issues.append(Issue("ERROR", str(path), "reviewer_id is placeholder"))
    elif reviewer_id != str(scorecard_stats.get("reviewer", "")):
        issues.append(
            Issue(
                "ERROR",
                str(path),
                "reviewer_id does not match scorecard reviewer: "
                f"{reviewer_id} vs {scorecard_stats.get('reviewer')}",
            )
        )

    average_score = scalar_float_from_results(text, "average_score")
    if average_score is None:
        issues.append(Issue("ERROR", str(path), "average_score must be numeric"))
    elif abs(average_score - float(scorecard_stats.get("average_score", 0.0))) > 0.005:
        issues.append(
            Issue(
                "ERROR",
                str(path),
                "average_score does not match scorecard: "
                f"{average_score:.2f} vs {float(scorecard_stats.get('average_score', 0.0)):.2f}",
            )
        )

    minimum_score = scalar_int_from_results(text, "minimum_score")
    if minimum_score is None:
        issues.append(Issue("ERROR", str(path), "minimum_score must be an integer"))
    elif minimum_score != int(scorecard_stats.get("minimum_score", 0)):
        issues.append(
            Issue(
                "ERROR",
                str(path),
                "minimum_score does not match scorecard: "
                f"{minimum_score} vs {int(scorecard_stats.get('minimum_score', 0))}",
            )
        )

    recommendation = scalar_from_results(text, "release_recommendation")
    if recommendation not in ALLOWED_RELEASE_RECOMMENDATIONS:
        issues.append(Issue("ERROR", str(path), f"invalid release_recommendation `{recommendation}`"))
    elif recommendation not in G06_CLEAR_RELEASE_RECOMMENDATIONS:
        issues.append(Issue("ERROR", str(path), f"recommendation does not clear G06: {recommendation}"))
    if recommendation and recommendation != str(scorecard_stats.get("release_recommendation", "")):
        issues.append(
            Issue(
                "ERROR",
                str(path),
                "release_recommendation does not match scorecard: "
                f"{recommendation} vs {scorecard_stats.get('release_recommendation')}",
            )
        )

    g01_decision = scalar_from_results(text, "g01_method_source_decision")
    if g01_decision not in G06_CLEAR_G01_DECISIONS:
        issues.append(Issue("ERROR", str(path), f"G01 method-source decision does not clear G06: {g01_decision}"))
    if g01_decision and g01_decision != str(scorecard_stats.get("g01_method_source_decision", "")):
        issues.append(
            Issue(
                "ERROR",
                str(path),
                "g01_method_source_decision does not match scorecard: "
                f"{g01_decision} vs {scorecard_stats.get('g01_method_source_decision')}",
            )
        )

    for key in ("g04_follow_through_readiness", "g04_false_completion_control"):
        result = scalar_from_results(text, key)
        scorecard_stats[key] = result
        score = int(scorecard_stats.get(f"{key}_score", 0) or 0)
        score_ok = score >= 4
        if result not in G06_CLEAR_G04_RESULTS:
            issues.append(Issue("ERROR", str(path), f"{key} does not clear G06: {result}"))
        if result == "pass" and not score_ok:
            issues.append(Issue("ERROR", str(path), f"{key} says pass but scorecard score is below 4"))

    theme_selection = scalar_from_results(text, "theme_selection_freshness")
    scorecard_stats["theme_selection_freshness"] = theme_selection
    theme_selection_score = int(scorecard_stats.get("theme_selection_freshness_score", 0) or 0)
    if theme_selection not in G06_CLEAR_THEME_SELECTION_RESULTS:
        issues.append(Issue("ERROR", str(path), f"theme_selection_freshness does not clear G06: {theme_selection}"))
    if theme_selection == "pass" and theme_selection_score < 4:
        issues.append(Issue("ERROR", str(path), "theme_selection_freshness says pass but scorecard score is below 4"))

    practice_falsification = scalar_from_results(text, "practice_falsification")
    scorecard_stats["practice_falsification"] = practice_falsification
    practice_falsification_score = int(scorecard_stats.get("practice_falsification_score", 0) or 0)
    if practice_falsification not in G06_CLEAR_PRACTICE_RESULTS:
        issues.append(Issue("ERROR", str(path), f"practice_falsification does not clear G06: {practice_falsification}"))
    if practice_falsification == "pass" and practice_falsification_score < 4:
        issues.append(Issue("ERROR", str(path), "practice_falsification says pass but scorecard score is below 4"))

    methodology_iteration = scalar_from_results(text, "methodology_iteration_traceability")
    scorecard_stats["methodology_iteration_traceability"] = methodology_iteration
    methodology_iteration_score = int(scorecard_stats.get("methodology_iteration_traceability_score", 0) or 0)
    if methodology_iteration not in G06_CLEAR_METHOD_ITERATION_RESULTS:
        issues.append(
            Issue(
                "ERROR",
                str(path),
                f"methodology_iteration_traceability does not clear G06: {methodology_iteration}",
            )
        )
    if methodology_iteration == "pass" and methodology_iteration_score < 4:
        issues.append(
            Issue(
                "ERROR",
                str(path),
                "methodology_iteration_traceability says pass but scorecard score is below 4",
            )
        )

    g05_decision = scalar_from_results(text, "g05_source_decision")
    if g05_decision not in G06_CLEAR_G05_DECISIONS:
        issues.append(Issue("ERROR", str(path), f"G05 source decision does not clear G06: {g05_decision}"))
    if g05_decision and g05_decision != str(scorecard_stats.get("g05_source_decision", "")):
        issues.append(
            Issue(
                "ERROR",
                str(path),
                "g05_source_decision does not match scorecard: "
                f"{g05_decision} vs {scorecard_stats.get('g05_source_decision')}",
            )
        )

    historical_consensus_decision = scalar_from_results(
        text, "historical_consensus_exception_decision"
    )
    if historical_consensus_decision not in G06_CLEAR_HISTORICAL_CONSENSUS_DECISIONS:
        issues.append(
            Issue(
                "ERROR",
                str(path),
                "historical consensus exception decision does not clear G06: "
                f"{historical_consensus_decision}",
            )
        )
    if historical_consensus_decision and historical_consensus_decision != str(
        scorecard_stats.get("historical_consensus_exception_decision", "")
    ):
        issues.append(
            Issue(
                "ERROR",
                str(path),
                "historical_consensus_exception_decision does not match scorecard: "
                f"{historical_consensus_decision} vs "
                f"{scorecard_stats.get('historical_consensus_exception_decision')}",
            )
        )

    p0_count = scalar_int_from_results(text, "p0_findings_count")
    if p0_count != 0:
        issues.append(Issue("ERROR", str(path), f"p0_findings_count must be 0, got `{p0_count}`"))
    if p0_count is not None and p0_count != int(scorecard_stats.get("p0_findings_count", 0)):
        issues.append(
            Issue(
                "ERROR",
                str(path),
                "p0_findings_count does not match scorecard: "
                f"{p0_count} vs {int(scorecard_stats.get('p0_findings_count', 0))}",
            )
        )
    if p0_count is not None and findings_p0_count != p0_count:
        issues.append(
            Issue(
                "ERROR",
                str(path),
                "findings table P0 count does not match summary: "
                f"{findings_p0_count} vs {p0_count}",
            )
        )

    p1_count = scalar_int_from_results(text, "p1_findings_count")
    if p1_count is None:
        issues.append(Issue("ERROR", str(path), "p1_findings_count must be an integer"))
    elif p1_count != int(scorecard_stats.get("p1_findings_count", 0)):
        issues.append(
            Issue(
                "ERROR",
                str(path),
                "p1_findings_count does not match scorecard: "
                f"{p1_count} vs {int(scorecard_stats.get('p1_findings_count', 0))}",
            )
        )
    if p1_count is not None and findings_p1_count != p1_count:
        issues.append(
            Issue(
                "ERROR",
                str(path),
                "findings table P1 count does not match summary: "
                f"{findings_p1_count} vs {p1_count}",
            )
        )

    action_label = scalar_from_results(text, "action_label_reproducibility")
    if action_label == "fail":
        issues.append(Issue("ERROR", str(path), "action_label_reproducibility failed"))

    if int(scorecard_stats.get("p0_findings_count", 0)) > 0:
        issues.append(Issue("ERROR", str(path), "scorecard contains P0 findings"))
    return issues


def validate_intake(path: Path) -> list[Issue]:
    issues: list[Issue] = []
    rows, csv_issues = read_csv(path)
    issues.extend(csv_issues)
    if not rows:
        issues.append(Issue("ERROR", str(path), "intake checklist has no rows"))
        return issues

    required_columns = {"check_id", "requirement", "pass_condition", "status", "notes"}
    header = set(rows[0].keys())
    missing = sorted(required_columns - header)
    if missing:
        issues.append(Issue("ERROR", str(path), f"missing columns: {missing}"))
        return issues

    requirements = {row.get("requirement", "").strip() for row in rows}
    missing_requirements = sorted(REQUIRED_INTAKE_REQUIREMENTS - requirements)
    if missing_requirements:
        issues.append(Issue("ERROR", str(path), f"missing requirements: {missing_requirements}"))

    for i, row in enumerate(rows, start=2):
        status = row.get("status", "").strip()
        if status not in {"pass", "accepted"}:
            issues.append(Issue("ERROR", str(path), f"row {i} not pass/accepted: {status}"))
    return issues


def validate_rubric_coverage(scorecard_path: Path) -> tuple[list[Issue], int]:
    issues: list[Issue] = []
    rubric_rows, rubric_issues = read_csv(G06_SELECTION_RUBRIC)
    scorecard_rows, scorecard_issues = read_csv(scorecard_path)
    issues.extend(rubric_issues + scorecard_issues)
    if rubric_issues or scorecard_issues:
        return issues, 0
    if not rubric_rows:
        return [Issue("ERROR", str(G06_SELECTION_RUBRIC), "selection rubric has no rows")], 0
    if not scorecard_rows:
        return [Issue("ERROR", str(scorecard_path), "scorecard has no rows")], 0

    score_by_dimension: dict[str, int] = {}
    for i, row in enumerate(scorecard_rows, start=2):
        dimension = row.get("dimension", "").strip()
        if not dimension:
            continue
        try:
            score_by_dimension[dimension] = int(row.get("score_1_to_5", "").strip())
        except ValueError:
            issues.append(Issue("ERROR", str(scorecard_path), f"row {i} score_1_to_5 must be integer"))

    decisions_checked = 0
    for i, row in enumerate(rubric_rows, start=2):
        decision = row.get("required_decision", "").strip()
        dimension = row.get("scorecard_dimension", "").strip()
        evidence_path = row.get("evidence_path", "").strip()
        try:
            minimum_score = int(row.get("minimum_release_score", "").strip())
        except ValueError:
            issues.append(Issue("ERROR", str(G06_SELECTION_RUBRIC), f"row {i} minimum_release_score must be integer"))
            continue
        if minimum_score < 4:
            issues.append(Issue("ERROR", str(G06_SELECTION_RUBRIC), f"row {i} minimum_release_score must be at least 4"))
        if not decision:
            issues.append(Issue("ERROR", str(G06_SELECTION_RUBRIC), f"row {i} missing required_decision"))
        if dimension not in score_by_dimension:
            issues.append(
                Issue(
                    "ERROR",
                    str(G06_SELECTION_RUBRIC),
                    f"rubric decision `{decision}` scorecard_dimension missing from completed scorecard: {dimension}",
                )
            )
        elif score_by_dimension[dimension] < minimum_score:
            issues.append(
                Issue(
                    "ERROR",
                    str(scorecard_path),
                    f"rubric decision `{decision}` score {score_by_dimension[dimension]} below {minimum_score}",
                )
            )
        if evidence_path and not (ROOT / evidence_path).exists():
            issues.append(Issue("ERROR", str(G06_SELECTION_RUBRIC), f"row {i} evidence_path missing: {evidence_path}"))
        decisions_checked += 1
    return issues, decisions_checked


def validate_assignment_tracker(path: Path, stats: dict[str, float | int | str]) -> list[Issue]:
    issues: list[Issue] = []
    rows, csv_issues = read_csv(path)
    issues.extend(csv_issues)
    if csv_issues:
        return issues
    g06_rows = [row for row in rows if row.get("gate_id", "").strip() == "G06"]
    if len(g06_rows) != 1:
        return [Issue("ERROR", str(path), f"expected exactly one G06 assignment row, got {len(g06_rows)}")]
    row = g06_rows[0]
    assigned_reviewer = row.get("assigned_reviewer", "").strip()
    assigned_date = row.get("assigned_date", "").strip()
    due_date = row.get("due_date", "").strip()
    reviewer_status = row.get("reviewer_status", "").strip()
    current_status = row.get("current_status", "").strip()
    independence_required = row.get("independence_required", "").strip().lower()

    if independence_required != "yes":
        issues.append(Issue("ERROR", str(path), "G06 assignment independence_required must be yes"))
    if assigned_reviewer in PLACEHOLDERS:
        issues.append(Issue("ERROR", str(path), "G06 assignment missing assigned_reviewer"))
    elif assigned_reviewer != str(stats.get("reviewer", "")):
        issues.append(
            Issue(
                "ERROR",
                str(path),
                "assigned_reviewer does not match completed scorecard reviewer: "
                f"{assigned_reviewer} vs {stats.get('reviewer')}",
            )
        )
    for field_name, value in (("assigned_date", assigned_date), ("due_date", due_date)):
        if not DATE_RE.match(value):
            issues.append(Issue("ERROR", str(path), f"G06 assignment {field_name} must be YYYY-MM-DD"))
    if reviewer_status not in G06_RETURN_REVIEWER_STATUSES:
        issues.append(Issue("ERROR", str(path), f"G06 assignment reviewer_status not returned/validated: {reviewer_status}"))
    if current_status not in G06_RETURN_ASSIGNMENT_STATUSES:
        issues.append(Issue("ERROR", str(path), f"G06 assignment current_status not return-ready: {current_status}"))
    return issues


def validate_independence_screen(path: Path) -> list[Issue]:
    issues: list[Issue] = []
    rows, csv_issues = read_csv(path)
    issues.extend(csv_issues)
    if csv_issues:
        return issues
    if not rows:
        return [Issue("ERROR", str(path), "independence screen has no rows")]
    required_columns = {"check_id", "status", "release_impact"}
    missing = sorted(required_columns - set(rows[0].keys()))
    if missing:
        return [Issue("ERROR", str(path), f"independence screen missing columns: {missing}")]
    by_id = {row.get("check_id", "").strip(): row for row in rows}
    for check_id in ("screen_05", "screen_06"):
        row = by_id.get(check_id)
        if not row:
            issues.append(Issue("ERROR", str(path), f"independence screen missing `{check_id}`"))
            continue
        status = row.get("status", "").strip()
        if status not in {"pass", "accepted"}:
            issues.append(Issue("ERROR", str(path), f"{check_id} must be pass/accepted for completed return, got {status}"))
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scorecard", required=True, help="completed external-reviewer-scorecard.csv")
    parser.add_argument("--results", required=True, help="completed external-review-results-YYYY-MM-DD.md")
    parser.add_argument("--intake", required=True, help="completed external-review-intake-checklist.csv")
    parser.add_argument("--assignment-tracker", required=True, help="updated g06-reviewer-assignment-tracker.csv")
    parser.add_argument("--independence-screen", required=True, help="updated g06-reviewer-independence-screen.csv")
    args = parser.parse_args()

    issues: list[Issue] = []
    scorecard_issues, stats = validate_scorecard(Path(args.scorecard))
    issues.extend(scorecard_issues)
    issues.extend(validate_results(Path(args.results), stats))
    issues.extend(validate_intake(Path(args.intake)))
    rubric_issues, rubric_decisions_checked = validate_rubric_coverage(Path(args.scorecard))
    issues.extend(rubric_issues)
    assignment_independence_checked = 0
    issues.extend(validate_assignment_tracker(Path(args.assignment_tracker), stats))
    assignment_independence_checked += 1
    issues.extend(validate_independence_screen(Path(args.independence_screen)))
    assignment_independence_checked += 1

    for issue in issues:
        print(issue.render())

    errors = [issue for issue in issues if issue.severity == "ERROR"]
    print("external_review_return_validation:")
    print(f"  g06_clearable: {str(not errors).lower()}")
    print(f"  average_score: {float(stats.get('average_score', 0.0)):.2f}")
    print(f"  minimum_score: {int(stats.get('minimum_score', 0))}")
    print(f"  p0_findings_count: {int(stats.get('p0_findings_count', 0))}")
    print(f"  p1_findings_count: {int(stats.get('p1_findings_count', 0))}")
    print(f"  g01_method_source_decision: {stats.get('g01_method_source_decision') or 'missing'}")
    print(f"  g04_follow_through_readiness: {stats.get('g04_follow_through_readiness') or 'missing'}")
    print(f"  g04_false_completion_control: {stats.get('g04_false_completion_control') or 'missing'}")
    print(f"  theme_selection_freshness: {stats.get('theme_selection_freshness') or 'missing'}")
    print(f"  practice_falsification: {stats.get('practice_falsification') or 'missing'}")
    print(
        "  methodology_iteration_traceability: "
        f"{stats.get('methodology_iteration_traceability') or 'missing'}"
    )
    print(f"  g05_source_decision: {stats.get('g05_source_decision') or 'missing'}")
    print(
        "  historical_consensus_exception_decision: "
        f"{stats.get('historical_consensus_exception_decision') or 'missing'}"
    )
    print(f"  release_recommendation: {stats.get('release_recommendation') or 'missing'}")
    print(f"  rubric_decisions_checked: {rubric_decisions_checked}")
    print(f"  assignment_independence_checked: {assignment_independence_checked}")
    print(f"  errors: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
