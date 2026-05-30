# CRM Expectation Map Notes

- company: Salesforce, Inc.
- ticker: CRM
- as_of_date: 2026-05-30
- purpose: strengthen the valuation / expectation bridge for the `long-term-integrated-thesis` workflow trial
- status: public-grade candidate, not final public-grade

## What Improved

The original expectation map had source gaps for enterprise value, FY1/FY2 consensus, peer range and historical range. The revised map now includes:

- current price, market cap and enterprise value
- FY2027 and FY2028 revenue and EPS estimates
- company FY2027 revenue, EPS, margin, operating cash flow and free cash flow guidance
- FY2026 free cash flow base from the 10-K
- modeled FY2027 free cash flow using company guidance
- current EV/Sales, EV/FCF, forward P/E and P/FCF
- peer current multiples for NOW, ADBE and ORCL
- broader current peer table for CRM, NOW, ADBE, ORCL, MSFT, SAP, INTU and PEGA
- historical CRM forward P/E, EV/Sales and EV/FCF from StockAnalysis ratio history
- rough historical CRM P/S range from 2021-2025
- rough historical trailing P/E context from CompaniesMarketCap

## Facts

- StockAnalysis showed CRM at $191.10 at the May 29, 2026 close, with market cap of $156.51B and enterprise value of $187.22B.
- StockAnalysis / Finnhub showed FY2027 revenue estimate of $46.59B and FY2028 revenue estimate of $51.01B.
- StockAnalysis / Finnhub showed FY2027 EPS estimate of $13.32 and FY2028 EPS estimate of $14.98.
- MarketScreener showed FY2028 free cash flow forecast of $16.458B.
- Salesforce guided FY2027 revenue to $45.9B-$46.2B, non-GAAP EPS to $14.06-$14.12, non-GAAP operating margin to 34.3%, and free cash flow growth to about 4%-5%.
- Salesforce FY2026 10-K reported FY2026 operating cash flow of $14.996B and capex of $594M, implying FCF of $14.402B.

## Inferences

- Modeled FY2027 FCF is about $15.05B using FY2026 FCF of $14.402B and the midpoint of FY2027 FCF growth guidance.
- CRM's current multiple profile is not aggressive versus NOW or ORCL, but is comparable to ADBE on EV/Sales and EV/FCF.
- The market is not pricing CRM as a hypergrowth AI-agent winner; it is pricing durable cash generation with moderate growth and execution skepticism.

## Current Peer Range

See `peer-valuation-table.csv`.

Summary:

- CRM current forward P/E and EV/FCF sit near the lower end of the broad software peer set.
- NOW, MSFT and ORCL show that higher multiples require clearer growth, platform quality, or infrastructure scarcity.
- ADBE, INTU and PEGA show that mature or challenged application software can trade near CRM-like or lower multiples.
- ORCL's EV/FCF is not meaningful because current FCF is negative after heavy capex.

## Historical Ratio Range

StockAnalysis ratio history now provides the missing historical range that was previously marked `source_gap`:

- forward P/E: 13.74 current, 16.77x FY2026, 31.67x FY2025, 30.40x FY2024, 29.97x FY2023, 55.99x FY2022
- EV/Sales: 4.37x current, 4.92x FY2026, 8.59x FY2025, 7.77x FY2024, 5.29x FY2023, 8.79x FY2022
- EV/FCF: 12.77x current, 14.18x FY2026, 26.18x FY2025, 28.51x FY2024, 26.26x FY2023, 44.07x FY2022

This materially improves G05. MarketScreener's FY2028 FCF forecast completes the remaining FY2 FCF field for internal gate tracking, subject to G06 reviewer challenge of source definitions.

## Judgments

The expectation map now materially improves valuation discipline and clears G05 for internal gate tracking, but remains subject to external reviewer challenge because:

- MarketScreener's FY2028 FCF forecast methodology needs reviewer challenge.
- Consensus EPS definitions may mix GAAP and non-GAAP conventions.
- Peer set is broader but still imperfect because peers mix enterprise applications, platform software, infrastructure software and workflow automation.
- Historical range now includes public forward P/E, EV/Sales and EV/FCF, but definitions and fiscal-year snapshot methodology require caution.

## Research Action Impact

The improved valuation map does not change the CRM action:

`watch_only_pending_product_monetization_map`

Reason: valuation is not the primary blocker. The blocker remains product-to-company monetization evidence: organic growth, retention, pricing and margin conversion from Agentforce/Data 360.

## Refresh Conditions

- stale_after: 2026-06-30
- must_refresh_if: Q2 FY27 earnings updates FY2027 guidance, Agentforce/Data 360 metrics, ASR settlement share count, debt/cash, or consensus FY2028 revenue/EPS materially changes.
