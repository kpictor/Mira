#!/usr/bin/env python3
"""Validate G06 external reviewer dispatch readiness.

This performs a real packet export into a temporary directory and audits the
export manifest against the reviewer bundle manifest and assignment tracker.
It proves the packet is dispatch-ready. It does not assign a reviewer, validate
a reviewer return, or clear G06.
"""

from __future__ import annotations

import csv
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATION_DIR = Path("cases/long-term-workflow-validation-2026-05-30")
MANIFEST = VALIDATION_DIR / "external-reviewer-bundle-manifest.csv"
ASSIGNMENT_TRACKER = VALIDATION_DIR / "g06-reviewer-assignment-tracker.csv"
BUILDER = Path("scripts/build_external_review_packet.py")

REQUIRED_SEND_PATHS = {
    "public-workflow-pack/README.md",
    "public-workflow-pack/workflow.md",
    "public-workflow-pack/fill-guide.md",
    "public-workflow-pack/external-reviewer-brief.md",
    "public-workflow-pack/external-review-request.md",
    "public-workflow-pack/external-reviewer-scorecard.csv",
    "public-workflow-pack/blind-review-assignment.md",
    "g06-reviewer-selection-rubric.csv",
    "public-workflow-pack/external-review-results-template.md",
    "public-workflow-pack/external-review-intake-checklist.csv",
    "g01-external-method-source-audit.csv",
    "g01-external-method-source-upgrade-2026-05-30.md",
    "trial-theme-matrix.csv",
    "theme-selection-refresh-audit.csv",
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
    "g05-fy2-fcf-source-upgrade-2026-05-30.md",
    "g05-crm-source-attempts.csv",
    "historical-consensus-source-attempts.csv",
    "historical-consensus-unavailable-data-exception-2026-05-30.md",
}

REQUIRED_SECTIONS = {
    "core_pack",
    "review_assignment",
    "review_return",
    "g01_method_source",
    "theme_selection",
    "practice_validation",
    "methodology_iteration",
    "lens_coverage",
    "g04_follow_through",
    "g05_source",
    "historical_consensus",
    "case_assignment",
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


def validate_assignment_tracker() -> list[Issue]:
    issues: list[Issue] = []
    rows, row_issues = read_csv(ASSIGNMENT_TRACKER)
    issues.extend(row_issues)
    if not rows:
        return issues + [Issue("ERROR", str(ASSIGNMENT_TRACKER), "assignment tracker has no rows")]
    ready_rows = [
        row
        for row in rows
        if row.get("gate_id", "").strip() == "G06"
        and row.get("current_status", "").strip() == "ready_to_assign_not_completed"
    ]
    if len(ready_rows) != 1:
        issues.append(Issue("ERROR", str(ASSIGNMENT_TRACKER), f"expected 1 ready-to-assign row, got {len(ready_rows)}"))
        return issues
    row = ready_rows[0]
    if row.get("reviewer_status", "").strip() != "not_assigned":
        issues.append(Issue("ERROR", str(ASSIGNMENT_TRACKER), "ready row must have reviewer_status not_assigned"))
    if row.get("assigned_reviewer", "").strip() or row.get("assigned_date", "").strip():
        issues.append(Issue("ERROR", str(ASSIGNMENT_TRACKER), "ready row cannot contain assigned reviewer/date"))
    if row.get("release_impact", "").strip() != "blocks_external_release":
        issues.append(Issue("ERROR", str(ASSIGNMENT_TRACKER), "ready row must block external release"))
    return issues


def export_packet(output_dir: Path) -> tuple[Path | None, list[Issue], str]:
    result = subprocess.run(
        [sys.executable, str(BUILDER), "--output", str(output_dir)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    output = "\n".join(part for part in (result.stdout, result.stderr) if part).strip()
    if result.returncode != 0:
        return None, [Issue("ERROR", str(BUILDER), f"packet export failed:\n{output}")], output
    manifest = output_dir / "reviewer-packet-export-manifest.csv"
    if not manifest.exists():
        return None, [Issue("ERROR", str(manifest), "export manifest missing")], output
    return manifest, [], output


def validate_export_manifest(export_manifest: Path) -> tuple[list[Issue], dict[str, int]]:
    issues: list[Issue] = []
    manifest_rows, manifest_issues = read_csv(MANIFEST)
    export_rows: list[dict[str, str]]
    try:
        with export_manifest.open(newline="", encoding="utf-8") as f:
            export_rows = list(csv.DictReader(f))
    except Exception as exc:
        return [Issue("ERROR", str(export_manifest), f"could not parse export manifest: {exc}")], {
            "send_items": 0,
            "send_files": 0,
            "send_directories": 0,
        }
    issues.extend(manifest_issues)

    send_rows = [row for row in manifest_rows if row.get("send_to_reviewer", "").strip() == "yes"]
    internal_rows = [
        row
        for row in manifest_rows
        if row.get("bundle_section", "").strip() == "internal_do_not_send"
    ]
    exported_manifest_paths = {row.get("manifest_path", "").strip() for row in export_rows}
    send_manifest_paths = {row.get("path", "").strip() for row in send_rows}

    missing_send = sorted(path for path in send_manifest_paths if path not in exported_manifest_paths)
    if missing_send:
        issues.append(Issue("ERROR", str(export_manifest), f"send_to_reviewer paths missing from export: {missing_send}"))
    extra_export = sorted(path for path in exported_manifest_paths if path not in send_manifest_paths)
    if extra_export:
        issues.append(Issue("ERROR", str(export_manifest), f"export includes non-send paths: {extra_export}"))

    missing_required = sorted(path for path in REQUIRED_SEND_PATHS if path not in exported_manifest_paths)
    if missing_required:
        issues.append(Issue("ERROR", str(export_manifest), f"required reviewer files missing: {missing_required}"))

    sent_sections = {row.get("bundle_section", "").strip() for row in send_rows}
    missing_sections = sorted(REQUIRED_SECTIONS - sent_sections)
    if missing_sections:
        issues.append(Issue("ERROR", str(MANIFEST), f"required dispatch sections missing: {missing_sections}"))

    for row in internal_rows:
        path = row.get("path", "").strip()
        if path in exported_manifest_paths:
            issues.append(Issue("ERROR", str(export_manifest), f"internal_do_not_send exported: {path}"))

    stats = {
        "send_items": len(export_rows),
        "send_files": sum(1 for row in export_rows if row.get("item_type", "") == "file"),
        "send_directories": sum(1 for row in export_rows if row.get("item_type", "") == "directory"),
    }
    if stats["send_items"] < 20:
        issues.append(Issue("ERROR", str(export_manifest), f"too few dispatch items: {stats['send_items']}"))
    return issues, stats


def main() -> int:
    issues: list[Issue] = []
    stats = {"send_items": 0, "send_files": 0, "send_directories": 0}
    with tempfile.TemporaryDirectory(prefix="mira-g06-dispatch-") as tmp_dir:
        output_dir = Path(tmp_dir) / "external-reviewer-packet"
        export_manifest, export_issues, _output = export_packet(output_dir)
        issues.extend(export_issues)
        if export_manifest:
            manifest_issues, stats = validate_export_manifest(export_manifest)
            issues.extend(manifest_issues)
    issues.extend(validate_assignment_tracker())

    errors = [issue for issue in issues if issue.severity == "ERROR"]
    for issue in issues:
        print(issue.render())
    print("external_review_dispatch_packet_validation:")
    print(f"  dispatch_ready: {str(not errors).lower()}")
    print(f"  send_items: {stats['send_items']}")
    print(f"  send_files: {stats['send_files']}")
    print(f"  send_directories: {stats['send_directories']}")
    print("  reviewer_assigned: false")
    print("  clears_g06: false")
    print(f"  errors: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
