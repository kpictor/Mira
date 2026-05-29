#!/usr/bin/env python3
"""Lightweight repository checks for open-source readiness."""

from __future__ import annotations

import csv
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_ROOT_FILES = [
    "README.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "DATA_POLICY.md",
    ".gitignore",
]

DATE_MARKERS = (
    "research_cutoff_date",
    "analysis_cutoff_date",
    "case_date",
    "release_date",
    "as_of",
)
REFRESH_MARKERS = (
    "stale_after",
    "must_refresh_if",
    "next refresh",
    "refresh after",
    "refresh policy",
    "refresh triggers",
)
DISCLAIMER_MARKERS = (
    "not_investment_advice",
    "not investment advice",
    "does not constitute investment advice",
    "不构成投资建议",
)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def has_any(text: str, markers: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(marker.lower() in lowered for marker in markers)


def validate_evidence_log(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.reader(handle)
            header = next(reader, None)
            rows = list(reader)
    except Exception as exc:  # pragma: no cover - diagnostic path
        return [f"{path}: cannot parse CSV: {exc}"]

    if not header:
        errors.append(f"{path}: missing header")
    if not rows:
        errors.append(f"{path}: no source rows")
    return errors


def validate_case(case_dir: Path) -> list[str]:
    errors: list[str] = []
    readme = case_dir / "README.md"
    evidence_log = case_dir / "evidence-log.csv"

    if not readme.exists():
        return [f"{case_dir}: missing README.md"]

    text = read_text(readme)
    if not has_any(text, DATE_MARKERS):
        errors.append(f"{readme}: missing cutoff/as-of metadata")
    if not has_any(text, REFRESH_MARKERS):
        errors.append(f"{readme}: missing refresh/staleness policy")
    if not has_any(text, DISCLAIMER_MARKERS):
        errors.append(f"{readme}: missing not-investment-advice disclaimer")

    if not evidence_log.exists():
        errors.append(f"{case_dir}: missing evidence-log.csv")
    else:
        errors.extend(validate_evidence_log(evidence_log))

    return errors


def main() -> int:
    errors: list[str] = []

    for rel_path in REQUIRED_ROOT_FILES:
        if not (ROOT / rel_path).exists():
            errors.append(f"missing required root file: {rel_path}")

    readme = ROOT / "README.md"
    if readme.exists():
        readme_text = read_text(readme)
        if not has_any(readme_text, DISCLAIMER_MARKERS):
            errors.append("README.md: missing investment disclaimer")
        if "Quickstart" not in readme_text:
            errors.append("README.md: missing Quickstart section")

    cases_dir = ROOT / "cases"
    if cases_dir.exists():
        for case_dir in sorted(path for path in cases_dir.iterdir() if path.is_dir()):
            errors.extend(validate_case(case_dir))

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
