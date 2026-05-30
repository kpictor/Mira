# Historical Source Cleanup

- cleanup_date: 2026-05-30
- scope: TDOC 2020-2022 and PTON 2020-2022 failure backtests
- status: improved_not_final_public_grade

## Purpose

The public-readiness audit flagged the historical failure backtests as strong internal evidence but not externally share-ready because valuation, transcript and archival trails were incomplete.

This cleanup improves the stable source trail without overstating completeness.

## TDOC Cleanup

Added:

- `../tdoc-2020-2022-failure-backtest/historical-valuation-reconstruction.csv`
- peak price support from MacroTrends search result
- year-end market-cap support from CompaniesMarketCap
- revised peak-era equity value from roughly $44B to roughly $45B using $294.54 and 152.7M shares
- near-peak enterprise value reconstruction using 2020 10-K cash, short-term investments, current debt and convertible notes

Improved:

- TDOC peak valuation is no longer an unsupported rough estimate.
- TDOC now has an approximate near-peak EV of roughly $45.6B with source-backed cash/debt adjustments.
- Year-end market-cap collapse from 2020 to 2022 is now source-backed.

Still missing:

- 2021/2022 consensus revenue, EBITDA and EPS expectations
- archived earnings-call transcript support
- exact same-day peak share count, cash and debt if the external example requires more precision than the near-date reconstruction

## PTON Cleanup

Added:

- `../pton-2020-2022-failure-backtest/historical-valuation-reconstruction.csv`
- peak price support from MacroTrends / StatMuse search results
- year-end market-cap support from CompaniesMarketCap
- alternative market-cap support from StatMuse / MarketCapHistory search results
- approximate peak-era equity value of roughly $49.3B using $167.42 and the 2021-01-29 10-Q share count
- approximate near-peak enterprise value of roughly $47.2B using Q2 FY2021 cash, marketable securities and no drawn debt

Improved:

- PTON valuation heat is now documented as a range rather than a single false-precision number.
- PTON now has a filing-backed near-peak share-count, net-cash and EV reconstruction.
- Source variance is explicit rather than hidden.

Still missing:

- FY2022/FY2023 consensus revenue and EBITDA expectations
- transcript archive and management Q&A excerpts
- exact same-day peak share count, cash and debt if the external example requires more precision than the near-date reconstruction

## Methodology Impact

This cleanup validates a rule for historical failure backtests:

- Do not use approximate peak valuation as a durable conclusion without a price source, share-count source and source-variance note.
- If exact peak-date EV or consensus is unavailable, mark the valuation reconstruction as `improved_not_final_public_grade`.
- Historical failure backtests can be internally useful before they are externally publishable.

## Public-Grade Status

The historical backtests move from:

`internal_pass_with_source_gaps`

to:

`partial_pass_source_cleanup_ev_improved`

They still do not satisfy full external publication standards.

## Archive Audit Added

Added:

- `historical-backtest-source-archive-audit.csv`
- `historical-backtest-publication-standard.md`

These files turn the remaining historical source gaps into a row-level publication gate.

Current rule:

- TDOC and PTON can support internal methodology validation.
- They cannot be used as fully public-grade external examples while any archive-audit row has `release_decision_impact = blocks_external_example`.

## Refresh Conditions

- stale_after: 2026-06-30
- must_refresh_if: exact peak-date share count, enterprise value, consensus estimates or transcript archives are obtained.
