#!/usr/bin/env python3
"""Validate the long-term workflow case set without calling release QA recursively."""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AS_OF = "2026-05-30"

VALIDATION_CASES = [
    "cases/etn-2026-05-long-term-workflow-trial",
    "cases/vrt-2026-05-long-term-workflow-trial",
    "cases/crm-2026-05-product-workflow-trial",
    "cases/lly-2026-05-glp1-workflow-dry-run",
    "cases/humanoid-robotics-2026-05-value-capture-screen",
    "cases/nuclear-ai-power-2026-05-value-capture-screen",
    "cases/stablecoin-payments-2026-05-value-capture-screen",
    "cases/defense-autonomy-drones-2026-05-value-capture-screen",
    "cases/tdoc-2020-2022-failure-backtest",
    "cases/pton-2020-2022-failure-backtest",
]


@dataclass
class Issue:
    severity: str
    subject: str
    message: str

    def render(self) -> str:
        return f"{self.severity}: {self.subject}: {self.message}"


def validate_case(case_path: str) -> Issue | None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_repo.py", case_path, "--as-of", AS_OF],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if result.returncode == 0:
        return None
    detail = "\n".join(part for part in (result.stdout, result.stderr) if part).strip()
    return Issue("ERROR", case_path, f"validate_repo failed with exit {result.returncode}: {detail}")


def main() -> int:
    issues = [issue for case_path in VALIDATION_CASES if (issue := validate_case(case_path))]
    for issue in issues:
        print(issue.render())
    print("validation_case_set:")
    print(f"  checked_cases: {len(VALIDATION_CASES)}")
    print(f"  errors: {len(issues)}")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
