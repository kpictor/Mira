# Workflow Patch Proposal After Iteration 01

- date: 2026-05-30
- target_methodology: `long-term-integrated-thesis`
- status: proposed_patch

## Patch 1: Theme-To-Company Handoff

Before using the long-term workflow for a single company that comes from a hot theme, require:

- `theme_definition`
- `theme_maturity`: `early_narrative`, `early_revenue`, `scaling_revenue`, `margin_conversion`, `mature_cycle`
- `value_chain_nodes`
- `public_company_expressions`
- `investable_purity`: `low`, `medium`, `high`
- `value_capture_path`
- `why_this_company_not_just_the_theme`
- `read_through_type`: `direct`, `supplier`, `customer`, `substitute`, `victim`, `enabler`, `derivative`
- `handoff_decision`: `single_equity_research`, `industry_map_first`, `watch_only`, `reject_for_now`

Stop rule:

- If `value_capture_path` is unclear, do not write a single-company long-term thesis. Build an industry map or watchlist instead.

## Patch 2: Product Evidence Ladder

Use this ladder before accepting product-led long-term claims:

1. `concept`
2. `demo`
3. `pilot`
4. `paid_deployment`
5. `repeat_usage`
6. `expansion`
7. `retention`
8. `pricing_power`
9. `margin_conversion`

Stop rule:

- Do not treat `demo`, `pilot` or management anecdotes as proof of durable product-market fit.

## Patch 3: Valuation Expectations Guardrail

Replace generic valuation language with:

- `valuation_anchor_type`
- `anchor_quality`: `high`, `medium`, `low`, `source_gap`
- `implied_assumption_range`
- `what_must_go_right`
- `what_is_already_priced`
- `false_precision_warning`
- `downside_path`
- `valuation_refresh_trigger`

Stop rule:

- If `anchor_quality = source_gap`, the workflow may still produce a research thesis but not an actionability conclusion.

## Patch 4: Direct Vs Read-Through Classification

For themes like GLP-1, AI power and humanoid robotics, classify exposure before research:

- `direct`
- `supplier`
- `customer`
- `substitute`
- `victim`
- `enabler`
- `derivative`

Stop rule:

- Do not mix direct beneficiaries and second-order read-throughs in one conclusion.

## Patch 5: Market Heat Vs Thesis Maturity

Add:

- `market_heat`: `low`, `medium`, `high`, `extreme`
- `thesis_maturity`: `unproven`, `early_evidence`, `scaling`, `financial_conversion`, `mature`
- `heat_maturity_gap`: `none`, `moderate`, `large`, `extreme`

Stop rule:

- If heat is `high` or `extreme` and thesis maturity is `unproven` or `early_evidence`, conclusion must be downgraded unless valuation expectations are explicitly conservative.

## Adoption Impact

These patches should be applied to the methodology card before live single-company trials. They do not make the method adopted. They make the next trial more falsifiable.
