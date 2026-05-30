# G05 FY2 FCF Source Upgrade

- upgrade_date: 2026-05-30
- gate: `G05 valuation_expectation_map`
- primary_case: `CRM_2026`
- status: pass_public_grade
- external_release_impact: clears_G05_subject_to_G06_reviewer_challenge

## Purpose

G05 previously required either a FY2 FCF source for CRM or an independent reviewer-accepted unavailable-data exception.

This upgrade records a public source for CRM FY2028 FCF forecast, removing the need to clear G05 through the unavailable-data exception path.

## Facts

- MarketScreener's Salesforce financial forecasts page shows Cash Flow Forecast free cash flow of:
  - `$14.910B` for fiscal January 2027
  - `$16.458B` for fiscal January 2028
  - `$18.134B` for fiscal January 2029
- CRM FY2027/FY2028 revenue and EPS estimates remain sourced from StockAnalysis/Finnhub.
- CRM historical forward P/E, EV/Sales and EV/FCF remain sourced from StockAnalysis ratio history.
- CRM current price, market cap, enterprise value and current multiples remain sourced from StockAnalysis.
- CRM FY2027 FCF in the expectation map remains explicitly labeled as modeled from company FY2026 FCF and FY2027 FCF growth guidance.

## What Changed

Prior G05 state:

- historical EV/FCF and forward P/E had been improved;
- FY2 FCF remained unresolved through either data or unavailable-data exception.

Current G05 state:

- FY2 FCF is now sourced from MarketScreener financial forecasts;
- unavailable-data exception packet remains useful as a fallback and reviewer audit trail, but is no longer the primary G05 clearing path.

## Inference

CRM now has the minimum public valuation bridge needed for G05:

- current valuation;
- FY1/FY2 revenue and EPS estimates;
- FY1 modeled FCF clearly labeled;
- FY2 public FCF forecast;
- historical forward P/E / EV/Sales / EV/FCF;
- current peer range;
- false-precision warnings.

## Judgment

Clear G05 at `pass_public_grade` for internal release-gate tracking.

This does not make the full workflow externally releasable. G06 still requires an independent reviewer to challenge source definitions, reproduce the map and accept or reject the release recommendation.

## Remaining Caveats

- MarketScreener methodology should be challenged by the reviewer, especially whether values are consensus mean, median or provider forecast.
- FY2027 FCF remains modeled from company guidance and historical FCF, not external consensus.
- EPS definitions may differ across StockAnalysis/Finnhub and Salesforce non-GAAP guidance.
- CRM actionability remains `watch_only_pending_product_monetization_map`; valuation data quality alone does not upgrade the thesis.

## Source Trail

- MarketScreener CRM financial forecasts: https://www.marketscreener.com/quote/stock/SALESFORCE-INC-12180/finances/
- CRM expectation map: `../crm-2026-05-product-workflow-trial/expectation-map.csv`
- CRM evidence log: `../crm-2026-05-product-workflow-trial/evidence-log.csv`
- CRM source attempts: `g05-crm-source-attempts.csv`
- Previous exception packet: `g05-crm-unavailable-data-exception-review.md`

## Refresh Conditions

- stale_after: 2026-06-30
- must_refresh_if: MarketScreener changes forecast values or methodology, FY2028 FCF forecast moves materially, StockAnalysis/Finnhub estimates change materially, external reviewer rejects MarketScreener as sufficient, or CRM issues updated FY2027/FY2028 cash-flow guidance.
