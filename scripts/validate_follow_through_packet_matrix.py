#!/usr/bin/env python3
"""Validate G04 follow-through packet exports for every execution candidate.

This is a readiness check only. It proves each tracked live case can generate
an execution packet with required G04 control files when a later material event
arrives. It does not validate a completed refresh and does not clear G04.
"""

from __future__ import annotations

import csv
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRACKER = Path("cases/long-term-workflow-validation-2026-05-30/g04-follow-through-execution-tracker.csv")
BUILDER = Path("scripts/build_follow_through_packet.py")
DEFAULT_CASE = "CRM_2026"
REQUIRED_CASES = {"ETN_2026", "VRT_2026", "CRM_2026", "LLY_2026"}
REQUIRED_EXPORTED_SOURCES = {
    "cases/long-term-workflow-validation-2026-05-30/follow-through-trigger-tracker.csv",
    "cases/long-term-workflow-validation-2026-05-30/g04-follow-through-event-watch-calendar.csv",
    "cases/long-term-workflow-validation-2026-05-30/g04-later-event-candidate-screen.csv",
    "cases/long-term-workflow-validation-2026-05-30/g04-follow-through-execution-tracker.csv",
    "cases/long-term-workflow-validation-2026-05-30/g04-follow-through-intake-checklist.csv",
    "scripts/validate_g04_later_event_candidate_screen.py",
    "scripts/validate_follow_through_refresh.py",
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
        with (ROOT / TRACKER).open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    except Exception as exc:
        return [], [Issue("ERROR", str(TRACKER), f"could not parse CSV: {exc}")]
    if not rows:
        return [], [Issue("ERROR", str(TRACKER), "execution tracker has no rows")]
    required = {"case_id", "current_status", "packet_status", "event_status", "refresh_status"}
    missing = sorted(required - set(rows[0].keys()))
    if missing:
        return rows, [Issue("ERROR", str(TRACKER), f"missing columns: {missing}")]
    return rows, []


def export_case(case_id: str, output_dir: Path) -> tuple[bool, str]:
    args = [sys.executable, str(BUILDER)]
    if case_id != DEFAULT_CASE:
        args.extend(["--case-id", case_id])
    args.extend(["--output", str(output_dir)])
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    output = "\n".join(part for part in (result.stdout, result.stderr) if part).strip()
    return result.returncode == 0, output


def read_export_manifest(output_dir: Path) -> tuple[list[dict[str, str]], list[Issue]]:
    manifest = output_dir / "follow-through-packet-export-manifest.csv"
    try:
        with manifest.open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    except Exception as exc:
        return [], [Issue("ERROR", str(manifest), f"could not parse export manifest: {exc}")]
    if not rows:
        return [], [Issue("ERROR", str(manifest), "export manifest has no rows")]
    required = {"item_role", "source_path", "export_path"}
    missing = sorted(required - set(rows[0].keys()))
    if missing:
        return rows, [Issue("ERROR", str(manifest), f"missing columns: {missing}")]
    return rows, []


def validate_exported_packet(case_id: str, output_dir: Path) -> list[Issue]:
    issues: list[Issue] = []
    rows, manifest_issues = read_export_manifest(output_dir)
    issues.extend(manifest_issues)
    if manifest_issues:
        return issues

    sources = {row.get("source_path", "").strip() for row in rows}
    missing_sources = sorted(REQUIRED_EXPORTED_SOURCES - sources)
    if missing_sources:
        issues.append(Issue("ERROR", case_id, f"packet missing required sources: {missing_sources}"))

    summary = output_dir / "follow-through-packet-summary.md"
    if not summary.exists():
        issues.append(Issue("ERROR", case_id, "packet summary missing"))
    else:
        summary_text = summary.read_text(encoding="utf-8")
        for marker in (f"case_id: `{case_id}`", "This packet does not clear G04 by itself."):
            if marker not in summary_text:
                issues.append(Issue("ERROR", case_id, f"packet summary missing `{marker}`"))

    for row in rows:
        export_path = row.get("export_path", "").strip()
        if export_path and not (output_dir / export_path).exists():
            issues.append(Issue("ERROR", case_id, f"manifest export path missing: {export_path}"))
    return issues


def validate_matrix() -> tuple[list[Issue], dict[str, int]]:
    issues: list[Issue] = []
    rows, row_issues = read_rows()
    issues.extend(row_issues)
    stats = {
        "tracked_cases": 0,
        "packet_ready_cases": 0,
        "default_case_checked": 0,
    }
    if row_issues:
        return issues, stats

    runnable_rows = [
        row
        for row in rows
        if row.get("current_status", "").strip()
        in {"ready_to_execute_waiting_event", "ready_to_refresh"}
    ]
    seen_cases = {row.get("case_id", "").strip() for row in runnable_rows}
    missing_cases = sorted(REQUIRED_CASES - seen_cases)
    if missing_cases:
        issues.append(Issue("ERROR", str(TRACKER), f"missing runnable cases: {missing_cases}"))

    for row in runnable_rows:
        case_id = row.get("case_id", "").strip()
        packet_status = row.get("packet_status", "").strip()
        event_status = row.get("event_status", "").strip()
        refresh_status = row.get("refresh_status", "").strip()
        stats["tracked_cases"] += 1

        if case_id not in REQUIRED_CASES:
            issues.append(Issue("ERROR", str(TRACKER), f"unsupported case_id `{case_id}`"))
            continue
        if packet_status != "packet_export_ready":
            issues.append(Issue("ERROR", case_id, f"packet_status must be packet_export_ready, got `{packet_status}`"))
        if event_status not in {"waiting_for_later_event", "later_event_available"}:
            issues.append(Issue("ERROR", case_id, f"event_status not packet-runnable: `{event_status}`"))
        if refresh_status not in {"not_started", "drafted_not_validated"}:
            issues.append(Issue("ERROR", case_id, f"refresh_status not packet-runnable: `{refresh_status}`"))

        with tempfile.TemporaryDirectory(prefix=f"mira-g04-packet-{case_id.lower()}-") as tmp_dir:
            output_dir = Path(tmp_dir) / "packet"
            ok, output = export_case(case_id, output_dir)
            if ok:
                issues.extend(validate_exported_packet(case_id, output_dir))
        if not ok:
            issues.append(Issue("ERROR", case_id, f"packet export failed:\n{output}"))
            continue
        expected_marker = f"selected_case: {case_id}"
        if expected_marker not in output:
            issues.append(Issue("ERROR", case_id, f"packet export missing `{expected_marker}`"))
            continue
        if not [issue for issue in issues if issue.severity == "ERROR" and issue.subject == case_id]:
            stats["packet_ready_cases"] += 1
        if case_id == DEFAULT_CASE:
            stats["default_case_checked"] = 1

    if stats["default_case_checked"] != 1:
        issues.append(Issue("ERROR", DEFAULT_CASE, "default CRM_2026 packet dry-run was not checked"))
    return issues, stats


def main() -> int:
    issues, stats = validate_matrix()
    errors = [issue for issue in issues if issue.severity == "ERROR"]
    for issue in issues:
        print(issue.render())
    print("follow_through_packet_matrix_validation:")
    print(f"  matrix_ready: {str(not errors).lower()}")
    print(f"  tracked_cases: {stats['tracked_cases']}")
    print(f"  packet_ready_cases: {stats['packet_ready_cases']}")
    print(f"  default_case_checked: {str(bool(stats['default_case_checked'])).lower()}")
    print(f"  errors: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
