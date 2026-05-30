#!/usr/bin/env python3
"""Validate the institutional colleague release bundle controls.

This is a pre-release safety check. It validates that the future external
release bundle preserves use boundaries, required caveats and cutover controls.
It does not approve external release.
"""

from __future__ import annotations

import csv
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATION_DIR = Path("cases/long-term-workflow-validation-2026-05-30")
PUBLIC_PACK = VALIDATION_DIR / "public-workflow-pack"

MANIFEST = VALIDATION_DIR / "institutional-release-bundle-manifest.csv"
CUTOVER = VALIDATION_DIR / "final-release-cutover-checklist.csv"
RELEASE_DECISION = VALIDATION_DIR / "public-release-decision.md"
RELEASE_NOTES = PUBLIC_PACK / "institutional-colleague-release-notes-template.md"
USE_BOUNDARIES = PUBLIC_PACK / "institutional-use-boundaries.md"
ADOPTION_FAQ = PUBLIC_PACK / "institutional-adoption-faq.md"
GO_NO_GO_TEMPLATE = VALIDATION_DIR / "external-release-go-no-go-template.md"
VALIDATION_ROOT = (ROOT / VALIDATION_DIR).resolve()

REQUIRED_INCLUDED_PATHS = {
    "public-workflow-pack/README.md",
    "public-workflow-pack/workflow.md",
    "public-workflow-pack/fill-guide.md",
    "public-workflow-pack/template-inventory.md",
    "public-workflow-pack/source-appendix.md",
    "public-workflow-pack/analyst-checklist.csv",
    "public-workflow-pack/operator-runbook.md",
    "public-workflow-pack/institutional-colleague-release-notes-template.md",
    "public-workflow-pack/institutional-colleague-acceptance-memo-template.md",
    "public-workflow-pack/institutional-use-boundaries.md",
    "public-workflow-pack/institutional-adoption-faq.md",
    "public-release-decision.md",
    "public-release-gate-tracker.csv",
    "objective-readiness-audit.csv",
    "goal-completion-audit.csv",
    "release-verification-command-manifest.csv",
    "external-release-action-queue.csv",
    "final-release-cutover-checklist.csv",
    "institutional-colleague-acceptance-checklist.csv",
    "external-reviewer-bundle-manifest.csv",
    "g06-external-review-handoff-2026-05-30.md",
    "g06-reviewer-candidate-screen.csv",
    "g06-reviewer-selection-rubric.csv",
    "g06-reviewer-independence-screen.csv",
    "trial-theme-matrix.csv",
    "theme-selection-refresh-audit.csv",
    "practice-falsification-audit.csv",
    "methodology-iteration-trace-audit.csv",
    "multi-lens-coverage-audit.csv",
    "g04-follow-through-handoff-2026-05-30.md",
    "follow-through-trigger-tracker.csv",
    "g04-follow-through-event-watch-calendar.csv",
    "g04-later-event-candidate-screen.csv",
    "historical-consensus-source-attempts.csv",
    "historical-consensus-unavailable-data-exception-2026-05-30.md",
    "g05-fy2-fcf-source-upgrade-2026-05-30.md",
    "g05-crm-source-attempts.csv",
}

BOUNDARY_MARKERS = {
    "G04",
    "G06",
    "not_ready_external_release",
    "objective_complete",
    "stale_after:",
    "must_refresh_if:",
}

RELEASE_NOTE_MARKERS = {
    "draft_not_released",
    "G04",
    "G06",
    "objective_complete",
    "final external methodology",
    "stale_after:",
    "must_refresh_if:",
}

FAQ_MARKERS = {
    "Not as a final external-release methodology",
    "G04",
    "G06",
    "source gaps",
    "stale-after",
}

GO_NO_GO_MARKERS = {
    "decision: `go` | `no_go`",
    "G04 true follow-through",
    "G06 external reviewer",
    "live case reproducibility",
    "G01 method-source decision",
    "theme selection freshness",
    "practice falsification",
    "methodology iteration traceability",
    "ordinary-vs-workflow delta",
    "template completeness",
    "G05 source challenge",
    "public example source quality",
    "historical consensus exception",
    "operational loop handoff",
    "institutional colleague acceptance",
    "completed checklist and dated acceptance memo pass return validator",
    "validate_long_term_release.py --require-external-ready",
}

OPERATOR_RUNBOOK = PUBLIC_PACK / "operator-runbook.md"

OPERATOR_RUNBOOK_MARKERS = {
    "G04",
    "G06",
    "objective_complete: false",
    "validate_long_term_release.py --require-external-ready",
    "validate_public_release_freshness.py",
    "validate_go_no_go_evidence_coverage.py",
    "validate_final_release_cutover.py",
    "validate_institutional_colleague_acceptance.py",
    "validate_institutional_colleague_acceptance_return.py",
    "validate_external_release_action_queue.py",
    "validate_g06_reviewer_selection_rubric.py",
    "build_external_review_packet.py --dry-run",
    "validate_external_review_dispatch_packet.py",
    "validate_g06_dispatch_readiness.py",
    "build_follow_through_packet.py --dry-run",
    "validate_follow_through_packet_matrix.py",
    "build_institutional_release_packet.py --dry-run",
    "export_ready: false",
    "stale_after:",
    "must_refresh_if:",
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


def is_relative_to(path: Path, base: Path) -> bool:
    try:
        path.relative_to(base)
        return True
    except ValueError:
        return False


def validate_manifest() -> list[Issue]:
    issues: list[Issue] = []
    rows, csv_issues = read_csv(MANIFEST)
    issues.extend(csv_issues)
    if not rows:
        issues.append(Issue("ERROR", str(MANIFEST), "manifest has no rows"))
        return issues

    required_columns = {
        "bundle_section",
        "path",
        "include_in_external_release",
        "required",
        "release_phase",
        "notes",
    }
    missing_columns = sorted(required_columns - set(rows[0].keys()))
    if missing_columns:
        issues.append(Issue("ERROR", str(MANIFEST), f"missing columns: {missing_columns}"))
        return issues

    included_paths = {
        row.get("path", "").strip()
        for row in rows
        if row.get("include_in_external_release", "").strip() == "yes"
    }
    missing_paths = sorted(REQUIRED_INCLUDED_PATHS - included_paths)
    if missing_paths:
        issues.append(Issue("ERROR", str(MANIFEST), f"missing included paths: {missing_paths}"))

    for i, row in enumerate(rows, start=2):
        path = row.get("path", "").strip()
        include = row.get("include_in_external_release", "").strip()
        required = row.get("required", "").strip()
        phase = row.get("release_phase", "").strip()
        if include not in {"yes", "no", "optional"}:
            issues.append(Issue("ERROR", str(MANIFEST), f"row {i} invalid include value `{include}`"))
        if required not in {"yes", "no"}:
            issues.append(Issue("ERROR", str(MANIFEST), f"row {i} invalid required value `{required}`"))
        if row.get("bundle_section", "").strip() == "internal_do_not_send":
            if include != "no" or phase != "internal_only":
                issues.append(
                    Issue("ERROR", str(MANIFEST), f"row {i} internal item is not protected")
                )
        if include == "yes" and phase != "external_release_only":
            issues.append(Issue("ERROR", str(MANIFEST), f"row {i} included item must be external_release_only"))
        if include == "optional" and phase != "external_release_optional":
            issues.append(Issue("ERROR", str(MANIFEST), f"row {i} optional item must be external_release_optional"))
        if path:
            candidate = (ROOT / VALIDATION_DIR / path).resolve()
            if include in {"yes", "optional"} and not is_relative_to(candidate, VALIDATION_ROOT):
                issues.append(Issue("ERROR", str(MANIFEST), f"row {i} included path escapes validation directory: {path}"))
            if not candidate.exists():
                issues.append(Issue("ERROR", str(MANIFEST), f"row {i} path missing: {path}"))
    return issues


def validate_cutover() -> list[Issue]:
    issues: list[Issue] = []
    rows, csv_issues = read_csv(CUTOVER)
    issues.extend(csv_issues)
    if not rows:
        issues.append(Issue("ERROR", str(CUTOVER), "cutover checklist has no rows"))
        return issues
    required = {
        "g04_true_follow_through",
        "g06_external_review",
        "validator_external_ready",
        "institutional_use_boundaries",
    }
    seen = {row.get("requirement", "").strip() for row in rows}
    missing = sorted(required - seen)
    if missing:
        issues.append(Issue("ERROR", str(CUTOVER), f"missing requirements: {missing}"))
    for i, row in enumerate(rows, start=2):
        status = row.get("status", "").strip()
        if status not in {"pending", "pass", "accepted"}:
            issues.append(Issue("ERROR", str(CUTOVER), f"row {i} invalid status `{status}`"))
    return issues


def validate_markers(path: Path, markers: set[str]) -> list[Issue]:
    text, issues = read_text(path)
    for marker in markers:
        if marker not in text:
            issues.append(Issue("ERROR", str(path), f"missing marker `{marker}`"))
    return issues


def validate_release_state() -> list[Issue]:
    issues: list[Issue] = []
    decision_text, read_issues = read_text(RELEASE_DECISION)
    issues.extend(read_issues)
    if "release_status: not_ready_external_release" in decision_text:
        notes_text, note_issues = read_text(RELEASE_NOTES)
        boundary_text, boundary_issues = read_text(USE_BOUNDARIES)
        faq_text, faq_issues = read_text(ADOPTION_FAQ)
        issues.extend(note_issues)
        issues.extend(boundary_issues)
        issues.extend(faq_issues)
        if "draft_not_released" not in notes_text:
            issues.append(
                Issue(
                    "ERROR",
                    str(RELEASE_NOTES),
                    "release notes must remain draft_not_released while public decision is not ready",
                )
            )
        if "not_ready_external_release" not in boundary_text:
            issues.append(
                Issue(
                    "ERROR",
                    str(USE_BOUNDARIES),
                    "use boundaries must preserve not_ready_external_release status",
                )
            )
        if "Not as a final external-release methodology" not in faq_text:
            issues.append(
                Issue("ERROR", str(ADOPTION_FAQ), "FAQ must state not final external-release")
            )
    return issues


def main() -> int:
    issues: list[Issue] = []
    issues.extend(validate_manifest())
    issues.extend(validate_cutover())
    issues.extend(validate_markers(RELEASE_NOTES, RELEASE_NOTE_MARKERS))
    issues.extend(validate_markers(USE_BOUNDARIES, BOUNDARY_MARKERS))
    issues.extend(validate_markers(ADOPTION_FAQ, FAQ_MARKERS))
    issues.extend(validate_markers(GO_NO_GO_TEMPLATE, GO_NO_GO_MARKERS))
    issues.extend(validate_markers(OPERATOR_RUNBOOK, OPERATOR_RUNBOOK_MARKERS))
    issues.extend(validate_release_state())

    errors = [issue for issue in issues if issue.severity == "ERROR"]
    for issue in issues:
        print(issue.render())
    print("institutional_release_bundle_validation:")
    print(f"  bundle_controlled: {str(not errors).lower()}")
    print(f"  errors: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
