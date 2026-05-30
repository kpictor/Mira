#!/usr/bin/env python3
"""Validate the long-term workflow release gate package.

This validator does not require the methodology to be externally ready.
It checks whether the release decision is internally consistent, whether
blocking gates are explicit, and whether required evidence paths exist.
Use --require-external-ready only when preparing final external release.
"""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass
from pathlib import Path


VALIDATION_DIR = Path("cases/long-term-workflow-validation-2026-05-30")
PUBLIC_PACK_DIR = VALIDATION_DIR / "public-workflow-pack"
GATE_TRACKER = VALIDATION_DIR / "public-release-gate-tracker.csv"
PUBLIC_DECISION = VALIDATION_DIR / "public-release-decision.md"
PUBLIC_AUDIT = VALIDATION_DIR / "public-readiness-audit.md"
G01_EXTERNAL_METHOD_SOURCE_AUDIT = VALIDATION_DIR / "g01-external-method-source-audit.csv"
G01_EXTERNAL_METHOD_SOURCE_UPGRADE = VALIDATION_DIR / "g01-external-method-source-upgrade-2026-05-30.md"
G01_EXTERNAL_METHOD_SCAN_VALIDATOR = Path("scripts/validate_g01_external_method_scan.py")
EXTERNAL_REVIEWER_BUNDLE = VALIDATION_DIR / "external-reviewer-bundle-manifest.csv"
INSTITUTIONAL_RELEASE_BUNDLE = VALIDATION_DIR / "institutional-release-bundle-manifest.csv"
CROSS_CASE_VALIDATION_MATRIX = VALIDATION_DIR / "cross-case-validation-matrix.csv"
OVERLAY_COVERAGE_AUDIT = VALIDATION_DIR / "overlay-coverage-audit.csv"
CROSS_CASE_VALIDATION_SUMMARY = VALIDATION_DIR / "cross-case-validation-summary.md"
HISTORICAL_BACKTEST_ARCHIVE_AUDIT = VALIDATION_DIR / "historical-backtest-source-archive-audit.csv"
HISTORICAL_BACKTEST_PUBLICATION_STANDARD = VALIDATION_DIR / "historical-backtest-publication-standard.md"
HISTORICAL_VALUATION_SOURCE_UPGRADE = VALIDATION_DIR / "historical-valuation-source-upgrade-2026-05-30.md"
HISTORICAL_TRANSCRIPT_SOURCE_UPGRADE = VALIDATION_DIR / "historical-transcript-source-upgrade-2026-05-30.md"
HISTORICAL_CONSENSUS_SOURCE_ATTEMPTS = VALIDATION_DIR / "historical-consensus-source-attempts.csv"
HISTORICAL_CONSENSUS_EXCEPTION = VALIDATION_DIR / "historical-consensus-unavailable-data-exception-2026-05-30.md"
FINAL_RELEASE_CUTOVER = VALIDATION_DIR / "final-release-cutover-checklist.csv"
EXTERNAL_GO_NO_GO_TEMPLATE = VALIDATION_DIR / "external-release-go-no-go-template.md"
FINAL_RELEASE_CUTOVER_VALIDATOR = Path("scripts/validate_final_release_cutover.py")
LONG_TERM_LOOP = Path("loops/long-term-thesis-loop.md")
G05_SOURCE_UPGRADE = VALIDATION_DIR / "g05-fy2-fcf-source-upgrade-2026-05-30.md"
G05_SOURCE_ATTEMPTS = VALIDATION_DIR / "g05-crm-source-attempts.csv"
CRM_EXPECTATION_MAP = Path("cases/crm-2026-05-product-workflow-trial/expectation-map.csv")
G04_HANDOFF = VALIDATION_DIR / "g04-follow-through-handoff-2026-05-30.md"
G04_INTAKE = VALIDATION_DIR / "g04-follow-through-intake-checklist.csv"
G04_EVENT_WATCH_CALENDAR = VALIDATION_DIR / "g04-follow-through-event-watch-calendar.csv"
G04_LATER_EVENT_CANDIDATE_SCREEN = VALIDATION_DIR / "g04-later-event-candidate-screen.csv"
G04_EXECUTION_TRACKER = VALIDATION_DIR / "g04-follow-through-execution-tracker.csv"
G04_REFRESH_VALIDATION_STANDARD = VALIDATION_DIR / "g04-follow-through-refresh-validation-standard.md"
CRM_G04_ASSIGNMENT = VALIDATION_DIR / "crm-g04-follow-through-assignment.md"
FOLLOW_THROUGH_REFRESH_VALIDATOR = Path("scripts/validate_follow_through_refresh.py")
FOLLOW_THROUGH_TRIGGER_TRACKER_VALIDATOR = Path("scripts/validate_follow_through_trigger_tracker.py")
G04_EVENT_WATCH_CALENDAR_VALIDATOR = Path("scripts/validate_g04_event_watch_calendar.py")
G04_LATER_EVENT_CANDIDATE_SCREEN_VALIDATOR = Path("scripts/validate_g04_later_event_candidate_screen.py")
FOLLOW_THROUGH_EXECUTION_TRACKER_VALIDATOR = Path("scripts/validate_follow_through_execution_tracker.py")
FOLLOW_THROUGH_PACKET_BUILDER = Path("scripts/build_follow_through_packet.py")
FOLLOW_THROUGH_PACKET_MATRIX_VALIDATOR = Path("scripts/validate_follow_through_packet_matrix.py")
G06_HANDOFF = VALIDATION_DIR / "g06-external-review-handoff-2026-05-30.md"
G06_RETURN_VALIDATION_STANDARD = VALIDATION_DIR / "g06-external-review-return-validation-standard.md"
EXTERNAL_REVIEW_RESULTS_TEMPLATE = PUBLIC_PACK_DIR / "external-review-results-template.md"
EXTERNAL_REVIEW_INTAKE = PUBLIC_PACK_DIR / "external-review-intake-checklist.csv"
EXTERNAL_REVIEW_ASSIGNMENT_TRACKER = VALIDATION_DIR / "g06-reviewer-assignment-tracker.csv"
G06_REVIEWER_CANDIDATE_SCREEN = VALIDATION_DIR / "g06-reviewer-candidate-screen.csv"
G06_REVIEWER_INDEPENDENCE_SCREEN = VALIDATION_DIR / "g06-reviewer-independence-screen.csv"
G06_REVIEWER_SELECTION_RUBRIC = VALIDATION_DIR / "g06-reviewer-selection-rubric.csv"
EXTERNAL_REVIEW_RETURN_VALIDATOR = Path("scripts/validate_external_review_return.py")
EXTERNAL_REVIEW_PACKET_VALIDATOR = Path("scripts/validate_external_review_packet.py")
EXTERNAL_REVIEW_ASSIGNMENT_TRACKER_VALIDATOR = Path("scripts/validate_external_review_assignment_tracker.py")
G06_REVIEWER_CANDIDATE_SCREEN_VALIDATOR = Path("scripts/validate_g06_reviewer_candidate_screen.py")
G06_REVIEWER_INDEPENDENCE_SCREEN_VALIDATOR = Path("scripts/validate_g06_reviewer_independence_screen.py")
G06_REVIEWER_SELECTION_RUBRIC_VALIDATOR = Path("scripts/validate_g06_reviewer_selection_rubric.py")
EXTERNAL_REVIEW_PACKET_BUILDER = Path("scripts/build_external_review_packet.py")
EXTERNAL_REVIEW_DISPATCH_PACKET_VALIDATOR = Path("scripts/validate_external_review_dispatch_packet.py")
G06_DISPATCH_READINESS_CHECKLIST = VALIDATION_DIR / "g06-dispatch-readiness-checklist.csv"
G06_DISPATCH_READINESS_VALIDATOR = Path("scripts/validate_g06_dispatch_readiness.py")
EXTERNAL_RELEASE_ACTION_QUEUE = VALIDATION_DIR / "external-release-action-queue.csv"
EXTERNAL_RELEASE_ACTION_QUEUE_VALIDATOR = Path("scripts/validate_external_release_action_queue.py")
LONG_TERM_VALIDATOR_REGRESSION_TEST = Path("scripts/test_long_term_release_validators.py")
LONG_TERM_RELEASE_CHECK_RUNNER = Path("scripts/run_long_term_release_checks.py")
VALIDATION_CASE_SET_VALIDATOR = Path("scripts/validate_validation_case_set.py")
RECENT_THEME_SELECTION_VALIDATOR = Path("scripts/validate_recent_theme_selection.py")
TRIAL_THEME_MATRIX_VALIDATOR = Path("scripts/validate_trial_theme_matrix.py")
THEME_SELECTION_REFRESH_AUDIT = VALIDATION_DIR / "theme-selection-refresh-audit.csv"
THEME_SELECTION_REFRESH_AUDIT_VALIDATOR = Path("scripts/validate_theme_selection_refresh_audit.py")
PUBLIC_RELEASE_FRESHNESS_VALIDATOR = Path("scripts/validate_public_release_freshness.py")
PUBLIC_WORKFLOW_PACK_VALIDATOR = Path("scripts/validate_public_workflow_pack.py")
INSTITUTIONAL_RELEASE_BUNDLE_VALIDATOR = Path("scripts/validate_institutional_release_bundle.py")
INSTITUTIONAL_RELEASE_PACKET_BUILDER = Path("scripts/build_institutional_release_packet.py")
OBJECTIVE_READINESS_AUDIT = VALIDATION_DIR / "objective-readiness-audit.csv"
OBJECTIVE_READINESS_VALIDATOR = Path("scripts/validate_objective_readiness.py")
GOAL_COMPLETION_AUDIT = VALIDATION_DIR / "goal-completion-audit.csv"
GOAL_COMPLETION_AUDIT_VALIDATOR = Path("scripts/validate_goal_completion_audit.py")
RELEASE_VERIFICATION_COMMAND_MANIFEST = VALIDATION_DIR / "release-verification-command-manifest.csv"
RELEASE_VERIFICATION_COMMAND_MANIFEST_VALIDATOR = Path("scripts/validate_release_verification_command_manifest.py")
POWER_CONTRACT_REGULATORY_TEMPLATE = Path("templates/power-contract-regulatory-check.csv")
STABLECOIN_RESERVE_REGULATORY_TEMPLATE = Path("templates/stablecoin-reserve-regulatory-check.csv")
GOVERNMENT_PROCUREMENT_PROGRAM_TEMPLATE = Path("templates/government-procurement-program-check.csv")
NUCLEAR_AI_POWER_CASE = Path("cases/nuclear-ai-power-2026-05-value-capture-screen")
STABLECOIN_PAYMENTS_CASE = Path("cases/stablecoin-payments-2026-05-value-capture-screen")
DEFENSE_AUTONOMY_CASE = Path("cases/defense-autonomy-drones-2026-05-value-capture-screen")
INSTITUTIONAL_RELEASE_NOTES = PUBLIC_PACK_DIR / "institutional-colleague-release-notes-template.md"
INSTITUTIONAL_USE_BOUNDARIES = PUBLIC_PACK_DIR / "institutional-use-boundaries.md"
INSTITUTIONAL_ADOPTION_FAQ = PUBLIC_PACK_DIR / "institutional-adoption-faq.md"
OPERATOR_RUNBOOK = PUBLIC_PACK_DIR / "operator-runbook.md"

REQUIRED_GATES = {
    "G01": "external_method_scan",
    "G02": "live_theme_company_tests",
    "G03": "historical_failure_backtests",
    "G04": "true_follow_through_refresh",
    "G05": "valuation_expectation_map",
    "G06": "external_independent_reviewer",
    "G07": "ordinary_vs_workflow_delta",
    "G08": "template_completeness",
    "G09": "source_quality_public_examples",
    "G10": "release_decision",
    "G11": "operational_loop",
}

EXTERNAL_CLEAR_STATUSES = {
    "pass_external",
    "pass_public_grade",
    "completed",
    "accepted",
    "ready_external_release",
}

INTERNAL_READY_STATUSES = {
    "pass_internal",
    "pass_internal_improved",
    "ready_internal_candidate",
    "candidate_internal_release",
    "partial_pass",
    "partial_pass_improved",
    "partial_pass_source_cleanup_improved",
    "partial_pass_exception_protocol_added",
    "partial_pass_historical_range_improved",
    "partial_pass_reviewer_simulation",
    "ready_for_reviewer_exception_decision",
    "ready_to_assign_not_completed",
    "ready_to_execute_waiting_event",
    "ready_to_run_not_completed",
    "not_ready",
}

KNOWN_HARD_BLOCKER_GATES = {"G04", "G05", "G06"}


@dataclass
class Issue:
    severity: str
    subject: str
    message: str

    def render(self) -> str:
        return f"{self.severity}: {self.subject}: {self.message}"


def read_text(root: Path, rel_path: Path) -> str:
    return (root / rel_path).read_text(encoding="utf-8")


def read_gate_rows(root: Path) -> tuple[list[dict[str, str]], list[Issue]]:
    path = root / GATE_TRACKER
    issues: list[Issue] = []
    if not path.exists():
        return [], [Issue("ERROR", str(GATE_TRACKER), "missing gate tracker")]

    try:
        with path.open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    except Exception as exc:
        return [], [Issue("ERROR", str(GATE_TRACKER), f"could not parse CSV: {exc}")]

    required_columns = {
        "gate_id",
        "gate",
        "required_for_external_release",
        "current_status",
        "evidence_path",
        "remaining_blocker",
        "next_action",
        "owner_type",
    }
    header = set(rows[0].keys()) if rows else set()
    missing = sorted(required_columns - header)
    if missing:
        issues.append(Issue("ERROR", str(GATE_TRACKER), f"missing columns: {missing}"))
    if not rows:
        issues.append(Issue("ERROR", str(GATE_TRACKER), "no gate rows"))
    return rows, issues


def evidence_exists(root: Path, evidence_path: str) -> bool:
    if not evidence_path:
        return False
    path = root / evidence_path
    return path.exists()


def validate_required_files(root: Path) -> list[Issue]:
    issues: list[Issue] = []
    required_files = [
        GATE_TRACKER,
        PUBLIC_DECISION,
        PUBLIC_AUDIT,
        G01_EXTERNAL_METHOD_SOURCE_AUDIT,
        G01_EXTERNAL_METHOD_SOURCE_UPGRADE,
        G01_EXTERNAL_METHOD_SCAN_VALIDATOR,
        EXTERNAL_REVIEWER_BUNDLE,
        INSTITUTIONAL_RELEASE_BUNDLE,
        CROSS_CASE_VALIDATION_MATRIX,
        OVERLAY_COVERAGE_AUDIT,
        CROSS_CASE_VALIDATION_SUMMARY,
        HISTORICAL_BACKTEST_ARCHIVE_AUDIT,
        HISTORICAL_BACKTEST_PUBLICATION_STANDARD,
        HISTORICAL_VALUATION_SOURCE_UPGRADE,
        HISTORICAL_TRANSCRIPT_SOURCE_UPGRADE,
        HISTORICAL_CONSENSUS_SOURCE_ATTEMPTS,
        HISTORICAL_CONSENSUS_EXCEPTION,
        FINAL_RELEASE_CUTOVER,
        EXTERNAL_GO_NO_GO_TEMPLATE,
        FINAL_RELEASE_CUTOVER_VALIDATOR,
        LONG_TERM_LOOP,
        PUBLIC_PACK_DIR / "README.md",
        PUBLIC_PACK_DIR / "workflow.md",
        PUBLIC_PACK_DIR / "fill-guide.md",
        PUBLIC_PACK_DIR / "analyst-checklist.csv",
        OPERATOR_RUNBOOK,
        PUBLIC_PACK_DIR / "external-reviewer-brief.md",
        PUBLIC_PACK_DIR / "external-review-request.md",
        PUBLIC_PACK_DIR / "external-reviewer-scorecard.csv",
        PUBLIC_PACK_DIR / "blind-review-assignment.md",
        G05_SOURCE_UPGRADE,
        G05_SOURCE_ATTEMPTS,
        CRM_EXPECTATION_MAP,
        G04_HANDOFF,
        G04_INTAKE,
        G04_EVENT_WATCH_CALENDAR,
        G04_LATER_EVENT_CANDIDATE_SCREEN,
        G04_EXECUTION_TRACKER,
        G04_REFRESH_VALIDATION_STANDARD,
        CRM_G04_ASSIGNMENT,
        FOLLOW_THROUGH_REFRESH_VALIDATOR,
        FOLLOW_THROUGH_TRIGGER_TRACKER_VALIDATOR,
        G04_EVENT_WATCH_CALENDAR_VALIDATOR,
        G04_LATER_EVENT_CANDIDATE_SCREEN_VALIDATOR,
        FOLLOW_THROUGH_EXECUTION_TRACKER_VALIDATOR,
        FOLLOW_THROUGH_PACKET_BUILDER,
        FOLLOW_THROUGH_PACKET_MATRIX_VALIDATOR,
        G06_HANDOFF,
        G06_RETURN_VALIDATION_STANDARD,
        EXTERNAL_REVIEW_ASSIGNMENT_TRACKER,
        G06_REVIEWER_CANDIDATE_SCREEN,
        G06_REVIEWER_INDEPENDENCE_SCREEN,
        G06_REVIEWER_SELECTION_RUBRIC,
        EXTERNAL_REVIEW_RETURN_VALIDATOR,
        EXTERNAL_REVIEW_PACKET_VALIDATOR,
        EXTERNAL_REVIEW_ASSIGNMENT_TRACKER_VALIDATOR,
        G06_REVIEWER_CANDIDATE_SCREEN_VALIDATOR,
        G06_REVIEWER_INDEPENDENCE_SCREEN_VALIDATOR,
        G06_REVIEWER_SELECTION_RUBRIC_VALIDATOR,
        EXTERNAL_REVIEW_PACKET_BUILDER,
        EXTERNAL_REVIEW_DISPATCH_PACKET_VALIDATOR,
        G06_DISPATCH_READINESS_CHECKLIST,
        G06_DISPATCH_READINESS_VALIDATOR,
        EXTERNAL_RELEASE_ACTION_QUEUE,
        EXTERNAL_RELEASE_ACTION_QUEUE_VALIDATOR,
        LONG_TERM_VALIDATOR_REGRESSION_TEST,
        LONG_TERM_RELEASE_CHECK_RUNNER,
        VALIDATION_CASE_SET_VALIDATOR,
        RECENT_THEME_SELECTION_VALIDATOR,
        TRIAL_THEME_MATRIX_VALIDATOR,
        THEME_SELECTION_REFRESH_AUDIT,
        THEME_SELECTION_REFRESH_AUDIT_VALIDATOR,
        PUBLIC_RELEASE_FRESHNESS_VALIDATOR,
        PUBLIC_WORKFLOW_PACK_VALIDATOR,
        INSTITUTIONAL_RELEASE_BUNDLE_VALIDATOR,
        INSTITUTIONAL_RELEASE_PACKET_BUILDER,
        OBJECTIVE_READINESS_AUDIT,
        OBJECTIVE_READINESS_VALIDATOR,
        GOAL_COMPLETION_AUDIT,
        GOAL_COMPLETION_AUDIT_VALIDATOR,
        RELEASE_VERIFICATION_COMMAND_MANIFEST,
        RELEASE_VERIFICATION_COMMAND_MANIFEST_VALIDATOR,
        EXTERNAL_REVIEW_RESULTS_TEMPLATE,
        EXTERNAL_REVIEW_INTAKE,
        POWER_CONTRACT_REGULATORY_TEMPLATE,
        STABLECOIN_RESERVE_REGULATORY_TEMPLATE,
        GOVERNMENT_PROCUREMENT_PROGRAM_TEMPLATE,
        NUCLEAR_AI_POWER_CASE / "routing.md",
        NUCLEAR_AI_POWER_CASE / "evidence-log.csv",
        NUCLEAR_AI_POWER_CASE / "value-capture-map.csv",
        NUCLEAR_AI_POWER_CASE / "power-contract-regulatory-check.csv",
        NUCLEAR_AI_POWER_CASE / "value-capture-screen.md",
        NUCLEAR_AI_POWER_CASE / "workflow-scorecard.csv",
        NUCLEAR_AI_POWER_CASE / "methodology-delta.md",
        STABLECOIN_PAYMENTS_CASE / "routing.md",
        STABLECOIN_PAYMENTS_CASE / "evidence-log.csv",
        STABLECOIN_PAYMENTS_CASE / "value-capture-map.csv",
        STABLECOIN_PAYMENTS_CASE / "stablecoin-reserve-regulatory-check.csv",
        STABLECOIN_PAYMENTS_CASE / "value-capture-screen.md",
        STABLECOIN_PAYMENTS_CASE / "workflow-scorecard.csv",
        STABLECOIN_PAYMENTS_CASE / "methodology-delta.md",
        DEFENSE_AUTONOMY_CASE / "routing.md",
        DEFENSE_AUTONOMY_CASE / "evidence-log.csv",
        DEFENSE_AUTONOMY_CASE / "value-capture-map.csv",
        DEFENSE_AUTONOMY_CASE / "government-procurement-program-check.csv",
        DEFENSE_AUTONOMY_CASE / "value-capture-screen.md",
        DEFENSE_AUTONOMY_CASE / "workflow-scorecard.csv",
        DEFENSE_AUTONOMY_CASE / "methodology-delta.md",
        INSTITUTIONAL_RELEASE_NOTES,
        INSTITUTIONAL_USE_BOUNDARIES,
        INSTITUTIONAL_ADOPTION_FAQ,
    ]
    for rel_path in required_files:
        if not (root / rel_path).exists():
            issues.append(Issue("ERROR", str(rel_path), "required release artifact missing"))
    return issues


def validate_gate_tracker(
    root: Path, rows: list[dict[str, str]]
) -> tuple[list[Issue], list[str], list[str]]:
    issues: list[Issue] = []
    non_clear_gates: list[str] = []
    hard_blockers: list[str] = []
    seen = {row.get("gate_id", "").strip(): row for row in rows}

    for gate_id, gate_name in REQUIRED_GATES.items():
        row = seen.get(gate_id)
        if not row:
            issues.append(Issue("ERROR", gate_id, f"missing required gate `{gate_name}`"))
            continue
        if row.get("gate", "").strip() != gate_name:
            issues.append(
                Issue(
                    "ERROR",
                    gate_id,
                    f"expected gate `{gate_name}`, got `{row.get('gate', '').strip()}`",
                )
            )

    for row in rows:
        gate_id = row.get("gate_id", "").strip()
        required = row.get("required_for_external_release", "").strip().lower()
        status = row.get("current_status", "").strip()
        evidence_path = row.get("evidence_path", "").strip()
        blocker = row.get("remaining_blocker", "").strip()
        next_action = row.get("next_action", "").strip()

        if required not in {"yes", "no"}:
            issues.append(Issue("ERROR", gate_id, "`required_for_external_release` must be yes/no"))
        if status not in EXTERNAL_CLEAR_STATUSES and status not in INTERNAL_READY_STATUSES:
            issues.append(Issue("WARN", gate_id, f"unrecognized current_status `{status}`"))
        if not evidence_exists(root, evidence_path):
            issues.append(Issue("ERROR", gate_id, f"evidence path missing: {evidence_path}"))
        if required == "yes" and status not in EXTERNAL_CLEAR_STATUSES:
            non_clear_gates.append(gate_id)
            if not blocker:
                issues.append(Issue("ERROR", gate_id, "blocking gate has empty remaining_blocker"))
            if not next_action:
                issues.append(Issue("ERROR", gate_id, "blocking gate has empty next_action"))
            if gate_id in KNOWN_HARD_BLOCKER_GATES:
                hard_blockers.append(gate_id)

    return issues, non_clear_gates, hard_blockers


def validate_release_decision(root: Path, hard_blockers: list[str]) -> list[Issue]:
    issues: list[Issue] = []
    if not (root / PUBLIC_DECISION).exists():
        return issues

    text = read_text(root, PUBLIC_DECISION)
    has_external_not_ready = "release_status: not_ready_external_release" in text
    has_internal_candidate = "internal_status: candidate_internal_release" in text
    if hard_blockers and not has_external_not_ready:
        issues.append(
            Issue(
                "ERROR",
                str(PUBLIC_DECISION),
                "blocking gates exist but release_status is not not_ready_external_release",
            )
        )
    if not has_internal_candidate:
        issues.append(
            Issue(
                "ERROR",
                str(PUBLIC_DECISION),
                "missing internal_status: candidate_internal_release",
            )
        )

    for gate_id in KNOWN_HARD_BLOCKER_GATES:
        if gate_id in hard_blockers and f"`{gate_id}`" not in text:
            issues.append(
                Issue("ERROR", str(PUBLIC_DECISION), f"blocking gate {gate_id} not named")
            )
    return issues


def validate_operating_loop(root: Path) -> list[Issue]:
    issues: list[Issue] = []
    if not (root / LONG_TERM_LOOP).exists():
        return issues

    text = read_text(root, LONG_TERM_LOOP)
    required_markers = [
        "candidate_internal_release",
        "not final external release",
        "theme-to-company-handoff",
        "six-lens-test",
        "expectation-map",
        "ordinary-vs-workflow-delta",
        "refresh-plan",
        "Release Status",
        "Stop Rules",
    ]
    for marker in required_markers:
        if marker not in text:
            issues.append(Issue("ERROR", str(LONG_TERM_LOOP), f"missing marker `{marker}`"))
    return issues


def validate_public_pack(root: Path) -> list[Issue]:
    issues: list[Issue] = []
    readme = root / PUBLIC_PACK_DIR / "README.md"
    if not readme.exists():
        return issues

    text = readme.read_text(encoding="utf-8")
    for marker in ("follow-through refresh", "expectation map", "external reviewer"):
        if marker not in text.lower():
            issues.append(
                Issue("ERROR", str(PUBLIC_PACK_DIR / "README.md"), f"missing `{marker}` limit")
            )
    overlay_checks = [
        (PUBLIC_PACK_DIR / "README.md", "power-contract-regulatory-check.csv"),
        (PUBLIC_PACK_DIR / "workflow.md", "Power Contract / Regulatory Quality"),
        (PUBLIC_PACK_DIR / "fill-guide.md", "Power Contract / Regulatory Check"),
        (PUBLIC_PACK_DIR / "template-inventory.md", "power-contract-regulatory-check.csv"),
        (PUBLIC_PACK_DIR / "analyst-checklist.csv", "power_contract_regulatory"),
        (LONG_TERM_LOOP, "power-contract-regulatory-check.csv"),
        (POWER_CONTRACT_REGULATORY_TEMPLATE, "interconnection_or_grid_status"),
        (PUBLIC_PACK_DIR / "README.md", "stablecoin-reserve-regulatory-check.csv"),
        (PUBLIC_PACK_DIR / "workflow.md", "Stablecoin Reserve / Regulatory Quality"),
        (PUBLIC_PACK_DIR / "fill-guide.md", "Stablecoin Reserve / Regulatory Check"),
        (PUBLIC_PACK_DIR / "template-inventory.md", "stablecoin-reserve-regulatory-check.csv"),
        (PUBLIC_PACK_DIR / "analyst-checklist.csv", "stablecoin_reserve_regulatory"),
        (LONG_TERM_LOOP, "stablecoin-reserve-regulatory-check.csv"),
        (STABLECOIN_RESERVE_REGULATORY_TEMPLATE, "reserve_yield_sensitivity"),
        (PUBLIC_PACK_DIR / "README.md", "government-procurement-program-check.csv"),
        (PUBLIC_PACK_DIR / "workflow.md", "Government Procurement / Program Quality"),
        (PUBLIC_PACK_DIR / "fill-guide.md", "Government Procurement / Program Check"),
        (PUBLIC_PACK_DIR / "template-inventory.md", "government-procurement-program-check.csv"),
        (PUBLIC_PACK_DIR / "analyst-checklist.csv", "government_procurement_program"),
        (LONG_TERM_LOOP, "government-procurement-program-check.csv"),
        (GOVERNMENT_PROCUREMENT_PROGRAM_TEMPLATE, "program_of_record_status"),
    ]
    for rel_path, marker in overlay_checks:
        path = root / rel_path
        if not path.exists():
            issues.append(Issue("ERROR", str(rel_path), "required power/regulatory overlay file missing"))
            continue
        if marker not in path.read_text(encoding="utf-8"):
            issues.append(Issue("ERROR", str(rel_path), f"missing power/regulatory overlay marker `{marker}`"))
    return issues


def validate_cross_case_validation(root: Path) -> list[Issue]:
    issues: list[Issue] = []

    matrix_path = root / CROSS_CASE_VALIDATION_MATRIX
    overlay_path = root / OVERLAY_COVERAGE_AUDIT
    summary_path = root / CROSS_CASE_VALIDATION_SUMMARY

    required_cases = {
        "ETN_2026",
        "VRT_2026",
        "CRM_2026",
        "LLY_2026",
        "TDOC_2020_2022",
        "PTON_2020_2022",
        "HUMANOID_ROBOTICS_2026",
        "NUCLEAR_AI_POWER_2026",
        "STABLECOIN_PAYMENTS_2026",
        "DEFENSE_AUTONOMY_2026",
    }
    required_overlays = {
        "long-term-expectation-map",
        "theme-value-capture-screen",
        "product-monetization-map",
        "pull-forward-check",
        "payer-access-net-price-check",
        "hardware-subscription-mix-check",
        "backlog-quality-check",
        "acquisition-value-capture-check",
        "cash-flow-quality-check",
        "power-contract-regulatory-check",
        "stablecoin-reserve-regulatory-check",
        "government-procurement-program-check",
        "source-gap-refresh",
        "follow-through-refresh",
    }

    if not matrix_path.exists():
        issues.append(Issue("ERROR", str(CROSS_CASE_VALIDATION_MATRIX), "cross-case validation matrix missing"))
    else:
        try:
            with matrix_path.open(newline="", encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
        except Exception as exc:
            rows = []
            issues.append(Issue("ERROR", str(CROSS_CASE_VALIDATION_MATRIX), f"could not parse CSV: {exc}"))
        required_columns = {
            "case_id",
            "case_type",
            "primary_lens_tested",
            "ordinary_research_failure_mode",
            "workflow_decision",
            "actionability_change",
            "overlay_or_patch_created",
            "remaining_public_release_caveat",
            "next_refresh_trigger",
        }
        header = set(rows[0].keys()) if rows else set()
        missing = sorted(required_columns - header)
        if missing:
            issues.append(Issue("ERROR", str(CROSS_CASE_VALIDATION_MATRIX), f"missing columns: {missing}"))
        seen_cases = {row.get("case_id", "").strip() for row in rows}
        missing_cases = sorted(required_cases - seen_cases)
        if missing_cases:
            issues.append(Issue("ERROR", str(CROSS_CASE_VALIDATION_MATRIX), f"missing cases: {missing_cases}"))
        for i, row in enumerate(rows, start=2):
            if not (row.get("ordinary_research_failure_mode") or "").strip():
                issues.append(Issue("ERROR", str(CROSS_CASE_VALIDATION_MATRIX), f"row {i} missing ordinary failure mode"))
            if not (row.get("remaining_public_release_caveat") or "").strip():
                issues.append(Issue("ERROR", str(CROSS_CASE_VALIDATION_MATRIX), f"row {i} missing public release caveat"))

    if not overlay_path.exists():
        issues.append(Issue("ERROR", str(OVERLAY_COVERAGE_AUDIT), "overlay coverage audit missing"))
    else:
        try:
            with overlay_path.open(newline="", encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
        except Exception as exc:
            rows = []
            issues.append(Issue("ERROR", str(OVERLAY_COVERAGE_AUDIT), f"could not parse CSV: {exc}"))
        required_columns = {
            "overlay_or_template",
            "triggered_by_cases",
            "workflow_pack_locations",
            "status",
            "remaining_gap",
            "external_release_use",
        }
        header = set(rows[0].keys()) if rows else set()
        missing = sorted(required_columns - header)
        if missing:
            issues.append(Issue("ERROR", str(OVERLAY_COVERAGE_AUDIT), f"missing columns: {missing}"))
        seen_overlays = {row.get("overlay_or_template", "").strip() for row in rows}
        missing_overlays = sorted(required_overlays - seen_overlays)
        if missing_overlays:
            issues.append(Issue("ERROR", str(OVERLAY_COVERAGE_AUDIT), f"missing overlays: {missing_overlays}"))

    if not summary_path.exists():
        issues.append(Issue("ERROR", str(CROSS_CASE_VALIDATION_SUMMARY), "cross-case validation summary missing"))
    else:
        text = summary_path.read_text(encoding="utf-8")
        for marker in ("G04", "G06", "internal institutional candidate", "What It Does Not Prove"):
            if marker not in text:
                issues.append(Issue("ERROR", str(CROSS_CASE_VALIDATION_SUMMARY), f"missing marker `{marker}`"))
    return issues


def validate_historical_backtest_archive(root: Path) -> list[Issue]:
    issues: list[Issue] = []
    audit_path = root / HISTORICAL_BACKTEST_ARCHIVE_AUDIT
    standard_path = root / HISTORICAL_BACKTEST_PUBLICATION_STANDARD

    required_pairs = {
        ("TDOC_2020_2022", "peak_price"),
        ("TDOC_2020_2022", "peak_date_share_count"),
        ("TDOC_2020_2022", "peak_enterprise_value"),
        ("TDOC_2020_2022", "consensus_expectations"),
        ("TDOC_2020_2022", "earnings_transcript_archive"),
        ("TDOC_2020_2022", "filing_backup"),
        ("PTON_2020_2022", "peak_price"),
        ("PTON_2020_2022", "peak_date_share_count"),
        ("PTON_2020_2022", "peak_enterprise_value"),
        ("PTON_2020_2022", "consensus_expectations"),
        ("PTON_2020_2022", "earnings_transcript_archive"),
        ("PTON_2020_2022", "filing_backup"),
    }

    if not audit_path.exists():
        issues.append(Issue("ERROR", str(HISTORICAL_BACKTEST_ARCHIVE_AUDIT), "historical archive audit missing"))
    else:
        try:
            with audit_path.open(newline="", encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
        except Exception as exc:
            rows = []
            issues.append(Issue("ERROR", str(HISTORICAL_BACKTEST_ARCHIVE_AUDIT), f"could not parse CSV: {exc}"))
        required_columns = {
            "case_id",
            "source_requirement",
            "current_status",
            "current_evidence_path",
            "public_grade_requirement",
            "release_decision_impact",
            "next_action",
        }
        header = set(rows[0].keys()) if rows else set()
        missing = sorted(required_columns - header)
        if missing:
            issues.append(Issue("ERROR", str(HISTORICAL_BACKTEST_ARCHIVE_AUDIT), f"missing columns: {missing}"))
        seen_pairs = {
            (row.get("case_id", "").strip(), row.get("source_requirement", "").strip())
            for row in rows
        }
        missing_pairs = sorted(required_pairs - seen_pairs)
        if missing_pairs:
            issues.append(Issue("ERROR", str(HISTORICAL_BACKTEST_ARCHIVE_AUDIT), f"missing source rows: {missing_pairs}"))
        blocking_rows = [
            row
            for row in rows
            if row.get("release_decision_impact", "").strip() == "blocks_external_example"
        ]
        if not blocking_rows:
            issues.append(
                Issue(
                    "ERROR",
                    str(HISTORICAL_BACKTEST_ARCHIVE_AUDIT),
                    "audit should preserve blocking rows until transcript/consensus gaps are closed",
                )
            )
        for i, row in enumerate(rows, start=2):
            status = row.get("current_status", "").strip()
            impact = row.get("release_decision_impact", "").strip()
            evidence_path = row.get("current_evidence_path", "").strip()
            if status not in {"improved", "partial", "incomplete", "complete"}:
                issues.append(Issue("ERROR", str(HISTORICAL_BACKTEST_ARCHIVE_AUDIT), f"row {i} invalid current_status `{status}`"))
            if impact not in {"can_use_internally_with_caveat", "blocks_external_example", "public_grade"}:
                issues.append(Issue("ERROR", str(HISTORICAL_BACKTEST_ARCHIVE_AUDIT), f"row {i} invalid release_decision_impact `{impact}`"))
            if evidence_path:
                candidate = (root / VALIDATION_DIR / evidence_path).resolve()
                if not candidate.exists():
                    issues.append(Issue("ERROR", str(HISTORICAL_BACKTEST_ARCHIVE_AUDIT), f"row {i} missing evidence path: {evidence_path}"))

    if not standard_path.exists():
        issues.append(Issue("ERROR", str(HISTORICAL_BACKTEST_PUBLICATION_STANDARD), "historical publication standard missing"))
    else:
        text = standard_path.read_text(encoding="utf-8")
        for marker in ("Peak price", "consensus", "transcript", "blocks_external_example", "not be used as fully public-grade"):
            if marker.lower() not in text.lower():
                issues.append(Issue("ERROR", str(HISTORICAL_BACKTEST_PUBLICATION_STANDARD), f"missing marker `{marker}`"))
    return issues


def validate_external_reviewer_bundle(root: Path) -> list[Issue]:
    issues: list[Issue] = []
    manifest = root / EXTERNAL_REVIEWER_BUNDLE
    if not manifest.exists():
        return [Issue("ERROR", str(EXTERNAL_REVIEWER_BUNDLE), "external reviewer bundle manifest missing")]

    try:
        with manifest.open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    except Exception as exc:
        return [Issue("ERROR", str(EXTERNAL_REVIEWER_BUNDLE), f"could not parse CSV: {exc}")]

    required_columns = {"bundle_section", "path", "send_to_reviewer", "required", "notes"}
    header = set(rows[0].keys()) if rows else set()
    missing = sorted(required_columns - header)
    if missing:
        issues.append(Issue("ERROR", str(EXTERNAL_REVIEWER_BUNDLE), f"missing columns: {missing}"))
    if not rows:
        issues.append(Issue("ERROR", str(EXTERNAL_REVIEWER_BUNDLE), "manifest has no rows"))
        return issues

    sent_required = 0
    one_of_count = 0
    has_do_not_send = False
    for i, row in enumerate(rows, start=2):
        rel_value = (row.get("path") or "").strip()
        send = (row.get("send_to_reviewer") or "").strip()
        required = (row.get("required") or "").strip()
        section = (row.get("bundle_section") or "").strip()
        if send not in {"yes", "no", "optional"}:
            issues.append(Issue("ERROR", str(EXTERNAL_REVIEWER_BUNDLE), f"row {i} invalid send_to_reviewer `{send}`"))
        if required not in {"yes", "no", "one_of"}:
            issues.append(Issue("ERROR", str(EXTERNAL_REVIEWER_BUNDLE), f"row {i} invalid required `{required}`"))
        if section == "internal_do_not_send":
            has_do_not_send = True
            if send != "no":
                issues.append(Issue("ERROR", str(EXTERNAL_REVIEWER_BUNDLE), f"row {i} internal_do_not_send must have send_to_reviewer=no"))
        if send == "yes" and required == "yes":
            sent_required += 1
        if send == "yes" and required == "one_of":
            one_of_count += 1
        if rel_value:
            candidate = (root / VALIDATION_DIR / rel_value).resolve()
            if (send == "yes" or required in {"yes", "one_of"}) and not candidate.exists():
                issues.append(Issue("ERROR", str(EXTERNAL_REVIEWER_BUNDLE), f"row {i} missing bundle path: {rel_value}"))

    if sent_required < 10:
        issues.append(Issue("ERROR", str(EXTERNAL_REVIEWER_BUNDLE), "too few required reviewer bundle files"))
    if one_of_count < 1:
        issues.append(Issue("ERROR", str(EXTERNAL_REVIEWER_BUNDLE), "manifest needs at least one assignable case"))
    if not has_do_not_send:
        issues.append(Issue("ERROR", str(EXTERNAL_REVIEWER_BUNDLE), "manifest must define internal_do_not_send rows"))
    return issues


def validate_institutional_release_package(root: Path) -> list[Issue]:
    issues: list[Issue] = []
    manifest = root / INSTITUTIONAL_RELEASE_BUNDLE
    if not manifest.exists():
        return [Issue("ERROR", str(INSTITUTIONAL_RELEASE_BUNDLE), "institutional release manifest missing")]

    try:
        with manifest.open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    except Exception as exc:
        return [Issue("ERROR", str(INSTITUTIONAL_RELEASE_BUNDLE), f"could not parse CSV: {exc}")]

    required_columns = {
        "bundle_section",
        "path",
        "include_in_external_release",
        "required",
        "release_phase",
        "notes",
    }
    header = set(rows[0].keys()) if rows else set()
    missing = sorted(required_columns - header)
    if missing:
        issues.append(Issue("ERROR", str(INSTITUTIONAL_RELEASE_BUNDLE), f"missing columns: {missing}"))
    if not rows:
        issues.append(Issue("ERROR", str(INSTITUTIONAL_RELEASE_BUNDLE), "manifest has no rows"))
        return issues

    required_included = 0
    has_internal_boundary = False
    for i, row in enumerate(rows, start=2):
        rel_value = (row.get("path") or "").strip()
        include = (row.get("include_in_external_release") or "").strip()
        required = (row.get("required") or "").strip()
        section = (row.get("bundle_section") or "").strip()
        phase = (row.get("release_phase") or "").strip()

        if include not in {"yes", "no", "optional"}:
            issues.append(
                Issue("ERROR", str(INSTITUTIONAL_RELEASE_BUNDLE), f"row {i} invalid include_in_external_release `{include}`")
            )
        if required not in {"yes", "no"}:
            issues.append(Issue("ERROR", str(INSTITUTIONAL_RELEASE_BUNDLE), f"row {i} invalid required `{required}`"))
        if phase not in {"external_release_only", "external_release_optional", "template_only", "internal_only"}:
            issues.append(Issue("ERROR", str(INSTITUTIONAL_RELEASE_BUNDLE), f"row {i} invalid release_phase `{phase}`"))
        if section == "internal_do_not_send":
            has_internal_boundary = True
            if include != "no":
                issues.append(Issue("ERROR", str(INSTITUTIONAL_RELEASE_BUNDLE), f"row {i} internal_do_not_send must not be included"))
        if include == "yes" and required == "yes":
            required_included += 1
        if rel_value:
            candidate = (root / VALIDATION_DIR / rel_value).resolve()
            if required == "yes" and not candidate.exists():
                issues.append(Issue("ERROR", str(INSTITUTIONAL_RELEASE_BUNDLE), f"row {i} missing release path: {rel_value}"))

    if required_included < 12:
        issues.append(Issue("ERROR", str(INSTITUTIONAL_RELEASE_BUNDLE), "too few required institutional release files"))
    if not has_internal_boundary:
        issues.append(Issue("ERROR", str(INSTITUTIONAL_RELEASE_BUNDLE), "manifest must define internal_do_not_send rows"))

    marker_checks = [
        (
            INSTITUTIONAL_RELEASE_NOTES,
            [
                "release_status:",
                "G04",
                "G06",
                "objective_complete",
                "institutional-colleague-acceptance-checklist.csv",
                "Known Limits",
                "stale_after:",
                "must_refresh_if:",
            ],
            "release notes template must preserve release status, G04/G06/objective caveats and refresh fields",
        ),
        (
            INSTITUTIONAL_USE_BOUNDARIES,
            ["Non-Negotiable Stop Rules", "G04", "G06", "objective_complete", "not_ready_external_release"],
            "use boundaries must preserve stop rules and current release/objective limits",
        ),
        (
            INSTITUTIONAL_ADOPTION_FAQ,
            [
                "not a stock-picking shortcut",
                "source gaps",
                "G04",
                "G06",
                "institutional-colleague-acceptance-checklist.csv",
            ],
            "adoption FAQ must state non-shortcut, source-gap and gate caveats",
        ),
        (
            OPERATOR_RUNBOOK,
            [
                "G04",
                "G06",
                "objective_complete: false",
                "validate_long_term_release.py --require-external-ready",
                "validate_public_release_freshness.py",
                "validate_go_no_go_evidence_coverage.py",
                "validate_final_release_cutover.py",
                "validate_institutional_colleague_acceptance.py",
                "validate_institutional_colleague_acceptance_return.py",
                "build_external_review_packet.py --dry-run",
                "validate_external_review_dispatch_packet.py",
                "validate_g06_dispatch_readiness.py",
                "build_follow_through_packet.py --dry-run",
                "validate_follow_through_packet_matrix.py",
                "build_institutional_release_packet.py --dry-run",
                "export_ready: false",
                "stale_after:",
                "must_refresh_if:",
            ],
            "operator runbook must preserve execution commands and release boundaries",
        ),
    ]
    for rel_path, markers, message in marker_checks:
        path = root / rel_path
        if not path.exists():
            issues.append(Issue("ERROR", str(rel_path), "required institutional release file missing"))
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                issues.append(Issue("ERROR", str(rel_path), f"{message}; missing `{marker}`"))
    return issues


def validate_final_release_cutover(root: Path, rows: list[dict[str, str]], non_clear_gates: list[str]) -> list[Issue]:
    issues: list[Issue] = []
    checklist_path = root / FINAL_RELEASE_CUTOVER
    template_path = root / EXTERNAL_GO_NO_GO_TEMPLATE

    if not checklist_path.exists():
        return [Issue("ERROR", str(FINAL_RELEASE_CUTOVER), "final release cutover checklist missing")]
    if not template_path.exists():
        issues.append(Issue("ERROR", str(EXTERNAL_GO_NO_GO_TEMPLATE), "go/no-go template missing"))

    try:
        with checklist_path.open(newline="", encoding="utf-8") as f:
            checklist_rows = list(csv.DictReader(f))
    except Exception as exc:
        return [Issue("ERROR", str(FINAL_RELEASE_CUTOVER), f"could not parse CSV: {exc}")]

    required_checks = {f"cutover_{i:02d}" for i in range(1, 14)}
    seen_checks = {row.get("check_id", "").strip() for row in checklist_rows}
    missing_checks = sorted(required_checks - seen_checks)
    if missing_checks:
        issues.append(Issue("ERROR", str(FINAL_RELEASE_CUTOVER), f"missing checks: {missing_checks}"))

    decision_text = read_text(root, PUBLIC_DECISION) if (root / PUBLIC_DECISION).exists() else ""
    g10 = next((row for row in rows if row.get("gate_id", "").strip() == "G10"), None)
    release_marked_ready = (
        "release_status: ready_external_release" in decision_text
        or (g10 and g10.get("current_status", "").strip() == "ready_external_release")
    )

    if release_marked_ready:
        if non_clear_gates:
            issues.append(
                Issue(
                    "ERROR",
                    str(PUBLIC_DECISION),
                    f"release marked ready while gates remain non-clear: {','.join(non_clear_gates)}",
                )
            )
        for i, row in enumerate(checklist_rows, start=2):
            status = (row.get("status") or "").strip()
            if status not in {"pass", "accepted"}:
                issues.append(
                    Issue("ERROR", str(FINAL_RELEASE_CUTOVER), f"row {i} not pass/accepted: {status}")
                )
        go_memos = sorted((root / VALIDATION_DIR).glob("external-release-go-no-go-*.md"))
        if not go_memos:
            issues.append(Issue("ERROR", str(VALIDATION_DIR), "ready release requires external-release-go-no-go-YYYY-MM-DD.md"))
        elif not any("decision: go" in memo.read_text(encoding="utf-8") for memo in go_memos):
            issues.append(Issue("ERROR", str(VALIDATION_DIR), "ready release requires go/no-go memo with decision: go"))
    return issues


def validate_g05_source_package(root: Path, rows: list[dict[str, str]]) -> list[Issue]:
    issues: list[Issue] = []
    g05 = next((row for row in rows if row.get("gate_id", "").strip() == "G05"), None)
    if not g05:
        return issues
    if g05.get("current_status", "").strip() != "pass_public_grade":
        return issues

    checks = [
        (G05_SOURCE_UPGRADE, "MarketScreener", "G05 source upgrade must cite MarketScreener"),
        (G05_SOURCE_ATTEMPTS, "marketscreener_crm_financials", "G05 source attempts must include MarketScreener row"),
        (CRM_EXPECTATION_MAP, "16.458B MarketScreener FY2028 FCF forecast", "CRM expectation map must include FY2 FCF source"),
        (
            PUBLIC_PACK_DIR / "external-reviewer-scorecard.csv",
            "g05_source_sufficiency",
            "reviewer scorecard must include G05 source-sufficiency challenge",
        ),
        (
            PUBLIC_PACK_DIR / "external-reviewer-brief.md",
            "G05 CRM Source-Sufficiency Challenge",
            "reviewer brief must include G05 source challenge task",
        ),
    ]
    for rel_path, marker, message in checks:
        path = root / rel_path
        if not path.exists():
            issues.append(Issue("ERROR", str(rel_path), "required G05 source package file missing"))
            continue
        if marker not in path.read_text(encoding="utf-8"):
            issues.append(Issue("ERROR", str(rel_path), message))
    return issues


def validate_g04_follow_through_package(root: Path, rows: list[dict[str, str]]) -> list[Issue]:
    issues: list[Issue] = []
    g04 = next((row for row in rows if row.get("gate_id", "").strip() == "G04"), None)
    if not g04:
        return issues

    checks = [
        (G04_HANDOFF, "G04 Clearing Rule", "G04 handoff must define clearing rule"),
        (G04_HANDOFF, "validate_follow_through_refresh.py", "G04 handoff must name the follow-through validator"),
        (G04_INTAKE, "g04_01", "G04 intake checklist must include later-event check"),
        (G04_REFRESH_VALIDATION_STANDARD, "g04_clearable", "G04 validation standard must describe clearability output"),
        (
            G04_REFRESH_VALIDATION_STANDARD,
            "same later-event `source_id` values",
            "G04 validation standard must require refresh/evidence-log source-id match",
        ),
        (
            FOLLOW_THROUGH_REFRESH_VALIDATOR,
            "refresh source_ids missing from evidence log later-event rows",
            "G04 validator must reject refresh source IDs absent from evidence log",
        ),
        (
            FOLLOW_THROUGH_REFRESH_VALIDATOR,
            "REQUIRED_G04_INTAKE_REQUIREMENTS",
            "G04 validator must require complete intake coverage",
        ),
        (
            FOLLOW_THROUGH_REFRESH_VALIDATOR,
            "must select exactly one approved refresh result label",
            "G04 validator must reject multiple refresh result labels",
        ),
        (
            FOLLOW_THROUGH_REFRESH_VALIDATOR,
            "does not match cutoff",
            "G04 validator must reject original_memo_date/cutoff mismatch",
        ),
        (
            FOLLOW_THROUGH_REFRESH_VALIDATOR,
            "is not after refresh_date",
            "G04 validator must require stale_after after refresh_date",
        ),
        (
            FOLLOW_THROUGH_REFRESH_VALIDATOR,
            "downstream_updates_checked",
            "G04 validator must report downstream release-state checks",
        ),
        (
            FOLLOW_THROUGH_REFRESH_VALIDATOR,
            "public readiness audit missing",
            "G04 validator must reject missing downstream public-readiness updates",
        ),
        (FOLLOW_THROUGH_REFRESH_VALIDATOR, "follow_through_refresh_validation", "G04 validator must report validation summary"),
        (CRM_G04_ASSIGNMENT, "original_memo_cutoff: 2026-05-30", "CRM G04 assignment must define original cutoff"),
        (Path("templates/follow-through-refresh.md"), "qualifies_as_true_follow_through", "follow-through template must include qualification field"),
        (VALIDATION_DIR / "follow-through-trigger-tracker.csv", "CRM_2026", "trigger tracker must include CRM"),
        (G04_EVENT_WATCH_CALENDAR, "CRM_2026", "event watch calendar must include CRM"),
        (G04_EVENT_WATCH_CALENDAR, "blocks_external_release", "event watch calendar must preserve G04 blocker"),
        (G04_EVENT_WATCH_CALENDAR_VALIDATOR, "g04_event_watch_calendar_validation", "event watch validator must report validation summary"),
    ]
    for rel_path, marker, message in checks:
        path = root / rel_path
        if not path.exists():
            issues.append(Issue("ERROR", str(rel_path), "required G04 follow-through file missing"))
            continue
        if marker not in path.read_text(encoding="utf-8"):
            issues.append(Issue("ERROR", str(rel_path), message))

    if g04.get("current_status", "").strip() in EXTERNAL_CLEAR_STATUSES:
        evidence_path = root / g04.get("evidence_path", "").strip()
        if not evidence_path.exists():
            issues.append(Issue("ERROR", "G04", "completed G04 must point to follow-through refresh file"))
        else:
            text = evidence_path.read_text(encoding="utf-8")
            required_markers = [
                "qualifies_as_true_follow_through: yes",
                "Event occurred after original memo cutoff",
                "Before / After",
                "follow_through_gate_status: pass",
                "must_refresh_if:",
            ]
            for marker in required_markers:
                if marker not in text:
                    issues.append(
                        Issue("ERROR", str(evidence_path), f"completed G04 refresh missing `{marker}`")
                    )
            if "qualifies_as_true_follow_through: no" in text:
                issues.append(Issue("ERROR", str(evidence_path), "G04 refresh marked non-qualifying"))
    return issues


def validate_g06_review_package(root: Path, rows: list[dict[str, str]]) -> list[Issue]:
    issues: list[Issue] = []
    g06 = next((row for row in rows if row.get("gate_id", "").strip() == "G06"), None)
    if not g06:
        return issues
    g06_next_action = g06.get("next_action", "")
    for marker in (
        "G01 method-source decision",
        "theme_selection_freshness result",
        "practice_falsification result",
        "G04 readiness/false-completion results",
        "G05 source decision",
        "historical consensus exception decision",
    ):
        if marker not in g06_next_action:
            issues.append(Issue("ERROR", "G06", f"gate tracker next_action missing `{marker}`"))

    checks = [
        (G06_HANDOFF, "G06 Clearing Rule", "G06 handoff must define clearing rule"),
        (
            EXTERNAL_REVIEW_RESULTS_TEMPLATE,
            "g01_method_source_decision",
            "external review results template must capture G01 method-source decision",
        ),
        (
            EXTERNAL_REVIEW_RESULTS_TEMPLATE,
            "g05_source_decision",
            "external review results template must capture G05 source decision",
        ),
        (
            EXTERNAL_REVIEW_RESULTS_TEMPLATE,
            "g04_follow_through_readiness",
            "external review results template must capture G04 readiness result",
        ),
        (
            EXTERNAL_REVIEW_RESULTS_TEMPLATE,
            "g04_false_completion_control",
            "external review results template must capture G04 false-completion result",
        ),
        (
            EXTERNAL_REVIEW_RESULTS_TEMPLATE,
            "practice_falsification",
            "external review results template must capture practice-falsification result",
        ),
        (
            EXTERNAL_REVIEW_INTAKE,
            "intake_05",
            "external review intake checklist must include G01 method-source decision check",
        ),
        (
            EXTERNAL_REVIEW_INTAKE,
            "intake_06",
            "external review intake checklist must include theme-selection freshness check",
        ),
        (
            EXTERNAL_REVIEW_INTAKE,
            "intake_07",
            "external review intake checklist must include practice-falsification check",
        ),
        (
            EXTERNAL_REVIEW_INTAKE,
            "intake_08",
            "external review intake checklist must include G04 result check",
        ),
        (
            EXTERNAL_REVIEW_INTAKE,
            "intake_09",
            "external review intake checklist must include G05 source decision check",
        ),
        (
            PUBLIC_PACK_DIR / "blind-review-assignment.md",
            "G01 Method-Source Basis",
            "blind assignment must include G01 method-source challenge",
        ),
        (
            PUBLIC_PACK_DIR / "blind-review-assignment.md",
            "Reviewer 4: G05 CRM Source Challenge",
            "blind assignment must include G05 source challenge",
        ),
        (
            PUBLIC_PACK_DIR / "blind-review-assignment.md",
            "Reviewer 5: G04 Follow-Through Readiness",
            "blind assignment must include G04 follow-through challenge",
        ),
        (
            G06_REVIEWER_INDEPENDENCE_SCREEN,
            "screen_05",
            "G06 reviewer independence screen must preserve reviewer-assignment pending row",
        ),
        (
            G06_REVIEWER_INDEPENDENCE_SCREEN_VALIDATOR,
            "clears_g06: false",
            "G06 reviewer independence screen validator must not clear G06",
        ),
        (
            PUBLIC_PACK_DIR / "external-reviewer-brief.md",
            "G01 Method-Source Sufficiency Challenge",
            "external reviewer brief must include G01 method-source challenge",
        ),
        (
            PUBLIC_PACK_DIR / "external-reviewer-brief.md",
            "G05 CRM Source-Sufficiency Challenge",
            "external reviewer brief must include G05 source challenge",
        ),
        (
            PUBLIC_PACK_DIR / "external-review-request.md",
            "What Not To Use",
            "external review request must define independence boundary",
        ),
        (
            PUBLIC_PACK_DIR / "external-review-request.md",
            "G04 true follow-through refresh has not been completed yet",
            "external review request must state known G04 blocker",
        ),
        (
            G06_RETURN_VALIDATION_STANDARD,
            "validate_external_review_return.py",
            "G06 return validation standard must name the validator script",
        ),
        (
            G06_RETURN_VALIDATION_STANDARD,
            "results memo scorecard summary values match",
            "G06 return validation standard must require memo-scorecard consistency",
        ),
        (
            G06_RETURN_VALIDATION_STANDARD,
            "results memo reviewer and review date match",
            "G06 return validation standard must require reviewer/date consistency",
        ),
        (
            G06_RETURN_VALIDATION_STANDARD,
            "assignment tracker has the same assigned reviewer",
            "G06 return validation standard must bind return to assignment tracker",
        ),
        (
            Path("scripts/validate_external_review_assignment_tracker.py"),
            "completed state must point to external review results memo",
            "G06 assignment tracker validator must reject completed state without results memo evidence",
        ),
        (
            G06_RETURN_VALIDATION_STANDARD,
            "independence screen `screen_05` and `screen_06`",
            "G06 return validation standard must require completed independence screen rows",
        ),
        (
            G06_RETURN_VALIDATION_STANDARD,
            "all required intake requirements",
            "G06 return validation standard must require complete intake coverage",
        ),
        (
            G06_RETURN_VALIDATION_STANDARD,
            "`finding_severity` values are limited",
            "G06 return validation standard must constrain finding severity values",
        ),
        (
            G06_RETURN_VALIDATION_STANDARD,
            "`owner:` and `fix:` markers",
            "G06 return validation standard must require P1 owner/fix markers",
        ),
        (
            G06_RETURN_VALIDATION_STANDARD,
            "Findings table P0/P1 rows match",
            "G06 return validation standard must require memo findings count consistency",
        ),
        (
            EXTERNAL_REVIEW_RETURN_VALIDATOR,
            "ALLOWED_FINDING_SEVERITIES",
            "G06 return validator must enforce finding severity enum",
        ),
        (
            EXTERNAL_REVIEW_RETURN_VALIDATOR,
            "parse_findings_table",
            "G06 return validator must parse results memo findings table",
        ),
        (
            EXTERNAL_REVIEW_RETURN_VALIDATOR,
            "P1 finding required_fix missing owner:",
            "G06 return validator must enforce P1 owner marker",
        ),
        (
            EXTERNAL_REVIEW_RETURN_VALIDATOR,
            "P1 finding required_fix missing fix:",
            "G06 return validator must enforce P1 fix marker",
        ),
        (
            EXTERNAL_REVIEW_RETURN_VALIDATOR,
            "findings table P1 count does not match summary",
            "G06 return validator must enforce memo P1 count consistency",
        ),
        (
            EXTERNAL_REVIEW_RETURN_VALIDATOR,
            "g06_clearable",
            "external review return validator must report G06 clearability",
        ),
        (
            EXTERNAL_REVIEW_RETURN_VALIDATOR,
            "assigned_reviewer does not match completed scorecard reviewer",
            "external review return validator must reject assignment reviewer mismatch",
        ),
        (
            EXTERNAL_REVIEW_RETURN_VALIDATOR,
            "assignment_independence_checked",
            "external review return validator must report assignment/independence checks",
        ),
        (
            EXTERNAL_REVIEW_RETURN_VALIDATOR,
            'parser.add_argument("--assignment-tracker", required=True',
            "external review return validator must require assignment tracker input",
        ),
        (
            EXTERNAL_REVIEW_RETURN_VALIDATOR,
            'parser.add_argument("--independence-screen", required=True',
            "external review return validator must require independence screen input",
        ),
    ]
    for rel_path, marker, message in checks:
        path = root / rel_path
        if not path.exists():
            issues.append(Issue("ERROR", str(rel_path), "required G06 review package file missing"))
            continue
        if marker not in path.read_text(encoding="utf-8"):
            issues.append(Issue("ERROR", str(rel_path), message))

    if g06.get("current_status", "").strip() in EXTERNAL_CLEAR_STATUSES:
        evidence_path = root / g06.get("evidence_path", "").strip()
        if not evidence_path.exists():
            issues.append(Issue("ERROR", "G06", "completed G06 must point to review results file"))
        else:
            text = evidence_path.read_text(encoding="utf-8")
            required_markers = [
                "reviewer_independence_confirmed: true",
                "p0_findings_count: 0",
                "g01_method_source_decision:",
                "g05_source_decision:",
                "release_recommendation:",
            ]
            for marker in required_markers:
                if marker not in text:
                    issues.append(
                        Issue("ERROR", str(evidence_path), f"completed G06 result missing `{marker}`")
                    )
            if "release_recommendation: release_internal_only" in text or "release_recommendation: reject" in text:
                issues.append(
                    Issue("ERROR", str(evidence_path), "completed G06 cannot recommend internal-only or reject")
                )
            if (
                "g01_method_source_decision: require_private_material" in text
                or "g01_method_source_decision: reject_basis" in text
            ):
                issues.append(Issue("ERROR", str(evidence_path), "G01 method-source basis rejected by reviewer"))
            if "g05_source_decision: reject_source" in text:
                issues.append(Issue("ERROR", str(evidence_path), "G05 source rejected by reviewer"))
    return issues


def render_summary(
    non_clear_gates: list[str], hard_blockers: list[str], issues: list[Issue]
) -> str:
    errors = [issue for issue in issues if issue.severity == "ERROR"]
    warnings = [issue for issue in issues if issue.severity == "WARN"]
    external_ready = not non_clear_gates and not errors
    internal_candidate = (
        not errors
        and not external_ready
        and set(hard_blockers).issubset(set(KNOWN_HARD_BLOCKER_GATES))
    )
    lines = [
        "long_term_release_validation:",
        f"  external_ready: {str(external_ready).lower()}",
        f"  internal_candidate_consistent: {str(internal_candidate).lower()}",
        f"  non_clear_gates: {','.join(non_clear_gates) if non_clear_gates else 'none'}",
        f"  hard_blocking_gates: {','.join(hard_blockers) if hard_blockers else 'none'}",
        f"  errors: {len(errors)}",
        f"  warnings: {len(warnings)}",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="repository root")
    parser.add_argument(
        "--require-external-ready",
        action="store_true",
        help="exit non-zero unless all external-release gates are clear",
    )
    args = parser.parse_args()

    root = Path(args.root)
    issues = validate_required_files(root)
    rows, csv_issues = read_gate_rows(root)
    issues.extend(csv_issues)

    non_clear_gates: list[str] = []
    hard_blockers: list[str] = []
    if rows:
        gate_issues, non_clear_gates, hard_blockers = validate_gate_tracker(root, rows)
        issues.extend(gate_issues)

    issues.extend(validate_release_decision(root, hard_blockers))
    issues.extend(validate_operating_loop(root))
    issues.extend(validate_public_pack(root))
    issues.extend(validate_cross_case_validation(root))
    issues.extend(validate_historical_backtest_archive(root))
    issues.extend(validate_external_reviewer_bundle(root))
    issues.extend(validate_institutional_release_package(root))
    issues.extend(validate_final_release_cutover(root, rows, non_clear_gates))
    issues.extend(validate_g04_follow_through_package(root, rows))
    issues.extend(validate_g05_source_package(root, rows))
    issues.extend(validate_g06_review_package(root, rows))

    for issue in issues:
        print(issue.render())
    print(render_summary(non_clear_gates, hard_blockers, issues))

    has_errors = any(issue.severity == "ERROR" for issue in issues)
    if has_errors:
        return 1
    if args.require_external_ready and non_clear_gates:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
