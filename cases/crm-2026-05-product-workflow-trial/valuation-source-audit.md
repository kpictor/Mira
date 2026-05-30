# CRM Valuation Source Audit

- company: Salesforce, Inc.
- ticker: CRM
- audit_date: 2026-05-30
- purpose: move CRM expectation map closer to public-grade reproducibility
- status: pass_public_grade_subject_to_g06_source_challenge

## What Was Added

The expectation map now has a fuller current peer table in `peer-valuation-table.csv`.
It also now has public historical ratio support from StockAnalysis ratio history.
It now has FY2028 FCF forecast support from MarketScreener.

Peer set:

- CRM
- NOW
- ADBE
- ORCL
- MSFT
- SAP
- INTU
- PEGA

The table adds current forward P/E, EV/Sales, EV/FCF where available and ROIC where available from public market-data pages.

## Public-Grade Assessment

This improves the CRM expectation map but still does not make it final public-grade.

### Pass

- Current price, market cap and enterprise value are sourced.
- FY2027/FY2028 revenue and EPS estimates are sourced.
- FY2027 FCF is modeled from company FY2026 FCF and FY2027 FCF growth guidance.
- Current peer multiple range is broader and reproducible.
- Historical forward P/E, EV/Sales and EV/FCF are documented from StockAnalysis ratio history.
- Historical P/S and trailing P/E ranges are retained as public cross-checks.
- FY2028 FCF forecast is documented from MarketScreener.

### Partial

- Historical valuation range is sourced but depends on StockAnalysis definitions and fiscal-year snapshot methodology.
- Peer table is wider, but peers are not perfectly comparable.
- FY2027 FCF is model-derived, not consensus.
- MarketScreener forecast methodology should be challenged by reviewer.

### Fail / Source Gap

- Consensus EPS definition may differ from Salesforce non-GAAP guidance.

## Decision Impact

No change to CRM research action.

`watch_only_pending_product_monetization_map`

Reason:

- The broader peer table reinforces that CRM is not being priced as a high-growth AI-agent winner.
- Valuation discipline improves, but the gating issue remains product monetization: Agentforce/Data 360 must bridge to organic growth, retention, pricing and margin conversion.
- The workflow should not upgrade actionability just because valuation appears reasonable versus high-quality peers.

## G05 Impact

This closes both prior G05 sub-gaps:

- historical EV/FCF and historical forward P/E are no longer source gaps for CRM;
- FY2028 FCF forecast is sourced from MarketScreener.

G05 is cleared for internal release-gate tracking. G06 still needs an independent reviewer to challenge MarketScreener source sufficiency and ratio definitions.

## Workflow Lesson

Expectation maps should separate:

- `current_peer_multiple_range`
- `historical_company_multiple_range`
- `consensus_growth_bridge`
- `cash_flow_consensus_gap`
- `definition_risk`

Otherwise analysts can overstate valuation precision by mixing current peer multiples, historical trailing multiples and forward consensus estimates into one vague "cheap/expensive" statement.

## Refresh Conditions

- stale_after: 2026-06-30
- must_refresh_if: Q2 FY27 changes product metrics, organic growth, FCF guide, ASR share count, debt/cash, peer multiples, or FY2028 consensus revenue/EPS.
