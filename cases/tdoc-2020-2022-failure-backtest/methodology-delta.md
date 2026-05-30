# Methodology Delta From TDOC Failure Backtest

- case: TDOC 2020-2022 telehealth pull-forward
- date: 2026-05-30
- status: historical_failure_backtest_delta
- linked_methodology: `cases/long-term-methodology-2026-05-30/methodology-card.md`

## What The Backtest Added

The live trials showed the workflow could discipline current enthusiasm. TDOC tests something harder: whether the method could have downgraded a past hot thesis before the visible accounting failure.

The answer is yes, with a caveat. The original six lenses were not enough by themselves. The workflow needed the later patches:

- `market_heat_vs_thesis_maturity`
- `product_monetization_map`
- `acquisition-driven value capture`
- `valuation_expectations`

The TDOC case adds one more required patch:

- `pull_forward_vs_structural_demand`

## Required New Lens: Pull-Forward Vs Structural Demand

Use when a thesis forms during an abnormal demand shock:

- pandemic
- stimulus
- regulatory deadline
- supply shortage
- one-time replacement cycle
- interest-rate or credit shock
- inventory restocking

Required fields:

- `shock_source`
- `duration_of_shock`
- `normalized_usage_baseline`
- `post_shock_retention`
- `payer_or_budget_persistence`
- `valuation_if_growth_normalizes`

Stop rule:

- If `shock_source` is material and `normalized_usage_baseline` or `post_shock_retention` is `source_gap`, the thesis cannot be upgraded to actionability.

## What Would Have Triggered Downgrade

TDOC would have triggered downgrade before the 2022 goodwill impairment because:

- market heat was extreme
- demand shock source was COVID-19
- visit growth was usage, not normalized retention
- Livongo synergy was a strategic claim before proven ROIC
- valuation required sustained high growth and margin improvement
- normalized post-shock demand evidence was missing

## Public-Grade Gap Remaining

This backtest is not yet public-ready because:

- near-peak EV bridge and transcript support are now improved; consensus expectation data still needs licensed export or reviewer-accepted exception
- source pages should be archived or backed by SEC filing excerpts
- peer comparison is missing
- there is only one historical failure case

## Next Backtest

Recommended:

- `PTON` or `BYND`

Reason:

- These test consumer behavior, hardware/fitness or alternative protein demand normalization, and valuation expectations without being purely healthcare/pandemic-service cases.

## Refresh Conditions

- stale_after: 2026-06-30
- must_refresh_if: additional TDOC historical filings, valuation data or consensus records change the downgrade timing.
