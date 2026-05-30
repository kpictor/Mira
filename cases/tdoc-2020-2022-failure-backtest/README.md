# TDOC 2020-2022 Failure Backtest

- company: Teladoc Health, Inc.
- ticker: TDOC
- task_mode: methodology_review + historical_failure_backtest
- research_object: failed long-term thesis pattern
- market_scope: US-listed telehealth / digital health
- research_cutoff_date: 2026-05-30
- as_of: 2026-05-30
- time_boundary: 2020-2022 historical backtest, reviewed on 2026-05-30
- primary_methodology_under_test: `long-term-integrated-thesis`
- linked_validation_program: `cases/long-term-workflow-validation-2026-05-30/`
- linked_theme: telehealth / COVID pull-forward
- status: iteration_06_failure_backtest
- not_investment_advice: true

## Backtest Question

Would the current workflow have downgraded TDOC before the 2022 goodwill impairment and thesis break?

## Short Answer

Yes, but only after the latest patches from ETN/VRT/CRM are applied.

The original six-lens framework would have flagged some risk, but the stronger downgrade trigger comes from the newer patches:

- `pull_forward_vs_structural_demand`
- `product_monetization_map`
- `acquisition-driven value capture`
- `valuation_expectations`
- `market_heat_vs_thesis_maturity`

## Key Finding

TDOC was not a fake company and telehealth was not a fake product. The failure pattern was subtler:

- a real demand shock was treated as a durable adoption curve
- usage and revenue growth were treated as proof of normalized retention and economics
- the Livongo acquisition expanded the narrative faster than the measurable ROIC path
- valuation expectations required pandemic-era growth to persist
- impairment came after the market had already begun rejecting the implied growth duration

## Files

- `failure-backtest.md`
- `evidence-log.csv`
- `historical-valuation-reconstruction.csv`
- `workflow-scorecard.csv`
- `methodology-delta.md`
- `pull-forward-check.csv`

## Refresh Conditions

- stale_after: 2026-06-30
- must_refresh_if: additional primary TDOC filings, historical consensus estimates, or better peak valuation data are added.
