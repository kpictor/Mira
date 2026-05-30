# Source Taxonomy Practice Run

- case_date: 2026-05-30
- analysis_cutoff_date: 2026-05-30
- source_boundary: `data/source-registry.csv`, `data/source-class-map.csv`, `data/source-taxonomy.md`, `data/source-coverage-matrix.csv`, `scripts/audit_sources.py`, `scripts/validate_repo.py`
- stale_after: 2026-06-29
- must_refresh_if: source registry, source taxonomy, source class map, coverage matrix, or validator rules change; new source class is introduced; any unmapped source appears
- not_investment_advice: true

## Objective

Run one full data-source governance practice using the new source taxonomy. The goal is to test whether the source classification layer is usable for institutional-style review before relying on it in formal Mira research.

## Procedure

1. Classify every current `source-registry.csv` row through `source-class-map.csv`.
2. Require each taxonomy `source_class` to have at least one registry example or an explicit exception.
3. Check workflow coverage through `source-coverage-matrix.csv`.
4. Run `scripts/audit_sources.py` for reproducible inventory statistics.
5. Run `scripts/validate_repo.py` for repository-level evidence and vocabulary gates.
6. Record durable claims in canonical `evidence-log.csv`.

## Facts

- `source-registry.csv` contains 53 source records as of this run.
- `source-class-map.csv` contains 53 mappings.
- The audit found 0 unmapped registry records and 0 mappings to unknown records.
- All 12 taxonomy source classes have at least one mapped registry example.
- `source-coverage-matrix.csv` covers 11 workflows.
- `scripts/validate_repo.py` returned 0 errors and 9 warnings. The warnings are legacy evidence-schema or stale historical-case warnings, not new source-taxonomy errors.

## Inferences

- The taxonomy layer is operational rather than descriptive only: every current source has a class, every class has a registry example, and the validator now checks source-map coverage.
- The coverage matrix is sufficient for first-pass routing across the current Mira workflows, but it does not remove the need for case-level evidence logs.
- The two newly added supply-chain and local-material source examples close the prior zero-coverage classes, but real case usage still needs claim-level evidence.

## Judgment

Source taxonomy v1 passes the go-live gate for Mira research routing and source-governance use. It is ready to support new research packages as a required pre-analysis check.

This does not mean all historical cases are migrated to canonical evidence schema. Legacy case warnings remain visible and should be handled as a separate migration workstream.

## Institutional Gate

| gate | status | evidence |
| --- | --- | --- |
| Every current source record classified | pass | 53 registry records, 53 class mappings, 0 unmapped |
| Every source class represented | pass | 12/12 source classes have mapped examples |
| Workflow source requirements documented | pass | 11 workflows in `source-coverage-matrix.csv` |
| Automated validation exists | pass | `scripts/validate_repo.py` checks source map and coverage matrix |
| Practice is reproducible | pass | `scripts/audit_sources.py` prints the inventory and workflow summary |
| Evidence trail exists | pass | canonical `evidence-log.csv` in this package |
| Known residual risk surfaced | pass | 9 legacy/stale warnings retained instead of hidden |

## Outputs

- `evidence-log.csv`: canonical evidence trail for this practice run.
- `source-class-summary.csv`: counts and go-live interpretation by source class.
- `workflow-coverage-check.csv`: coverage matrix practice gate by workflow.

## Refresh

Refresh this practice before live governance use after 2026-06-29, or immediately if any of these changes:

- A source is added to `source-registry.csv`.
- A source class is added, renamed, deprecated, or split.
- A workflow is added to Mira routing.
- Validator rules change.
- Legacy evidence migration changes the baseline warning count.
