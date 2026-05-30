# Methodology Delta: PTON Failure Backtest

- case: PTON 2020-2022
- review_date: 2026-05-30
- affected_method: `long-term-integrated-thesis`
- decision: keep under trial; add hardware/subscription mix sub-lens

## What The Case Adds Beyond TDOC

TDOC showed that abnormal demand and acquisition narratives can masquerade as durable long-term thesis evidence.

PTON adds a different pattern:

- The product can be real.
- The subscription base can be real.
- Churn can remain relatively low.
- The stock can still fail if the hardware acquisition engine and inventory commitments were calibrated to abnormal demand.

This means `product_reality` and `pull_forward_vs_structural_demand` are necessary but not sufficient for hardware-led subscription models.

## Patch Required

Add `hardware_subscription_mix_check`.

Use when:

- subscription growth depends on devices, equipment, hardware, physical installation or inventory
- the installed base is created through one-time product sales
- hardware gross profit is part of customer acquisition payback
- management is expanding inventory, factories, logistics or supplier commitments during abnormal demand

Required fields:

- `hardware_revenue_growth`
- `hardware_gross_margin`
- `subscriber_growth_source`
- `retention_or_churn`
- `engagement_quality`
- `inventory_or_capacity_commitment`
- `replacement_cycle`
- `normalized_new_user_demand`
- `unit_economics_after_normalization`

Stop rule:

- If subscription growth depends on hardware placements and normalized hardware demand or hardware gross margin is a source gap, use `research_action: watch_only_pending_normalized_hardware_demand`.

## Evidence Standard

Minimum evidence for upgrading a hardware-led subscription thesis:

1. Hardware demand remains resilient after the abnormal demand window.
2. Hardware gross margin remains positive under normal freight, discounting and returns.
3. Subscriber retention is not only low churn but also healthy engagement and renewal.
4. Inventory/capacity commitments are proportional to normalized demand.
5. Unit economics remain attractive without one-time demand shock support.
6. Valuation does not already require continued pandemic-era hardware growth.

## Methodology Result

The method improves materially after PTON because it can now distinguish:

- product love versus durable purchasing behavior
- installed-base retention versus new-user acquisition
- subscription revenue quality versus hardware acquisition cost
- inventory commitment versus demand proof

## Remaining Public-Grade Gaps

- verified peak market cap / EV
- FY2022/FY2023 consensus expectations before the downgrade
- earnings-call transcript archive
- peer/category demand data
- chart-ready evidence appendix

## Refresh Conditions

- stale_after: 2026-06-30
- must_refresh_if: expectation-map data or archived transcripts change the downgrade trigger.
