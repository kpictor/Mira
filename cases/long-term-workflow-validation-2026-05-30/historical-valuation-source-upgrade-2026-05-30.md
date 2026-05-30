# Historical Valuation Source Upgrade

- upgrade_date: 2026-05-30
- scope: TDOC 2020-2022 and PTON 2020-2022 historical failure backtests
- status: improved_not_final_public_grade
- stale_after: 2026-06-30
- must_refresh_if: exact same-day peak EV, contemporaneous consensus estimates or transcript archives are obtained

## Purpose

This upgrade reduces false precision in the historical failure backtests.

Before this pass, TDOC and PTON had peak-price and directional market-cap evidence, but the peak enterprise-value bridge was still too loose for public example use.

This pass adds source-backed near-peak balance-sheet inputs and keeps the remaining consensus gap explicit. Transcript support is handled in `historical-transcript-source-upgrade-2026-05-30.md`.

## TDOC Upgrade

Source-backed inputs:

- peak close: $294.54 on 2021-02-08 from the historical price source already logged in the case
- shares reference: 152.7M near-peak shares from SEC companyfacts / 2020 filing context
- cash and short-term investments: about $786.6M from the 2020 10-K
- current debt plus convertible senior notes net: about $1.422B from the 2020 10-K

Derived result:

- approximate equity value: about $45.0B
- approximate near-peak enterprise value: about $45.6B

Status:

- better than the prior rough market-cap-only framing
- still not exact same-day EV because price date, share count and balance-sheet date do not perfectly match
- still not public-grade because contemporaneous consensus support remains incomplete

## PTON Upgrade

Source-backed inputs:

- peak close: $167.42 on 2021-01-13 from the historical price source already logged in the case
- near-peak shares: 294.5M Class A and Class B shares outstanding as of 2021-01-29 from the Q2 FY2021 10-Q
- cash and marketable securities: about $2.11B as of 2020-12-31 from the Q2 FY2021 10-Q
- drawn debt: no drawn credit-facility borrowings as of 2020-12-31 from the Q2 FY2021 10-Q

Derived result:

- approximate equity value: about $49.3B
- approximate near-peak enterprise value: about $47.2B

Status:

- better than the prior FY2021 10-K share-reference framing
- still not exact same-day EV because price date, share count and balance-sheet date do not perfectly match
- still not public-grade because contemporaneous consensus support remains incomplete

## Methodology Rule Added

Historical failure backtests may use a near-peak EV bridge only when all four conditions are visible:

1. peak price and date are stated;
2. share-count date is stated and near-date mismatch is disclosed;
3. cash/debt source and date are stated;
4. the conclusion says whether consensus and transcript support are present or still missing.

If any condition is missing, the backtest can support internal learning but cannot be presented as an externally public-grade example.
