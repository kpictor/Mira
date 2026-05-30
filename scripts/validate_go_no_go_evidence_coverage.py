#!/usr/bin/env python3
"""Validate that public release gates are covered by go/no-go evidence rows.

This guards against drift: if a release gate is added to the gate tracker,
the final go/no-go template and cutover validator must require explicit
passed evidence before a final external release can be signed.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATION_DIR = Path("cases/long-term-workflow-validation-2026-05-30")
GATE_TRACKER = VALIDATION_DIR / "public-release-gate-tracker.csv"
GO_NO_GO_TEMPLATE = VALIDATION_DIR / "external-release-go-no-go-template.md"
CUTOVER_VALIDATOR = Path("scripts/validate_final_release_cutover.py")


@dataclass(frozen=True)
class EvidenceRequirement:
    key: str
    row_label: str
    required_evidence: str
    error_marker: str

    @property
    def template_row(self) -> str:
        return f"| {self.row_label} | {self.required_evidence} | pending | replace |"

    @property
    def passed_row(self) -> str:
        return f"| {self.row_label} | {self.required_evidence} | pass |"


EVIDENCE_REQUIREMENTS = {
    "g01_method_source": EvidenceRequirement(
        "g01_method_source",
        "G01 method-source decision",
        "reviewer accepts or caveats public method-source basis",
        "go/no-go memo missing passed G01 evidence row",
    ),
    "live_case_reproducibility": EvidenceRequirement(
        "live_case_reproducibility",
        "live case reproducibility",
        "reviewer reproduces or caveats assigned live/fresh case action label",
        "go/no-go memo missing passed live case evidence row",
    ),
    "historical_consensus_exception": EvidenceRequirement(
        "historical_consensus_exception",
        "historical consensus exception",
        "reviewer accepts or caveats TDOC/PTON unavailable-data exception",
        "go/no-go memo missing passed historical consensus evidence row",
    ),
    "g04_true_follow_through": EvidenceRequirement(
        "g04_true_follow_through",
        "G04 true follow-through",
        "completed qualifying later-event refresh",
        "go/no-go memo missing passed G04 evidence row",
    ),
    "g05_source_challenge": EvidenceRequirement(
        "g05_source_challenge",
        "G05 source challenge",
        "reviewer accepts or caveats MarketScreener FY2 FCF source",
        "go/no-go memo missing passed G05 evidence row",
    ),
    "g06_external_reviewer": EvidenceRequirement(
        "g06_external_reviewer",
        "G06 external reviewer",
        "completed scorecard, results memo and intake checklist",
        "go/no-go memo missing passed G06 evidence row",
    ),
    "theme_selection_freshness": EvidenceRequirement(
        "theme_selection_freshness",
        "theme selection freshness",
        "reviewer accepts or caveats recent-theme freshness and refresh controls",
        "go/no-go memo missing passed theme selection evidence row",
    ),
    "practice_falsification": EvidenceRequirement(
        "practice_falsification",
        "practice falsification",
        "reviewer accepts or caveats case-grounded methodology claims",
        "go/no-go memo missing passed practice falsification evidence row",
    ),
    "methodology_iteration_traceability": EvidenceRequirement(
        "methodology_iteration_traceability",
        "methodology iteration traceability",
        "reviewer accepts or caveats case-failure-to-patch traceability",
        "go/no-go memo missing passed methodology iteration evidence row",
    ),
    "ordinary_vs_workflow_delta": EvidenceRequirement(
        "ordinary_vs_workflow_delta",
        "ordinary-vs-workflow delta",
        "reviewer accepts or caveats actionability delta versus ordinary memo",
        "go/no-go memo missing passed ordinary-vs-workflow evidence row",
    ),
    "template_completeness": EvidenceRequirement(
        "template_completeness",
        "template completeness",
        "reviewer accepts or caveats workflow template usability and completeness",
        "go/no-go memo missing passed template completeness evidence row",
    ),
    "public_example_source_quality": EvidenceRequirement(
        "public_example_source_quality",
        "public example source quality",
        "reviewer accepts or caveats source quality for public examples",
        "go/no-go memo missing passed public source-quality evidence row",
    ),
    "release_validator": EvidenceRequirement(
        "release_validator",
        "release validator",
        "`validate_long_term_release.py --require-external-ready` exits 0",
        "go/no-go memo missing passed release validator evidence row",
    ),
    "operational_loop_handoff": EvidenceRequirement(
        "operational_loop_handoff",
        "operational loop handoff",
        "release owner confirms long-term-thesis loop is final external version",
        "go/no-go memo missing passed operational loop evidence row",
    ),
    "institutional_colleague_acceptance": EvidenceRequirement(
        "institutional_colleague_acceptance",
        "institutional colleague acceptance",
        "completed checklist and dated acceptance memo pass return validator",
        "go/no-go memo missing passed institutional colleague acceptance evidence row",
    ),
}


REQUIRED_GATE_COVERAGE = {
    "G01": ("g01_method_source",),
    "G02": ("live_case_reproducibility",),
    "G03": ("historical_consensus_exception",),
    "G04": ("g04_true_follow_through",),
    "G05": ("g05_source_challenge",),
    "G06": (
        "g06_external_reviewer",
        "theme_selection_freshness",
        "practice_falsification",
        "methodology_iteration_traceability",
    ),
    "G07": ("ordinary_vs_workflow_delta", "practice_falsification"),
    "G08": ("template_completeness",),
    "G09": ("public_example_source_quality", "historical_consensus_exception"),
    "G10": ("release_validator",),
    "G11": ("operational_loop_handoff",),
}

NON_GATE_REQUIRED_ROWS = ("institutional_colleague_acceptance",)


def read_required_gates() -> tuple[list[str], list[str]]:
    errors: list[str] = []
    try:
        with (ROOT / GATE_TRACKER).open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    except Exception as exc:
        return [], [f"could not parse {GATE_TRACKER}: {exc}"]

    gates = [
        row.get("gate_id", "").strip()
        for row in rows
        if row.get("required_for_external_release", "").strip().lower() == "yes"
    ]
    if not gates:
        errors.append(f"{GATE_TRACKER} has no required external-release gates")
    duplicates = sorted({gate for gate in gates if gates.count(gate) > 1})
    if duplicates:
        errors.append(f"{GATE_TRACKER} duplicate required gates: {duplicates}")
    return gates, errors


def main() -> int:
    errors: list[str] = []
    required_gates, gate_errors = read_required_gates()
    errors.extend(gate_errors)

    try:
        template_text = (ROOT / GO_NO_GO_TEMPLATE).read_text(encoding="utf-8")
    except Exception as exc:
        template_text = ""
        errors.append(f"could not read {GO_NO_GO_TEMPLATE}: {exc}")

    try:
        validator_text = (ROOT / CUTOVER_VALIDATOR).read_text(encoding="utf-8")
    except Exception as exc:
        validator_text = ""
        errors.append(f"could not read {CUTOVER_VALIDATOR}: {exc}")

    missing_gate_mappings = [gate for gate in required_gates if gate not in REQUIRED_GATE_COVERAGE]
    if missing_gate_mappings:
        errors.append(f"required gates missing go/no-go evidence mapping: {missing_gate_mappings}")

    stale_gate_mappings = [gate for gate in REQUIRED_GATE_COVERAGE if gate not in required_gates]
    if stale_gate_mappings:
        errors.append(f"go/no-go evidence mapping references non-required gates: {stale_gate_mappings}")

    required_evidence_keys = {
        key
        for gate in required_gates
        for key in REQUIRED_GATE_COVERAGE.get(gate, ())
    }
    required_evidence_keys.update(NON_GATE_REQUIRED_ROWS)

    unknown_keys = sorted(key for key in required_evidence_keys if key not in EVIDENCE_REQUIREMENTS)
    if unknown_keys:
        errors.append(f"go/no-go evidence mapping references unknown evidence rows: {unknown_keys}")

    evidence_rows_checked = 0
    for key in sorted(required_evidence_keys):
        requirement = EVIDENCE_REQUIREMENTS.get(key)
        if requirement is None:
            continue
        evidence_rows_checked += 1
        if requirement.template_row not in template_text:
            errors.append(f"missing go/no-go evidence row: {requirement.template_row}")
        if requirement.passed_row not in validator_text:
            errors.append(f"cutover validator missing passed-row check: {requirement.row_label}")
        if requirement.error_marker not in validator_text:
            errors.append(f"cutover validator missing error marker: {requirement.error_marker}")

    for error in errors:
        print(f"ERROR: {error}")
    print("go_no_go_evidence_coverage_validation:")
    print(f"  required_gates_checked: {len(required_gates)}")
    print(f"  evidence_rows_checked: {evidence_rows_checked}")
    print(f"  non_gate_required_rows_checked: {len(NON_GATE_REQUIRED_ROWS)}")
    print(f"  cutover_error_markers_checked: {evidence_rows_checked}")
    print(f"  errors: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
