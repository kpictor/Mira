# Iteration 07: PTON Failure Backtest

- date: 2026-05-30
- case: `PTON_2020_2022`
- validation_type: historical_failure_backtest
- objective: test whether the workflow catches consumer hardware/subscription demand pull-forward before the market collapse
- result: positive_partial

## Why PTON

PTON is deliberately different from TDOC:

- consumer behavior instead of healthcare utilization
- hardware-led subscription model instead of virtual-care service model
- inventory and logistics commitments instead of acquisition goodwill as the main operating stress
- product love and low churn coexisting with broken hardware unit economics

This prevents the workflow from overfitting to one COVID-era failure pattern.

## Workflow Result

The workflow would have downgraded PTON by Q2 FY2022, before the FY2022 full-year postmortem, because the thesis depended on variables that were either deteriorating or not yet proven:

- normalized hardware demand
- hardware gross margin after price cuts, freight, returns and logistics deleveraging
- inventory/capacity commitment quality
- installed-base engagement after reopening
- valuation if hardware growth normalized

Correct state:

`watch_only_pending_normalized_hardware_demand_and_inventory_clearance`

## Patch Added

Add `hardware_subscription_mix_check`.

Stop rule:

- If subscription growth depends on hardware placements and normalized hardware demand or hardware gross margin is a source gap, do not upgrade to actionability.

## Evidence Quality

Strong internal evidence:

- SEC 10-K and 10-Q filings
- SEC companyfacts inventory and goodwill data
- company-disclosed subscription, churn, workout, revenue and margin metrics

Remaining external-public gaps:

- exact peak valuation / EV
- FY2022 and FY2023 consensus before the break
- earnings-call transcript excerpts
- peer/category demand data

## Methodology Impact

PTON materially improves the method because it forces a distinction between:

- product love and purchasing durability
- subscription retention and new-user acquisition
- installed-base growth and replacement-cycle economics
- inventory commitment and demand proof

## Refresh Conditions

- stale_after: 2026-06-30
- must_refresh_if: historical valuation or consensus evidence changes the downgrade timing, or transcript evidence contradicts the inventory/hardware-margin interpretation.
