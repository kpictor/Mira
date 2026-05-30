#!/usr/bin/env python3
"""Validate recent hot-theme selection and refresh discipline together."""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_AS_OF = date(2026, 5, 30)


@dataclass
class Check:
    name: str
    args: list[str]
    required_markers: tuple[str, ...]


CHECKS = (
    Check(
        name="trial_theme_matrix_validation",
        args=["scripts/validate_trial_theme_matrix.py"],
        required_markers=("themes: 7", "source_ids_checked:", "errors: 0"),
    ),
    Check(
        name="theme_selection_refresh_audit_validation",
        args=["scripts/validate_theme_selection_refresh_audit.py"],
        required_markers=(
            "themes: 7",
            "source_ids_checked: 22",
            "refresh_triggers_checked: 7",
            "replacement_rules_checked: 7",
            "errors: 0",
        ),
    ),
)


def parse_date(value: str) -> date | None:
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def run_check(check: Check, as_of: str) -> tuple[bool, str]:
    result = subprocess.run(
        [sys.executable, *check.args, "--as-of", as_of],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=120,
    )
    output = "\n".join(part for part in (result.stdout, result.stderr) if part).strip()
    if result.returncode != 0:
        return False, f"{check.name} exited {result.returncode}:\n{output}"
    missing = [marker for marker in check.required_markers if marker not in output]
    if missing:
        return False, f"{check.name} missing markers {missing}:\n{output}"
    return True, output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--as-of", default=DEFAULT_AS_OF.isoformat(), help="as-of date YYYY-MM-DD")
    args = parser.parse_args()
    as_of = parse_date(args.as_of)
    if as_of is None:
        print(f"ERROR: --as-of: invalid date `{args.as_of}`")
        return 1

    failures: list[str] = []
    passed = 0
    for check in CHECKS:
        ok, detail = run_check(check, args.as_of)
        if ok:
            passed += 1
        else:
            failures.append(detail)

    for failure in failures:
        print(f"ERROR: {failure}")
    print("recent_theme_selection_validation:")
    print(f"  as_of: {args.as_of}")
    print(f"  component_checks: {len(CHECKS)}")
    print(f"  passed_checks: {passed}")
    print("  themes: 7")
    print("  refresh_triggers_checked: 7")
    print("  replacement_rules_checked: 7")
    print(f"  errors: {len(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
