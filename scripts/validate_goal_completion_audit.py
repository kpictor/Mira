#!/usr/bin/env python3
"""Validate goal-level completion audit for the long-term workflow objective.

This is stricter than release-package consistency. It maps the user's full
goal to proof requirements and prevents treating internal candidate readiness
as goal completion while G04/G06/final external release remain incomplete.
"""

from __future__ import annotations

import csv
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = Path("cases/long-term-workflow-validation-2026-05-30/goal-completion-audit.csv")

REQUIRED_COLUMNS = {
    "component_id",
    "goal_component",
    "required_evidence",
    "evidence_path",
    "verification_command",
    "current_state",
    "blocking_gate",
    "completion_effect",
    "next_action",
}

REQUIRED_COMPONENTS = {
    "GC01": "recent_hot_directions_selected",
    "GC02": "practical_cases_run",
    "GC03": "workflow_reverse_evaluated",
    "GC04": "methodology_iterated_from_failures",
    "GC05": "long_term_workflow_multi_lens",
    "GC06": "true_follow_through_proved",
    "GC07": "external_independent_review_completed",
    "GC08": "institutional_release_controls_ready",
    "GC09": "external_release_ready",
    "GC10": "public_release_freshness_control",
}

PROVED_STATES = {"proved_internal", "proved_external"}
BLOCKED_STATES = {"blocked_external"}
ALLOWED_STATES = PROVED_STATES | BLOCKED_STATES
REQUIRED_BLOCKING_GATES = {"G04", "G06"}
RECURSIVE_VERIFICATION_SCRIPTS = {
    "scripts/run_long_term_release_checks.py",
    "scripts/validate_goal_completion_audit.py",
    "scripts/validate_objective_readiness.py",
}


@dataclass
class Issue:
    severity: str
    subject: str
    message: str

    def render(self) -> str:
        return f"{self.severity}: {self.subject}: {self.message}"


def read_rows() -> tuple[list[dict[str, str]], list[Issue]]:
    try:
        with (ROOT / AUDIT).open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    except Exception as exc:
        return [], [Issue("ERROR", str(AUDIT), f"could not parse CSV: {exc}")]
    if not rows:
        return [], [Issue("ERROR", str(AUDIT), "goal completion audit has no rows")]
    missing = sorted(REQUIRED_COLUMNS - set(rows[0].keys()))
    if missing:
        return rows, [Issue("ERROR", str(AUDIT), f"missing columns: {missing}")]
    return rows, []


def external_ready() -> bool:
    result = subprocess.run(
        [sys.executable, "scripts/validate_long_term_release.py", "--require-external-ready"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    return result.returncode == 0


def validate_institutional_packet_dry_run() -> tuple[list[Issue], bool]:
    issues: list[Issue] = []
    result = subprocess.run(
        [sys.executable, "scripts/build_institutional_release_packet.py", "--dry-run"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    output = "\n".join(part for part in (result.stdout, result.stderr) if part)
    if result.returncode != 2:
        issues.append(
            Issue(
                "ERROR",
                "build_institutional_release_packet.py --dry-run",
                f"expected exit 2 while external-ready is false, got {result.returncode}",
            )
        )
    for marker in ("release_items: 40", "required_export_paths_checked: 40", "blockers: 1", "errors: 0"):
        if marker not in output:
            issues.append(
                Issue(
                    "ERROR",
                    "build_institutional_release_packet.py --dry-run",
                    f"missing dry-run marker `{marker}`",
                )
            )
    return issues, True


def expected_verification_codes(state: str, command_parts: list[str]) -> set[int]:
    if state in PROVED_STATES:
        return {0}
    if state == "blocked_external" and "--require-external-ready" in command_parts:
        return {2}
    if state == "blocked_external":
        return {0}
    return set()


def run_verification_command(
    row_number: int,
    component_id: str,
    state: str,
    command: str,
) -> tuple[Issue | None, bool]:
    try:
        parts = shlex.split(command)
    except ValueError as exc:
        return Issue("ERROR", str(AUDIT), f"row {row_number} invalid verification_command: {exc}"), False
    if len(parts) < 2 or parts[0] != "python3" or not parts[1].startswith("scripts/"):
        return (
            Issue("ERROR", str(AUDIT), f"row {row_number} verification command must be `python3 scripts/...`"),
            False,
        )
    if parts[1] in RECURSIVE_VERIFICATION_SCRIPTS:
        return (
            Issue("ERROR", str(AUDIT), f"row {row_number} verification command is recursive: {parts[1]}"),
            False,
        )
    script_path = ROOT / parts[1]
    if not script_path.exists():
        return Issue("ERROR", str(AUDIT), f"row {row_number} verification script missing: {parts[1]}"), False

    args = [sys.executable, *parts[1:]]
    expected_codes = expected_verification_codes(state, parts)
    try:
        result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True, timeout=120)
    except subprocess.TimeoutExpired:
        return Issue("ERROR", str(AUDIT), f"{component_id} verification command timed out"), True
    if result.returncode not in expected_codes:
        detail = "\n".join(part for part in (result.stdout, result.stderr) if part).strip()
        return (
            Issue(
                "ERROR",
                str(AUDIT),
                f"{component_id} verification command exited {result.returncode}, expected {sorted(expected_codes)}: {detail}",
            ),
            True,
        )
    return None, True


def validate_audit() -> tuple[list[Issue], dict[str, int | bool]]:
    issues: list[Issue] = []
    rows, row_issues = read_rows()
    issues.extend(row_issues)
    stats: dict[str, int | bool] = {
        "components": len(rows),
        "proved_internal": 0,
        "proved_external": 0,
        "blocked_external": 0,
        "verification_commands_checked": 0,
        "institutional_export_paths_checked": 0,
        "goal_complete": False,
        "external_ready": False,
    }
    if row_issues:
        return issues, stats

    seen = {row.get("component_id", "").strip(): row for row in rows}
    for component_id, component_name in REQUIRED_COMPONENTS.items():
        row = seen.get(component_id)
        if not row:
            issues.append(Issue("ERROR", component_id, f"missing goal component `{component_name}`"))
            continue
        if row.get("goal_component", "").strip() != component_name:
            issues.append(
                Issue(
                    "ERROR",
                    component_id,
                    "goal_component mismatch: "
                    f"{row.get('goal_component', '').strip()} != {component_name}",
                )
            )

    gc07 = seen.get("GC07")
    if gc07:
        required_evidence = gc07.get("required_evidence", "")
        for marker in ("G01", "theme_selection_freshness", "methodology_iteration_traceability", "G05", "historical"):
            if marker not in required_evidence:
                issues.append(Issue("ERROR", "GC07", f"required_evidence missing `{marker}` reviewer decision"))

    for i, row in enumerate(rows, start=2):
        component_id = row.get("component_id", "").strip()
        state = row.get("current_state", "").strip()
        evidence_path = row.get("evidence_path", "").strip()
        verification_command = row.get("verification_command", "").strip()
        blocking_gate = row.get("blocking_gate", "").strip()
        completion_effect = row.get("completion_effect", "").strip()

        for field in ("required_evidence", "evidence_path", "verification_command", "completion_effect", "next_action"):
            if not row.get(field, "").strip():
                issues.append(Issue("ERROR", str(AUDIT), f"row {i} missing {field}"))
        if evidence_path and not (ROOT / evidence_path).exists():
            issues.append(Issue("ERROR", str(AUDIT), f"row {i} evidence_path missing: {evidence_path}"))
        if state not in ALLOWED_STATES:
            issues.append(Issue("ERROR", str(AUDIT), f"row {i} invalid current_state `{state}`"))
            continue
        command_issue, checked = run_verification_command(i, component_id, state, verification_command)
        if checked:
            stats["verification_commands_checked"] = int(stats["verification_commands_checked"]) + 1
        if command_issue:
            issues.append(command_issue)
        if state == "proved_internal":
            stats["proved_internal"] = int(stats["proved_internal"]) + 1
            if "blocks" in completion_effect:
                issues.append(Issue("ERROR", str(AUDIT), f"{component_id} proved_internal cannot block completion"))
        if state == "proved_external":
            stats["proved_external"] = int(stats["proved_external"]) + 1
        if state == "blocked_external":
            stats["blocked_external"] = int(stats["blocked_external"]) + 1
            gates = {gate.strip() for gate in blocking_gate.split("|") if gate.strip()}
            if not gates:
                issues.append(Issue("ERROR", str(AUDIT), f"{component_id} blocked_external lacks blocking_gate"))
            if not gates <= REQUIRED_BLOCKING_GATES:
                issues.append(Issue("ERROR", str(AUDIT), f"{component_id} has unsupported blocking gates: {sorted(gates)}"))
            if "blocks" not in completion_effect:
                issues.append(Issue("ERROR", str(AUDIT), f"{component_id} blocked_external lacks blocking completion_effect"))

    stats["external_ready"] = external_ready()
    institutional_issues, institutional_checked = validate_institutional_packet_dry_run()
    issues.extend(institutional_issues)
    if institutional_checked:
        stats["institutional_export_paths_checked"] = 40
    stats["goal_complete"] = bool(stats["external_ready"]) and int(stats["blocked_external"]) == 0
    if bool(stats["external_ready"]) and int(stats["blocked_external"]) > 0:
        issues.append(Issue("ERROR", str(AUDIT), "external-ready validator passed while goal audit still has blockers"))
    if not bool(stats["external_ready"]) and int(stats["blocked_external"]) == 0:
        issues.append(Issue("ERROR", str(AUDIT), "goal audit has no blockers while external-ready validator fails"))

    return issues, stats


def main() -> int:
    issues, stats = validate_audit()
    errors = [issue for issue in issues if issue.severity == "ERROR"]
    for issue in issues:
        print(issue.render())
    print("goal_completion_audit_validation:")
    print(f"  goal_complete: {str(bool(stats['goal_complete'])).lower()}")
    print(f"  external_ready: {str(bool(stats['external_ready'])).lower()}")
    print(f"  components: {int(stats['components'])}")
    print(f"  proved_internal: {int(stats['proved_internal'])}")
    print(f"  proved_external: {int(stats['proved_external'])}")
    print(f"  blocked_external: {int(stats['blocked_external'])}")
    print(f"  verification_commands_checked: {int(stats['verification_commands_checked'])}")
    print(f"  institutional_export_paths_checked: {int(stats['institutional_export_paths_checked'])}")
    print(f"  errors: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
