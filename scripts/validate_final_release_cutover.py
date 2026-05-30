#!/usr/bin/env python3
"""Validate final external-release cutover controls.

This standalone validator checks whether the cutover checklist, release
decision, gate tracker and go/no-go memo are mutually consistent. In the
current internal-candidate state it should pass consistency checks while
reporting cutover_ready=false. It does not clear G04/G06.
"""

from __future__ import annotations

import csv
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATION_DIR = Path("cases/long-term-workflow-validation-2026-05-30")
CUTOVER = VALIDATION_DIR / "final-release-cutover-checklist.csv"
GATE_TRACKER = VALIDATION_DIR / "public-release-gate-tracker.csv"
PUBLIC_DECISION = VALIDATION_DIR / "public-release-decision.md"
GO_NO_GO_TEMPLATE = VALIDATION_DIR / "external-release-go-no-go-template.md"

REQUIRED_CHECKS = {f"cutover_{i:02d}" for i in range(1, 14)}
ALLOWED_CURRENT_STATUSES = {"pending", "pass", "accepted"}
EXTERNAL_CLEAR_STATUSES = {
    "pass_external",
    "pass_public_grade",
    "completed",
    "accepted",
    "ready_external_release",
}
GO_MEMO_RE = re.compile(r"^external-release-go-no-go-\d{4}-\d{2}-\d{2}\.md$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
PLACEHOLDERS = {"", "replace", "YYYY-MM-DD", "`go` | `no_go`", "draft"}


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


def external_ready() -> bool:
    result = subprocess.run(
        [sys.executable, "scripts/validate_long_term_release.py", "--require-external-ready"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    return result.returncode == 0


def scalar_from_text(text: str, key: str) -> str:
    pattern = re.compile(rf"^[ \t]*-[ \t]*{re.escape(key)}:[ \t]*(.*)[ \t]*$", re.MULTILINE)
    match = pattern.search(text)
    if not match:
        return ""
    return match.group(1).strip().strip("`")


def validate_go_memos(go_memos: list[Path]) -> tuple[list[Issue], bool]:
    issues: list[Issue] = []
    has_go_decision = False
    for memo in go_memos:
        rel_memo = memo.relative_to(ROOT)
        try:
            text = memo.read_text(encoding="utf-8")
        except Exception as exc:
            issues.append(Issue("ERROR", str(rel_memo), f"could not read go/no-go memo: {exc}"))
            continue

        decision = scalar_from_text(text, "decision")
        decision_date = scalar_from_text(text, "decision_date")
        release_owner = scalar_from_text(text, "release_owner")
        release_status = scalar_from_text(text, "release_status")
        stale_after = scalar_from_text(text, "stale_after")
        must_refresh_if = scalar_from_text(text, "must_refresh_if")

        if decision not in {"go", "no_go"}:
            issues.append(Issue("ERROR", str(rel_memo), f"invalid decision `{decision}`"))
        if decision == "go":
            has_go_decision = True
        if not DATE_RE.match(decision_date):
            issues.append(Issue("ERROR", str(rel_memo), f"invalid decision_date `{decision_date}`"))
        if release_owner in PLACEHOLDERS:
            issues.append(Issue("ERROR", str(rel_memo), "release_owner is placeholder"))
        if stale_after in PLACEHOLDERS or not DATE_RE.match(stale_after):
            issues.append(Issue("ERROR", str(rel_memo), f"invalid stale_after `{stale_after}`"))
        if must_refresh_if in PLACEHOLDERS:
            issues.append(Issue("ERROR", str(rel_memo), "must_refresh_if is placeholder"))
        if "paste final validator output here" in text:
            issues.append(Issue("ERROR", str(rel_memo), "validator output is placeholder"))
        if "replace" in text:
            issues.append(Issue("ERROR", str(rel_memo), "memo still contains `replace` placeholder"))
        if "| pending |" in text:
            issues.append(Issue("ERROR", str(rel_memo), "required evidence table still contains pending rows"))
        if "| G04 true follow-through | completed qualifying later-event refresh | pass |" not in text:
            issues.append(Issue("ERROR", str(rel_memo), "go/no-go memo missing passed G04 evidence row"))
        if "| G06 external reviewer | completed scorecard, results memo and intake checklist | pass |" not in text:
            issues.append(Issue("ERROR", str(rel_memo), "go/no-go memo missing passed G06 evidence row"))
        if "| live case reproducibility | reviewer reproduces or caveats assigned live/fresh case action label | pass |" not in text:
            issues.append(Issue("ERROR", str(rel_memo), "go/no-go memo missing passed live case evidence row"))
        if "| G01 method-source decision | reviewer accepts or caveats public method-source basis | pass |" not in text:
            issues.append(Issue("ERROR", str(rel_memo), "go/no-go memo missing passed G01 evidence row"))
        if (
            "| theme selection freshness | reviewer accepts or caveats recent-theme freshness and refresh controls | pass |"
            not in text
        ):
            issues.append(Issue("ERROR", str(rel_memo), "go/no-go memo missing passed theme selection evidence row"))
        if "| practice falsification | reviewer accepts or caveats case-grounded methodology claims | pass |" not in text:
            issues.append(Issue("ERROR", str(rel_memo), "go/no-go memo missing passed practice falsification evidence row"))
        if (
            "| methodology iteration traceability | reviewer accepts or caveats case-failure-to-patch traceability | pass |"
            not in text
        ):
            issues.append(
                Issue("ERROR", str(rel_memo), "go/no-go memo missing passed methodology iteration evidence row")
            )
        if "| ordinary-vs-workflow delta | reviewer accepts or caveats actionability delta versus ordinary memo | pass |" not in text:
            issues.append(Issue("ERROR", str(rel_memo), "go/no-go memo missing passed ordinary-vs-workflow evidence row"))
        if "| template completeness | reviewer accepts or caveats workflow template usability and completeness | pass |" not in text:
            issues.append(Issue("ERROR", str(rel_memo), "go/no-go memo missing passed template completeness evidence row"))
        if "| G05 source challenge | reviewer accepts or caveats MarketScreener FY2 FCF source | pass |" not in text:
            issues.append(Issue("ERROR", str(rel_memo), "go/no-go memo missing passed G05 evidence row"))
        if "| public example source quality | reviewer accepts or caveats source quality for public examples | pass |" not in text:
            issues.append(Issue("ERROR", str(rel_memo), "go/no-go memo missing passed public source-quality evidence row"))
        if (
            "| historical consensus exception | reviewer accepts or caveats TDOC/PTON unavailable-data exception | pass |"
            not in text
        ):
            issues.append(Issue("ERROR", str(rel_memo), "go/no-go memo missing passed historical consensus evidence row"))
        if "| operational loop handoff | release owner confirms long-term-thesis loop is final external version | pass |" not in text:
            issues.append(Issue("ERROR", str(rel_memo), "go/no-go memo missing passed operational loop evidence row"))
        if (
            "| institutional colleague acceptance | completed checklist and dated acceptance memo pass return validator | pass |"
            not in text
        ):
            issues.append(
                Issue(
                    "ERROR",
                    str(rel_memo),
                    "go/no-go memo missing passed institutional colleague acceptance evidence row",
                )
            )
        if "| release validator | `validate_long_term_release.py --require-external-ready` exits 0 | pass |" not in text:
            issues.append(Issue("ERROR", str(rel_memo), "go/no-go memo missing passed release validator evidence row"))
        if decision == "go" and release_status != "ready_external_release":
            issues.append(Issue("ERROR", str(rel_memo), "go decision requires release_status ready_external_release"))
    return issues, has_go_decision


def validate_cutover() -> tuple[list[Issue], dict[str, int | bool]]:
    issues: list[Issue] = []
    checklist_rows, checklist_issues = read_csv(CUTOVER)
    gate_rows, gate_issues = read_csv(GATE_TRACKER)
    decision_text, decision_issues = read_text(PUBLIC_DECISION)
    _template_text, template_issues = read_text(GO_NO_GO_TEMPLATE)
    issues.extend(checklist_issues)
    issues.extend(gate_issues)
    issues.extend(decision_issues)
    issues.extend(template_issues)

    stats: dict[str, int | bool] = {
        "checks": len(checklist_rows),
        "passed_or_accepted": 0,
        "pending": 0,
        "non_clear_gates": 0,
        "go_memo_present": False,
        "external_ready": False,
        "cutover_ready": False,
    }
    if checklist_issues or gate_issues or decision_issues or template_issues:
        return issues, stats

    seen_checks = {row.get("check_id", "").strip() for row in checklist_rows}
    missing_checks = sorted(REQUIRED_CHECKS - seen_checks)
    if missing_checks:
        issues.append(Issue("ERROR", str(CUTOVER), f"missing checks: {missing_checks}"))

    for i, row in enumerate(checklist_rows, start=2):
        status = row.get("status", "").strip()
        if status not in ALLOWED_CURRENT_STATUSES:
            issues.append(Issue("ERROR", str(CUTOVER), f"row {i} invalid status `{status}`"))
        if status in {"pass", "accepted"}:
            stats["passed_or_accepted"] = int(stats["passed_or_accepted"]) + 1
        if status == "pending":
            stats["pending"] = int(stats["pending"]) + 1
        for field in ("requirement", "pass_condition", "notes"):
            if not row.get(field, "").strip():
                issues.append(Issue("ERROR", str(CUTOVER), f"row {i} missing {field}"))

    non_clear_gates = [
        row.get("gate_id", "").strip()
        for row in gate_rows
        if row.get("required_for_external_release", "").strip().lower() == "yes"
        and row.get("current_status", "").strip() not in EXTERNAL_CLEAR_STATUSES
    ]
    stats["non_clear_gates"] = len(non_clear_gates)

    release_marked_ready = "release_status: ready_external_release" in decision_text
    release_marked_not_ready = "release_status: not_ready_external_release" in decision_text
    if not release_marked_ready and not release_marked_not_ready:
        issues.append(Issue("ERROR", str(PUBLIC_DECISION), "release_status must be ready_external_release or not_ready_external_release"))

    go_memos = sorted(
        path
        for path in (ROOT / VALIDATION_DIR).glob("external-release-go-no-go-*.md")
        if GO_MEMO_RE.match(path.name)
    )
    stats["go_memo_present"] = bool(go_memos)
    go_memo_issues, has_go_decision = validate_go_memos(go_memos)
    issues.extend(go_memo_issues)

    stats["external_ready"] = external_ready()
    all_checks_passed = int(stats["passed_or_accepted"]) == len(REQUIRED_CHECKS)
    stats["cutover_ready"] = bool(stats["external_ready"]) and all_checks_passed and has_go_decision

    if bool(stats["cutover_ready"]) and not release_marked_ready:
        issues.append(Issue("ERROR", str(PUBLIC_DECISION), "cutover ready but release decision is not ready_external_release"))
    if release_marked_ready and not bool(stats["cutover_ready"]):
        issues.append(Issue("ERROR", str(PUBLIC_DECISION), "release marked ready but cutover_ready is false"))
    if not bool(stats["external_ready"]) and all_checks_passed:
        issues.append(Issue("ERROR", str(CUTOVER), "all cutover checks pass while external-ready validator fails"))
    if not bool(stats["external_ready"]) and int(stats["pending"]) == 0:
        issues.append(Issue("ERROR", str(CUTOVER), "external-ready false but checklist has no pending rows"))
    if not bool(stats["external_ready"]) and has_go_decision:
        issues.append(Issue("ERROR", str(PUBLIC_DECISION), "go/no-go memo says go while external-ready validator fails"))
    if bool(stats["external_ready"]) and int(stats["non_clear_gates"]) > 0:
        issues.append(Issue("ERROR", str(GATE_TRACKER), f"external-ready true with non-clear gates: {non_clear_gates}"))

    return issues, stats


def main() -> int:
    issues, stats = validate_cutover()
    errors = [issue for issue in issues if issue.severity == "ERROR"]
    for issue in issues:
        print(issue.render())
    print("final_release_cutover_validation:")
    print(f"  cutover_ready: {str(bool(stats['cutover_ready'])).lower()}")
    print(f"  external_ready: {str(bool(stats['external_ready'])).lower()}")
    print(f"  checks: {int(stats['checks'])}")
    print(f"  passed_or_accepted: {int(stats['passed_or_accepted'])}")
    print(f"  pending: {int(stats['pending'])}")
    print(f"  non_clear_gates: {int(stats['non_clear_gates'])}")
    print(f"  go_memo_present: {str(bool(stats['go_memo_present'])).lower()}")
    print(f"  errors: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
