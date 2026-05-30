# Methodology Delta From ETN Trial

- case: ETN long-term workflow trial
- date: 2026-05-30
- status: iteration_delta
- linked_methodology: `cases/long-term-methodology-2026-05-30/methodology-card.md`

## What The Workflow Improved

The workflow prevented a common theme mistake:

> AI/data-center power demand is strong -> ETN has exposure -> bullish long-term conclusion.

Instead, it forced the conclusion through value capture and valuation:

> ETN has credible supplier/enabler exposure, but the stock already carries a premium multiple, so the next required artifact is an expectation map.

This is a real improvement over narrative memo writing.

## New Defects Exposed

### P0: No Standard Expectation Map Template

The method says to reverse-engineer valuation expectations, but the ETN trial showed we need a reusable table:

- current price
- current market cap / enterprise value
- FY1/FY2 consensus revenue, EPS and FCF
- company guidance midpoint
- historical multiple range
- peer multiple range
- implied growth duration
- implied margin/ROIC path
- downside multiple and earnings path

Without this, valuation work stays too qualitative.

Patch applied:

- Added `templates/long-term-expectation-map.csv`.
- Added a case-level `expectation-map.csv` for ETN with explicit `source_gap` fields.

### P1: Backlog Quality Needs Its Own Sub-Lens

ETN's backlog is central, but backlog is not automatically revenue.

Add backlog quality fields:

- `firm_commitment_definition`
- `delivery_timing`
- `book_to_bill`
- `cancellation_or_deferral_risk`
- `margin_of_backlog`
- `customer_concentration`
- `capacity_constraint`

### P1: Acquisition-Driven Value Capture Needs Guardrails

Boyd Thermal strengthens data-center exposure, but it also raises integration and ROIC risk.

Add acquisition fields:

- `strategic_fit`
- `purchase_price`
- `funding_mix`
- `integration_cost`
- `incremental_margin`
- `ROIC_path`
- `what_would_show_value_creation`

### P2: Consumer Lens Should Allow Translation

For infrastructure cases, `consumer_demand` should not be forced literally. It should be translated to the ultimate demand unit:

- compute demand
- power demand
- data-center capacity demand
- enterprise workload demand

## Proposed Workflow Patch

Add a `single_company_expectation_map_required` rule:

- If `market_heat = high` or `extreme`
- and `valuation_anchor_type` is available
- and the research output is a single-equity memo

then the memo must include:

- FY1 valuation on guidance or consensus
- at least one peer/historical valuation range
- explicit assumption ranges for growth, margin and duration
- downside path

If those are missing, set:

- `research_action: watch_only_pending_expectation_map`

## Validation Impact

The ETN trial raises the workflow from directionally useful to partially operational. It is still not public-grade because:

- consensus and peer valuation are missing
- there is no historical failure backtest
- there is no follow-through refresh yet
- another analyst could challenge the conclusion, but not fully reproduce the expectation map because it is incomplete

## Next Trial

Run either:

- `VRT`: same theme, higher purity, more valuation heat
- `enterprise_ai_agents_and_software_monetization`: different theme, product evidence ladder stress

Recommended next move:

- Run `VRT` as a contrast case to ETN before leaving AI infrastructure. This will test whether the workflow handles purity versus valuation heat.

## Refresh Conditions

- stale_after: 2026-06-30
- must_refresh_if: ETN Q2 2026 results materially change backlog, guidance or margin assumptions; consensus/peer valuation data is added; or VRT comparison contradicts the ETN handoff findings.
