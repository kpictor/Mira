# G05 Expectation Map Upgrade

- upgrade_date: 2026-05-30
- gate: `G05 valuation_expectation_map`
- primary_case: `CRM_2026`
- status: partial_pass_historical_range_improved
- external_release_impact: not_cleared

## Supersession Note

This report has been superseded by:

- `g05-fy2-fcf-source-upgrade-2026-05-30.md`

MarketScreener FY2028 FCF forecast was later found and added to the CRM expectation map, so G05 now clears for internal gate tracking subject to G06 reviewer challenge.

## Purpose

G05 requires at least one public-grade expectation map or an accepted unavailable-data exception. CRM is the closest candidate, so this upgrade focuses on whether the remaining gaps can be reduced with public sources.

## Facts

- CRM current price, market cap, enterprise value and current multiples are sourced from StockAnalysis.
- CRM FY2027/FY2028 revenue and EPS estimates are sourced from StockAnalysis/Finnhub.
- CRM FY2027 FCF is modeled from Salesforce FY2026 reported FCF and Salesforce FY2027 FCF growth guidance; it is not consensus FCF.
- StockAnalysis ratio history now supplies CRM historical forward P/E, EV/Sales and EV/FCF from FY2022 through current.
- CompaniesMarketCap historical P/S and trailing P/E remain cross-checks, not the primary historical valuation range.
- FY2028 FCF consensus remains unavailable from the public sources used in the workflow.

## What Changed

Prior status:

- CRM had FY2 FCF consensus missing.
- CRM had historical EV/FCF and forward P/E missing.

Current status:

- historical EV/FCF and forward P/E are improved with StockAnalysis ratio history;
- FY2 FCF consensus remains the main G05 source gap.

## Inference

CRM is now a stronger public-grade candidate because the valuation-history bridge no longer depends on trailing P/E or P/S proxies alone.

The remaining FY2 FCF consensus gap matters because free cash flow is central to the CRM valuation argument. Modeled FCF can support interpretation, but it cannot be labeled consensus or used to clear an external-release gate without reviewer acceptance.

## Judgment

Do not clear G05 yet.

Upgrade G05 from `partial_pass_exception_protocol_added` to `partial_pass_historical_range_improved`.

The next valid paths are:

1. source FY2028 FCF consensus from an acceptable public or paid data export;
2. ask an independent reviewer to accept the unavailable-data exception for CRM after reviewing the source attempts, modeled-label discipline and false-precision warning.

## Decision Impact

No change to CRM actionability.

`watch_only_pending_product_monetization_map`

Reason: valuation quality improved, but product monetization and FY2 FCF consensus remain insufficient for valuation-led actionability.

## Source Trail

- CRM expectation map: `../crm-2026-05-product-workflow-trial/expectation-map.csv`
- CRM evidence log: `../crm-2026-05-product-workflow-trial/evidence-log.csv`
- CRM valuation source audit: `../crm-2026-05-product-workflow-trial/valuation-source-audit.md`
- StockAnalysis CRM ratios: https://stockanalysis.com/stocks/crm/financials/ratios/
- StockAnalysis CRM forecast: https://stockanalysis.com/stocks/crm/forecast/

## Refresh Conditions

- stale_after: 2026-06-30
- must_refresh_if: FY2028 FCF consensus becomes available, StockAnalysis changes ratio history definitions, paid data export is added, or external reviewer accepts/rejects the unavailable-data exception.
