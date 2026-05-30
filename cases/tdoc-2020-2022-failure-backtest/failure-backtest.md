# TDOC Failure Backtest

- case: TDOC telehealth / COVID pull-forward
- period: 2020-2022
- review_date: 2026-05-30
- method_under_test: `long-term-integrated-thesis`
- result: workflow would have downgraded before the 2022 impairment if current patches existed

## Backtest Conclusion

The current workflow would not have said "telehealth is fake." It would have said:

> TDOC has real demand growth and a real product category, but the long-term thesis is provisional because normalized post-COVID retention, payer persistence, acquisition value capture and valuation expectations are not proven.

That distinction matters. The correct pre-2022 action would likely have been:

`watch_only_pending_normalized_demand_and_acquisition_value_capture`

## What The Old Narrative Likely Overweighted

1. Visit growth and revenue growth during a pandemic demand shock.
2. The strategic attractiveness of combining Teladoc and Livongo.
3. TAM expansion from episodic virtual visits into whole-person virtual care.
4. A market valuation that assumed high growth duration.

None of those were worthless signals. The error was treating them as durable proof before normalized evidence arrived.

## What The Workflow Would Have Flagged

### 1. Pull-Forward Vs Structural Demand

Q3 2020 revenue growth of 109% and visits growth of 206% were real. But the shock source was COVID-19, not ordinary adoption behavior.

The workflow should have asked:

- What is the normalized usage baseline after the shock?
- Do visits remain elevated after reopening?
- Are employers/payers renewing at similar economics?
- Does usage translate into margin and retention?

Because those answers were source gaps in the hot phase, the long-term thesis should have been downgraded.

### 2. Product Monetization

Visits are usage, not necessarily durable monetization. Revenue is monetization, but revenue under a one-time demand shock does not by itself prove normalized retention.

The workflow would classify key metrics:

- `visits`: usage proxy
- `revenue growth`: direct revenue, but shock-contaminated
- `Livongo chronic-care narrative`: product expansion claim
- `cross-sell`: source gap unless measured
- `margin/ROIC`: source gap or weak

### 3. Acquisition-Driven Value Capture

The Livongo merger gave TDOC a broader thesis: whole-person virtual care. The workflow should not have accepted that as value creation until the case showed:

- measurable cross-sell
- payer/employer retention
- chronic-care engagement durability
- margin contribution
- ROIC path relative to purchase price

The 2022 goodwill collapse is postmortem evidence that the market and accounting value assigned to acquisition-driven growth was not durable.

### 4. Valuation Expectations

At peak-market enthusiasm, TDOC's equity value appears to have been tens of billions of dollars against 2020 revenue near $1.1B and 2021 revenue near $2.0B. That valuation required long growth duration and significant future margin improvement.

The workflow would not need exact precision to downgrade. It would need only to ask:

- What if growth normalizes after the pandemic?
- What if Livongo cross-sell takes longer than expected?
- What if payer economics do not support the implied margin path?

If those assumptions are not evidenced, the thesis cannot be public-grade.

## Timing Of Downgrade

The best pre-impairment downgrade point was not after the 2022 goodwill charge. It was when the thesis depended on pandemic-era demand and Livongo synergy while normalized retention and acquisition ROIC evidence were still missing.

Practical downgrade trigger:

`market_heat: extreme` + `shock_source: COVID` + `normalized_usage_baseline: source_gap` + `acquisition_ROIC_path: source_gap`

Recommended state:

`watch_only_pending_normalized_demand`

## What This Backtest Proves

This is the first historical case showing that the workflow can add value beyond live-case discipline. It would have forced a downgrade before the accounting impairment if the current patches existed.

## What It Does Not Prove

- It does not prove the workflow is fully public-grade.
- Peak price, approximate equity value and near-peak EV reconstruction are now improved. Consensus expectation reconstruction remains incomplete unless the unavailable-data exception is reviewer-accepted.
- The source trail needs archival cleanup before sharing externally.
- This is one failure case; at least one more backtest is still needed.

## Method Change Needed

Add `pull_forward_vs_structural_demand` as a required lens when a thesis forms during a demand shock.

Required fields:

- `shock_source`
- `duration_of_shock`
- `normalized_usage_baseline`
- `post_shock_retention`
- `payer_or_budget_persistence`
- `valuation_if_growth_normalizes`

Stop rule:

- If a company forms its long-term thesis during an abnormal demand shock and normalized retention is a source gap, do not issue an actionability conclusion.

## Refresh Conditions

- stale_after: 2026-06-30
- must_refresh_if: verified historical price/consensus data changes the valuation framing, or archival source review changes the timing of the downgrade trigger.
