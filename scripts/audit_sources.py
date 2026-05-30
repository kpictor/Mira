#!/usr/bin/env python3
"""Audit Mira source registry coverage against source taxonomy artifacts."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "source-registry.csv"
CLASS_MAP_PATH = ROOT / "data" / "source-class-map.csv"
COVERAGE_MATRIX_PATH = ROOT / "data" / "source-coverage-matrix.csv"

SOURCE_CLASSES = [
    "issuer_primary_disclosure",
    "regulatory_and_exchange",
    "official_macro_and_industry",
    "market_price_and_trading",
    "aggregated_financial_data",
    "consensus_and_estimates",
    "sellside_and_expert_research",
    "professional_media",
    "industry_and_supply_chain_signal",
    "social_and_community_signal",
    "local_user_material",
    "mira_derived_analysis",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> int:
    registry_rows = read_csv(REGISTRY_PATH)
    class_map_rows = read_csv(CLASS_MAP_PATH)
    coverage_rows = read_csv(COVERAGE_MATRIX_PATH)

    registry_ids = {row["source_id"] for row in registry_rows}
    mapped_ids = {row["source_id"] for row in class_map_rows}
    class_counts = Counter(row["source_class"] for row in class_map_rows)
    workflow_ids = [row["workflow"] for row in coverage_rows]

    print("# Source Audit")
    print()
    print(f"registry_records: {len(registry_rows)}")
    print(f"class_mappings: {len(class_map_rows)}")
    print(f"unmapped_registry_records: {len(registry_ids - mapped_ids)}")
    print(f"unknown_mapped_records: {len(mapped_ids - registry_ids)}")
    print(f"coverage_workflows: {len(workflow_ids)}")
    print()
    print("## Source Class Counts")
    print()
    for source_class in SOURCE_CLASSES:
        print(f"- {source_class}: {class_counts[source_class]}")
    print()
    print("## Coverage Workflows")
    print()
    for workflow in workflow_ids:
        print(f"- {workflow}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
