# Methodology Delta From CRM Product Trial

- case: CRM product-reality workflow trial
- date: 2026-05-30
- status: iteration_delta
- linked_methodology: `cases/long-term-methodology-2026-05-30/methodology-card.md`

## What The Workflow Improved

The CRM trial proved that the product evidence ladder is useful, but it needs more nuance.

The workflow avoided two bad shortcuts:

1. Rejecting Agentforce as mere AI narrative.
2. Accepting Agentforce ARR and usage metrics as a fully proven long-term company acceleration thesis.

CRM has evidence beyond demos and pilots. It has disclosed ARR, usage and bookings metrics. But the workflow correctly found the missing bridge: product traction must translate into organic revenue acceleration, retention, pricing power and margin conversion.

## New Defects Exposed

### P0: Need Product Monetization Map

The product ladder says where evidence sits, but it does not yet force the company-level bridge.

Add a product monetization map:

- `product_metric`
- `metric_type`: `ARR`, `usage`, `bookings`, `active_users`, `tokens`, `records`, `API_calls`
- `economic_link`: `direct_revenue`, `expansion_signal`, `retention_signal`, `usage_proxy`, `cost_driver`
- `incrementality`: `new`, `cross_sell`, `bundle`, `acquired`, `source_gap`
- `customer_cohort`
- `retention_or_renewal_evidence`
- `pricing_evidence`
- `margin_evidence`
- `total_company_bridge`

### P1: Usage Metrics Need Economic Classification

Agentic Work Units, tokens, records ingested and active users are not interchangeable.

Add usage classification:

- `revenue_metered`
- `engagement_proxy`
- `infrastructure_cost_driver`
- `adoption_breadth`
- `retention_indicator`

Stop rule:

- Do not treat usage growth as monetization unless the metric is tied to pricing, revenue, retention or margin.

### P1: Acquisition Contribution Must Be Separated From Product Growth

Salesforce's FY27 guide and ARR disclosures include Informatica contribution. This means product growth must be split:

- organic product growth
- acquired contribution
- packaging / reclassification
- cross-sell into installed base

### P2: Capital Allocation Can Distort Per-Share Evidence

The $25B ASR changes share count and EPS interpretation while increasing debt. The workflow needs to flag when per-share improvement is partly financial engineering rather than operating acceleration.

## Proposed Workflow Patch

Add `product_monetization_map_required` when:

- `product_reality` is a primary lens
- the hot theme is AI/software/product-led
- management discloses usage or ARR metrics

If the monetization map lacks retention/pricing/margin evidence, use:

- `research_action: watch_only_pending_product_monetization_map`

Patch applied:

- Added `templates/product-monetization-map.csv`.
- Added a case-level `product-monetization-map.csv` for CRM.

## Validation Impact

The workflow is now more useful across different theme types:

- ETN/VRT tested infrastructure value capture and valuation burden.
- CRM tested product evidence quality and monetization bridge.

Still not public-grade:

- no product-led contrast case yet
- no historical failure backtest
- no transcript/customer evidence
- no peer comparison against NOW/PLTR/MSFT

## Next Trial

Run one of:

- `NOW`: enterprise workflow adoption and AI monetization contrast
- `PLTR`: high-conviction AI platform with valuation heat contrast
- historical failure backtest: metaverse / telehealth / EV charging / alternative protein

Recommended next move:

- Historical failure backtest. The workflow has now seen three live cases; it needs to prove it could have downgraded a past hot thesis before the market did.

## Refresh Conditions

- stale_after: 2026-06-30
- must_refresh_if: Salesforce Q2 FY27 changes Agentforce/Data 360 ARR, AWUs, bookings growth, organic revenue acceleration or margin guidance.
