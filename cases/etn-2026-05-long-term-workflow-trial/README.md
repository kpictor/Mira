# ETN Long-Term Workflow Trial

- company: Eaton Corporation plc
- ticker: ETN
- task_mode: first_pass_research + methodology_live_trial
- research_object: single_equity
- market_scope: US-listed industrial / electrical equipment
- time_boundary: 3-5 year long-term thesis, evidence through 2026-05-30
- research_cutoff_date: 2026-05-30
- as_of: 2026-05-30
- primary_methodology_under_test: `long-term-integrated-thesis`
- linked_validation_program: `cases/long-term-workflow-validation-2026-05-30/`
- linked_theme: `ai_power_and_data_center_infrastructure`
- status: iteration_03_single_company_trial_seed
- not_investment_advice: true

## Trial Purpose

This case tests whether the long-term workflow can avoid a blanket bullish conclusion from a hot AI-power theme and instead force:

- theme-to-company value-capture mapping
- backlog conversion discipline
- valuation expectations guardrails
- refresh triggers tied to observable claims

## Files

- `investment-memo.md`
- `case-notes.md`
- `evidence-log.csv`
- `workflow-scorecard.csv`
- `methodology-delta.md`
- `expectation-map.csv`

## Current Verdict

The workflow materially improved conclusion discipline.

An ordinary theme memo might stop at: data-center power demand is strong, Eaton has record Electrical Americas sales and backlog, therefore ETN is a clean AI infrastructure beneficiary.

The workflow forces a weaker but better conclusion: Eaton has a credible value-capture path, but at roughly 30x 2026 adjusted EPS guidance midpoint and roughly 36x GAAP EPS guidance midpoint, the stock already prices in durable high-quality growth. The case should remain `watch_only_pending_expectation_map` until consensus, peer range, backlog conversion and margin-normalization assumptions are mapped.

The first `expectation-map.csv` is intentionally incomplete. The `source_gap` fields are part of the result, not a formatting failure.

## Refresh Conditions

- stale_after: 2026-06-30
- must_refresh_if: Q2 2026 earnings, management updates FY2026 guidance, Electrical Americas backlog/order growth decelerates, Boyd Thermal integration changes margin expectations, hyperscaler capex guidance changes, or ETN valuation multiple materially compresses or expands.
