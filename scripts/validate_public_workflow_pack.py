#!/usr/bin/env python3
"""Validate the public workflow pack for external-review consistency.

This is a packaging and usability check. It does not make the pack externally
ready; it keeps the public-facing workflow files internally consistent while
G04/G06 remain open.
"""

from __future__ import annotations

import csv
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACK = Path("cases/long-term-workflow-validation-2026-05-30/public-workflow-pack")

README = PACK / "README.md"
WORKFLOW = PACK / "workflow.md"
FILL_GUIDE = PACK / "fill-guide.md"
CHECKLIST = PACK / "analyst-checklist.csv"
TEMPLATE_INVENTORY = PACK / "template-inventory.md"
OPERATOR_RUNBOOK = PACK / "operator-runbook.md"
SOURCE_APPENDIX = PACK / "source-appendix.md"

REQUIRED_FILES = {
    README,
    WORKFLOW,
    FILL_GUIDE,
    CHECKLIST,
    TEMPLATE_INVENTORY,
    OPERATOR_RUNBOOK,
    SOURCE_APPENDIX,
}

OVERLAYS = {
    "theme-value-capture-screen.csv": {
        "workflow": "Theme-To-Company Handoff",
        "fill": "Theme Value-Capture Screen",
        "checklist": "theme_value_capture",
    },
    "product-monetization-map.csv": {
        "workflow": "Product Monetization Map",
        "fill": "Product Monetization Map",
        "checklist": "product_monetization",
    },
    "pull-forward-check.csv": {
        "workflow": "Pull-Forward Vs Structural Demand",
        "fill": "Pull-Forward Check",
        "checklist": "pull_forward",
    },
    "payer-access-net-price-check.csv": {
        "workflow": "Payer Access / Net Price",
        "fill": "Payer Access / Net Price Check",
        "checklist": "payer_access",
    },
    "hardware-subscription-mix-check.csv": {
        "workflow": "Hardware / Subscription Mix",
        "fill": "Hardware / Subscription Mix Check",
        "checklist": "hardware_subscription",
    },
    "backlog-quality-check.csv": {
        "workflow": "Backlog Quality",
        "fill": "Backlog Quality Check",
        "checklist": "backlog_quality",
    },
    "acquisition-value-capture-check.csv": {
        "workflow": "Acquisition-Driven Value Capture",
        "fill": "Acquisition Value-Capture Check",
        "checklist": "acquisition_value_capture",
    },
    "cash-flow-quality-check.csv": {
        "workflow": "Cash Flow Quality",
        "fill": "Cash-Flow Quality Check",
        "checklist": "cash_flow_quality",
    },
    "power-contract-regulatory-check.csv": {
        "workflow": "Power Contract / Regulatory Quality",
        "fill": "Power Contract / Regulatory Check",
        "checklist": "power_contract_regulatory",
    },
    "stablecoin-reserve-regulatory-check.csv": {
        "workflow": "Stablecoin Reserve / Regulatory Quality",
        "fill": "Stablecoin Reserve / Regulatory Check",
        "checklist": "stablecoin_reserve_regulatory",
    },
    "government-procurement-program-check.csv": {
        "workflow": "Government Procurement / Program Quality",
        "fill": "Government Procurement / Program Check",
        "checklist": "government_procurement_program",
    },
}

REQUIRED_DECISION_LABELS = {
    "actionable",
    "watch_only_pending_expectation_map",
    "watch_only_pending_product_monetization_map",
    "industry_map_first",
    "reject_for_now",
}

BOUNDARY_MARKERS = {
    "candidate_internal_release",
    "not final public-grade",
    "G04",
    "G06",
    "objective_complete: false",
    "stale_after:",
    "must_refresh_if:",
}

SOURCE_TRAIL_SECTIONS = {
    "### ETN": {"backlog-quality", "expectation-map"},
    "### VRT": {"cash-flow quality", "expectation burden"},
    "### CRM": {"product monetization map", "Known gaps"},
    "### LLY": {"payer access", "Known gaps"},
    "### Humanoid Robotics": {"industry_map_first", "Known gaps"},
    "### Nuclear / SMR / AI Power": {"power-contract", "Known gaps"},
    "### Stablecoin Payments": {"stablecoin reserve", "Known gaps"},
    "### Defense Autonomy / Drones / Counter-UAS": {"government procurement", "Known gaps"},
    "### TDOC": {"pull-forward", "Known gaps"},
    "### PTON": {"hardware/subscription", "Known gaps"},
}

SOURCE_APPENDIX_MARKERS = {
    "Use the highest available source",
    "Each Mira-derived calculation must list upstream sources and formula",
    "private buyside process detail remains undercovered",
    "no actionability conclusion may depend on a source gap",
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


def read_text(path: Path) -> tuple[str, list[Issue]]:
    try:
        return (ROOT / path).read_text(encoding="utf-8"), []
    except Exception as exc:
        return "", [Issue("ERROR", str(path), f"could not read file: {exc}")]


def read_checklist_sections() -> tuple[set[str], list[Issue]]:
    try:
        with (ROOT / CHECKLIST).open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    except Exception as exc:
        return set(), [Issue("ERROR", str(CHECKLIST), f"could not parse CSV: {exc}")]
    if not rows:
        return set(), [Issue("ERROR", str(CHECKLIST), "checklist has no rows")]
    required_columns = {"check_id", "section", "question", "minimum_public_grade_evidence", "status_options"}
    missing = sorted(required_columns - set(rows[0].keys()))
    if missing:
        return set(), [Issue("ERROR", str(CHECKLIST), f"missing columns: {missing}")]
    sections: set[str] = set()
    issues: list[Issue] = []
    for i, row in enumerate(rows, start=2):
        section = row.get("section", "").strip()
        sections.add(section)
        if row.get("status_options", "").strip() == "":
            issues.append(Issue("ERROR", str(CHECKLIST), f"row {i} missing status_options"))
        if "pass" not in row.get("status_options", "") or "fail" not in row.get("status_options", ""):
            issues.append(Issue("ERROR", str(CHECKLIST), f"row {i} status_options must include pass and fail"))
    return sections, issues


def external_ready() -> bool:
    result = subprocess.run(
        [sys.executable, "scripts/validate_long_term_release.py", "--require-external-ready"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    return result.returncode == 0


def markdown_h3_sections(text: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current_heading: str | None = None
    for line in text.splitlines():
        if line.startswith("### "):
            current_heading = line.strip()
            sections[current_heading] = []
            continue
        if current_heading is not None:
            sections[current_heading].append(line)
    return {heading: "\n".join(lines) for heading, lines in sections.items()}


def validate_pack() -> tuple[list[Issue], dict[str, int | bool]]:
    issues: list[Issue] = []
    stats: dict[str, int | bool] = {
        "files_checked": 0,
        "overlays_checked": 0,
        "source_sections_checked": 0,
        "external_ready": False,
    }

    for path in REQUIRED_FILES:
        if not (ROOT / path).exists():
            issues.append(Issue("ERROR", str(path), "required public pack file missing"))
        else:
            stats["files_checked"] = int(stats["files_checked"]) + 1

    readme, readme_issues = read_text(README)
    workflow, workflow_issues = read_text(WORKFLOW)
    fill_guide, fill_issues = read_text(FILL_GUIDE)
    inventory, inventory_issues = read_text(TEMPLATE_INVENTORY)
    runbook, runbook_issues = read_text(OPERATOR_RUNBOOK)
    source_appendix, source_issues = read_text(SOURCE_APPENDIX)
    checklist_sections, checklist_issues = read_checklist_sections()
    issues.extend(
        readme_issues
        + workflow_issues
        + fill_issues
        + inventory_issues
        + runbook_issues
        + source_issues
        + checklist_issues
    )
    if readme_issues or workflow_issues or fill_issues or inventory_issues or runbook_issues or source_issues or checklist_issues:
        return issues, stats
    source_sections = markdown_h3_sections(source_appendix)

    for marker in BOUNDARY_MARKERS:
        if marker not in readme and marker not in runbook:
            issues.append(Issue("ERROR", str(PACK), f"missing boundary marker `{marker}`"))
    if "Four-theme direction scan" in readme:
        issues.append(Issue("ERROR", str(README), "README still says Four-theme direction scan"))
    if "Seven-theme direction scan" not in readme:
        issues.append(Issue("ERROR", str(README), "README must describe the seven-theme direction scan"))

    for label in REQUIRED_DECISION_LABELS:
        if label not in readme:
            issues.append(Issue("ERROR", str(README), f"missing decision label `{label}`"))

    for template, markers in OVERLAYS.items():
        stats["overlays_checked"] = int(stats["overlays_checked"]) + 1
        if template not in readme:
            issues.append(Issue("ERROR", str(README), f"missing overlay template `{template}`"))
        if markers["workflow"] not in workflow:
            issues.append(Issue("ERROR", str(WORKFLOW), f"missing workflow overlay `{markers['workflow']}`"))
        if markers["fill"] not in fill_guide:
            issues.append(Issue("ERROR", str(FILL_GUIDE), f"missing fill-guide overlay `{markers['fill']}`"))
        if template not in inventory:
            issues.append(Issue("ERROR", str(TEMPLATE_INVENTORY), f"missing template inventory row `{template}`"))
        if markers["checklist"] not in checklist_sections:
            issues.append(Issue("ERROR", str(CHECKLIST), f"missing checklist section `{markers['checklist']}`"))

    for marker in SOURCE_APPENDIX_MARKERS:
        if marker not in source_appendix:
            issues.append(Issue("ERROR", str(SOURCE_APPENDIX), f"missing source appendix marker `{marker}`"))

    for section, markers in SOURCE_TRAIL_SECTIONS.items():
        stats["source_sections_checked"] = int(stats["source_sections_checked"]) + 1
        section_text = source_sections.get(section)
        if section_text is None:
            issues.append(Issue("ERROR", str(SOURCE_APPENDIX), f"missing source-trail section `{section}`"))
            continue
        for marker in markers:
            if marker not in section_text:
                issues.append(Issue("ERROR", str(SOURCE_APPENDIX), f"source appendix section `{section}` missing marker `{marker}`"))

    stats["external_ready"] = external_ready()
    if not bool(stats["external_ready"]):
        if "pack_status: external_release" in readme:
            issues.append(Issue("ERROR", str(README), "pack_status cannot be external_release while external-ready fails"))
        if "export_ready: true" in runbook:
            issues.append(Issue("ERROR", str(OPERATOR_RUNBOOK), "runbook cannot say export_ready: true while external-ready fails"))
    return issues, stats


def main() -> int:
    issues, stats = validate_pack()
    errors = [issue for issue in issues if issue.severity == "ERROR"]
    for issue in issues:
        print(issue.render())
    print("public_workflow_pack_validation:")
    print(f"  files_checked: {int(stats['files_checked'])}")
    print(f"  overlays_checked: {int(stats['overlays_checked'])}")
    print(f"  source_sections_checked: {int(stats['source_sections_checked'])}")
    print(f"  external_ready: {str(bool(stats['external_ready'])).lower()}")
    print(f"  errors: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
