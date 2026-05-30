# Iteration 06: Historical Failure Backtest Plan

- date: 2026-05-30
- validation_gap: prove the workflow can downgrade a past hot thesis before the market does
- status: planned

## Why This Is Required

Live cases test whether the workflow is useful today. They do not prove it can avoid past mistakes.

Before this methodology can be shared with institutional colleagues, it must show that it would have caught at least one historical failure pattern:

- market heat ahead of evidence maturity
- pull-forward demand mistaken for durable demand
- product adoption mistaken for sustainable unit economics
- acquisition-driven narrative mistaken for value creation
- valuation expectations disconnected from normalized growth

## Recommended First Backtest: TDOC / Telehealth Pull-Forward

Candidate:

- `TDOC`

Period:

- initial hot phase: 2020-2021
- thesis break / impairment phase: 2022

Why TDOC is a good test:

- The pandemic created a real product-demand shock.
- Teladoc had actual revenue and visit growth, not just narrative.
- The Livongo merger created a whole-person virtual care thesis and acquisition-driven value-capture claim.
- The later goodwill impairment and growth normalization provide a clear postmortem path.

## Initial Source Trail

- Teladoc Q3 2020 release: Q3 revenue grew 109% and visits grew 206%.
  https://ir.teladoc.com/news-and-events/investor-news/press-release-details/2020/Teladoc-Health-Reports-Third-Quarter-2020-Results/default.aspx
- Teladoc / Livongo merger announcement: expected 2020 pro forma revenue of approximately $1.3B and 85% pro forma growth.
  https://ir.teladoc.com/news-and-events/investor-news/press-release-details/2020/Teladoc-Health-and-Livongo-Merge-to-Create-New-Standard-in-Global-Healthcare-Delivery-Access-and-Experience/default.aspx
- Teladoc FY2021 release: Q4 2021 revenue grew 45% and visits grew 41%.
  https://ir.teladoc.com/news-and-events/investor-news/press-release-details/2022/Teladoc-Health-Reports-Fourth-Quarter-and-Full-Year-2021-Results/default.aspx
- Teladoc Q2 2022 release: $3.0B non-cash goodwill impairment charge.
  https://ir.teladochealth.com/news-and-events/investor-news/press-release-details/2022/Teladoc-Health-Reports-Second-Quarter-2022-Results/
- Teladoc Q3 2022 release: $9.6B non-cash goodwill impairment charges in first nine months of 2022.
  https://ir.teladochealth.com/news-and-events/investor-news/press-release-details/2022/Teladoc-Health-Reports-Third-Quarter-2022-Results/default.aspx

## Backtest Questions

### Theme-To-Company Handoff

- Was the thesis about telehealth as a category, or TDOC as the public-company value capturer?
- Did the workflow distinguish direct telehealth demand from pandemic pull-forward?
- Did it separate Livongo acquisition narrative from organic product-market fit?

### Market Heat Vs Thesis Maturity

- Was market heat extreme relative to evidence maturity?
- Which evidence was durable and which was COVID-period pull-forward?
- Did visit growth prove retention, payer economics, utilization or margin quality?

### Product Monetization Map

- Which metrics were product usage, which were revenue, and which were acquisition-driven?
- Were chronic care / whole-person care claims linked to retention, pricing or margin?
- Did the workflow require post-pandemic normalized demand evidence?

### Acquisition-Driven Value Capture

- Did the Livongo transaction create a clear ROIC path?
- Was goodwill/value creation tied to measurable cross-sell, retention, margin and payer adoption?
- What would have forced a downgrade before the impairment?

### Valuation Expectations

- What growth duration, revenue scale and margin path did the peak valuation require?
- Did the market price imply sustained pandemic-era growth?
- Would normalized growth have invalidated the valuation before goodwill impairment?

## Expected Workflow Patches

The backtest should test whether existing patches are enough:

- `market_heat_vs_thesis_maturity`
- `product_monetization_map`
- `acquisition-driven value capture`
- `valuation_expectations`
- `capital_allocation_distortion`

Potential new patch:

- `pull_forward_vs_structural_demand`

Required fields:

- `shock_source`
- `duration_of_shock`
- `normalized_usage_baseline`
- `post_shock_retention`
- `payer_or_budget_persistence`
- `valuation_if_growth_normalizes`

## Required Outputs

Create:

- `cases/tdoc-2020-2022-failure-backtest/README.md`
- `failure-backtest.md`
- `evidence-log.csv`
- `workflow-scorecard.csv`
- `methodology-delta.md`

## Success Criteria

The backtest is successful only if it can answer:

- Would the workflow have downgraded TDOC before the 2022 impairment?
- Which exact field would have triggered the downgrade?
- Was the failure mainly demand normalization, valuation expectations, acquisition value capture, product monetization, or some combination?
- What should Mira change so the same mistake is less likely in a future hot theme?

## Refresh Conditions

- stale_after: 2026-06-30
- must_refresh_if: a better historical failure candidate is selected, or TDOC source trail lacks enough evidence to reconstruct the thesis and failure path.
