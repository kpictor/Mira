"""Minimal validator for an emitted artifact bundle (ships with P1).

Checks the teeth the architecture doc moved forward from P3:

- the manifest exists, is valid JSON, and carries the required keys;
- every ``canonical_family`` is in the enum;
- every ``source_id`` is a registry source, a known adapter source, or a
  ``mira_calc__`` derived id;
- evidence / ingestion / ledger headers match the canonical schemas;
- every ledger row references a real evidence row, and every derived evidence
  row has a ledger row + non-empty ``upstream_sources`` (mirrors
  ``validate_repo.py:678``);
- every derived number carries input sources.
"""

from __future__ import annotations

import csv
import json
import os
from collections import namedtuple

from .canonical import CANONICAL_FAMILIES, POSTURES
from .emit import EVIDENCE_COLUMNS, INGESTION_COLUMNS, LEDGER_COLUMNS

Issue = namedtuple("Issue", "level msg")
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_REGISTRY = os.path.join(_REPO_ROOT, "data", "source-registry.csv")
_ADAPTER_SOURCE_IDS = {p.source_id for p in POSTURES.values()}


def validate_bundle(out_dir: str) -> list[Issue]:
    issues: list[Issue] = []
    manifest_path = os.path.join(out_dir, "dataset-manifest.json")
    if not os.path.exists(manifest_path):
        return [Issue("ERROR", f"missing dataset-manifest.json in {out_dir}")]
    try:
        manifest = json.load(open(manifest_path, encoding="utf-8"))
    except ValueError as exc:
        return [Issue("ERROR", f"manifest is not valid JSON: {exc}")]

    for key in ("ingestion_id", "source_id", "field_coverage", "calculation_ledger_required"):
        if not manifest.get(key):
            issues.append(Issue("ERROR", f"manifest missing required key: {key}"))

    for fc in manifest.get("field_coverage", []):
        fam = fc.get("canonical_family")
        if fam not in CANONICAL_FAMILIES:
            issues.append(Issue("ERROR", f"unknown canonical_family in manifest: {fam!r}"))

    registry_ids = _registry_source_ids(issues)
    ev_source_ids, derived_ids = _check_evidence(out_dir, registry_ids, issues)
    _check_ingestion(out_dir, issues)
    _check_ledger(out_dir, ev_source_ids, derived_ids, issues)
    return issues


def _registry_source_ids(issues: list[Issue]) -> set:
    try:
        with open(_REGISTRY, encoding="utf-8") as fh:
            return {row["source_id"].strip() for row in csv.DictReader(fh) if row.get("source_id")}
    except OSError:
        issues.append(Issue("WARN", f"could not read source registry at {_REGISTRY}"))
        return set()


def _check_evidence(out_dir, registry_ids, issues) -> tuple[set, set]:
    path = os.path.join(out_dir, "evidence-log.csv")
    ev_ids: set = set()
    derived_ids: set = set()
    if not os.path.exists(path):
        issues.append(Issue("ERROR", "missing evidence-log.csv"))
        return ev_ids, derived_ids
    with open(path, encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != EVIDENCE_COLUMNS:
            issues.append(Issue("ERROR", "evidence-log.csv header does not match v1.2 schema"))
        for i, row in enumerate(reader, start=2):
            sid = row.get("source_id", "").strip()
            ev_ids.add(sid)
            if row.get("claim_type") == "derived_calculation":
                derived_ids.add(sid)
                if row.get("upstream_sources", "").strip() in {"", "not_applicable", "na", "n/a"}:
                    issues.append(Issue("ERROR", f"evidence row {i}: derived_calculation needs upstream_sources"))
            _check_source_id(sid, registry_ids, i, issues)
    return ev_ids, derived_ids


def _check_source_id(sid: str, registry_ids: set, line: int, issues: list[Issue]) -> None:
    if not sid or sid.startswith("mira_calc__"):
        return
    if sid in registry_ids:
        return
    if sid in _ADAPTER_SOURCE_IDS:
        issues.append(Issue("WARN", f"evidence row {line}: source_id '{sid}' is a known adapter "
                                    f"source but not yet in source-registry.csv"))
    else:
        issues.append(Issue("ERROR", f"evidence row {line}: unknown source_id '{sid}'"))


def _check_ingestion(out_dir, issues) -> None:
    path = os.path.join(out_dir, "ingestion-log.csv")
    if not os.path.exists(path):
        issues.append(Issue("ERROR", "missing ingestion-log.csv"))
        return
    with open(path, encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != INGESTION_COLUMNS:
            issues.append(Issue("ERROR", "ingestion-log.csv header does not match schema"))


def _check_ledger(out_dir, ev_source_ids, derived_ids, issues) -> None:
    path = os.path.join(out_dir, "calculation-ledger.csv")
    ledgered_refs: set = set()
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            if reader.fieldnames != LEDGER_COLUMNS:
                issues.append(Issue("ERROR", "calculation-ledger.csv header does not match schema"))
            for i, row in enumerate(reader, start=2):
                ref = row.get("evidence_log_ref", "").strip()
                ledgered_refs.add(ref)
                if ref not in ev_source_ids:
                    issues.append(Issue("ERROR", f"ledger row {i}: evidence_log_ref '{ref}' has no evidence row"))
                if not row.get("input_sources", "").strip():
                    issues.append(Issue("ERROR", f"ledger row {i}: derived number missing input_sources"))
    # every derived evidence row must be backed by a ledger row
    for sid in derived_ids - ledgered_refs:
        issues.append(Issue("ERROR", f"derived evidence row '{sid}' has no calculation-ledger row"))
