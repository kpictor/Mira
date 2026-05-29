# Evidence Log Validation Report

- report_date: 2026-05-29
- validator: `scripts/validate_repo.py --report-only`
- schema_ref: `data/evidence-log-schema.md`; `data/controlled-vocabulary.md`
- status: strict_validator_green_with_legacy_warnings

## Summary

Current repository state after introducing canonical evidence schema, `legacy_evidence_schema` handling and controlled vocabulary checks:

- strict errors: 0
- warnings: 9 as of 2026-05-29
- new templates: canonical
- migrated canonical cases:
  - `cases/nvts-2026-05/evidence-log.csv`
  - `cases/aapl-2026-04/evidence-log.csv`
  - `cases/crwv-2026-05/evidence-log.csv`
  - `cases/wolf-2026-05/evidence-log.csv`
- remaining historical cases: explicitly marked `legacy_evidence_schema: true`
- controlled vocabulary: enforced for `decision_type`, thesis `state`, `research_action`, `setup_type`, `position_sizing_implication` and PM index state/actionability tokens
- PM index stale dates: date-like `stale_after` cells are checked against the validation date

This report intentionally does not hide legacy drift. Existing legacy case outputs remain useful as historical research artifacts, but they should not be treated as canonical evidence-log examples until migrated.

## Legacy Findings

### Source-Record Schema Used As Evidence Log

These remaining files use source-registry style columns inside `evidence-log.csv` and are now explicitly marked `legacy_evidence_schema: true`:

- `cases/a-share-etf-options-underlyings-2026-05-26/evidence-log.csv`
- `cases/ai-hardware-bottleneck-watchlist-2026-05/evidence-log.csv`
- `cases/etf-discovery-2026-05-09/evidence-log.csv`
- `cases/etf-listing-analysis-2026-05-09/evidence-log.csv`

Required action:

- Rename or migrate source-level records to `source-log.csv`, then create canonical claim-level `evidence-log.csv`.

### Missing Claim-Level Required Fields

These files are old claim logs but lack canonical claim fields such as `claim_text`, `source_speaker`, `verification_status`, `authority_level`, `source_date`, `url_or_path`, or `upstream_sources`, and are now explicitly marked `legacy_evidence_schema: true`:

- `cases/abf-2026-05/evidence-log.csv`
- `cases/cohr-2026-05/evidence-log.csv`
- `cases/eose-2026-05/evidence-log.csv`
- `cases/figr-2026-05/evidence-log.csv`

Required action:

- Migrate active cases first.
- If a historical case remains unmigrated, mark it as legacy and avoid using it as a sample package.

### Canonical Sample Created

These cases have been migrated to the canonical claim-level schema:

- `cases/nvts-2026-05/evidence-log.csv`: current earnings flagship sample.
- `cases/aapl-2026-04/evidence-log.csv`: legacy public sample now has canonical evidence rows.
- `cases/crwv-2026-05/evidence-log.csv`: earnings/event-delta sample now has canonical evidence rows.
- `cases/wolf-2026-05/evidence-log.csv`: narrative-heavy weak-evidence sample now has canonical evidence rows.

## Methodology Adoption Correction

`memory/methodologies/adopted.md` previously marked methods adopted based on design/sample work. This has been corrected, so the validator no longer reports methodology adoption warnings:

- no method is currently `adopted`
- `framework-routing` moved back to `trial`
- `supply-chain` moved back to `trial`
- future adoption requires real cases plus follow-through or postmortem

## Migration Priority

1. ETF discovery/listing cases, with `source-log.csv` split from claim evidence
2. AI hardware bottleneck watchlist and A-share ETF/options underlyings discovery packages
3. Remaining earnings cases: COHR, EOSE, FIGR
4. ABF industry package

## Acceptance Bar

The repo should not claim a case is a standard sample unless:

- `python3 scripts/validate_repo.py` passes for that case
- every durable conclusion can trace to canonical evidence rows
- weak claim types are downgraded
- L6 or derived calculations include upstream sources
- event or thesis outputs identify expectation variable impact
