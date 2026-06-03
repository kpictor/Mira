# Mira Handoff Contracts

Use this contract when one Mira loop or skill passes structured context to
another. The goal is to preserve source posture and avoid silently upgrading
claims during synthesis.

## Common Fields

Every handoff should include:

- `handoff_id`
- `producer`
- `consumer`
- `research_object`
- `market_scope`
- `time_boundary`
- `as_of_date`
- `source_scope`
- `readiness_level`
- `blocking_gaps`
- `source_ids`
- `evidence_log_refs`
- `calculation_refs`
- `thesis_impact`
- `recommended_consumer_action`
- `open_items`
- `must_refresh_if`

## Evidence Record Fields

When claims are passed across modules, preserve:

- `source_id`
- `claim_area`
- `claim_type`
- `claim_text`
- `verification_status`
- `authority_level`
- `source_date`
- `as_of_date`
- `confidence`
- `evidence_category`
- `freshness_status`
- `conflict_status`
- `treatment`
- `readiness_impact`
- `upstream_sources`

## Standard Handoff Types

### `earnings_to_equity_research`

Use when an earnings analysis changes or tests a single-equity thesis.

Required additions:

- `earnings_period`
- `reported_metrics`
- `guidance_changes`
- `management_commentary`
- `market_reaction`
- `peer_readthrough`
- `expectation_delta`
- `financial_snapshot_path`
- `peer_comparison_path`

### `sec_to_research_package`

Use when SEC analysis supplies facts or conflicts for a research package.

Required additions:

- `filing_type`
- `filing_date`
- `period_end`
- `filing_url_or_path`
- `metric_table_path`
- `risk_delta_path`
- `conflicts_with_existing_sources`

### `industry_to_single_equity`

Use when an industry or concept analysis nominates companies for single-equity
research.

Required additions:

- `concept_boundary`
- `value_chain_position`
- `profit_pool_hypothesis`
- `company_shortlist_rank`
- `company_specific_thesis_seed`
- `required_company_sources`

### `macro_to_equity_overlay`

Use when macro, rates, liquidity, FX, commodity or policy work becomes an
equity overlay.

Required additions:

- `macro_variable`
- `transmission_channel`
- `market_pricing_proxy`
- `company_exposure`
- `refresh_calendar`

## Import Discipline

- Preserve producer evidence labels and add consumer notes; do not overwrite.
- Do not collapse reported, adjusted, modeled and scenario values into one
  unqualified metric.
- If `readiness_level` is `watch_only`, `not_actionable` or `needs_refresh`,
  downstream conclusions inherit that downgrade until the named gap is fixed.
- If `conflict_status` is `unresolved` or `contradicted`, downstream work must
  name the controlling source or carry the conflict forward.
