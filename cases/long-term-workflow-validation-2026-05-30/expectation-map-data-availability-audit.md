# Expectation Map Data Availability Audit

- audit_date: 2026-05-30
- scope: CRM, ETN, VRT, LLY expectation maps
- status: exception_protocol_added_not_final_public_grade

## Purpose

The public-readiness audit requires at least one public-grade expectation map.

The current blocker is not just analyst effort. Some fields, especially FY2 FCF consensus and historical EV/FCF / forward P/E series, are not consistently available from the public/free sources used in this workspace.

This audit prevents two bad outcomes:

- filling missing consensus fields with model-derived numbers while calling them consensus
- treating an easier metric such as trailing P/E or P/S as equivalent to historical EV/FCF or forward P/E

## Current State

| case | strongest valuation evidence | main remaining source gap | status |
| --- | --- | --- | --- |
| CRM | EV, FY1/FY2 revenue and EPS, modeled FY1 FCF, MarketScreener FY2 FCF forecast, broader peer table, historical forward P/E, EV/Sales and EV/FCF from StockAnalysis ratio history. | Reviewer should challenge MarketScreener methodology under G06. | pass_public_grade_subject_to_g06_source_challenge |
| ETN | Current price, share count and company guidance support rough P/E framing. | Full consensus, peer table and historical range. | internal_only |
| VRT | Current price, share count and company guidance support rough P/E framing. | Full consensus, peer table and historical range. | internal_only |
| LLY | StockAnalysis market data and FY1/FY2 revenue/EPS estimates; NVO peer reference. | FCF consensus, historical range, fuller peer table. | internal_only |

## Exception Protocol

If FY2 FCF consensus or historical EV/FCF / forward P/E is unavailable from public sources:

1. Keep the field as `source_gap`.
2. Document source attempts and what was available instead.
3. Label any modeled value as `modeled`, not consensus.
4. Add a `false_precision_warning`.
5. Do not use valuation as the reason for actionability.
6. If valuation is a gating lens, use a watch-only label until the missing field is obtained or an independent reviewer accepts the unavailable-data exception.

## CRM Assessment

CRM is the closest candidate to public-grade because:

- current market data are sourced
- FY1/FY2 revenue and EPS estimates are sourced
- FY1 FCF is modeled from company FY2026 FCF and FY2027 FCF growth guide
- broader peer table exists
- historical forward P/E, EV/Sales and EV/FCF context exists from StockAnalysis ratio history
- historical P/S and trailing P/E context exists as a cross-check

CRM now clears G05 for internal release-gate tracking because:

- FY2 FCF forecast is sourced from MarketScreener
- historical EV/FCF and forward P/E are sourced from StockAnalysis ratio history
- FY1 modeled FCF remains clearly labeled as modeled, not consensus

Remaining caveats:

- consensus EPS definition may differ from Salesforce non-GAAP guidance
- historical ratio definitions and fiscal-year snapshots require caution
- MarketScreener methodology should be challenged by an external reviewer

The correct status is:

`pass_public_grade_subject_to_g06_source_challenge`

## G05 Upgrade

The prior audit had two CRM source gaps: FY2 FCF and historical EV/FCF / forward P/E. The historical range gap is improved with public StockAnalysis ratio history, and the FY2 FCF gap is improved with MarketScreener's FY2028 FCF forecast.

This is a material improvement but not a loophole. CRM remains watch-only from a valuation-actionability standpoint because product monetization remains the actionability blocker.

G05 is no longer the hard release blocker; G06 must still challenge source sufficiency.

## Methodology Impact

Add `expectation_map_unavailable_data_exception`.

This is not a loophole for actionability. It is a reproducibility rule:

- honest source gaps are acceptable for internal watch-only work
- missing data cannot be silently substituted
- unavailable-data exceptions require reviewer acceptance before external sharing

## Refresh Conditions

- stale_after: 2026-06-30
- must_refresh_if: MarketScreener FCF forecast, StockAnalysis ratio definitions, paid data export, or independent reviewer feedback changes the expectation-map status.
