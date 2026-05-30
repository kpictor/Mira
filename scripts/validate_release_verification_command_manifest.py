#!/usr/bin/env python3
"""Validate release verification command manifest.

The institutional release packet should carry a machine-readable command list
with expected current outcomes. This keeps reproducibility from living only in
runbook prose.
"""

from __future__ import annotations

import csv
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = Path("cases/long-term-workflow-validation-2026-05-30/release-verification-command-manifest.csv")
OPERATOR_RUNBOOK = Path("cases/long-term-workflow-validation-2026-05-30/public-workflow-pack/operator-runbook.md")

REQUIRED_COLUMNS = {
    "command_id",
    "command",
    "expected_exit_current",
    "purpose",
    "release_phase",
    "notes",
}

REQUIRED_COMMAND_IDS = {
    "cmd_01",
    "cmd_02",
    "cmd_03",
    "cmd_04",
    "cmd_05",
    "cmd_06",
    "cmd_07",
    "cmd_08",
    "cmd_09",
    "cmd_10",
    "cmd_11",
    "cmd_12",
}

ALLOWED_PHASES = {
    "internal_candidate",
    "release_safety",
    "completion_audit",
    "external_release_blocker",
}

RECURSIVE_SCRIPTS = {
    "scripts/run_long_term_release_checks.py",
    "scripts/test_long_term_release_validators.py",
    "scripts/validate_release_verification_command_manifest.py",
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
        with (ROOT / MANIFEST).open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    except Exception as exc:
        return [], [Issue("ERROR", str(MANIFEST), f"could not parse CSV: {exc}")]
    if not rows:
        return [], [Issue("ERROR", str(MANIFEST), "manifest has no rows")]
    missing = sorted(REQUIRED_COLUMNS - set(rows[0].keys()))
    if missing:
        return rows, [Issue("ERROR", str(MANIFEST), f"missing columns: {missing}")]
    return rows, []


def read_runbook() -> tuple[str, list[Issue]]:
    try:
        return (ROOT / OPERATOR_RUNBOOK).read_text(encoding="utf-8"), []
    except Exception as exc:
        return "", [Issue("ERROR", str(OPERATOR_RUNBOOK), f"could not read file: {exc}")]


def parse_expected_exit(value: str, row_number: int) -> tuple[int | None, Issue | None]:
    try:
        expected = int(value.strip())
    except ValueError:
        return None, Issue("ERROR", str(MANIFEST), f"row {row_number} invalid expected_exit_current `{value}`")
    if expected < 0 or expected > 255:
        return None, Issue("ERROR", str(MANIFEST), f"row {row_number} expected_exit_current out of range")
    return expected, None


def validate_command(row_number: int, command_id: str, command: str, expected_exit: int) -> tuple[Issue | None, bool]:
    try:
        parts = shlex.split(command)
    except ValueError as exc:
        return Issue("ERROR", str(MANIFEST), f"row {row_number} invalid command: {exc}"), False
    if len(parts) < 2 or parts[0] != "python3" or not parts[1].startswith("scripts/"):
        return Issue("ERROR", str(MANIFEST), f"row {row_number} command must start with `python3 scripts/...`"), False
    if parts[1] in RECURSIVE_SCRIPTS:
        return Issue("ERROR", str(MANIFEST), f"row {row_number} recursive command is not allowed: {parts[1]}"), False
    if not (ROOT / parts[1]).exists():
        return Issue("ERROR", str(MANIFEST), f"row {row_number} command script missing: {parts[1]}"), False

    result = subprocess.run([sys.executable, *parts[1:]], cwd=ROOT, text=True, capture_output=True, timeout=180)
    if result.returncode != expected_exit:
        detail = "\n".join(part for part in (result.stdout, result.stderr) if part).strip()
        return (
            Issue(
                "ERROR",
                str(MANIFEST),
                f"{command_id} exited {result.returncode}, expected {expected_exit}: {detail}",
            ),
            True,
        )
    return None, True


def external_ready() -> bool:
    result = subprocess.run(
        [sys.executable, "scripts/validate_long_term_release.py", "--require-external-ready"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=180,
    )
    return result.returncode == 0


def validate_manifest() -> tuple[list[Issue], dict[str, int | bool]]:
    issues: list[Issue] = []
    rows, row_issues = read_rows()
    issues.extend(row_issues)
    stats = {
        "commands": len(rows),
        "commands_executed": 0,
        "runbook_commands_checked": 0,
        "external_blocker_commands": 0,
        "expected_failures_checked": 0,
        "external_ready": external_ready(),
    }
    if row_issues:
        return issues, stats
    runbook_text, runbook_issues = read_runbook()
    issues.extend(runbook_issues)
    if runbook_issues:
        return issues, stats
    if "release-verification-command-manifest.csv" not in runbook_text:
        issues.append(Issue("ERROR", str(OPERATOR_RUNBOOK), "runbook must reference release-verification-command-manifest.csv"))
    if "validate_release_verification_command_manifest.py" not in runbook_text:
        issues.append(
            Issue("ERROR", str(OPERATOR_RUNBOOK), "runbook must tell release owner to run command manifest validator")
        )

    seen = {row.get("command_id", "").strip() for row in rows}
    missing_ids = sorted(REQUIRED_COMMAND_IDS - seen)
    extra_ids = sorted(seen - REQUIRED_COMMAND_IDS)
    if missing_ids:
        issues.append(Issue("ERROR", str(MANIFEST), f"missing command ids: {missing_ids}"))
    if extra_ids:
        issues.append(Issue("ERROR", str(MANIFEST), f"unexpected command ids: {extra_ids}"))

    for i, row in enumerate(rows, start=2):
        command_id = row.get("command_id", "").strip()
        command = row.get("command", "").strip()
        phase = row.get("release_phase", "").strip()
        for field in ("command_id", "command", "expected_exit_current", "purpose", "release_phase", "notes"):
            if not row.get(field, "").strip():
                issues.append(Issue("ERROR", str(MANIFEST), f"row {i} missing {field}"))
        if phase not in ALLOWED_PHASES:
            issues.append(Issue("ERROR", str(MANIFEST), f"row {i} invalid release_phase `{phase}`"))
        if phase == "external_release_blocker":
            stats["external_blocker_commands"] += 1
        expected_exit, exit_issue = parse_expected_exit(row.get("expected_exit_current", ""), i)
        if exit_issue:
            issues.append(exit_issue)
            continue
        assert expected_exit is not None
        if command not in runbook_text:
            issues.append(Issue("ERROR", str(OPERATOR_RUNBOOK), f"runbook missing manifest command `{command}`"))
        else:
            stats["runbook_commands_checked"] += 1
        if expected_exit != 0:
            stats["expected_failures_checked"] += 1
        if phase == "external_release_blocker" and not bool(stats["external_ready"]) and expected_exit == 0:
            issues.append(
                Issue(
                    "ERROR",
                    str(MANIFEST),
                    f"{command_id} external blocker command must currently have nonzero expected exit while external_ready is false",
                )
            )
        if phase == "external_release_blocker" and bool(stats["external_ready"]) and expected_exit != 0:
            issues.append(
                Issue(
                    "ERROR",
                    str(MANIFEST),
                    f"{command_id} external blocker command must have expected exit 0 once external_ready is true",
                )
            )
        command_issue, executed = validate_command(i, command_id, command, expected_exit)
        if executed:
            stats["commands_executed"] += 1
        if command_issue:
            issues.append(command_issue)

    if stats["external_blocker_commands"] < 2:
        issues.append(Issue("ERROR", str(MANIFEST), "manifest must include at least two external release blocker commands"))
    if not bool(stats["external_ready"]) and int(stats["expected_failures_checked"]) < 2:
        issues.append(Issue("ERROR", str(MANIFEST), "manifest must check current expected failures"))
    if bool(stats["external_ready"]) and int(stats["expected_failures_checked"]) != 0:
        issues.append(Issue("ERROR", str(MANIFEST), "externally ready manifest must not expect failing commands"))
    return issues, stats


def main() -> int:
    issues, stats = validate_manifest()
    errors = [issue for issue in issues if issue.severity == "ERROR"]
    for issue in issues:
        print(issue.render())
    print("release_verification_command_manifest_validation:")
    print(f"  external_ready: {str(bool(stats['external_ready'])).lower()}")
    print(f"  commands: {stats['commands']}")
    print(f"  commands_executed: {stats['commands_executed']}")
    print(f"  runbook_commands_checked: {stats['runbook_commands_checked']}")
    print(f"  external_blocker_commands: {stats['external_blocker_commands']}")
    print(f"  expected_failures_checked: {stats['expected_failures_checked']}")
    print(f"  errors: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
