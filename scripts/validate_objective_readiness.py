#!/usr/bin/env python3
"""Validate objective-level readiness for the long-term workflow goal.

This maps the user's full objective to concrete evidence and prevents calling
the project complete while G04/G06 or final external release remain incomplete.
"""

from __future__ import annotations

import csv
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = Path("cases/long-term-workflow-validation-2026-05-30/objective-readiness-audit.csv")

REQUIRED_REQUIREMENTS = {
    "OBJ01": "select_recent_hot_directions",
    "OBJ02": "run_practical_cases",
    "OBJ03": "reverse_evaluate_workflow",
    "OBJ04": "iterate_methodology_from_case_failures",
    "OBJ05": "cover_multi_lens_long_term_method",
    "OBJ06": "prove_follow_through_loop",
    "OBJ07": "external_independent_reviewer",
    "OBJ08": "institutional_colleague_release_controls",
    "OBJ09": "public_grade_final_release",
    "OBJ10": "public_release_freshness_control",
}

BLOCKING_STATUSES = {
    "incomplete_g04",
    "incomplete_g06",
    "incomplete_external_release",
}

PASSING_INTERNAL_STATUSES = {
    "met_internal",
}
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


def read_rows(path: Path) -> tuple[list[dict[str, str]], list[Issue]]:
    try:
        with (ROOT / path).open(newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f)), []
    except Exception as exc:
        return [], [Issue("ERROR", str(path), f"could not parse CSV: {exc}")]


def run_release_validator(require_external_ready: bool = False) -> subprocess.CompletedProcess[str]:
    args = [sys.executable, "scripts/validate_long_term_release.py"]
    if require_external_ready:
        args.append("--require-external-ready")
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True)


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


def expected_verification_codes(status: str, command_parts: list[str]) -> set[int]:
    if status in PASSING_INTERNAL_STATUSES:
        return {0}
    if status in BLOCKING_STATUSES and "--require-external-ready" in command_parts:
        return {2}
    if status in BLOCKING_STATUSES:
        return {0}
    return set()


def run_verification_command(
    row_number: int,
    req_id: str,
    status: str,
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
    expected_codes = expected_verification_codes(status, parts)
    try:
        result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True, timeout=120)
    except subprocess.TimeoutExpired:
        return Issue("ERROR", str(AUDIT), f"{req_id} verification command timed out"), True
    if result.returncode not in expected_codes:
        detail = "\n".join(part for part in (result.stdout, result.stderr) if part).strip()
        return (
            Issue(
                "ERROR",
                str(AUDIT),
                f"{req_id} verification command exited {result.returncode}, expected {sorted(expected_codes)}: {detail}",
            ),
            True,
        )
    return None, True


def validate_audit() -> tuple[list[Issue], dict[str, int | bool]]:
    issues: list[Issue] = []
    rows, csv_issues = read_rows(AUDIT)
    issues.extend(csv_issues)
    stats: dict[str, int | bool] = {
        "requirements": 0,
        "met_internal": 0,
        "blocking": 0,
        "verification_commands_checked": 0,
        "institutional_export_paths_checked": 0,
        "objective_complete": False,
        "external_ready": False,
    }
    if not rows:
        issues.append(Issue("ERROR", str(AUDIT), "objective readiness audit has no rows"))
        return issues, stats

    required_columns = {
        "requirement_id",
        "objective_requirement",
        "completion_status",
        "evidence_path",
        "verification_command",
        "proof_standard",
        "current_evidence",
        "next_action",
        "release_impact",
    }
    missing_columns = sorted(required_columns - set(rows[0].keys()))
    if missing_columns:
        issues.append(Issue("ERROR", str(AUDIT), f"missing columns: {missing_columns}"))
        return issues, stats

    seen = {row.get("requirement_id", "").strip(): row for row in rows}
    for req_id, req_name in REQUIRED_REQUIREMENTS.items():
        row = seen.get(req_id)
        if not row:
            issues.append(Issue("ERROR", req_id, f"missing objective requirement `{req_name}`"))
            continue
        if row.get("objective_requirement", "").strip() != req_name:
            issues.append(
                Issue(
                    "ERROR",
                    req_id,
                    "objective requirement mismatch: "
                    f"{row.get('objective_requirement', '').strip()} != {req_name}",
                )
            )

    obj07 = seen.get("OBJ07")
    if obj07:
        proof_standard = obj07.get("proof_standard", "")
        for marker in (
            "G01 method-source",
            "theme_selection_freshness",
            "methodology_iteration_traceability",
            "G05 source",
            "historical consensus",
        ):
            if marker not in proof_standard:
                issues.append(Issue("ERROR", "OBJ07", f"proof_standard missing `{marker}` reviewer decision"))

    for i, row in enumerate(rows, start=2):
        req_id = row.get("requirement_id", "").strip()
        status = row.get("completion_status", "").strip()
        evidence_path = row.get("evidence_path", "").strip()
        verification_command = row.get("verification_command", "").strip()
        release_impact = row.get("release_impact", "").strip()
        for field in ("proof_standard", "current_evidence", "next_action", "verification_command"):
            if not row.get(field, "").strip():
                issues.append(Issue("ERROR", str(AUDIT), f"row {i} missing {field}"))
        if evidence_path and not (ROOT / evidence_path).exists():
            issues.append(Issue("ERROR", str(AUDIT), f"row {i} missing evidence path: {evidence_path}"))
        if status in PASSING_INTERNAL_STATUSES:
            stats["met_internal"] = int(stats["met_internal"]) + 1
            command_issue, checked = run_verification_command(i, req_id, status, verification_command)
            if checked:
                stats["verification_commands_checked"] = int(stats["verification_commands_checked"]) + 1
            if command_issue:
                issues.append(command_issue)
        elif status in BLOCKING_STATUSES:
            stats["blocking"] = int(stats["blocking"]) + 1
            command_issue, checked = run_verification_command(i, req_id, status, verification_command)
            if checked:
                stats["verification_commands_checked"] = int(stats["verification_commands_checked"]) + 1
            if command_issue:
                issues.append(command_issue)
            if "blocks" not in release_impact:
                issues.append(
                    Issue(
                        "ERROR",
                        str(AUDIT),
                        f"row {i} {req_id} blocking status lacks blocking release_impact",
                    )
                )
        else:
            issues.append(Issue("ERROR", str(AUDIT), f"row {i} invalid completion_status `{status}`"))

    stats["requirements"] = len(rows)

    release_internal = run_release_validator(False)
    if release_internal.returncode != 0:
        issues.append(
            Issue(
                "ERROR",
                "validate_long_term_release.py",
                f"internal validator failed with exit {release_internal.returncode}",
            )
        )

    release_external = run_release_validator(True)
    stats["external_ready"] = release_external.returncode == 0
    institutional_issues, institutional_checked = validate_institutional_packet_dry_run()
    issues.extend(institutional_issues)
    if institutional_checked:
        stats["institutional_export_paths_checked"] = 40
    stats["objective_complete"] = stats["external_ready"] and int(stats["blocking"]) == 0
    if stats["external_ready"] and int(stats["blocking"]) > 0:
        issues.append(
            Issue(
                "ERROR",
                str(AUDIT),
                "external validator passed while objective audit still has blocking rows",
            )
        )
    if not stats["external_ready"] and int(stats["blocking"]) == 0:
        issues.append(
            Issue(
                "ERROR",
                str(AUDIT),
                "objective audit has no blocking rows but external validator is not ready",
            )
        )
    return issues, stats


def main() -> int:
    issues, stats = validate_audit()
    errors = [issue for issue in issues if issue.severity == "ERROR"]
    for issue in issues:
        print(issue.render())
    print("objective_readiness_validation:")
    print(f"  objective_complete: {str(bool(stats['objective_complete'])).lower()}")
    print(f"  external_ready: {str(bool(stats['external_ready'])).lower()}")
    print(f"  requirements: {int(stats['requirements'])}")
    print(f"  met_internal: {int(stats['met_internal'])}")
    print(f"  blocking: {int(stats['blocking'])}")
    print(f"  verification_commands_checked: {int(stats['verification_commands_checked'])}")
    print(f"  institutional_export_paths_checked: {int(stats['institutional_export_paths_checked'])}")
    print(f"  errors: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
